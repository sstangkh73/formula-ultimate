# Work 158 Result: v2 Hex-Socket Fasteners as Threaded Joints

Thai companion: `2026-10-12_158_v2-hex-socket-fasteners-result.th.md`

Date: 2026-10-12

Plan: `2026-10-12_158_v2-hex-socket-fasteners-plan.md`

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/fasteners.py` (new): `FastenerConfig`,
  `SOCKETED_LEAF_GRAMMAR_VERSION = "func-leaf-socketed-v2"`, `hexagon`,
  `socket_program`, `socket_base_program`, `validate_v2_program`,
  `pin_program`, `socket_axis`, `socket_exits`, `add_fasteners`,
  `fastener_problems`, `fastener_config_record`.
- `src/formula_ultimate/hierarchy/functional.py`: `with_threaded_axes`;
  `config_sha256_v2` takes an optional fastener record (hash unchanged when
  it is absent).
- `scripts/hierarchy/functional_realization.py`: validates with
  `validate_v2_program`.
- `scripts/hierarchy/generate_functional_vehicle.py`: runs `add_fasteners`
  and `fastener_problems` after the Work 157 refinement, writes the threaded
  axes, hashes the fastener config.
- `tests/test_hierarchy_fasteners.py` (new, 10 tests, one CAD subprocess).

## Decisions

- Sockets go only on leaves Work 157 left unbored (no bore/socket
  intersection to reason about). Every such leaf tries (`socket_probability =
  1.0`, 24 draws). A first config (p = 0.6, 12 draws, `min_apothem_m = 1e-3`)
  gave only 7 joints on seed 23 and 3 on seed 10, so the config was widened to
  `min_apothem_m = 5e-4 m` and 24 draws before any acceptance run. Counts
  (pure-Python planning): seeds 11/23/37/0/10 give 22/18/21/14/10.
- Hexagon instead of a cylinder: flat faces tessellate exactly, so the pin
  faces are parallel to the socket faces at exactly the clearance
  `c = 2.5e-5 m` (a quarter of the 1e-4 m contact tolerance). A cylinder would
  have a gap and penetration that depend on the CAD tessellation.
- Pin ids are `<holed leaf id>.pin`, interface ids `<pin id>.thread`; the pin is
  a new child of the holed leaf's parent assembly. Pin materials are drawn per
  pin from the declared catalogue with their own derived seed, so the
  existing leaf material draws do not change.

## Commands and exit status

1. `python -m unittest tests.test_hierarchy_fasteners tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional -v`
   exit 0: `Ran 25 tests`, `OK`.
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work158/seed11`
   exit 0: `seed 11: 248 leaves, 247 interfaces, 0 motions`.
3. `python artifacts/work158/check.py artifacts/work158/seed11` (gitignored
   spot check with the acceptance helpers) exit 0: `threaded 22`,
   `b10 failures 0`, worst interface gap `2.4999994e-05 m`, worst pin
   penetration `0.0`; 114/248 leaves holed, 162/248 non-prismatic.
4. `pwsh -NoProfile -File auto-loop/verify.ps1` exit 1 (Gate 3 only):
   - Gate 1: `material publication boundary: PASS`.
   - Gate 2: `Ran 1123 tests in 729.577s`, `OK (skipped=11)`.
   - Gate 3: `Ran 41 tests`, `FAILED (failures=10)`. The v1 suite 13/13 and all
     v2 Tier A tests pass; TierB10 now passes; B1-B9 (missing
     `function_evidence`) and C1 (missing evaluator) fail as expected.

## Limitations

- A hexagonal pin in a socket is a representation of a threaded fastener: no
  helix, preload, friction or load path. The contract checks a through-hole only.
- The pin clamps nothing beyond its own holed leaf; the joint only shows that
  a fastener occupies a hole.
- The joint count depends on how many unbored leaves have room clear of their
  cap contact patches; seed 10 has only 10 joints, so a later change that
  bores more leaves could drop some seeds below 8.

## Follow-up

- Tier B function evidence. Note that every B1-B9 test first checks that
  `function_evidence` has all nine keys, so none of B1-B9 passes until all
  nine capabilities have evidence; plan the functional modules accordingly.
- Tier C1 evaluator (independent of the geometry; a good Codex task).
