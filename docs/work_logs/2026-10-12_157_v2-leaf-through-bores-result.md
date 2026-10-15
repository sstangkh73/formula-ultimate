# Work 157 Result: v2 Leaf Through-Bores That Preserve Contact Patches

Thai companion: `2026-10-12_157_v2-leaf-through-bores-result.th.md`

Date: 2026-10-12

Status: Completed

Plan: `2026-10-12_157_v2-leaf-through-bores-plan.md`

## Files changed

- `src/formula_ultimate/hierarchy/leaf_refinement.py` (new, pure Python):
  `RefinementConfig` (bore probability 0.8, tilt 5–40 deg, radius fraction
  0.12–0.30 of `rho`, wall fraction 0.12, 12 draws), `REFINED_LEAF_GRAMMAR_VERSION =
  "func-leaf-bored-v2"`, `contact_patches`, `bore_parameters`, `bore_program`,
  `base_program`, `bore_exits`, `validate_refined_program`, `refine_layout`,
  `refinement_problems`, `refinement_config_record`.
- `scripts/hierarchy/functional_realization.py` (new, CAD runtime):
  `realize_program` validates a v1 or refined program and reuses the
  unchanged executor and `tessellate_m`.
- `src/formula_ultimate/hierarchy/functional.py`: `config_sha256_v2` takes an
  optional refinement record (unchanged output without it);
  `with_leaf_grammar_versions` records each program's own grammar in the
  manifest.
- `scripts/hierarchy/generate_functional_vehicle.py`: refine after planning,
  re-check with `refinement_problems` (raises on any problem), realize with
  `realize_program`, hash the refinement config.
- `tests/test_hierarchy_leaf_refinement.py` (new, 9 tests, one through the CAD
  runtime).

## Decisions

- Deviation from the plan: the bore axis point is `(ox, oy, h/2)` with a
  drawn lateral offset instead of a fixed `(0, 0, h/2)`. Reason: with a centred
  axis, 104 of 110 leaves with a received contact patch (seed 11) could not
  be bored because the exits fell on the centred patches. The clearance rule
  became `|(ox, oy)| + (h/2) tan b + r / cos b <= (1 - wall) rho`. The bore
  probability was raised from 0.5 to 0.8 (refined share 25–33 % at 0.5 was
  too close to the 25 % threshold).
- Refinement only removes material inside the inscribed cylinder, so it
  cannot create interpenetration, and the layout boxes and interfaces are
  unchanged (checked by `refinement_problems`).
- Patch rules: a target cap under a smaller source cap (mode `inside`)
  receives the source disk; a source cap holding a target region (mode
  `around`) receives that region. In the other cases the leaf's whole face
  outline stays in contact.

## Commands and results

1. `python -m unittest tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional tests.test_hierarchy_functional_joints`
   -> exit 0, `Ran 19 tests in 43.411s`, `OK` (after one test fix: a bore of
   radius `0.99 * inscribed` was not rejected because the limit is
   `inscribed - tolerance`, which is almost the same value; the test now uses
   radius `inscribed`).
2. Pure planning share (bored leaves / leaves): seed 11 92/226, 23 110/229,
   37 101/229, 0 72/177, 1 81/201, 2 99/228; `refinement_problems` empty for all.
3. `.tools/cadquery-mcp/Scripts/python.exe scripts/hierarchy/generate_functional_vehicle.py --seed 11 --out artifacts/work157/s11`
   -> exit 0, 22 s, 226 leaves.
   `python artifacts/work157/spot_check.py artifacts/work157/s11` (acceptance
   helpers): bored 92, non-prismatic 160, holed (genus >= 1) 92, worst
   interface gap 2.1e-18 m.
4. `pwsh -NoProfile -File auto-loop/verify.ps1` -> Gate 1 PASS; Gate 2
   `Ran 1113 tests in 648.508s`, `OK (skipped=11)`; Gate 3
   `Ran 41 tests`, `FAILED (failures=11)`: v1 suite 13/13 pass, v2 Tier A0,
   A1, A2 (vacuous, no motions yet) and A3 pass; B1–B10 and C1 fail as before.

## Limitations

- Before this item the v2 meshes already passed the non-prismatic share
  (Gate 3 failed A1 on holes only). The proxy samples the 20 largest
  triangles, so some straight extrusions count as non-prismatic. The bores add
  genuinely oblique faces, but the proxy is not a shape-quality measure.
- A bore is a representation feature with no declared purpose (lightening,
  passage). It does not show load capacity.
- Contact checks use the declared face geometry; the acceptance measurement
  confirms seed 11 only in this item (seeds 23 and 37 through Gate 3).

## Follow-up

- Tier B10: real `threaded` fastener joints (>= 8 per seed). A suggested
  route: axial (tilt 0) bores in a holed leaf plus a new pin leaf whose shaft
  runs along the bore axis inside the hole and whose flat head sits on the
  cap, so the axis passes through the hole of one part and the pin material.
- Then the per-capability functional modules (Tier B) and the Level-0
  evaluator (Tier C).
