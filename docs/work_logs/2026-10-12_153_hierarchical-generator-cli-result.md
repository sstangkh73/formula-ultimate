# Work 153 Result: Hierarchical Vehicle Generator CLI

Thai companion: `2026-10-12_153_hierarchical-generator-cli-result.th.md`

Date: 2026-10-12

Status: Completed

## Files changed

- `src/formula_ultimate/hierarchy/decomposition.py`: `decompose(seed, config,
  start_attempt=0)`; the default behaviour is unchanged.
- `src/formula_ultimate/hierarchy/composition.py` (new): `plan_vehicle`
  (decompose -> layout -> `layout_problems`; on `LayoutFailure` continue from
  the next decomposition attempt, at most `max_plan_attempts=8`, rejections
  recorded), `load_leaf_materials`, `assign_materials`,
  `composition_config_sha256`, `build_part_tree`, `build_manifest`,
  `manifest_bytes`. `DESIGN_LANGUAGE_VERSION = "hier-composition-v1"`,
  `contact_tolerance_m = 1e-4`.
- `scripts/hierarchy/generate_hierarchical_vehicle.py` (new): the contract
  entry point. Realizes each leaf with Work 151 `realize_leaf` into
  `DIR/meshes/<leaf id>.stl`, takes mass and centre of mass from the re-read
  STL, writes `manifest.json` (sorted keys, no NaN).
- `tests/test_hierarchy_composition.py` (new, 12 tests, one runs the CLI
  under the CAD runtime for seed 37).
- This result pair, the plan pair, `auto-loop/progress.md` and
  `auto-loop/progress.th.md`.

## Decisions

- Materials: v1 reads the existing synthetic record
  `synthetic_aluminium_like_verification_v1` from
  `config/materials/engineering_material_manufacturing_v1.json` at run time
  (`evidence_status=synthetic`, `design_use_allowed=false`). No material value
  was written into a tracked file. Densities appear only in generated
  packages under `artifacts/` or temporary directories. The per-leaf draw is
  seed-driven so a larger catalogue can be added without code changes.
- Joint kinds are the Work 150 labels. `interference` joints carry no
  `interference_m` because the layout makes flush contact (the field is
  optional in the contract).
- The layout fallback is part of the declared search, not a per-seed case.

## Commands and exit status

1. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_hierarchical_vehicle.py --seed 11 --out artifacts/work153/seed11`
   exit 0, `226 leaves, 225 interfaces`, 13.8 s.
2. Same for `--seed 4`: exit 0, two decomposition attempts rejected by layout
   and recorded on stderr, `180 leaves, 179 interfaces`.
3. `python -m unittest discover -s auto-loop/acceptance`: `Ran 13 tests in 66.881s`, `OK`.
4. `python -m unittest tests.test_hierarchy_composition tests.test_hierarchy_decomposition`:
   `Ran 24 tests in 86.384s`, `OK`.
5. Planning sweep seeds 0..39 (pure Python): 0 failures, 1 seed (4) needed the
   fallback.
6. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gate 1 `PASS`; Gate 2
   `Ran 1094 tests in 502.849s`, `OK (skipped=11)`; Gate 3 `Ran 13 tests in
   71.967s`, `OK`; `ALL GATES PASSED`.

## Limitations

- Passing Gate 3 is a geometry and assembly representation gate only. Nothing
  shows that any part works, carries load or survives heat.
- One synthetic material: every mass is a representation value, not a design
  mass.
- Joint kind labels have no physical model behind them.
- Box disjointness makes the vehicle sparse; it is not packaged.
- The acceptance penetration check samples vertices and centroids only.

## Follow-up

- Replace the synthetic material with catalogue-only materials (values stay
  in `/private/` or are read at run time), and record the material choice
  procedure.
- Couple the hierarchy to Level-0 physics and the race kernel (a later goal).
