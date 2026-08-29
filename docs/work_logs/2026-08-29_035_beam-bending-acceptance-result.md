# Work 035 Result: Beam-Bending Acceptance

Status: Completed

Thai companion: `2026-08-29_035_beam-bending-acceptance-result.th.md`

## Outcome

The linear beam-bending specimen is implemented and passed through three real
Gmsh/CalculiX meshes. The accepted evidence closes transverse force and support
moment, matches Euler-Bernoulli tip displacement/external work, reproduces the
signed interior `Sxx` field within the declared RMS gate, and passes last-two-
mesh convergence.

## Files changed

- `config/structural/beam_bending_acceptance_v1.json`
- `src/formula_ultimate/structural/acceptance.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_beam_bending_acceptance.py`
- `scripts/run_work035.ps1`
- `tests/test_beam_bending_acceptance.py`
- `tests/test_structural_acceptance.py`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.md`
- `docs/physics/BEAM_BENDING_ACCEPTANCE.th.md`
- Work 035 plan/result records in English and Thai

Ignored replay evidence was generated under `artifacts/work035/`.

## Decisions and observed failures

- CalculiX node sets are now wrapped at 16 entries per line. The initial coarse
  run exposed this format limit with 18 fixed nodes and exited `201`; the run was
  rejected before physical evaluation and a regression test was added.
- Complete six-component stress tensors are retained by the parser. Work 034's
  axial-stress view remains derived from the same admitted tensor evidence.
- Total reaction force uses CalculiX's explicit total row to avoid summing
  per-node values rounded for text output. Reaction moment is computed from
  nodal reactions about the fixed-face centroid.
- `Sxx` is evaluated at tetrahedron centroids with volume-weighted signed RMS
  error and signed correlation over a predeclared interior domain.
- The original `6 mm`-deep fixture and coarse meshes failed bending accuracy.
  Later `2.0 mm` and `1.5 mm` trials failed the unchanged `15%` stress RMS gate
  at `19.77%` and `15.14%`. The accepted sequence begins at `1.4 mm`; tolerance
  was not loosened.

## Accepted evidence

References: tip `2.38095238095238e-5 m`, root moment `0.6 N*m`, root outer
stress `2.08333333333333e6 Pa`, external work `5.95238095238095e-5 J`.

| Mesh | Nodes | C3D4 | Tip error | Stress RMS | Correlation | Force closure | Moment closure |
|---|---:|---:|---:|---:|---:|---:|---:|
| coarse_1p4mm | 6,944 | 31,022 | 4.1889% | 14.2772% | 0.989799 | 3.54e-12 | 2.66e-8 |
| medium_1p2mm | 10,343 | 48,003 | 3.1378% | 12.1645% | 0.992602 | 1.83e-12 | 4.22e-8 |
| fine_1mm | 16,767 | 81,764 | 2.2179% | 10.1221% | 0.994880 | 4.59e-12 | 2.46e-8 |

Last-two displacement/work change was `0.00949702932475448`; stress-error
absolute change was `0.0204245660076813`. All gates passed.

## Validation

Commands returned exit `0` in fail-fast order:

```powershell
py -3.14 -m unittest tests.test_beam_bending_acceptance tests.test_structural_acceptance -v
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work035.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\run_work034.ps1
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```

Relevant output:

```text
focused: Ran 12 tests ... OK
Work 035: status=passed, 3 meshes, fine=16767 nodes/81764 C3D4
Work 034 regression: status=passed, 3 meshes
full: Ran 280 tests in 36.865s ... OK
compileall: no output
git diff --check: no errors
git diff --cached --check: no errors
```

The staged scope contained only the 13 explicit Work 035 files. The commit hash
will be reported in the final handoff.

## Falsification review and limitations

Supporting evidence includes load/moment closure, analytical global response,
signed stress-field agreement, mesh convergence, fresh artifacts, and retained
failed attempts. The simple regular beam and excluded end regions remain strong
alternative explanations; this is not arbitrary-geometry validation.

No independent solver or physical beam data was used. Internal strain energy
is not independently parsed. Yield, plasticity, torsion, buckling, fracture,
fatigue, joints, connection removal, and `DNF` coupling remain missing. The next
work item is the separately gated solid-shaft torsion specimen.
