# Work 085 Result: Generalized Meshed Torsion, Bearing, and Housing Route

Thai companion: `2026-09-04_085_generalized-meshed-torsion-bearing-housing-result.th.md`

## Status and outcome

Status: Stopped

All nine exact-geometry Gmsh/CalculiX solves converged and every force, moment, and energy residual passed. The work nevertheless stopped at its preregistered per-metric mesh-convergence gate: `converter_housing_mount` maximum displacement changed by `0.13187908211258156` (`13.1879%`) between the `6 mm` and `4.5 mm` meshes, exceeding the frozen `0.12` (`12%`) limit. The gate was not relaxed and no passing result was emitted.

The runner and contract remain useful fail-closed remediation infrastructure, but this work does not close Work 084's structural blocker and does not authorize Gate B or integration.

## Files changed

- `config/structural/generalized_meshed_torsion_bearing_housing_v1.json`
- `src/formula_ultimate/structural/generalized_coupling.py`
- `scripts/structural/run_generalized_structural_coupling.py`
- `tests/test_generalized_structural_coupling.py`
- `docs/contracts/GENERALIZED_MESHED_STRUCTURAL_COUPLING_V1.md` and Thai companion
- this result and its Thai companion
- the Work 085 plan and Thai companion, changed to `Stopped`

Generated solver evidence under `artifacts/work085/` is ignored and was not committed.

## Exact evidence

- `output_shaft_combined` last-two changes: displacement `3.9998%`, compliance `5.1700%`, p90 stress `1.6225%`; fine p90 stress `144476407.786 Pa`.
- `support_block_bearing`: displacement `4.2929%`, compliance `2.5150%`, p90 stress `8.8751%`; fine p90 stress `1675373.113 Pa`.
- `converter_housing_mount`: displacement `13.1879%` (failed), compliance `11.1479%`, p90 stress `8.3687%`; fine p90 stress `305585.035 Pa`.
- Maximum observed residuals across all nine solves: force `6.980456828420865e-7`, moment `1.4117028561584432e-6`, energy `4.489527613110193e-8`.
- Solver-evidence file SHA-256: `71244cf626bc593f953dc5c37329541eb55462340a6c28885601b4d733f2c247`.

Two earlier stopped roots exposed a CalculiX input serialization issue. Long free-field values such as `-2.2621670056434022E-06` were rejected even though they were finite. The runner now writes fixed-width scientific notation and removes only arithmetic noise below `1e-12 N`; all nine solves then completed. This correction changes input serialization, not results or gates.

## Validation commands

```powershell
python scripts\structural\run_generalized_structural_coupling.py `
  --config config\structural\generalized_meshed_torsion_bearing_housing_v1.json `
  --output-root artifacts\work085\run_g `
  --gmsh "C:\Program Files\FreeCAD 1.1\bin\gmsh.exe" `
  --ccx "C:\Program Files\FreeCAD 1.1\bin\ccx.exe"
# exit 1 after all nine solves; fail-closed at last-two mesh convergence

python -m unittest tests.test_generalized_structural_coupling tests.test_repository_contract -v
# exit 0; Ran 18 tests; OK

python -m compileall -q src scripts tests
# exit 0
```

## Evidence review and next work

Supporting evidence: exact upstream identities, nine converged solves, non-empty disjoint regions, residual closure, and two cases satisfying every mesh metric. Contradicting evidence: one housing displacement metric exceeds the gate. Alternative explanation: the housing's complex bores/fins require a finer asymptotic range than `8/6/4.5 mm`; the current trend cannot prove that without another frozen experiment. Missing evidence: finer housing meshes and exact replay of a passing result.

The next separately numbered work must freeze a finer housing sequence without changing the `12%` gate, reuse the already passing shaft/support evidence by exact identity, and rerun/replay before integration.
