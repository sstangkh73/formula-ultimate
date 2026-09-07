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
[`.github/workflows/tests.yml`](.github/workflows/tests.yml). The run history at
https://github.com/sstangkh73/formula-ultimate/actions shows the result at every
commit.

### Current status

As of 7 September 2026, the suite is green on both platforms:

| Environment | Result |
| --- | --- |
| Local, Windows, Python 3.14 | `Ran 794 tests` — **OK (skipped=8)** |
| CI, Ubuntu, Python 3.11 and 3.14 | `Ran 794 tests` — **OK (skipped=32)** |

The extra skips on CI are the tests that replay recorded evidence from
`artifacts/`, which `.gitignore` excludes because of its size. They skip with a
message naming the missing path rather than failing, so a clean checkout can
reach a green run; where the artifacts are present the same tests run and assert
exactly what they did before.

### The cross-platform difference that used to make CI red, and how it was fixed

Until 7 September 2026 two tests failed on Linux while passing on Windows. Both
compared a SHA-256 digest of a simulation run against a recorded value. The
cause was found by measurement, not by guessing, and the method is reusable:
[`tools/xplat_digest_probe.py`](tools/xplat_digest_probe.py) prints every
intermediate quantity as a float hex literal, ordered from the C library upward,
so diffing two platforms names the first layer that diverges.

What the probe showed, in order:

1. The parsed configuration, the initial state, and the first three simulation
   steps were **bit-identical** on both platforms. The inputs were not the
   problem, and neither was line-ending or JSON parsing.
2. Running the probe on Linux under both Python 3.11 and 3.14 gave **identical**
   output, which ruled out the interpreter version and the numpy version.
3. Tracing every math call located the first differing value: an argument to a
   tyre force calculation, one unit in the last place apart.
4. The normal-load solve upstream of it was bit-identical, so the difference was
   in the requested force, not the load.
5. The requested force comes from the wheel slip law, which computed it with
   **`math.tanh`**. IEEE 754 does not require the elementary functions to be
   correctly rounded, and the Windows UCRT and Linux glibc disagreed by one ulp
   on **35 of 111 sampled arguments**, and on **9 of the first 40 calls** this
   model makes. The first divergence in the entire run was
   `tanh(0x1.3755407c17994p-10)`, returning `...385` on Windows and `...386` on
   Linux.

One ulp was enough because the longitudinal slip heat is computed as a
difference of nearly equal terms, which amplified it by roughly two hundred
times within a few steps, and from there it reached the differential speed, the
recorded state, and the digest.

The fix computes tanh in decimal arithmetic
([`src/formula_ultimate/physics/deterministic_math.py`](src/formula_ultimate/physics/deterministic_math.py)),
which is a software implementation with deterministic semantics rather than a
call into the host C library. The digests for work 073 and work 074 were
rerecorded because the computation changed; the historical evidence under
`artifacts/` still holds the values the old slip law produced and was left
untouched. [`tests/test_deterministic_math.py`](tests/test_deterministic_math.py)
now asserts the exact bit patterns, so the property is enforced rather than
assumed.

### What is still true about reproducibility here

The model calls other elementary functions — 28 `cos`, 26 `sin`, 9 `atan2`,
and others — that carry the same risk. They agree between these two platforms at
the arguments this model currently reaches, and the green CI run is evidence of
that, but it is not a proof that they always will. A digest recorded on one
machine reproducing on another is therefore an **empirical result for the
configurations under test**, not a guarantee for every future configuration.
Saying otherwise would overstate what has been demonstrated.

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
