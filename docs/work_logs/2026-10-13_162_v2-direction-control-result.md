# Work 162 Result: v2 direction control (steering post and arm)

Thai companion: `2026-10-13_162_v2-direction-control-result.th.md`

Plan: `2026-10-13_162_v2-direction-control-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/direction_control.py` (new):
  `add_direction_control`, `direction_control_problems`, `steering_bore`,
  `convex_hull`, `steer_ids`, `DirectionControlConfig`
  (version `func-direction-control-v1`).
- `scripts/hierarchy/generate_functional_vehicle.py`: calls
  `add_direction_control` after `add_ground_contacts`, adds
  `direction_control_problems` to the mechanism re-check and hashes the config
  under `direction_control` in `config_sha256`.
- `tests/test_hierarchy_direction_control.py` (new, 8 tests including one CAD
  realization test).
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`).

## Decisions

- Steering is a root-level assembly `m<k>-direction_control` (k = 5 with four
  ground corners) with boss (`bonded` to the deck), post (`bonded` to the
  boss) and arm (`bearing` to the post), all `func-leaf-mechanism-v2` prisms
  along +z. The motion is `{arm}`, revolute about +z through the post axis,
  range drawn in [0.3, 0.8] rad. The axis is perpendicular to every
  ground-contact axis (y).
- Bore: 96-gon, apothem `r_p + c` (c = 2.5e-5 m), vertex at every post
  vertex direction (96 is a multiple of 6 and 8), so the static gap is c, the
  vertex samples see the bearing contact, and no rotation can penetrate.
- The arm floats c above the boss top (thrust clearance, not modelled as a
  contact). The post is placed at the +x end of the bay, centred in y, with
  the full sweep circle 0.02 m inside the bay and the deck sides; if the bay
  or deck is narrow, the arm length is shortened (an error is raised if it
  cannot exceed the hub radius). The -x part of the bay stays free.

## Validation

| Command | Exit | Output |
|---|---|---|
| `python -m unittest tests.test_hierarchy_direction_control tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms` | 0 | `Ran 26 tests`, `OK` |
| `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed S --out artifacts/work162/seedS` (S = 11, 23, 37) | 0 | 268 / 267 / 270 leaves, 5 motions each |
| `python artifacts/work162/check.py artifacts/work162 TierA0Interfaces TierA0Hierarchy TierA0Capabilities TierA0NoFixedTemplate TierA1GeometryLanguage TierA2Motions TierA3Inertia TierB4GroundPropulsion TierB5DirectionControl TierB6Braking` (acceptance classes, nine-key check relaxed locally) | 0 | `Ran 14 tests`, `OK` |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work162/seed11/manifest.json --out artifacts/work162/l0_seed11.json` | 0 | `finished`, 10756.945 s, 1988.451 kg, residual 0.0 J |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 1 | Gate 1 PASS; Gate 2 `Ran 1156 tests`, `OK (skipped=11)`; Gate 3 `FAILED (failures=9)`, only B1-B9 (nine-key check) |

Steering evidence: seeds 11/23/37 range 0.743/0.792/0.393 rad; root mass
1988.5/2096.5/1484.0 kg.

## Limitations

- The arm is not linked to the wheels; there is no steering geometry or
  vehicle dynamics. Axial retention of the arm is not modelled.
- B5 can only pass in the real suite after all nine evidence keys exist.
- Representation gate only, not physical validation.

## Follow-up

Power transmission (two full-turn rollers on posts with a `rolling` contact),
energy converter (chamber + guided piston), vessel and controller housing
with voids, heat-rejection fins, then the B7 backbone reach check.
