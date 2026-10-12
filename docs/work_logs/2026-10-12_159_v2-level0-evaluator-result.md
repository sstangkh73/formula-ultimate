# Work 159 Result: v2 Level-0 evaluator on the existing race kernel

Thai companion: `2026-10-12_159_v2-level0-evaluator-result.th.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/level0.py` (new): manifest root mass,
  leaf-mesh frontal (y-z) box, drag area `C_box * extent_y * extent_z`,
  `RaceVehicle`/`RaceControl` from config, `run_full_race`, nine output fields,
  deterministic `result_bytes` (sorted keys, indent 2).
- `config/hierarchy/level0_race_v1.json` (new): `monza_2026`, `C_box = 1.0`,
  `C_rr = 0.015`, 4000 N, 4.0e9 J, no waste heat or auxiliary power, time step
  1 s, timeout 36000 s, 64 bisection iterations, seed 0.
- `scripts/hierarchy/evaluate_level0.py` (new): CLI `--manifest`, `--out`,
  optional `--config`.
- `tests/test_hierarchy_level0.py` (new, 7 tests).
- `auto-loop/progress.md`, and these plan/result records.

## Decisions

- Mass is the manifest root `mass_kg` as written (no recomputation), so the
  race responds to the declared vehicle mass.
- The drag area is a bound on the frontal box, not a derived drag; the
  contract only bounds it (`<= 1.5 * extent_y * extent_z`).
- Constant force with no thermal load keeps the run to the kernel's
  longitudinal and energy paths; no new race model was written.

## Validation

- `python -m unittest tests.test_hierarchy_level0 -v`: exit 0, `Ran 7 tests`, `OK`.
- `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work158/seed11/manifest.json --out artifacts/work159/a.json`
  (and again to `b.json`), then `cmp`: identical. Output: `finished`,
  `race_time_s = 8563.913278125894`, `mass_kg = 351.9110894669954`,
  `drag_area_m2 = 5.022968018346177`, `consumed_energy_j = 1226880000.0`,
  residual `0.0`. Runtime about 3 s.
- Falsification check (root mass x1.5, `artifacts/work159/heavy`): `finished`,
  `race_time_s = 8593.223`, `mass_kg = 527.867`, so slower by about 29.3 s.
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 PASS; Gate 2
  `Ran 1130 tests`, `OK (skipped=11)`; Gate 3 `FAILED (failures=9)`: v1 13/13,
  v2 all of Tier A, B10 and **C1 pass**; B1-B9 fail (no `function_evidence`).

## Review

- Supporting evidence: the race time increases with mass; output is
  byte-identical; the kernel id comes from the kernel's replay metadata.
- Contradicting evidence / limits: the mass effect is small (+0.34 % for
  +50 % mass) because a large frontal box (5.0 m^2) makes drag dominate and a
  constant force ignores power limits. The time is not a lap-time prediction.
- Alternative explanation: none for the direction of the effect; acceleration
  and rolling resistance both scale with mass.
- Confidence: high for the coupling gate, none for performance claims.

## Limitations

Lumped mass and bounded drag only; no cornering, power limit, or thermal load.
Not physical validation.

## Follow-up

B1-B9 capability modules and `function_evidence` (all nine needed before any
B1-B9 test can pass).
