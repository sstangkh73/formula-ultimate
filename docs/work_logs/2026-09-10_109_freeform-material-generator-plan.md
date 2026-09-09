# Work 109 Plan: Open Free-Form Material Generator

Thai companion: `2026-09-10_109_freeform-material-generator-plan.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Objective

Implement a bounded implicit material/void generator that can change continuous boundaries and topology without named-part templates, while retaining explicit resolution, labels, mutation ancestry, conversion error, resource accounting and deterministic replay.

## Scope and experiment

The source representation is a finite uniform Cartesian occupancy/material field in SI units. It is an admitted first implicit-volume implementation, not a universal adaptive geometry system. Registered operators are boundary displacement, cavity routing, branching, split, merge and material redistribution.

- Independent variables: edit operator, cell resolution, mutation seed and complexity cap.
- Dependent variables: occupied volume, connected-component and enclosed-void counts, label volumes, thin-feature survival, surface conversion error, execution operations and geometry identity.
- Controls: identical spatial domain, material labels, seed schedule, operator slots and per-attempt cell/operation budgets; Work 108 remains the fixed B-rep comparison route.
- Falsification: create/close a through-hole, split/reconnect occupied regions, preserve an asymmetric thin feature, reject vanished required cavities, label mixing, invalid bounds, over-budget edits and renaming-only pseudo-novelty.

## Planned files

- `src/formula_ultimate/search/freeform_material_generator.py`
- `config/development/freeform_material_generator_v1.json`
- `scripts/development/run_freeform_material_generator.py`
- `tests/test_freeform_material_generator.py`
- `docs/contracts/FREEFORM_MATERIAL_GENERATOR_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored generated corpus, OBJ surfaces, ancestry and reports under `artifacts/work109/`

## Implementation and validation

1. Validate exact-schema SI domain, resolution, feature/budget limits, labels, source field and seeded operator schedule.
2. Construct occupancy directly from implicit primitives, apply each bounded edit causally and archive before/after identities and topology descriptors.
3. Extract a watertight oriented voxel boundary to OBJ, measure its enclosed volume against field volume and reject non-manifold/duplicate faces.
4. Execute registered mutation chains plus resolution-enlargement trials and unsupported-conversion controls.
5. Produce deterministic `result.json` and exact replay.

Planned gates:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_freeform_material_generator tests.test_repository_contract -v
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_a
python scripts/development/run_freeform_material_generator.py --config config/development/freeform_material_generator_v1.json --output-root artifacts/work109/run_b --replay-reference artifacts/work109/run_a/result.json
python -m compileall -q src scripts tests
```

Run affected regressions, `git diff --check`, explicit staging, staged-name inspection and `git diff --cached --check` before one immediate scoped commit.

## Success criteria

All registered operators execute within the fixed budget; the hole/split/reconnect/thin-feature and negative controls behave as declared; surface volume agrees with field volume within the frozen tolerance; representation refinement is reported without being relabeled physical truth; identical inputs replay exactly; bilingual implementation evidence is committed.

## Risks and non-goals

Grid anisotropy, voxel aliasing and limited resolution can masquerade as design constraints. They remain observable and motivate Work 110 meshing/refinement. Non-goals: functional superiority, target silhouette, mixed-property homogenization, structural/flow/thermal physics, manufacturing, whole-vehicle or physical validation, dependency installation, push or history rewrite.
