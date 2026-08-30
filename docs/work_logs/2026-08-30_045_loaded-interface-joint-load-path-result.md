# Work 045 Result: Loaded Interface and Joint Load Path

Status: Completed

Thai companion: `2026-08-30_045_loaded-interface-joint-load-path-result.th.md`

## Outcome

Execution and the mesh/equilibrium/energy/identity hypotheses passed. The combined preferred hypothesis was rejected because the one-support compliance changed by `299.021%`; transferability outside the exact two-support fixture is blocked.

## Files changed

- `config/structural/loaded_interface_plate_v1.json`
- `src/formula_ultimate/structural/loaded_interface.py` and structural exports
- `scripts/cad/generate_loaded_interface_plate.py`
- `scripts/cad/inspect_loaded_interface_freecad.py`
- `scripts/structural/run_loaded_interface_acceptance.py`
- `scripts/run_work045.ps1`
- `tests/test_loaded_interface.py`
- `docs/physics/LOADED_INTERFACE_JOINT_LOAD_PATH.md` and `.th.md`
- matching Work 045 plan/result pairs

Ignored CAD/STEP/mesh/solver evidence is under `artifacts/work045/`.

## Decisions and deviations

- Used geometric center/radius/axis/area signatures because STEP does not preserve application face labels reliably.
- Froze `6/4/3 mm` mesh levels before any structural result.
- The first solver attempt was not admitted: `.17g` coordinates exceeded the CalculiX free-field parser limit. `.12g` serialization fixed only the deck interface and preserved the frozen geometry/meshes.
- A replay probe found OCCT wall-clock time was the sole difference between otherwise identical STEP files. Canonicalizing that header produced identical repeat hashes without changing geometry.
- Mesh convergence passed, while the retained one-support solve rejected transferability as designed.

## Validation

```powershell
py -3.14 -m unittest tests.test_loaded_interface -v
# exit 0; Ran 3 tests; OK

.\scripts\run_work045.ps1
# exit 0; status=passed; mesh_convergence=supported; transferability=rejected

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 310 tests in 24.032s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0

git diff --check
# exit 0

# two independent CAD exports after canonicalization
# identical SHA-256: 6F20D310970723738ABAFB19FA212264F14A5147880144280C2DBE92502C4AEE
```

Fine baseline force/moment/energy residuals were `4.14e-9`, `1.08e-9`, and `2.28e-8`. Last-two compliance change was `0.6959%`. The one-support sensitivity changed compliance by `299.021%` and peak von Mises from `5.60` to `27.61 MPa`.

## Limitations and follow-up

The interfaces are rigid bonded cylindrical surfaces, not contact joints. Raw maximum stress is reported but not promoted as bearing strength. Gate A remains open because Work 041 cross-element convergence and Work 045 transferability are rejected. Work 046 must not begin as a promotable structural-fitness coupling until separately numbered remediation resolves or explicitly bounds both blockers.
