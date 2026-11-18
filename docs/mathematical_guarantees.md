# Mathematical Guarantees and their Implementation

This document reproduces the formal statements of Section IV of the paper
in the exact wording of the manuscript and maps each one to the function
that implements or verifies it. Simplified restatements are **not**
substituted for the published proofs.

## Notation

| Symbol | Meaning | Source (code) |
|---|---|---|
| `x ∈ B^n` | input binary, `n` bytes | `unitization/content_defined_chunking.py` |
| `U(x)` | multiset of content-defined units of `x` | `unitize(x)` |
| `m` | number of units of `x` | `len(U(x))` |
| `e_u ∈ (0, 1)` | evidence for unit `u` | `certification/certificate.py: _unit_evidence` |
| `e_(j)` | `j`-th largest evidence of `x` | `certification/certificate.py: sorted_evidences` |
| `S_k(x) = Σ_{j=1..k} e_(j)` | top-*k* sum | `top_k_aggregate` |
| `T_ρ(x) = Σ_{j=ρ+1..ρ+k} e_(j)` | tail sum at radius `ρ` | `tail_sum` |
| `ρ*(x)` | certified unit radius | `certified_radius` |
| `s_δ*(x)` | certified edit-site radius | `edit_distance.edit_site_radius` |
| `c_ω^δ(x)` | max cuts in `δ+ω−1` positions | `edit_distance.max_cuts_in_window` |

## Lemma 1 (Unit isolation)

> For every unit `u`, the embedding `z_u` and the evidence `e_u` in
> Eq. (7) are functions of the byte string of `u` alone.

**Implementation.** `src/certmalconv/models/certmalconv.py::forward_units`
does not read any argument other than the byte string of the current
unit. The structural invariant is checked in two tests:

- `tests/test_unit_survival.py::test_evidence_unchanged_after_insertion`
  compares `e_u` on a unit before and after an insertion elsewhere in
  the file and asserts bit-identity.
- `tests/test_reproducibility.py::test_disassembler_bitwise` compares
  decoder output on the same tile across 5 seeds.

## Lemma 2 (Edit locality)

> Let `x′` be obtained from `x` by `s` edits at disjoint sites. Let
> `Z_i = [a_i, b_i + ω − 1]`. Then
> `d_U(x, x′) ≤ Σ (1 + |{p ∈ Z_i : κ_p(x) = 1}|)`.
> Appending content after the last byte alters at most the last unit.

**Implementation.**
`src/certmalconv/certification/edit_distance.py::edit_locality_bound`
returns the right-hand side given the cut positions of `x` (computed
once by the Gear pass).

**Independent verification.**
`experiments/08_certificate_verification/run.py` enumerates every edit
in the five families of Table XIV, applies them, re-unitizes, and
compares the number of altered units against the bound. The run logs
19,500 trials and zero violations.

## Lemma 3 (Cut-density bound)

> For a window of `δ + ω − 1` positions,
> `|{p ∈ Z : κ_p(x) = 1}| ≤ c_ω^δ(x)`.

**Implementation.** `edit_distance.max_cuts_in_window` returns
`c_ω^δ(x)` in one pass with a deque of size `δ + ω − 1`.

## Proposition 1 (Certified detection)

> Let `x` satisfy `ŷ_cert(x) = 1`. For every `ρ ≤ ρ*(x)` and every
> `x′ ∈ A_ρ(x)`,
> `S_k(x′) ≥ T_ρ(x) ≥ θ`, hence `ŷ_cert(x′) = ŷ(x′) = 1`. The pair
> `(ŷ_cert, ρ*)` is sound in the sense of Definition 2.

**Implementation.** `certification/certificate.py::certified_radius`
returns `ρ*(x) = max{ρ ∈ N : T_ρ(x) ≥ θ}` by scanning the sorted
evidences, which is the exact constructive form of the proof.

**Independent verification.** `certificate_verifier.py::verify` loads
the released checkpoint, computes `ρ*(x)` and `s_δ*(x)` for every
certified test malware, applies every admissible edit at most
`s_δ*(x)` times, re-runs the detector, and asserts both:

1. the file is still flagged (`ŷ(x′) = 1`),
2. every surviving unit has bit-identical evidence.

All 1,872 certified files kept their verdict on the full run
(see `results/certification/verifier_log.csv`).

## Corollary 1 (Edit-site certificate)

> Let `ŷ_cert(x) = 1`, and let `x′` be obtained from `x` by at most
> `s_δ*(x)` edits at disjoint sites. Then `ŷ(x′) = 1`.

**Implementation.** `edit_distance.edit_site_radius` computes
`s_δ*(x) = ⌊ ρ*(x) / (1 + c_ω^δ(x)) ⌋`. The proof combines Lemma 2
and Proposition 1; the code exposes each bound as a separate function
to make unit-testing trivial.

## Remark 1 (Tightness)

> The bound `S_k(x′) ≥ T_ρ(x)` cannot be improved without assumptions
> on attacker-chosen content.

The attacker that rewrites the `ρ` highest-evidence units into
near-zero content is implemented in `attacks/tur.py`. The verification
harness confirms that `S_k(x′)` approaches `T_ρ(x)` on such inputs; no
attack ever pushed `S_k(x′)` below `T_{ρ*(x)}(x)` on a certified file.

## Proposition 2 (OR gate)

> (i) If `ŷ_cert(x′) = 1` then `ŷ(x′) = 1`, whatever the value of
> `g(x′)`.
> (ii) With thresholds set by Eq. (19), the false-positive rate of `ŷ`
> on `D_cal` is at most `α_1 + α_2`.

**Implementation.** The OR is a one-line expression in
`models/certmalconv.py::decide`. Part (ii) is calibrated by
`training/calibration.py::calibrate_quantile` using empirical
quantiles. The union-bound assertion is checked at the end of every
calibration pass and logged to `results/calibration/*.csv`.

## Proof-to-code map (at a glance)

| Statement | File | Function |
|---|---|---|
| Lemma 1 | `models/certmalconv.py` | `forward_units` |
| Lemma 2 | `certification/edit_distance.py` | `edit_locality_bound` |
| Lemma 3 | `certification/edit_distance.py` | `max_cuts_in_window` |
| Proposition 1 | `certification/certificate.py` | `certified_radius` |
| Corollary 1 | `certification/edit_distance.py` | `edit_site_radius` |
| Remark 1 | `attacks/tur.py` | `TopUnitRewrite` |
| Proposition 2 | `models/certmalconv.py`, `training/calibration.py` | `decide`, `calibrate_quantile` |

## Scope of the certificate

The certificate is **one-sided and conditional**:

- It protects malicious verdicts against insertion of any size and up
  to `s_δ*(x)` local rewrites of at most `δ` bytes each.
- It says nothing about benign files that an attacker wants flagged.
- It says nothing about family labels; `FamilyHead` outputs are not
  covered by any proof.
- It does **not** cover the false-positive rate on unseen benign
  files; `α_1 + α_2` is a calibration-time guarantee.

Global rewrites (packing, whole-program virtualization) change almost
every unit and fall outside any useful radius; a static unpacking
stage, as used by DSMalConv, can run before unitization without
affecting the proof, in which case the certificate applies to the
unpacked bytes.
