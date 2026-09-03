# Work 082 Result: Geometry-to-Structural Physics Coupling V1

Thai companion: `2026-09-03_082_geometry-structural-coupling-v1-result.th.md`

## Status and verdict

Status: Completed

Verdict: the exact Work 081 bracket STEP/interface identity now drives a real three-level Gmsh/CalculiX software-coupling experiment. All residual and refinement gates passed, the reference remained in the synthetic elastic domain, and a severed critical connection causally removed its transmitted wrench and produced `dnf`. Because the bound material is synthetic, `design_use_allowed=false`; this is not real-part capacity.

## Files changed

- `config/structural/geometry_structural_coupling_v1.json`
- `src/formula_ultimate/structural/geometry_coupling.py`
- `scripts/structural/run_geometry_structural_coupling.py`
- `tests/test_geometry_structural_coupling.py`
- `docs/contracts/GEOMETRY_STRUCTURAL_COUPLING_V1.md` and Thai companion
- this result and Thai companion
- the Work 082 plan and Thai companion, marked `Completed`

Generated mesh, deck, DAT, FRD, and result evidence remains ignored under `artifacts/work082/`.

## Evidence and decisions

- Exact STEP, FreeCAD report, surface signature, and synthetic material-record hashes are checked before meshing.
- Gmsh imported the STEP and produced `2,924`, `8,542`, and `17,463` C3D4 elements.
- Medium-to-fine changes were approximately `1.27%` displacement, `1.11%` compliance, and `1.65%` p90 stress, below `5%`.
- Fine residuals were `4.4238208804794904e-8` force, `2.249840148494702e-8` moment, and `3.1124177238745204e-8` energy.
- Fine displacement was `1.5955631992710995e-5 m`; p90 von Mises stress was `3.926391799777586e6 Pa`.
- Raw CalculiX FRD includes a runtime `1UTIME` value. Only that one field is canonicalized for hashing; missing/ambiguous time metadata rejects. Raw FRD remains preserved.
- Exact reruns produced result identity `3b5d82a7a60f68a8420f1fe5bea9915e494cc29f98bf568e1862903e929b805a` and identical result-file SHA-256 `48636e7c20f520d9c6800ab8a893fe4f0e9bb8d2c55acb9a22b94d056b0be44b`.

Supporting evidence: three converged meshes, closed force/moment/energy ledgers, stable refinement, exact replay, and causal failure propagation. Contradicting evidence: raw FRD byte identity changes only with its clock field; canonical evidence records this rather than claiming raw equality. Alternative explanation: bonded constraints and linear elasticity can make the bounded response appear cleaner than a real joint. Missing evidence: sourced material/process, contact/preload/friction, plastic redistribution, fracture, fatigue, and experiment. Confidence is high for this software path and low for real capacity.

## Exact validation

```powershell
python scripts/structural/run_geometry_structural_coupling.py `
  --config config/structural/geometry_structural_coupling_v1.json `
  --geometry-root artifacts/work081 `
  --output-root artifacts/work082/run_d `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# run_d exit 0; run_e exit 0; identical result identity/file hash

python -m unittest tests.test_geometry_structural_coupling -v
# exit 0; Ran 10 tests; OK

python -m unittest tests.test_geometry_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 16 tests; OK

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests -q
# exit 0; Ran 534 tests in 410.066s; OK (skipped=3)
```

## Limitation and follow-up

Work 083 may consume the exact geometry/solver interface and failure protocol, but it may not claim a validated ground-interaction design while material/process evidence remains synthetic. Any such candidate must state a non-admission verdict or obtain separate sourced evidence.
