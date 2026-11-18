# Methodology

## 1. Why content-defined units

A fixed-size split fails the first design requirement of the paper: an
insertion at position *a* shifts every later boundary and therefore every
later chunk. The unit edit distance of a single-byte insertion grows with
the file size rather than with the attack.

Content-defined chunking fixes this. A cut is placed wherever a short
sliding window of bytes satisfies a hash condition, so cut positions move
with the content. We use the Gear rolling hash adopted by FastCDC:

```
H_i  = (2 · H_{i-1} + Γ[x_i])  mod 2^64
cut  = (i >= ω)  AND  ((H_i >> (64 - ℓ)) == 0)
```

with `ω = 64` (the hash depends on only the 64 preceding bytes) and
`ℓ = 11` (mean unit length 2 KiB). We draw `Γ` uniformly from
`{1, …, 2^64 - 2^(64-ℓ)}`, which rules out the fixed point
`(2^64 - Γ[b]) mod 2^64` and prevents constant byte runs (zero padding,
RLE-compressed sections) from producing a cut at every byte.

## 2. Per-tile dual-view encoding

Each unit is split into fixed-size tiles of `T = 4096` bytes, aligned to
the first byte of the unit. Alignment to the unit (rather than the file)
is what makes every downstream tensor a function of unit bytes alone.

### 2.1 Byte view

A tile is reshaped row-by-row into a `64 × 64` grayscale patch
(`T = R² = 64² = 4096`). Values are normalized to `[0, 1]`. A three-block
CNN with batch normalization, ReLU, max pooling and global average
pooling maps the patch to a 128-dimensional embedding. Channel sizes
are `(32, 64, 128)` with `3 × 3` kernels.

### 2.2 Structure view

Whole-program disassembly is the slowest stage of graph-based detectors
and would couple the graph of one region to code elsewhere in the file.
We decode each tile on its own with a linear sweep, which disassembles
consecutive instructions from the first byte and resumes at the next
byte after an invalid encoding. Linear sweep recovers almost all
instructions of compiler-generated x86 and x64 code; its errors
concentrate around inline data such as jump tables and stay inside their
tile.

We decode in both x86-32 and x86-64 modes because (i) the file header
cannot be read (it would couple the decoder to another unit) and (ii)
SOREL-20M disarms samples by zeroing the machine field. Basic blocks
end at control-transfer instructions and start at direct-branch targets
that land inside the tile. Fall-through and in-tile direct edges become
graph edges; branches that leave the tile point to a single exit node.

Each block carries the 11 attributes used by MAGIC and DSMalConv:
numeric constants, string constants, transfer, call, arithmetic,
comparison, move, termination, data-declaration instruction counts,
total instruction count, and out-degree. A 4-layer GIN
(`32 → 64 → 64 → 128 → 128` hidden) updates node states and a linear
projection combines the mean readouts of the two modes into a
128-dimensional embedding.

### 2.3 Fusion and unit evidence

An element-wise gate between the byte- and structure-view embeddings
produces a per-dimension weighting:

```
γ  = σ(W_γ · [h_C ‖ h_G] + b_γ)
z  = γ ⊙ h_C + (1 - γ) ⊙ h_G
```

The unit embedding takes the element-wise maximum over its tiles, and a
linear head maps it to a scalar evidence in `(0, 1)`.

## 3. Monotone top-k aggregation

Let `e_(1) ≥ e_(2) ≥ … ≥ e_(m)` be the sorted unit evidences. The
certified verdict flags the file when

```
S_k(x) = Σ_{j=1..k} e_(j) ≥ θ.
```

Because the sum of the *k* largest values cannot decrease when values
are added, any insertion raises `S_k`. When an attacker alters at most
`ρ` units, the worst case removes the `ρ` largest evidences, and the
file score is then at least the tail sum
`T_ρ(x) = Σ_{j=ρ+1..ρ+k} e_(j)`.

The certified radius `ρ*(x)` is the largest `ρ` for which `T_ρ(x) ≥ θ`.
It is strictly non-increasing in `ρ`, so one scan over the sorted
evidences finds it.

The analyst-facing quantity is the number of edit sites the verdict
withstands:

```
s_δ*(x) = ⌊ ρ*(x) / (1 + c_ω^δ(x)) ⌋
```

where `c_ω^δ(x)` is the largest number of cuts of `x` inside any window
of `δ + ω - 1` positions, computed in the same pass over the file.

## 4. Global branch and OR gate

The top-*k* rule trades some recall for its guarantee: malware whose
malicious content is spread thinly over many weak units may never
produce *k* strong units. A global branch pools all unit embeddings
with gated attention and emits a scalar `g(x)` with its own threshold
`θ_g`. The final verdict is the logical OR of the two branches.

An OR cannot turn a malicious verdict into a benign one, so every
certified detection survives the global branch (Proposition 2 in the
paper). The branch costs part of the false-positive budget, which is
accounted for by the union bound at calibration time:
`α = α_1 + α_2` with `α_1 = α_2 = 0.05%` in all reported experiments.

## 5. Open-set family head

Family evidence is concentrated in the highest-evidence units, so the
family head reads the mean embedding of the *k* top units:

```
ℓ_c(x) = W_f · (1/k) Σ_{j=1..k} z_(j)(x) + b_f
p(c|x) = softmax(ℓ(x))
```

Unknown families are rejected with an energy score

```
E(x) = − log Σ_c exp(ℓ_c(x))
```

thresholded so that 95% of validation malware from known families is
accepted. The family label is **not** certified; an attacker who cannot
change the detection verdict may still change the predicted family.

## 6. Certificate-aware training

Only file-level labels are available, so training is a multiple-instance
problem. Cross-entropy on `S_k` alone would teach the model to place
evidence in a few units, which gives a radius of zero. We train the
tail sum directly with a hinge-style loss:

```
L_cert = mean_{x∈B_1}  [θ_0 + m - T_{ρ_0}(x)]_+
       + mean_{x∈B_0}  [S_k(x) - θ_0 + m]_+
```

with `θ_0 = k/2`, `m = 0.1`, and a target radius `ρ_0(t)` that ramps
from 0 to `ρ_max = 8` over a 25-epoch window after a 5-epoch warm-up.

Two-pass hard-unit mining keeps the gradient cheap: pass 1 scores every
unit without gradient, pass 2 recomputes only the units that enter the
loss (top `ρ_0 + k` for malware, top `k` for benign, plus `r = 8`
random units per file). Within each selected unit, the max-over-tiles
in Eq. (7) passes gradient only to the arg-max tile.

## 7. Threshold calibration

At deployment, thresholds are set on a held-out benign calibration set
so that each branch respects half the false-positive budget:

```
θ   = Q_{1 - α_1} ({ S_k(x) : x ∈ D_cal })
θ_g = Q_{1 - α_2} ({ g(x)  : x ∈ D_cal })
η   = chosen so 95 % of validation known-family malware is accepted
```

By the union bound the OR gate has calibration FPR at most
`α_1 + α_2`.
