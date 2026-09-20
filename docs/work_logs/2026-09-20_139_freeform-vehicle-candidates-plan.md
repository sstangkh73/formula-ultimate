# Work 139 Plan: Free-form Vehicle Candidates

Thai companion: `2026-09-20_139_freeform-vehicle-candidates-plan.th.md`

Date: 2026-09-20 (Asia/Bangkok)

Status: Completed

Execution plan card: `docs/plans/detailed_part_to_vehicle_v1/work139-freeform_vehicle_candidates.md`

## Objective

Let a vehicle candidate declare a component as an admitted Work 092 free-form solid instead of a box or a cylinder, build it, gate its packaging on the built solids, and evaluate every component with the Work 138 evaluator.

## Entry evidence

- `scripts/cad/generate_vehicle_assembly.py` emits only a box or a cylinder; `config/vehicle/topology_neutral_vehicle_v1.json` is the four-component base assembly the campaign mutates.
- `artifacts/work092/run_e/` holds ten admitted free-form solids, each one valid solid, with `manifest.json` and `result.json` carrying their declaration and STEP hashes.
- `scripts/cad/generate_freeform_solid_corpus.py` exposes `execute_candidate(candidate, profiles)`, which rebuilds a corpus member in CadQuery from its declaration; the profiles come from the Work 091 wire config.
- Work 138 provides `validate_protocol`, `evaluate_candidate` and the six-value status vocabulary, with an admitted run at result SHA-256 `50e50ed6fa8aa3dfe93804f3a3e67a1471331b203c0da4c1d1c6001d0054d6ec`.

## Scope

- `src/formula_ultimate/search/freeform_vehicle_candidate.py`: declaration schema and validation, required function-tag coverage, packaging gates against the built manifest, generation of the Work 138 evaluation protocol, and run summary.
- `scripts/cad/build_freeform_vehicle_candidate.py`: run under the pinned CadQuery runtime; build each component from a primitive or from an admitted corpus member, place it, export per-component and assembly STEP, and measure volume, mass, centre, bounding box, pairwise intersection and keep-out clearance.
- `scripts/development/run_freeform_vehicle_candidate.py`: build both candidates, gate packaging, evaluate every component through Work 138, run the eight controls, write `result.json` with a canonical SHA-256, and support `--replay-reference`.
- `config/development/freeform_vehicle_candidate_v1.json`: the primitive baseline and the free-form variant, differing in one component.
- `tests/test_freeform_vehicle_candidate.py`: logic tests that always run; kernel tests skip without CadQuery.
- `docs/contracts/FREEFORM_VEHICLE_CANDIDATE_V1.md` and its Thai companion; the plan-card pair; the index rows; this bilingual plan and its result.

## Validation

1. `python -m unittest tests.test_freeform_vehicle_candidate -v`: exit 0.
2. `.tools/cadquery-mcp/Scripts/python.exe scripts/cad/build_freeform_vehicle_candidate.py ...`: exit 0 for both candidates.
3. `python scripts/development/run_freeform_vehicle_candidate.py --config ... --output-root artifacts/work139/run_a`: exit 0, eight controls rejected, every component carrying one registered status.
4. The same runner into `run_b` with `--replay-reference`: exit 0 and an identical result SHA-256.
5. `python -m unittest tests.test_repository_contract -v`, `python -m unittest discover -s tests`, `python -m compileall -q src scripts tests`, `git diff --check`, `git diff --cached --check`: exit 0.

## Success and failure criteria

Success: both candidates build, the packaging gates are measured on the built solids, every component carries one registered status, all eight controls are rejected, and the replay is exact.

Failure: a free-form component is silently replaced by a primitive, a packaging gate is waived, a component disappears from the accounting, or the run claims a discovery.

## Risks and non-goals

- Risk: a corpus member does not fit its slot. Then the candidate stops as `incomplete_composition`; substituting a box is forbidden.
- Risk: the matched pair reads as a superiority claim. The result must state that one pair under one load case establishes nothing beyond evaluability.
- Non-goals: no new free-form declaration outside the admitted corpus, no scaling of corpus members, no race-time coupling, no search, no push, no history rewrite.
