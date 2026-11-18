# Threat Model

Section II-B of the paper fixes the attacker's goal, knowledge,
capability, and the defender's constraints. This document reiterates
them verbatim for the reproducibility record and lists what the
certificate does and does not cover.

## Attacker goal

The attacker holds a malicious binary `x` that the detector flags and
wants a binary `x′` that is classified as benign while keeping the
malicious behaviour of `x`. Attacks in the reverse direction (making
benign software look malicious) and training-time poisoning are
**outside scope**.

## Attacker knowledge (white-box)

The attacker knows:

- the full architecture,
- the model weights (including all five seeds),
- the thresholds `θ` and `θ_g`,
- the unitization parameters (Gear table `Γ`, `ω`, `ℓ`),
- the training data distribution.

The certificate does **not** rely on any secret.

## Attacker capability

Functionality-preserving edits are grouped into three classes:

| Class | Description | Covered by the certificate? |
|---|---|---|
| Insertion | append overlay, slack-space fill, section add, header extension | Yes, **unbounded** size |
| Local rewrite | trampoline at call site, call-based redividing, opcode insertion | Yes, up to `s_δ*(x)` sites of `≤ δ` bytes each |
| Global rewrite | packing, whole-program obfuscation, virtualization | Empirical evaluation only |

The budget is measured on the **byte string**, not per view. A single
problem-space edit alters every representation computed from the edited
bytes; the unit edit distance captures exactly that.

## Defender constraints

- **Static.** Reads the file once, does not execute it.
- **Linear time.** Decision in `O(n)` for a file of `n` bytes.
- **Bounded memory.** Independent of file size.

## Out-of-scope attacks

The certificate makes no claims about:

1. False-positive attacks that force a benign file into the flagged
   class.
2. Family-label manipulation (an attacker who cannot change the
   detection verdict may still change the predicted family;
   Section VII-A).
3. Training-time poisoning.
4. Global obfuscation that rewrites most of the file (packing,
   virtualization). For packed samples the detector sees the packer
   stub and the packed payload; detection then depends on whether these
   units are themselves suspicious. A static unpacking stage, as used
   by DSMalConv, can run before unitization without affecting the
   proof.
5. Software vulnerabilities in the decoder itself (e.g., a parser
   crash triggered by a crafted file). These are vulnerabilities, not
   learning problems. The linear-sweep decoder has a small attack
   surface because it does not follow control flow across the file.

## Attack suite used in the paper

| Attack | Space | Reference | Implementation |
|---|---|---|---|
| FGSM | feature | Goodfellow et al., 2015 | `attacks/fgsm.py` |
| SNIA | feature (graph) | Zapzalka et al., 2025 | `attacks/snia.py` |
| SNICA | feature (graph) | Zapzalka et al., 2025 | `attacks/snica.py` |
| Full DOS / Extend / Shift | problem (insertion) | Demetrio et al., 2021 | `attacks/insertion_attack.py` |
| MalGuise | problem (rewrite) | Ling et al., 2024 | `attacks/malguise.py` |
| PhantomCall | problem (rewrite) | Akil et al., 2026 | `attacks/phantomcall.py` |
| MalAOI | problem (rewrite) | Peng et al., 2025 | `attacks/malaoi.py` |
| TUR (greedy) | adaptive white-box | this paper | `attacks/tur.py` |
| TUR-Opt (beam) | adaptive white-box | this paper | `attacks/tur_opt.py` |

Functionality of every problem-space sample is checked dynamically in
an isolated sandbox (Cuckoo 2.0.7 for PE, Ubuntu 22.04 guest with
LiSa-style syscall tracing for ELF). Samples that crash, time out, or
fail to reach the original's security-relevant API calls are discarded
and do not count as successes. Adversarial samples are **never**
uploaded to public scanning services.
