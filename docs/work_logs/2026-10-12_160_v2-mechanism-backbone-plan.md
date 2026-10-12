# Work 160 Plan: v2 mechanism layer framework and structural deck

Thai companion: `2026-10-12_160_v2-mechanism-backbone-plan.th.md`

Status: Completed

## Objective

Start the Tier B capability work with a mechanism layer that is planned after
the v1 cluster is realized and measured. This item adds the framework and its
first member: a structural deck (`load_structure`) directly under the measured
cluster, joined to the cluster's lowest leaf. Later items hang wheels, brakes,
steering, transmission, converter, vessel, controller and heat surfaces on the
deck.

## Design (decided here, recorded for later items)

- The v1 cluster (decomposition, layout, bores, fasteners) is unchanged. After
  its meshes are written, the generator reads them back and measures the
  cluster box `[X0,X1] x [Y0,Y1] x [Z0,Z1]` and the lowest leaf.
- Mechanism leaves live in new root-level assemblies `m<k>-<capability>`
  tagged with their capabilities, so every evidence part lies in a tagged
  subtree. They connect to the v1 cluster only through the deck.
- Deck: a flat chamfered-octagon plate, top face at `Z0`, footprint = cluster
  footprint plus a seed-drawn margin, plus a reserved bay in +x for later
  modules, plus a lip for the future wheel lines. Seed-drawn thickness,
  margin, chamfer and bay length. Interface `bonded` between the deck and the
  cluster's lowest leaf (that leaf has a vertex at `Z0` above the deck top).
- Mechanism leaf grammar `func-leaf-mechanism-v2`: polygon `section` (outer
  loop plus optional hole loops) -> straight `extrude` along local +z ->
  rigid `transform`s. Flat faces only, so contacts and clearances are exact
  after tessellation.
- The merged manifest appends mechanism parts and assemblies under the root
  and recomputes every assembly mass and centre of mass with the same
  arithmetic as `part_tree.roll_up`. Interfaces of v2 kinds (`bearing`,
  `guide`, `rolling`) are appended at manifest level, outside the v1
  `PartTree` validator.
- Evidence is emitted only for finished capabilities. This item emits
  `load_structure: {members: [deck]}`. Acceptance B1-B9 cannot pass until all
  nine are present (the suite checks the key set first).

## Planned files

- `src/formula_ultimate/hierarchy/mechanisms.py` (new, pure Python).
- `scripts/hierarchy/functional_realization.py` (dispatch for the mechanism
  grammar).
- `scripts/hierarchy/generate_functional_vehicle.py` (measure cluster, plan
  and realize the layer, merge).
- `src/formula_ultimate/hierarchy/functional.py` (`config_sha256_v2` takes an
  optional mechanism record).
- `tests/test_hierarchy_mechanisms.py` (new).
- Work log plan/result (EN + TH), `auto-loop/progress.md` (+ `.th.md`).

## Validation

- `python -m unittest tests.test_hierarchy_mechanisms -v`
- Generate seeds 11, 23, 37 into `artifacts/work160/` and check with the
  acceptance helpers: closed deck mesh, deck-cluster gap <= tolerance, no
  interpenetration, roll-up, inertia, Level-0 still `finished`.
- `pwsh -NoProfile -File auto-loop/verify.ps1` (Gates 1 and 2 must pass;
  Gate 3 Tier A, B10 and C1 must stay green).

## Success criteria

Tests pass; Gates 1-2 pass; no previously passing Gate 3 test regresses.

## Risks

- Deck mass changes the Level-0 time (must still finish).
- Float32 rounding of the deck top versus `Z0` is about 1e-7 m, far below
  the 1e-4 m contact tolerance.

## Non-goals

No wheels, motions or other capability evidence yet. No claim that the deck
carries load.
