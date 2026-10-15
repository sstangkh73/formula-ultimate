# Work 163 Result: v2 power transmission (rolling roller chain)

Thai companion: `2026-10-13_163_v2-power-transmission-result.th.md`

Plan: `2026-10-13_163_v2-power-transmission-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/power_transmission.py` (new):
  `add_power_transmission`, `power_transmission_problems`, `free_strip`,
  `bay_occupants`, `transmission_ids`, `PowerTransmissionConfig`
  (version `func-power-transmission-v1`).
- `scripts/hierarchy/generate_functional_vehicle.py`: calls
  `add_power_transmission` after `add_direction_control`, adds
  `power_transmission_problems` to the mechanism re-check and hashes the
  config under `power_transmission` in `config_sha256`.
- `tests/test_hierarchy_power_transmission.py` (new, 7 tests).
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`).

## Decisions

- One root-level assembly `m<k>-power_transmission` (k = 6) tagged
  `[power_transmission]` with 2 or 3 stations laid along y in the free -x
  strip of the deck bay (from `bay_x0 + 0.02 m` to the nearest bay
  occupant's sweep circle minus 0.02 m). Each station: boss (`bonded` to the
  deck), post (`bonded` to the boss), roller (N_r-gon disc, N_r in
  {48, 64, 96}, Work 162 96-gon bore of apothem `r_p + c`, c = 2.5e-5 m,
  floating c above the boss, `bearing` to the post).
- Neighbouring roller centres are `R_i + R_j + c` apart (circumradii) with a
  vertex pointing at each neighbour, so the sampled vertex gap of each
  `rolling` interface is c and no full-turn sweep can reach a neighbour.
- Motions `<assembly>.r<i>` = {roller i}, revolute about +z, range 2 pi.
  Evidence `power_transmission: {chain: [r0, r1, ...]}`.
- If the strip is narrow, roller radii are clamped and the last station is
  dropped; planning raises if even two minimum rollers do not fit.

## Validation

| Command | Exit | Output |
|---|---|---|
| `python -m unittest tests.test_hierarchy_power_transmission tests.test_hierarchy_direction_control` | 0 | `Ran 15 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed S --out artifacts/work163/seedS` (S = 11, 23, 37) | 0 | packages written |
| `python artifacts/work163/check.py artifacts/work163 TierA0Interfaces TierA2Motions TierB3PowerTransmission TierB4GroundPropulsion TierB5DirectionControl TierB6Braking TierA1GeometryLanguage TierA3Inertia` (acceptance classes, nine-key check relaxed locally) | 0 | `Ran 10 tests`, `OK` |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work163/seed11/manifest.json --out artifacts/work163/l0_seed11.json` | 0 | `finished`, 10757.947 s, 1993.034 kg, residual 0.0 J |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1163 tests`, `OK (skipped=11)`; Gate 3 `Ran 41 tests`, `FAILED (failures=9)`, only B1-B9 (nine-key check) |

Transmission evidence: seeds 11/23/37 chain length 3/2/3 rollers, each
range 2 pi rad, 2/1/2 `rolling` interfaces.

## Limitations

- The rollers are not linked to the wheels or a converter; no torque,
  efficiency, slip or tooth model. Contact is one vertex pair per pair of
  rollers (a sampled proxy).
- B3 can only pass in the real suite after all nine evidence keys exist.
- Representation gate only, not physical validation.

## Follow-up

Energy converter (chamber with a bore + guided prismatic piston), energy
storage vessel and controller housing with internal voids, heat-rejection
fins, then the B7 load-structure reach check.
