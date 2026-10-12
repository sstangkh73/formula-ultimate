# Loop Progress

Thai companion: `progress.th.md`

Memory between iterations. The agent appends to the Log section every
iteration and commits it with its work item. The Thai companion is updated in
the same commit.

## Starting state (Work 148)

- Goal: `auto-loop/GOAL.md`, hierarchical free-form composition v1.
- Gate 1 (material publication boundary) and Gate 2 (repository suite) are the
  regression gates. Gate 3 (acceptance) fails because
  `scripts/hierarchy/generate_hierarchical_vehicle.py` does not exist yet.
- Next free work number: 149.
- Known baseline behaviour: on 2026-10-11 the repository suite on clean `main`
  failed once (4 failures, test names not captured) and passed on two
  reruns (`Ran 1042 tests ... OK (skipped=11)`). If Gate 2 fails in tests
  unrelated to your change, rerun once and record the test names here. Do not
  edit or skip existing tests. If the cause cannot be found, write it to
  `auto-loop/BLOCKED`.
- Several existing tests read gitignored local evidence (`artifacts/`,
  `papers/`). They pass in this checkout but fail in a fresh clone or
  worktree, so run the loop in this checkout only.

## Log

### Work 149 (iteration 1): part-tree data model, Completed

- Done: `src/formula_ultimate/hierarchy/part_tree.py` with frozen node,
  interface and tree dataclasses, `validate_part_tree`, iterative `roll_up`,
  metrics (`levels`, `leaf_ids`, `subtree_height`, `subtree_leaves`,
  `topology_signature` with the acceptance definition), and
  `to_manifest_nodes`/`to_manifest_interfaces` with the exact contract field
  sets. Tests: `tests/test_hierarchy_part_tree.py` (11 tests).
- Who: Codex wrote the code and tests. Claude reviewed the diff and wrote the
  records.
- Gates: Gate 1 PASS. Gate 2 `Ran 1053 tests`, `OK (skipped=11)`. Gate 3
  fails 13/13 because the generator is missing (expected).
- Problems and how to avoid them:
  - Calling `bash auto-loop/tools/codex.sh "$(cat file)"` is refused by the
    permission checker. A gitignored wrapper script was refused too. What
    works is a literal prompt that points at a task file:
    `bash auto-loop/tools/codex.sh "Read the task specification in the file auto-loop/.loop/taskNNN.txt (read only; do not edit anything under auto-loop/) and carry it out exactly."`
    Write the task file under the gitignored `auto-loop/.loop/` first.
  - Codex wrote its own work-log files with the wrong number (148). Tell
    Codex explicitly: "do not create or edit any docs/work_logs files".
  - `verify.ps1` does not write `last-verify.txt` (the runner does). To see
    the summary, pipe through
    `grep -a -E "^== Gate|PASS|^Ran |^OK|FAILED|^FAIL:|^ERROR:"`.
    Compound shell commands (`;`, `${...}`) can need approval, so keep each
    Bash call to a single pipeline.
- Next: Milestone 2. A seed-driven decomposition procedure that builds an
  abstract tree (no geometry) covering all nine capabilities: subtree height
  >= 2 and >= 5 leaves per capability, >= 4 levels, >= 150 leaves, and
  different topologies for seeds 11, 23 and 37, with no conventional part
  catalogue.

### Work 150 (iteration 2): seed-driven abstract decomposition, Completed

- Done: `src/formula_ultimate/hierarchy/decomposition.py` with
  `decompose(seed, config)`: capability grouping (single or pairs), recursive
  random-composition leaf budgets, anchor child = largest-budget child,
  per-node `characteristic_length_m` (planning target), abstract attachments
  (satellite's anchor leaf -> seed-chosen leaf of the anchor subtree) with a
  joint kind, and a rejection search checked by `constraint_violations`. The
  root has no functions; sub-assemblies inherit their group's functions;
  leaves have none. Ids: `vehicle`, `g<i>-<caps>`, `<parent>.a<i>` (assembly)
  / `<parent>.p<i>` (part). Tests: `tests/test_hierarchy_decomposition.py` (12).
- Who: Claude (the design needed full context).
- Gates: Gate 1 PASS. Gate 2 `Ran 1065 tests`, `OK (skipped=11)`. Gate 3
  fails 13/13 (no generator yet).
- Evidence: seeds 0..39: 175..229 leaves, 7..8 levels, planned leaf length
  ratio 103..277, maximum fan-out 12.
- Problems: `sed -i` and commands with an env-var prefix need approval; use
  the Edit tool instead. The package is installed, so
  `python -c "from formula_ultimate..."` works without PYTHONPATH.
- Next: Milestone 3, leaf geometry via `components/freeform_solid_grammar.py`
  / `scripts/cad/*` under CadQuery: size from `characteristic_length_m`, STL
  export in metres, mass and CoM from the exported mesh, box-fill fraction
  <= 25 % (hand the CadQuery part to Codex with a precise spec). Split it if
  too big: (a) build and export one leaf and measure its mass, (b) placement.

### Work 151 (iteration 3): leaf geometry realization, Completed

- Done: `src/formula_ultimate/hierarchy/leaf_geometry.py` (pure Python):
  `leaf_program(rng, L, placement, leaf_id)` draws a star-shaped Work 091
  profile (closed polyline or periodic B-spline) extruded straight along
  local +z (Work 092 `section -> extrude -> transform...`); flat caps at local
  z=0 and z=`contact.height_m` with declared `contact.inscribed_radius_m` /
  `outer_radius_m`. `placement_transforms(axis, flip, spin, translation)`,
  `with_placement`, `transform_points` (pure replica of the CAD placement),
  `stl_bytes`/`read_binary_stl`, `closure_problems`, `measure_mesh` (mass and
  CoM from re-read float32 triangles, acceptance formulas).
  `scripts/hierarchy/leaf_realization.py` (CAD runtime): `realize_leaf(program,
  stl_path, density)` reuses `execute_candidate` unchanged, tessellates at
  2e-3 L, writes a deterministic binary STL in metres. Tests:
  `tests/test_hierarchy_leaf_geometry.py` (9, CAD part via subprocess).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1074 tests`, `OK (skipped=11)`. Gate 3
  fails 13/13 (no generator yet).
- Evidence: 600 random leaves (L 0.004..4 m) all closed, 18.9 s total (~30 ms
  per leaf), box-fill <= 0.858, bbox diagonal 0.44..1.50 L.
- Problems: side faces deviate up to the linear tolerance (2e-3 L), so contact
  must be cap-to-cap (flat, exact). Fresh tessellation of a placed shape
  differs from the local one by up to that tolerance.
- Next (milestone 4, placement): suggested design. Make leaf AABBs pairwise
  disjoint (touching allowed): the acceptance penetration test only checks
  pairs whose AABBs overlap by more than `contact_tolerance_m`. Interface
  contact: put the smaller leaf's cap flat on the larger leaf's cap, centred so
  its outer radius fits inside the other's inscribed radius (then its cap
  vertices are at distance 0). The attachment graph of Work 150 is a spanning
  tree over leaves (sum of (children-1) = leaves-1), but random targets deep
  inside the anchor subtree may be unreachable without collisions; consider
  choosing the target at layout time among leaves with a free cap (record the
  procedure), and a collision-checked candidate search over cap directions.
  Keep placement planning in pure Python (`transform_points`, contact data),
  then realize in CAD.

### Work 152 (iteration 4): leaf layout planner, Completed

- Done: `src/formula_ultimate/hierarchy/layout.py` (pure Python). `layout(tree)`
  places every leaf axis-aligned. Contact faces (`leaf_faces`): 2 caps plus
  one flush polyline hull side face per polyline leaf, made axis-aligned by
  choosing the spin. Growth: the anchor child first, then each satellite's
  anchor leaf goes cap-first onto a face of any leaf already placed in the same
  assembly. Fit rules "inside" and "around". A fresh source may be resized
  0.004 m..4x planned. Boxes are interior-disjoint. A room-keeping claim box
  pass, then a plain pass. Up to 16 deterministic attempts.
  `layout_problems` re-checks everything from the programs. `PlannedInterface`
  carries `a_face`/`b_face`/`mode`. Tests: `tests/test_hierarchy_layout.py` (8).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1082 tests`, `OK (skipped=11)`. Gate 3
  fails 13/13 (no generator yet).
- Evidence: seeds 0..62 all lay out except seed 4 (`LayoutFailure`, crowding).
  CAD spot check (`artifacts/work152/cad_spot_check.py`, run under the CAD
  python) for seeds 11/23/37 using the acceptance helpers: every interface
  gap <= 8.5e-18 m, 0 overlapping mesh-box pairs (tol 1e-4), box-like
  fraction 0, diagonal ratio 139/179/267. About 10-14 s to realize about 229
  leaves.
- Problems found: cap-only contact made every leaf inherit the root axis (one
  column, every seed failed), so side faces were added. Shrink-only fitting
  cascaded, so "around" enlarging was added. A lone anchor leaf has only 2 caps,
  so targets now cover the whole assembly. `sed -i` and `awk` pipelines need
  approval; use the Edit tool or Python heredocs.
- Next: the generator CLI `scripts/hierarchy/generate_hierarchical_vehicle.py`
  (CAD runtime): `decompose` -> `layout` -> `realize_leaf` per leaf ->
  manifest with the exact contract fields (`contact_tolerance_m` e.g. 1e-4;
  interfaces `id,a,b,kind` only; part `generator={grammar_version: LEAF_GRAMMAR_VERSION,
  program, program_sha256}`; `git_commit` from `git rev-parse HEAD`;
  `config_sha256` over decomposition + layout config), roll-up via
  `part_tree.roll_up` from measured leaf masses. Materials: catalog-only ids;
  check how the existing code exposes catalog material ids and densities without
  copying private values into tracked files (densities only in `artifacts/`
  output). Seed 4 needs a declared fallback such as the next decomposition attempt.
  Do not special-case the acceptance seeds.

### Work 153 (iteration 5): generator CLI, Completed

- Done: `src/formula_ultimate/hierarchy/composition.py` (`plan_vehicle`:
  decompose -> layout -> `layout_problems`; on `LayoutFailure` continue from
  the next decomposition attempt via the new `decompose(..., start_attempt)`,
  at most 8 plan attempts, rejections recorded; material draw per leaf;
  `composition_config_sha256`; `build_manifest`; deterministic
  `manifest_bytes`). `scripts/hierarchy/generate_hierarchical_vehicle.py`
  (contract entry point, meshes in `DIR/meshes/<leaf id>.stl`, masses from
  the re-read STL). Tests: `tests/test_hierarchy_composition.py` (12).
- Material decision: v1 reads the existing synthetic record
  `synthetic_aluminium_like_verification_v1`
  (`config/materials/engineering_material_manufacturing_v1.json`) at run
  time; no material value is written to tracked files.
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1094 tests`, `OK (skipped=11)`. Gate 3
  `Ran 13 tests`, `OK`. `ALL GATES PASSED` (run before commit on the dirty
  tree; `git_commit` equals HEAD at run time, so a rerun after commit should
  still pass).
- Evidence: seed 11 226 leaves in 13.8 s; seed 4 needed the fallback (two
  rejected attempts) and generated 180 leaves; planning sweep seeds 0..39 had
  0 failures.
- Problems: `${PIPESTATUS[0]}` and `cmd; echo $?` need approval; pipe
  `pwsh ... verify.ps1 2>&1 | grep -a -E ...` alone, which prints
  `ALL GATES PASSED` when it passes.
- Next: the goal is met. Remaining iterations: confirm `verify.ps1` on the
  clean committed tree. Possible hardening (each its own work item): replace
  the single synthetic material with a catalogue-only choice whose values are
  read at run time from gitignored data (with a synthetic fallback for clean
  clones), add `interference_m` handling, and speed up
  `tests/test_hierarchy_composition.py` (86 s).

## Goal v2 starting state (Work 154)

- Goal v1 was met in Works 149–153. `auto-loop/GOAL.md` is now goal v2,
  functional composition. Read it in full.
- Gates 1 and 2 pass. In Gate 3, the v1 suite passes and the v2 suite fails
  because `scripts/hierarchy/generate_functional_vehicle.py` and
  `scripts/hierarchy/evaluate_level0.py` do not exist yet.
- The v2 tests are tiered (`TierA*`, `TierB*`, `TierC*`). Work A, then B,
  then C, and use `last-verify.txt` to see which tiers pass.
- The tests from Works 149–153 are now protected. Keep the v1 API and the v1
  generator working, and add v2 modules beside them.
- Lessons from v1 (see the log above): pass Codex tasks through a task file
  under `auto-loop/.loop/`; tell Codex not to write work logs; keep each Bash
  call to one pipeline; use the Edit tool instead of `sed -i`.
- Next free work number: 155.

## Log (goal v2)

### Work 155 (v2 iteration 1): v2 generator skeleton with measured inertia, Completed

- Done: `src/formula_ultimate/hierarchy/functional.py` (`mesh_inertia`,
  `config_sha256_v2`, `build_functional_manifest`, version
  `func-composition-v2`) and `scripts/hierarchy/generate_functional_vehicle.py`
  (v1 plan + realization unchanged, STL re-read, inertia, `up_axis`,
  `motions = []`, `function_evidence = {}`). Tests:
  `tests/test_hierarchy_functional.py` (6).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1100 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=13, errors=1)`: v1 suite 13/13 pass; v2 passes TierA0
  except Interfaces, TierA2 (vacuous, no motions) and TierA3.
- Problems: TierA0Interfaces fails because v1 layout emits `threaded`
  interfaces (49 in seed 11) without `axis_point_m`/`axis_dir`; TierB10 errors
  on the same. A grep pattern ending in `$` (e.g. `ok$`) triggers an approval
  prompt; use the pattern from Work 149 exactly.
- Next (suggested roadmap, record deviations): (1) v2 interface kinds: in the
  v2 package, give threaded joints a real hole in one leaf and a pin through
  it, or relabel v1 contacts that cannot carry an axis to another v1 kind
  (decide; keep >= 8 real threaded joints for TierB10); (2) TierA1 geometry
  language: non-prismatic leaves (e.g. tapered/lofted or revolved profiles) for
  >= 25 % and holed leaves for >= 5 %; (3) per-capability functional modules
  (wheels at the lowest z with bearings, steering, brake disc + stator, vessel
  with void, chamber + piston/rotor, housing with contents, finned surfaces,
  backbone) placed by a v2 layout, then the Level-0 evaluator.

### Work 156 (v2 iteration 2): v2 flush-contact joint kinds, Completed

- Done: `functional.py` adds `FLUSH_JOINT_KINDS` (v1 kinds minus `threaded`)
  and `V2_DECOMPOSITION_CONFIG`; the v2 generator plans with it and hashes it.
  Decision: flat cap/side contacts have no hole or axis, so v2 never labels
  them `threaded`; `threaded` is reserved for future hole-and-pin fasteners.
  v1 is unchanged. Tests: `tests/test_hierarchy_functional_joints.py` (4).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1104 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=12)`: v1 13/13; v2 all Tier A0 pass (Interfaces fixed),
  A2 (vacuous), A3 pass; A1, B1–B10, C1 fail. B10 now fails on count 0 < 8.
- Problems: `cd "..." && git ...` triggers an approval prompt; run git from
  the default working directory without `cd`.
- Next: Tier A1 geometry language in a v2 leaf grammar (new module beside
  `leaf_geometry.py`): >= 25 % non-prismatic leaves (e.g. tapered extrusion
  or loft; note the acceptance check rejects a shape whose faces are 99 %
  parallel/perpendicular to one direction, so a straight extrusion of any
  profile is prismatic) and >= 5 % with a through-hole (genus >= 1). Keep the
  flat contact caps so the v1 layout still works. Then fasteners: a holed
  plate leaf plus a pin leaf through it as `threaded` with axis (>= 8/seed).

### Work 157 (v2 iteration 3): v2 leaf through-bores, Completed

- Done: `src/formula_ultimate/hierarchy/leaf_refinement.py` (post-layout,
  pure Python): for a seed-chosen subset (p = 0.8) of placed leaves, one
  oblique cylindrical bore (tilt 5-40 deg, drawn lateral axis offset) is cut
  from the local extrusion before the placement transforms
  (`section -> extrude -> bore -> transforms`, grammar `func-leaf-bored-v2`).
  The bore stays inside the inscribed cylinder (material removal only, so no
  new interpenetration and unchanged boxes) and its cap exits keep clear of
  the contact patches each cap receives (`contact_patches`).
  `refinement_problems` re-checks everything. `scripts/hierarchy/functional_realization.py`
  realizes v1 or refined programs. The v2 generator records each leaf's
  grammar version and hashes the refinement config. Tests:
  `tests/test_hierarchy_leaf_refinement.py` (9).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1113 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=11)`: v1 13/13; v2 all of Tier A passes (A1 fixed;
  seed 11: 92/226 holed, 160 non-prismatic, worst interface gap 2e-18 m);
  B1-B10 and C1 fail.
- Problems: centred bores were blocked on 104/110 leaves with received
  patches, so a lateral axis offset was added. Note that A1's non-prismatic
  share already passed before (the proxy samples the 20 largest triangles).
- Next: Tier B10 fasteners (>= 8 `threaded` joints per seed, axis through a
  hole of one part and the material of the other, axis point inside the holed
  part's thickness). Suggested: new pin leaves (inside the tree, under the
  same subtree as the holed part so capability tagging holds) with a shaft
  along an axial (tilt 0) bore of a holed leaf and a flat head resting on the
  cap; interface `threaded` between holed leaf and pin with `axis_point_m` at
  the mid-plane. Adding leaves changes the tree, so check part_tree validation,
  roll-up and the A0 tests (box disjointness of the pin vs. the holed leaf is
  impossible: the acceptance penetration check only measures depth, so a pin
  inside a hole with clearance is fine, but `layout_problems` box rules are
  v1 only; keep pins out of that check or extend a v2 re-check).

### Work 158 (v2 iteration 4): hex-socket fasteners as threaded joints, Completed

- Done: `src/formula_ultimate/hierarchy/fasteners.py` (pure Python): after the
  Work 157 bores, every unbored leaf tries one axial regular-hexagon socket
  (`hole` loop of the extruded profile, grammar `func-leaf-socketed-v2`, clear
  of cap contact patches). Each socket gets a new pin leaf `<holed>.pin` (v1
  hexagonal extrusion, apothem and height inset by clearance 2.5e-5 m, child
  of the holed leaf's parent) and a `threaded` interface `<pin>.thread` whose
  axis is the socket axis at mid thickness. `fastener_problems` re-checks.
  `functional.with_threaded_axes` writes the axes; `functional_realization`
  validates with `validate_v2_program`. Tests:
  `tests/test_hierarchy_fasteners.py` (10).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1123 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=10)`: v1 13/13; v2 all Tier A pass and TierB10 passes
  (seed 11: 22 joints, worst gap 2.5e-5 m, 0 penetration); B1-B9 and C1 fail.
- Evidence: joints per seed 11/23/37/0/10 = 22/18/21/14/10. The first config
  (p 0.6, 12 draws, min apothem 1 mm) gave 7 on seed 23, so it was widened
  before any acceptance run.
- Problems: none blocking. Note for B1-B9: `evidence()` asserts all nine
  `function_evidence` keys first, so no B1-B9 test passes until all nine
  capabilities have evidence. Do not reduce the unbored leaf pool (more bores)
  without re-checking joint counts (seed 10 has only 10).
- Next: Tier C1 evaluator `scripts/hierarchy/evaluate_level0.py` is
  independent of the geometry (needs root mass, mesh frontal extent, the
  existing `physics/race.py`, a versioned config); good Codex task. Then the
  B capability modules (design them together: wheels at the lowest z with
  bearings, steering, brake rotor + stator, vessel with void, chamber +
  moving member, housing with contents, finned surface, backbone), possibly
  as dedicated subassemblies placed under the matching capability subtrees.

### Work 159 (v2 iteration 5): Level-0 evaluator on the existing kernel, Completed

- Done: `src/formula_ultimate/hierarchy/level0.py`,
  `config/hierarchy/level0_race_v1.json` (monza_2026, frontal-box drag
  coefficient 1.0, C_rr 0.015, 4000 N, 4e9 J, dt 1 s, timeout 36000 s) and
  `scripts/hierarchy/evaluate_level0.py`. Mass = manifest root `mass_kg` as
  written; drag area = 1.0 x leaf-mesh y-z extent. Tests:
  `tests/test_hierarchy_level0.py` (7).
- Who: Claude (too small to delegate).
- Gates: Gate 1 PASS. Gate 2 `Ran 1130 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: v1 13/13; v2 Tier A, B10 and C1 pass; B1-B9 fail.
- Evidence: seed 11 `finished` 8563.9 s; root mass x1.5 gives 8593.2 s
  (small effect, drag-dominated with a 5.0 m^2 frontal box). Evaluator ~3 s.
- Problems: `cp -r` and grep patterns with `$` need approval; use Python
  `shutil` and the grep pattern `"== |PASS|FAIL|Ran |OK \(|ALL GATES"`.
  C1 adds mass/drag through the root node only, so adding capability modules
  later must keep root mass and finishing intact (re-run the evaluator).
- Next: B1-B9. All nine `function_evidence` entries are needed before any of
  them passes, so plan a design item first (one work item: a module
  framework + the simplest capability, e.g. B8 finned heat surface or B9
  housing with contents), then add one capability per item, emitting
  evidence only for those done and keeping A-tier tests green. Consider
  placing dedicated mechanism subassemblies (wheels at lowest z with
  bearings, steering, brake rotor/stator, vessel, chamber+piston, housing)
  under the matching capability subtrees, below the v1 layout's lowest z for
  wheels so only they touch the ground band.

### Work 160 (v2 iteration 6): mechanism layer framework and structural deck, Completed

- Done: `src/formula_ultimate/hierarchy/mechanisms.py` (pure Python). After the
  v1 cluster is realized, the generator re-reads its meshes (`measure_cluster`:
  box + lowest leaf/vertex) and plans a mechanism layer: root-level assemblies
  `m<k>-<capability>`; mechanism leaf grammar `func-leaf-mechanism-v2`
  (`prism_program`: polygon outer + hole loops -> straight extrude -> rigid
  transforms, flat faces only). First member: deck `m0-load_structure.deck`, a
  chamfered octagon with its top at the cluster's lowest z `Z0`, footprint =
  cluster + margin, a +x bay (0.8-1.2 m) for later modules and a 0.14 m x lip
  on both ends for the ground-contact lines; `bonded` seat interface to the
  cluster's lowest leaf. `merge_mechanism_layer` appends nodes under the root,
  re-rolls masses (same arithmetic as `part_tree.roll_up`) and appends
  interfaces at manifest level (so v2 kinds bypass the v1 `PartTree`
  validator). `Backbone` dataclass carries the deck frame (x0/x1/y0/y1, z_top,
  thickness, core_x0/core_x1, bay_x0) for later modules. Evidence emitted:
  `load_structure` only. Tests: `tests/test_hierarchy_mechanisms.py` (10).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1140 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: only B1-B9 (key set incomplete); A, B10, C1 green.
- Evidence: seed 11 249 leaves, 25 s; Level-0 `finished` 9682 s; root mass
  528 -> 1766 kg (deck ~1240 kg, synthetic density). Consider a thinner deck
  or lightening holes later.
- Planned design for the next items (record deviations):
  - Ground contacts + braking (one item, group tagged
    `[ground_propulsion, braking]`, per-corner sub-assemblies): wheel centre
    lines at x = core_x0 - 0.06 and core_x1 + 0.06 (deck lip covers them, so
    the CoM stays >= 0.06 m inside the support rectangle when everything else
    is symmetric or inside the core); wheels outside the deck in y, axis y,
    regular N-gon disc with an N-gon bore, a vertex pointing straight down so
    the band points sit at the wheel centre x. Fixed axle: N-gon prism along y,
    cap seated on the deck side face (radius < t/2 - 2 mm), flat top face.
    Bearing: bore apothem = axle circumradius + c (c = 2.5e-5), bore phase
    offset pi/N so the static gap is c and no rotation can penetrate. Rotor
    disc between deck and wheel in the same motion as the wheel (motion parts
    {wheel, rotor}, `bonded` to the wheel); stator block on the axle's flat top
    face and the deck side face, 0.5 mm from the rotor face. Wheels must be the
    only parts within 1 mm of the lowest z (rotor radius <= R - 1 cm).
  - Bay modules on the deck top: steering post + arm (z axis, range >= 0.2),
    two or three rollers on vertical posts with rims c apart (`rolling`),
    tube with flat bottom + piston (prismatic `guide`, stroke inside the tube),
    vessel and controller housing as outer prism minus an inner scaled prism
    (needs a void option: `boolean_subtract`; verify CadQuery tessellation
    orients the inner shell inward), contents floating 5e-5 m above the
    cavity floor, comb-profile fin plates (area ratio >= 3).
- Next: the ground-contact + braking item above (B4, B6 evidence; also
  direction_control can follow quickly).

### Work 161 (v2 iteration 7): wheel-and-brake ground-contact corners, Completed

- Done: `src/formula_ultimate/hierarchy/ground_contacts.py` (pure Python).
  `add_ground_contacts(layer, seed, catalogue)` extends the Work 160 layer
  (`plan_mechanisms` unchanged: its protected test asserts the deck-only
  layer) with four root-level corners `m1..m4-ground_propulsion_braking`
  tagged `[ground_propulsion, braking]`: axle (flat top, seated on the deck
  side face, `bonded`), stator pad on the axle top (`bonded`), rotor
  (`bonded` to wheel), wheel (vertex down, `bearing` to axle); motion
  `<corner>.spin` = {wheel, rotor}, revolute 2 pi. `y_prism` maps a world
  (dx, dz) profile to an outward-y extrusion on either side.
  `ground_contact_problems` re-checks. Evidence adds `ground_propulsion` and
  `braking`. Tests: `tests/test_hierarchy_ground_contacts.py` (8).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1148 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: only B1-B9 (nine-key check); A, B10, C1 green.
  A local run of the acceptance classes with the key-set check relaxed
  (`artifacts/work161/check.py`, gitignored) passes B4 and B6 on 11/23/37.
- Evidence: CoM margin 1.198/1.087/0.591 m; brake gap 5.0e-4 m; seed 11
  Level-0 `finished` 10757 s, 1988 kg.
- Problems (lesson for later modules): the acceptance contact test samples
  only vertices and triangle centroids, so every interface needs a vertex of
  one part ON the other's surface. A stator overhanging a face and an
  N_a-gon bore around an N_a-gon axle both failed (gaps 5e-4 and 1.5e-3 m).
  Fixes: a narrow stator foot inside the face, and a 48-gon bore of apothem
  r_a + c with a vertex at each axle vertex direction. Shell `for` loops with
  `$s` need approval; run one generator call per Bash call.
- Next: direction control (z-axis steering post + arm in the deck bay at
  `backbone.bay_x0..core_x1`, `bearing`, range >= 0.2 rad, its own root
  assembly tagged `direction_control`, attached to the deck). Then
  transmission rollers (`rolling`), converter (chamber + piston `guide`),
  vessel/housing voids, heat fins. All nine keys are needed before B1-B9
  can pass in the real suite.

### Work 162 (v2 iteration 8): steering post and arm, Completed

- Done: `src/formula_ultimate/hierarchy/direction_control.py` (pure Python).
  `add_direction_control(layer, seed, catalogue)` adds root assembly
  `m5-direction_control` tagged `[direction_control]` at the +x end of the
  deck bay: boss (`bonded` to deck), post (`bonded` to boss), arm (convex
  hull of hub + tip polygons, 96-gon bore apothem r_p + c, floats c above the
  boss, `bearing` to post). Motion `<assembly>.steer` = {arm}, revolute +z,
  range 0.3-0.8 rad. The full sweep circle stays 0.02 m inside the bay and
  deck sides; the -x part of the bay (`bay_x0` up to
  `steer x - reach - 0.02`) is still free. `direction_control_problems`
  re-checks. Tests: `tests/test_hierarchy_direction_control.py` (8).
- Who: Claude.
- Gates: Gate 1 PASS. Gate 2 `Ran 1156 tests`, `OK (skipped=11)`. Gate 3
  `FAILED (failures=9)`: only B1-B9 (nine-key check); A, B10, C1 green.
  Local relaxed check (`artifacts/work162/check.py`) passes A0/A1/A2/A3, B4,
  B5, B6 on 11/23/37.
- Evidence: ranges 0.743/0.792/0.393 rad; seed 11 Level-0 `finished`
  10757 s, 1988 kg.
- Problems: none. Copy the relaxed check script to each new artifacts dir.
- Next: power transmission (B3): two or more full-turn revolute members, each
  consecutive pair linked by an interface (e.g. two vertical-axis rollers on
  posts on the deck bay's free -x part, rims c apart with a `rolling`
  interface; each roller `bearing` to its post, posts `bonded` to deck;
  watch the sweep: a full-turn polygon roller sweeps its circumcircle, so the
  partner's vertices must stay outside it, e.g. gear-free discs with a
  vertex-to-face gap of c via matched polygons, or one roller as a 96-gon).
  Then converter, vessel/housing voids, fins, B7.
