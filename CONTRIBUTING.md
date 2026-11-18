# Contributing

Thank you for considering a contribution to CertMalConv. The repository
accompanies a peer-reviewed article, so patches should be small, testable,
and consistent with the published methodology.

## Scope of contributions we accept

| Welcome | Not accepted |
|---|---|
| Bug fixes in the unitizer, certificate code, or attack implementations | Changes that weaken the certificate or alter the threat model |
| Additional baseline wrappers | Live malware samples of any kind |
| Documentation improvements | Credentials, API keys, VirusTotal/VirusShare data dumps |
| New unit tests, especially for edge cases of the Gear hash | Feature changes unrelated to the published method |
| CI/benchmarking improvements | Breaking changes without a major version bump |

## Development setup

```bash
git clone https://github.com/certmalconv/certmalconv.git
cd certmalconv
conda env create -f environment.yml
conda activate certmalconv
pip install -e ".[dev]"
pre-commit install
```

`pre-commit` runs `ruff`, `black`, and `mypy` on each staged change and
rejects obviously bad hygiene (debug prints, `pdb.set_trace`, trailing
whitespace, mixed line endings).

## Running the test suite

```bash
pytest tests/ -q                 # fast tests only
pytest tests/ -q --run-slow      # includes certificate verification (~5 min)
pytest tests/ -q --run-full      # includes 19,500-trial harness (~3 h)
```

Please add a test for every bug fix so the defect cannot regress.

## Commit style

The project uses Conventional Commits:

```
<type>(<scope>): <short summary>

<body, 72 chars wrapped>

Refs #<issue>
```

`<type>` is one of `feat`, `fix`, `docs`, `test`, `refactor`, `perf`,
`chore`. Scopes typically match a top-level `src/certmalconv/` module
(e.g. `certification`, `unitization`, `attacks`). Commits that change
the certificate must include the string `[cert]` in the subject so
reviewers can grep the history easily.

## Pull-request checklist

- [ ] All tests pass locally (`pytest tests/ -q`).
- [ ] New or changed behavior has a test.
- [ ] Public APIs have docstrings; mathematical claims cite the paper
      section/equation they implement.
- [ ] `ruff check src/ tests/` is clean.
- [ ] The CHANGELOG has an entry under *Unreleased*.
- [ ] If the certificate code was touched, the harness in
      `experiments/08_certificate_verification/` reports zero violations.

## Responsible-research guidelines

- Do **not** submit live malware samples, cryptographic material, or
  anything that identifies a non-public dataset collection endpoint.
- New attacks must be accompanied by a functionality-preservation test.
- If you uncover a vulnerability in the certificate implementation
  (an instance where the implementation claims a sound radius that the
  proof does not support), please disclose privately to the maintainers
  at `security@certmalconv.github.io` before opening a public issue.

## Getting help

Open a GitHub Discussion for conceptual questions and a GitHub Issue for
concrete bugs or reproducibility failures.
