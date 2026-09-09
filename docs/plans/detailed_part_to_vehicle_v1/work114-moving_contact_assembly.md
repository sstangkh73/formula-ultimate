# Work 114: Moving and compliant contact assembly

Thai companion: `work114-moving_contact_assembly.th.md`

Status: Planned

Original Work 106 package: 113

Dependencies: Work 113

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Demonstrate compatible motion and load transfer through a small detailed assembly, including contact history.

Work 113 detailed/reduced joint models and Work 112 frames; retain Work 088 moving/rigid conflict as a regression case.

## 2. Proposed files

- `src/formula_ultimate/assembly/moving_contact_assembly.py`
- `config/development/moving_contact_assembly_v1.json`
- `scripts/development/run_moving_contact_assembly.py`
- `tests/test_moving_contact_assembly.py`

## 3. Implementation sequence

1. Define generalized coordinates, constraints, initial conditions and allowed motion envelopes.
2. Couple rigid/flexible members to physical joints; track contact opening, closing and slip history.
3. Check swept-volume collision and clearance through motion, not only the initial pose.
4. Compare detailed and reduced responses under time-step refinement and reversal.

## 4. Experiment

- IV: Joint placement, compliance, motion input, preload and time step.
- DV: Constraint drift, transmitted force/moment, clearance, energy and phase response.
- Controls: Identical geometry, initial energy and imposed boundary histories.

## 5. Tests and falsification

Free rigid motion, incompatible constraints, severed coupling, impact/reversal and reduced-model range violation; recover reactions rather than invent them.

## 6. Registration and acceptance

Freeze time-step ladder, contact event rules, clearance tolerance and allowed constraint/energy residuals.

Registered motion cases pass consistency/refinement gates; collisions or incompatible joints block that assembly, not the entire representation.

## 7. Deliverables and handoff

Motion replay, swept-clearance report, contact histories, energy ledger and applicability bounds.

Provides dynamic assembly capability to Works 117, 118 and 119.

## 8. Risks and non-goals

Stiff contact and flexible modes may need different time scales. Expose coupling error; no complete suspension, crash or vehicle-readiness claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_moving_contact_assembly tests.test_repository_contract -v
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_a
python scripts/development/run_moving_contact_assembly.py --config config/development/moving_contact_assembly_v1.json --output-root artifacts/work114/run_b --replay-reference artifacts/work114/run_a/result.json
```
