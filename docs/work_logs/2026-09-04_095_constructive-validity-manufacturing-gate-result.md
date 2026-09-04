# Work 095 Result: Constructive Validity and Manufacturing Gate

Thai companion: `2026-09-04_095_constructive-validity-manufacturing-gate-result.th.md`

## Status and outcome

Status: Completed

Work 095 implements a deterministic fail-closed constructive-validity and coarse manufacturing gate. A matched 48-opportunity pilot gave one primitive control and five Work 092 curved/free-form identities the same eight scenarios. Every family produced one accepted baseline, one preregistered repaired case, and six visible rejected controls, for an equal synthetic-fixture yield of `0.25`.

This is gate-behavior evidence over synthetic matched measurements. It is not independently measured manufacturability evidence for the referenced STEP geometry.

## Files changed

- `config/manufacturing/constructive_validity_gate_v1.json`
- `src/formula_ultimate/components/constructive_validity.py`
- `src/formula_ultimate/components/__init__.py`
- `scripts/experiments/run_constructive_validity_pilot.py`
- `tests/test_constructive_validity.py`
- `docs/contracts/CONSTRUCTIVE_VALIDITY_MANUFACTURING_GATE_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored replay evidence under `artifacts/work095/`

## Decisions and evidence

- Source candidate IDs and STEP hashes are checked against the Work 092 manifest and primitive witness configuration. The dimensional/process evidence is separately labeled `synthetic_contract_fixture`.
- Exact schemas reject unknown fields, non-finite values, and numeric aliases for Boolean flags. Python's `1 == True` behavior was found by a negative test and closed with exact type checks.
- Constructive violations cover invalid B-rep, wrong solid count, self-intersection, zero thickness, and sliver feature size. Process violations cover minimum wall/ligament/radius, tool access, overhang/support, enclosed void/escape, tolerance, joining access, and material/process compatibility.
- Every applicable violation is returned in stable order. The matched `unsupported_wall` scenario records both `wall_below_minimum` and `unsupported_overhang`.
- Only `add_support`, `increase_escape_hole`, and `increase_joining_access` are preregistered. The pilot uses `add_support`; its evidence before/after hashes, operation, original genotype, evaluated genotype, and provenance identity are recorded.
- Hidden, unregistered, over-budget, and post-observation repairs reject. No performance evidence is used by the gate.

## Pilot evidence

- Total opportunities: `48`; opportunities per family: `8`
- Families: `primitive_control`, `curved_branch`, `tapered_hollow_duct`, `lofted_rotary_member`, `organic_load_bridge`, `variable_section_shell`
- Status per family: `accepted=1`, `repaired=1`, `rejected=6`
- Validity yield per family: `0.25` for all six families
- Required cause counts per family: `self_intersection=1`, `sliver_feature=1`, `zero_thickness=1`, `tool_access_blocked=1`, `wall_below_minimum=1`, `unsupported_overhang=1`, `hidden_repair=1`
- Gate SHA-256: `4e9f8b3d739ccbcdb88c395954e4fcf6ad295ea6ca6c7b82cb53fb94b4531e8f`
- Result SHA-256: `59f7df5aa86c0c858eb336867a7c10a4b934db66629f44b0e5f4493619830e14`
- `post_observation_repair_allowed: false`; `cad_measurement_executed: false`

## Exact validation commands

```powershell
python -m unittest tests.test_constructive_validity -q
# exit 0; 9 tests passed

python scripts/experiments/run_constructive_validity_pilot.py --config config/manufacturing/constructive_validity_gate_v1.json --mutation-protocol config/experiments/topology_mutation_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --work092-manifest artifacts/work092/run_g/manifest.json --primitive-witness config/cad/step_freecad_geometry_witness_v2.json --output artifacts/work095/run_a/result.json
# exit 0; 48 opportunities; yield_per_family=[0.25]

python scripts/experiments/run_constructive_validity_pilot.py --config config/manufacturing/constructive_validity_gate_v1.json --mutation-protocol config/experiments/topology_mutation_v1.json --solid-config config/cad/freeform_brep_solid_grammar_v2.json --work092-manifest artifacts/work092/run_g/manifest.json --primitive-witness config/cad/step_freecad_geometry_witness_v2.json --output artifacts/work095/run_b/result.json --replay-reference artifacts/work095/run_a/result.json
# exit 0; exact complete-result replay

python -m compileall -q src scripts tests
# exit 0

python -m unittest tests.test_constructive_validity tests.test_repository_contract -q
# exit 0; 15 tests passed

python -m unittest discover -s tests -q
# exit 0; 672 tests passed in 283.044 s; 7 expected environment-dependent skips
```

## Limitations and follow-up

Matched synthetic scalar evidence proves equal gate treatment, not equal real failure probability. The gate does not derive thickness fields, curvature, access paths, voids, or joining regions from CAD. It also does not prove supplier capability, structural capacity, production quality, cost, safety, or physical validity. Work 096 must recover independent semantic geometry witnesses; those measurements can then replace the synthetic fixtures without changing the fail-closed rules.
