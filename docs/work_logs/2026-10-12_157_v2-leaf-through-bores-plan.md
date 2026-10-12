# Work 157 Plan: v2 Leaf Through-Bores That Preserve Contact Patches

Thai companion: `2026-10-12_157_v2-leaf-through-bores-plan.th.md`

Date: 2026-10-12

Status: Completed

## Objective

Goal v2 Tier A1 requires at least 25 % of leaves to be non-prismatic (no
single direction leaves 99 % of the mesh area parallel or perpendicular to it)
and at least 5 % to have a through-hole (genus >= 1). Every v1 leaf is a
straight extrusion, which is prismatic and has genus 0 (seed 11: 0/226 holed).

Add a v2 leaf refinement step that runs after the v1 layout. For a seed-chosen
subset of leaves it adds one cylindrical through-bore to the local extruded
solid before its placement transforms. The bore axis passes through the local
axis point `(0, 0, h/2)`, is tilted from the extrusion axis by a drawn angle
`beta` (an oblique bore gives wall normals that are neither parallel nor
perpendicular to the extrusion axis), enters through one end cap and leaves
through the other, and never reaches the side walls.

Refinement only removes material inside the leaf, so it cannot create new
interpenetration and the leaf box does not grow. Contact is kept by rule:
each bore exit ellipse on a cap must stay clear of every contact patch that
the cap receives from a neighbour.

## Geometry rules (SI units, local leaf frame)

- Extrusion along local +z from `z = 0` to `z = h`; declared inscribed radius
  `rho = inscribed_radius_m - linear_tolerance_m`.
- Bore radius `r = f * rho`, `f` drawn in a declared range; tilt `beta` drawn
  in a declared range (5 to 40 degrees), azimuth `phi` uniform.
- Lateral clearance: `(h/2) tan(beta) + r / cos(beta) <= (1 - wall) rho`,
  so the bore stays inside the inscribed cylinder over `0 <= z <= h`. When no
  tilt in the range fits, the leaf is left unrefined (no silent clipping).
- Exit centres: `-/+ (h/2) tan(beta) (cos phi, sin phi)` on caps 0 and 1;
  exit radius bound `r / cos(beta)`.
- Patch rules from the planned interfaces: a cap that is the target face of a
  smaller source cap (mode `inside`) receives the source disk; a source cap
  that holds a target region (mode `around`) receives that target region
  (disk outer radius or rectangle half-diagonal). The other cases keep the
  leaf's full face outline in contact, so they need no clearance. Each exit
  must be at least `patch radius + r / cos(beta) + linear tolerance` from
  every patch centre on its cap.

## Scope

- New `src/formula_ultimate/hierarchy/leaf_refinement.py` (pure Python):
  config, refined grammar version, `contact_patches`, `bore_program`,
  `validate_refined_program`, `base_program`, `refine_layout`.
- New `scripts/hierarchy/functional_realization.py` (CAD runtime): realize a
  v1 or refined program with the existing executor and tessellation.
- `functional.py`: record each leaf's own grammar version in the manifest.
- `scripts/hierarchy/generate_functional_vehicle.py`: refine after planning,
  realize with the new realizer, hash the refinement config.
- New tests `tests/test_hierarchy_leaf_refinement.py`.

## Planned files

- `src/formula_ultimate/hierarchy/leaf_refinement.py` (new)
- `scripts/hierarchy/functional_realization.py` (new)
- `src/formula_ultimate/hierarchy/functional.py`
- `scripts/hierarchy/generate_functional_vehicle.py`
- `tests/test_hierarchy_leaf_refinement.py` (new)
- this plan and result pair (English and Thai)
- `auto-loop/progress.md`, `auto-loop/progress.th.md`

## Validation

1. `python -m unittest tests.test_hierarchy_leaf_refinement tests.test_hierarchy_functional tests.test_hierarchy_functional_joints -v`
2. Generator run for seed 11 under the CAD runtime into `artifacts/work157/`
   and a spot check of the A1 shares and interface contact with the
   acceptance helpers.
3. `pwsh -NoProfile -File auto-loop/verify.ps1`: Gates 1 and 2 must pass;
   Gate 3 recorded per tier.

## Success criteria

- `TierA1GeometryLanguage` passes; all Tier A0 tests, A2 and A3 still pass;
  the v1 suite still passes.
- No v1 module or existing test changes.

## Risks

- Bored meshes might fail closure or the genus count if the tessellation is
  poor; the realizer measures every mesh and raises on closure problems.
- A small leaf might get a bore near the tessellation tolerance; the radius
  fraction and wall margin keep features well above `2e-3 L`.
- Non-prismatic by an oblique bore is the acceptance proxy, not a claim about
  structural purpose.

## Non-goals

- No fasteners, `threaded` joints, motions or function evidence.
- No tapered or lofted leaves in this item.
- No special-casing of seeds 11, 23 or 37.
