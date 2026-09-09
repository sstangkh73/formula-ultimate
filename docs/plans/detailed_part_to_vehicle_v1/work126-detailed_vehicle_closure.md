# Work 126: Complete detailed digital candidate

Thai companion: `work126-detailed_vehicle_closure.th.md`

Status: Planned

Original Work 106 package: 125

Dependencies: Work 118, Work 119, Work 120, Work 121, Work 122, Work 123, Work 124, Work 125

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Realize every required physical function and internal hardware path in one inspectable whole-candidate assembly.

Applicable subsystem models, Work 125 local evidence and an exploratory architecture; isolated superiority is not required for every part.

## 2. Proposed files

- `src/formula_ultimate/assembly/detailed_vehicle_closure.py`
- `config/development/detailed_vehicle_closure_v1.json`
- `scripts/development/run_detailed_vehicle_closure.py`
- `tests/test_detailed_vehicle_closure.py`

## 3. Implementation sequence

1. Trace external functions to material regions, internal hardware and interfaces; list all unresolved gaps.
2. Generate/place parts and connection detail, permitting multifunctional regions and architecture changes.
3. Close mass/inertia, occupied volume, energy, signal, heat and load-path ledgers.
4. Audit assembly and swept motion, then rerun affected local/coupled evidence on the final revision.

## 4. Experiment

- IV: Part placement, joining strategy, architecture and tolerance state.
- DV: Hardware coverage, overlap/clearance, complete mass, motion compatibility and required-domain gaps.
- Controls: Same external functions/task and authoritative material ownership.

## 5. Tests and falsification

Remove a fastener/support/seal/signal path where required; detect hidden voids, double mass, interference and stale subsystem envelopes.

## 6. Registration and acceptance

Freeze completeness checklist, geometry-detail level G3, functional coverage, tolerance and collision/motion gates.

All required geometry/hardware paths close and final revision is inspectable. Essential missing physics means a detailed exploratory candidate, not promotion-ready.

## 7. Deliverables and handoff

Whole and individual CAD, exploded/section views, region bill, assembly sequence, closure matrix and unresolved list.

Supplies exact candidate identities for Works 127–130.

## 8. Risks and non-goals

Do not reuse Work 088 blocked geometry without new evidence. G3 detail is not physical validation; purchased parts need provenance and are not generated discoveries.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_detailed_vehicle_closure tests.test_repository_contract -v
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_a
python scripts/development/run_detailed_vehicle_closure.py --config config/development/detailed_vehicle_closure_v1.json --output-root artifacts/work126/run_b --replay-reference artifacts/work126/run_a/result.json
```
