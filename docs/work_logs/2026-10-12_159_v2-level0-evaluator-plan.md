# Work 159 Plan: v2 Level-0 evaluator on the existing race kernel

Thai companion: `2026-10-12_159_v2-level0-evaluator-plan.th.md`

Status: Completed

## Objective

Add `scripts/hierarchy/evaluate_level0.py`, which reads a v2 package manifest
and runs the existing `physics/race.py` kernel (`race-level0-v1`) on the
vehicle's root mass and a drag area bounded by its mesh frontal extent. This
targets acceptance Tier C1.

## Scope

- `src/formula_ultimate/hierarchy/level0.py`: pure functions to read the
  manifest, measure the leaf-mesh frontal (y-z) extent, build the
  `RaceVehicle`/`RaceControl` from a versioned config, run `run_full_race` and
  return exactly the nine contract fields.
- `config/hierarchy/level0_race_v1.json`: circuit id, drag coefficient on the
  frontal box, rolling resistance, tractive force, onboard energy, thermal
  parameters and control settings, all SI.
- `scripts/hierarchy/evaluate_level0.py`: CLI `--manifest`, `--out`.
- `tests/test_hierarchy_level0.py`: new tests.

## Physical assumptions (SI)

- Mass: the manifest root `mass_kg`, unchanged (lumped point mass).
- Drag area: `C_box * extent_y * extent_z`, `C_box = 1.0`, with extents from
  all leaf mesh vertices. This is a bound, not a derived drag (contract allows
  `0 < A <= 1.5 * extent_y * extent_z`).
- Rolling resistance coefficient 0.015, air density from the circuit (ISA) or
  1.225 kg/m^3, gravity 9.80665 m/s^2, zero grade.
- Constant commanded tractive force 4000 N, onboard energy 4.0e9 J (more than
  `F * race distance`), no waste heat or auxiliary power, so the thermal model
  stays at ambient. Circuit `monza_2026` from `config/circuits/real_circuits_v1.json`.
- Time step 1 s, timeout 36000 s, 64 bisection iterations, seed 0.

## Validation

- `python -m unittest tests.test_hierarchy_level0 -v`
- Run the CLI twice on the Work 158 seed-11 package and compare bytes; run with
  root mass x1.5 and check it is slower.
- `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass).

## Success criteria

Tests pass, Gates 1-2 pass, and TierC1 passes in Gate 3 (or fails only for a
reason recorded in the result).

## Experiment definition

- Independent variable: root mass (x1.0 vs x1.5).
- Dependent variable: race time and outcome.
- Controls: the same circuit, force, energy, drag area and control settings.
- Failure criterion: the heavier vehicle is not slower (the race ignores the
  vehicle).

## Risks

- Under constant force, a mass change alters time only through acceleration
  and rolling resistance; both scale with mass, so the check should hold.
- The drag box is a bound, not aerodynamics.

## Non-goals

No B1-B9 capability geometry, no new race model, no claim of lap time or
physical validity.
