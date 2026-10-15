# Work 161 Plan: v2 ground contacts with braking rotors and stators

Thai companion: `2026-10-12_161_v2-ground-contacts-braking-plan.th.md`

Status: Completed

## Objective

Add four rotating ground-contact corners to the v2 mechanism layer, hung on
the Work 160 deck, so that the package carries real `ground_propulsion` and
`braking` evidence: full-turn revolute motions with `bearing` interfaces, only
the rotating contacts in the ground band, a centre of mass inside the support
polygon, and a fixed stator 0.5 mm from a rotating rotor.

## Design

- New pure-Python module `src/formula_ultimate/hierarchy/ground_contacts.py`
  with `add_ground_contacts(layer, seed, catalogue, config)` that extends a
  `MechanismLayer` (the Work 160 `plan_mechanisms` output stays unchanged, so
  its protected tests keep passing) and `ground_contact_problems(layer)` that
  re-checks the rules from the program vertices.
- Corner lines at `x = core_x0 - 0.06` and `x = core_x1 + 0.06`, both deck
  sides in y. Each corner is a root-level assembly
  `m<k>-ground_propulsion_braking` tagged `[ground_propulsion, braking]` with
  four `func-leaf-mechanism-v2` prisms extruded outward along y:
  - axle: regular N_a-gon (flat face on top), cap seated on the deck side
    face at mid thickness, circumradius `r_a <= t/2 - 2 mm`; `bonded` to the
    deck;
  - stator: pentagon pad resting on the axle's flat top face (`bonded`), in
    the y slab next to the deck, 0.5 mm from the rotor face;
  - rotor: N_r-gon disc with an N_a-gon bore, `bonded` to the wheel;
  - wheel: N_w-gon disc (even N_w, one vertex straight down) with the same
    bore; `bearing` interface to the axle.
- Bore: N_a-gon of apothem `r_a + c` (c = 2.5e-5 m) whose face normals point
  at the axle vertices, so the static gap is c and no rotation can bring the
  axle into the bore wall.
- Motion per corner `{wheel, rotor}`, revolute about the axle axis, range 2 pi.
- Wheel radius is drawn per vehicle with `R > t/2 + 1 mm + margin` so the
  wheel bottom vertex is the global lowest point and the deck bottom, rotor,
  axle and stator stay above the 1 mm ground band.
- Evidence: `ground_propulsion: {motions: [4 ids]}`,
  `braking: {rotor_motion: <first corner motion>, stator: <its stator>}`.
- The generator calls `add_ground_contacts` after `plan_mechanisms` and hashes
  the ground-contact config into `config_sha256`.

## Planned files

- `src/formula_ultimate/hierarchy/ground_contacts.py` (new)
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_ground_contacts.py` (new)
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`)

## Validation

- `python -m unittest tests.test_hierarchy_ground_contacts tests.test_hierarchy_mechanisms -v`
- Generate seeds 11, 23, 37 into `artifacts/work161/` and run the B4/B6
  measurement logic (ground band owners, hull margin, brake gap) and the
  sweep and interpenetration checks with the acceptance helpers; run the
  Level-0 evaluator on seed 11 (must still finish).
- `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass; Tier
  A, B10 and C1 must stay green. B4/B6 cannot pass yet because the suite
  requires all nine evidence keys first.

## Success criteria

Focused tests pass, the manual B4/B6 checks pass on the three seeds, Gates 1-2
pass and no previously passing Gate 3 test regresses.

## Risks

- Extra mass changes Level-0 time; it must still finish.
- More prismatic leaves lower the non-prismatic share (A1 needs >= 25 %).
- The CoM margin depends on cluster mass distribution; it is measured, not
  forced.

## Non-goals

No steering, transmission or drive coupling yet. No tyre, contact-patch or
braking-torque physics. Not physical validation.
