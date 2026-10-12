# Loop Goal v2: Functional Composition

Thai companion: `GOAL.th.md`

Protected: the loop stops if this file changes. Set by Work 154. It replaces
goal v1, which Works 149–153 met.

## What the project owner wants

The system designs every part of the vehicle freely, from the smallest
fastener up to whole systems, with no prescribed shapes and no conventional
part list. Goal v1 built the hierarchy, but its parts were straight
extrusions and its function labels did not change any geometry. Goal v2
requires **function to show up in geometry and motion**. Storage must hold
volume. A converter must have a member that moves inside a chamber. Wheels or
other ground contacts must turn and carry the car stably. Fasteners must pass
through holes. The vehicle must then run the existing Level-0 race. How each
function is realized is the system's own choice. The contract below only
says what must be measurably true.

## Done means

`pwsh -NoProfile -File auto-loop/verify.ps1` exits 0 on a clean, committed tree:

1. Gate 1: the material publication boundary passes.
2. Gate 2: the whole repository suite passes. This includes the tests from
   Works 149–153, which are protected, so the v1 API must keep working.
3. Gate 3: both acceptance suites pass. The v1 suite
   (`test_hierarchical_composition.py`) still checks the v1 generator. The v2
   suite (`test_functional_composition.py`) checks the new v2 generator.

## Time box and expected result

The loop is sized for about 8 hours. The v1 run averaged about 25 min per
iteration, and verification is slower now, so expect about 16 iterations
against an estimated 15–20 work items. The v2 tests are grouped in tiers, and
`auto-loop/.loop/last-verify.txt` shows which tiers pass:

| Tier | Content | Estimate |
|---|---|---|
| A | v1 contract on the v2 package, geometry language, motions with sweeps, inertia | 5–6 items, expected to pass |
| B | evidence for each function, threaded through-holes, static ground stability | 8–10 items, mostly expected |
| C | Level-0 race on the existing kernel, with a mass-sensitivity check | 2–3 items, possible |

Suggested order: A, then B, then C. Commit a working state at every step.

## Entry points

```text
.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed S --out DIR
python scripts/hierarchy/evaluate_level0.py --manifest DIR/manifest.json --out RESULT.json
```

The generator must finish within 30 minutes per seed. The evaluator must
finish within 10 minutes and be deterministic. The v1 entry point
`generate_hierarchical_vehicle.py` must keep passing the v1 suite. The v2
generator may reuse and extend v1 modules, but it must not break their tests.

## v2 manifest contract

Everything in the v1 contract applies (see the v1 acceptance suite and the
Work 148 records). The changes are as follows.

The top-level fields are the v1 fields plus `up_axis` (`"z"`), `motions`,
`function_evidence` and `vehicle_inertia_kg_m2` (3x3, about the vehicle
centre of mass, in kg m^2).

Interface kinds are the v1 kinds plus `bearing`, `guide` and `rolling`. A
`threaded` interface must also carry `axis_point_m` and a unit `axis_dir`.
The axis point must lie within the holed part's thickness.

A motion is
`{id, parts, type: "revolute", axis_point_m, axis_dir, range_rad}` or
`{id, parts, type: "prismatic", axis_point_m, axis_dir, stroke_m}`. `parts`
are leaf ids that move rigidly together, and a leaf belongs to at most one
motion. A revolute sweep covers `[-range/2, +range/2]`. A prismatic sweep
covers `[0, stroke]` along `axis_dir`.

`function_evidence` has exactly the nine capabilities:

| Capability | Fields | Checked |
|---|---|---|
| `energy_storage` | `vessel`, `stored_volume_m3` | vessel's internal void volume >= declared >= 0.01 m^3 |
| `energy_converter` | `chamber`, `motion` | the chamber has a bore (genus >= 1) or a cavity; >= 50 % of the moving member's samples lie inside the chamber's box and outside its material |
| `power_transmission` | `chain` | >= 2 full-turn revolute motions, consecutive members joined by an interface |
| `ground_propulsion` | `motions` | >= 2 full-turn revolute motions; only their parts touch the ground band (lowest z + 1 mm); the CoM lies >= 0.05 m inside the support polygon |
| `direction_control` | `motion` | revolute, range >= 0.2 rad, axis >= 30 deg from every ground-propulsion axis |
| `braking` | `rotor_motion`, `stator` | full-turn rotor; a non-moving stator within 2 mm of the rotor |
| `load_structure` | `members` | members are connected by interfaces; every other capability has an interface to a member |
| `heat_rejection` | `surfaces` | total area >= 3x the area of a sphere of the same total volume |
| `controller` | `housing`, `contents` | the housing has a cavity, and >= 2 content parts lie entirely inside it |

Every part named in the evidence and every motion part used for a capability
must lie in a subtree that is tagged with that capability.

## Further checks

- At least 25 % of leaves are non-prismatic: no single direction leaves 99 %
  of the area parallel or perpendicular to it. At least 5 % of leaves have a
  through-hole (genus >= 1).
- Every motion has a `bearing` (revolute) or `guide` (prismatic) interface
  between a moving part and a fixed part. Sweeping each motion over its range
  in 8–16 poses must not bring sampled points deeper than 1 mm into any other
  leaf.
- `vehicle_inertia_kg_m2` must match the meshes within a relative 1e-5.
- There are at least 8 `threaded` joints. Each one's axis passes through a
  hole of one part (no material on the axis line, material in every one of 8
  radial directions) and through the material of the other part.
- Level-0, on the seed-11 vehicle: the output fields are exactly
  `manifest_sha256, mass_kg, drag_area_m2, outcome, race_time_s,
  consumed_energy_j, terminal_energy_boundary_residual_j, circuit_id,
  race_kernel`, with `race_kernel = "race-level0-v1"` (the existing
  `physics/race.py` kernel). `outcome = "finished"`. `mass_kg` equals the root
  mass. `0 < drag_area_m2 <= 1.5` x the frontal (y-z) extent. The energy
  residual is at most 1 J. Two runs give byte-identical output. **Falsification
  check:** the same package with the root mass raised by 50 % must race slower
  or fail to finish.

## Boundaries

The v1 boundaries all still apply: `AGENTS.md`, catalog-only materials, no
material values in tracked files, reuse of the existing grammar, gates and
vocabulary, and no hard-coded conventional part list. In addition:

- Do not special-case seeds 11, 23 or 37, and do not special-case the
  acceptance code.
- Use the existing `physics/race.py` kernel for Level-0. Do not write a
  substitute race model. Declare the circuit, energy budget and control
  settings in a versioned config. Physical assumptions use SI units and are
  written in the work logs.
- Separate new code as `src/formula_ultimate/hierarchy/` modules plus tests.
  Never edit an existing tracked test.

## What passing does NOT mean

Passing is a representation, kinematic-clearance and Level-0 coupling gate.
It does not show that a part carries load, that a chamber holds pressure, or
that a thread is a real helix. It does not show that the vehicle is fast or
better than a baseline. Level-0 uses lumped mass and drag only, and the
contract's choice of function evidence is itself a design-language bias,
toward recognisable mechanisms.

## Known limitations of the checks

- Contact, penetration and sweep checks sample vertices and triangle
  centroids.
- "Non-prismatic" and the heat area ratio are proxies.
- Threads are checked as through-holes only.
- The drag area is only bounded, not derived.
