# Work 130: Manufacturing, tolerance and assembly handoff

Thai companion: `work130-manufacturing_tolerance_handoff.th.md`

Status: Planned

Original Work 106 package: 129

Dependencies: Work 126, Work 129

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Assess whether the selected detailed candidate can be made, assembled and inspected by explicitly evaluated routes.

Work 126 final detail, Work 129 critical margins and applicable material/process data.

## 2. Proposed files

- `src/formula_ultimate/assembly/manufacturing_tolerance_handoff.py`
- `config/development/manufacturing_tolerance_handoff_v1.json`
- `scripts/development/run_manufacturing_tolerance_handoff.py`
- `tests/test_manufacturing_tolerance_handoff.py`

## 3. Implementation sequence

1. Map each region/feature to candidate process routes, stock assumptions and inspection access.
2. Check tool access, trapped volumes, joining sequence, fastening access and replaceability where required.
3. Propagate tolerances into fit, preload, clearance and critical physical margins.
4. Create inspection/assembly handoff and return necessary redesign to new candidate revisions.

## 4. Experiment

- IV: Process route, tolerance allocation, assembly order and material variability.
- DV: Accessible/manufacturable features, fit yield, margin sensitivity and unresolved process gaps.
- Controls: Same candidate functional requirements and evidence level across process options.

## 5. Tests and falsification

Inaccessible fastener, trapped internal core, impossible assembly order and worst-case clearance/preload; nominal-only fit must not pass tolerance readiness.

## 6. Registration and acceptance

Freeze evaluated routes, process capability evidence, tolerances, uncertainty propagation and inspection criteria.

Claim readiness only for explicitly passing routes with complete access/tolerance evidence; unsupported routes remain unknown, not globally impossible.

## 7. Deliverables and handoff

Manufacturing/assembly dossier, tolerance map, inspection plan and redesign/blocker list.

Defines testable selected hardware and conditions for Work 131 after separate authorization.

## 8. Risks and non-goals

Process capability must come from evidence, not a minimum-feature heuristic alone. No purchasing, fabrication or safety certification is authorized here.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_manufacturing_tolerance_handoff tests.test_repository_contract -v
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_a
python scripts/development/run_manufacturing_tolerance_handoff.py --config config/development/manufacturing_tolerance_handoff_v1.json --output-root artifacts/work130/run_b --replay-reference artifacts/work130/run_a/result.json
```
