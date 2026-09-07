# Evidence index

Every claim made about this project in a CV, abstract, or competition submission
should be checkable by a reader with no access to the author. This file names the
claim, the artifact behind it, and the command that reproduces it.

Repository: https://github.com/sstangkh73/formula-ultimate
Author ORCID: https://orcid.org/0009-0000-2979-1916
Licence: code MIT (`LICENSE`), documents and data CC BY 4.0 (`LICENSE-DATA.md`)

## Scale of the codebase

| Claim | How to check |
| --- | --- |
| Python modules | `git ls-files '*.py' \| wc -l` |
| Lines of Python | `git ls-files '*.py' \| xargs cat \| wc -l` |
| Automated test files | `git ls-files 'tests/*.py' \| wc -l` |
| The suite passes | `python -m pip install -e . && python -m unittest discover -s tests -v` |

These are counts at the current commit, not figures frozen in a document. Any
number quoted elsewhere should agree with what these commands return; if it does
not, the commands are correct and the document is stale.

## Continuous integration

The test suite runs on every push and pull request via GitHub Actions:
[`.github/workflows/tests.yml`](.github/workflows/tests.yml).

This is the strongest verification available here — a reader does not need to
take "the tests pass" on trust, or even run anything locally. The run history at
https://github.com/sstangkh73/formula-ultimate/actions shows whether the suite
passed at each commit, including commits made before any CV was written.

## Research claims

| Claim | Where it is defined or enforced |
| --- | --- |
| Agents design a complete 3D vehicle without a prescribed conventional architecture | Research question and constraints in `README.md`; the discovery pipeline in `src/` |
| The race and energy contract derives from the published 2026 FIA Formula One regulations | `README.md` cites Sporting Regulation B5.1.4 and Technical Regulation C6.4.4, with links to the FIA source documents |
| All primary propulsion energy must be carried before the race, with no replenishment during it | Encoded as a checked constraint, not a stated intention — see the energy accounting in `src/` and its tests under `tests/` |
| Designs are accepted only after multi-fidelity physics validation | Evidence gates in `src/`, exercised by the test suite |
| A design cannot win by exploiting the simulator | Conservation-residual and validation gates; see the gate tests in `tests/` |

## What "fastest" means here, stated precisely

The objective is the lowest total race time **among candidates that complete the
declared race and pass the required evidence gates**. It is not peak speed, and
it is not a short-lived run before structural or thermal failure. This
distinction is written into `README.md` because an unstated objective is not a
checkable one.

## What is not claimed

- No result is claimed to beat a conventional Formula One car in reality. The
  comparison is against optimised conventional baselines inside the declared
  simulation contract.
- Physics fidelity is layered and bounded. Passing the current gates means a
  design survived the fidelity levels implemented so far, which is stated in the
  reports rather than implied to be complete.
- Where a research question is still open, `docs/` records it as a plan, not a
  finding. Plans under `docs/plans/` are intentions; only reports carry results.
