# Limitations

## 1. Certificate scope

The certificate is **one-sided** and **conditional**.

- It protects malicious verdicts only. A benign file that an attacker
  wants flagged is not covered.
- It covers insertion of any size and up to `s_δ*(x)` local rewrites
  of at most `δ` bytes each. Global rewrites (packing, whole-program
  virtualization) fall outside any useful radius.
- The family label is not certified. An attacker who cannot change
  the detection verdict can still move probability between known
  families without crossing the energy threshold `η`.
- The false-positive rate is controlled statistically by calibration
  (Proposition 2) and holds on `D_cal` by construction. On unseen
  benign files it holds only under exchangeability of calibration and
  deployment files; benign drift breaks the assumption and requires
  recalibration (see Table XVIII).

## 2. Cost of the guarantee

The top-*k* rule ignores weak evidence spread over many units, which
costs recall on malware whose malicious logic is thin and distributed.
The OR gate recovers part of this recall, but files detected only by
the global branch carry **no certificate**, and the gate spends part
of the false-positive budget. The certified share of detections,
rather than overall accuracy, is therefore the figure to watch when
tuning `k`, `α_1` and `α_2`.

## 3. Decoder assumptions

The proof assumes the decoder computes the same local graph from the
same bytes. A decoder bug that a crafted file could trigger (a parser
crash, for example) is a software vulnerability, not a learning
problem. The linear-sweep decoder has a small attack surface compared
with whole-program analyzers because it does not follow control flow
across the file, but it is not formally verified.

## 4. Dataset validity

In the dataset groups of DSMalConv, benign and malicious files come
from different sources within each group. A detector can exploit
source artefacts (compiler or linker signatures) rather than malicious
behaviour. We measure the risk in Section VI-K (Table XVI) with six
controls:

- near-duplicate filtering (TLSH, Jaccard on unit multisets),
- family-aware splits (AVClass2),
- malware-source held out (BODMAS, SOREL, VirusShare),
- benign-source held out,
- toolchain-artefact normalisation,
- the MOTIF common-collection experiment.

The gap between CertMalConv and DSMalConv stays ≤ 0.26 F1 points
across all controls. A source-artefact probe reaches 68.47% accuracy,
so some artefact signal is present but bounded.

## 5. Empirical attacks hold only for what we ran

The certificate holds for **any** edit within the stated budget. The
empirical attack results (Table IX, Table XV) hold only for the
attacks we implemented. Stronger adaptive attacks against the global
branch remain possible and do not violate the certificate when they
succeed, because the global branch is **not** certified.

## 6. Reimplemented baselines

Table XIX lists which baselines are run from released code (R) and
which are reimplemented from their papers (I). A reimplementation may
understate the performance of a baseline whose code is not public.
Readers who want to re-examine a specific baseline comparison should
consult the configuration under `baselines/<method>/` and, where
available, the official repository.

## 7. Hardware and software coupling

Reported timings assume a single NVIDIA A100-SXM4 40 GB. The
end-to-end 5.32× speedup over DSMalConv is a function of both the
algorithmic cost (Section IV-C) and the kernel efficiency on this
hardware. Users on other hardware should recompute the latency table
locally; the slope of the latency-vs-size curve (`0.044 ms/KiB`) is
hardware-dependent but its linearity is not.

## 8. Operational scope

The paper concerns static detection and classification. The
certificate does not transfer to dynamic analysis (sandbox verdicts,
behavioural monitors), and the operational configuration
(`k = 3`, `α_1 = α_2 = 0.05%`) was tuned for the five dataset groups
of DSMalConv. A deployment with a different base rate of malware or a
different tolerance for false positives should recalibrate thresholds
rather than reuse ours blindly.
