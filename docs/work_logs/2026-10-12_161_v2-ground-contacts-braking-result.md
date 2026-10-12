# Work 161 Result: v2 ground contacts with braking rotors and stators

Thai companion: `2026-10-12_161_v2-ground-contacts-braking-result.th.md`

Plan: `2026-10-12_161_v2-ground-contacts-braking-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/ground_contacts.py` (new, pure Python):
  `GroundContactConfig`, `draw_corner_geometry`, `y_prism`, the profiles,
  `add_ground_contacts`, `ground_contact_problems`,
  `ground_contact_config_record`.
- `scripts/hierarchy/generate_functional_vehicle.py`: calls
  `add_ground_contacts` after `plan_mechanisms`, re-checks with both problem
  functions, and hashes the ground-contact record inside the mechanism record.
- `tests/test_hierarchy_ground_contacts.py` (new, 8 tests including one CAD
  realization test).
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`).

## Decisions

- `plan_mechanisms` is unchanged (its protected Work 160 tests assert the
  deck-only layer). The corners are added by a separate function that extends
  the `MechanismLayer`.
- Four root-level corner assemblies `m1..m4-ground_propulsion_braking`, each
  tagged `[ground_propulsion, braking]`: axle (6- or 8-gon, flat top face,
  seated on the deck side face at mid thickness, `bonded` to the deck),
  stator (hexagonal pad on the axle's top face, `bonded`), rotor (24/32-gon
  disc, `bonded` to the wheel), wheel (16/20/24-gon, vertex down, `bearing` to
  the axle). Motion per corner `{wheel, rotor}`, revolute, range 2 pi, about
  the axle axis.
- Deviation from the Work 160 sketch: the bore is a 48-gon (a multiple of 6
  and 8) of apothem `r_a + c` with a vertex at every axle vertex direction,
  not an N_a-gon. The acceptance contact check samples only vertices and
  triangle centroids. With an N_a-gon bore, no sample of either mesh came
  within 1e-4 m of the other: the first run measured a 1.47e-3 m gap. The
  48-gon keeps free rotation (inscribed radius `r_a + c` > axle circumradius)
  and brings the bore vertices within about 6e-5 m of the axle edges.
- The stator foot first overhung the axle's top face, so no sample landed on
  it (measured 4.98e-4 m). The foot is now 0.8 times the top-face half width
  and the pad widens above the face plane.
- All wheels share one radius per vehicle, so all four bottom vertices define
  the ground band. The radius is capped by the front-rear spacing.
- `braking` evidence names corner 1. All four corners have a rotor and a
  stator.

## Validation

| Command | Exit | Output |
|---|---|---|
| `python -m unittest tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms` | 0 | `Ran 18 tests`, `OK` |
| generator seeds 11, 23, 37 and a seed-11 replay into `artifacts/work161/` | 0 | 265 / 264 / 267 leaves, 4 motions each |
| `python artifacts/work161/check.py artifacts/work161 <A0*, A1, A2, A3, B4, B6, B10>` (acceptance classes on the generated packages; evidence key-set assertion relaxed locally only) | 0 | `Ran 20 tests`, `OK` |
| `python scripts/hierarchy/evaluate_level0.py --manifest artifacts/work161/seed11/manifest.json --out ...` | 0 | `finished`, 10756.8 s, mass 1987.6 kg, residual 0.0 J |
| `pwsh -NoProfile -File auto-loop/verify.ps1` | 3 | Gate 1 PASS; Gate 2 `Ran 1148 tests`, `OK (skipped=11)`; Gate 3 `FAILED (failures=9)`: only B1-B9, all on the nine-key evidence check; v1 13/13, Tier A, B10 and C1 pass |

Measured on seeds 11 / 23 / 37: CoM margin inside the support polygon
1.198 / 1.087 / 0.591 m (>= 0.05 required), brake gap 5.0e-4 m on all three,
non-prismatic leaves 162/265, 174/264, 166/267.

## Limitations

- B4 and B6 pass only in the local relaxed check. The protected suite checks
  the full nine-key evidence set first.
- The wheels are polygonal discs about a fixed axle. There is no tyre,
  traction, rolling-resistance or brake-torque model. The ground band is a
  geometric check only.
- Vehicle mass rose to about 2.0 t with the synthetic material, so Level-0
  time grew (seed 11: 9682 s -> 10757 s).

## Follow-up

- Direction control: a z-axis steering post plus arm in the deck bay
  (range >= 0.2 rad, `bearing`).
- Power transmission (rollers in `rolling` contact), energy converter
  (chamber plus piston, `guide`), vessel and controller housing with voids,
  and a finned heat surface.
