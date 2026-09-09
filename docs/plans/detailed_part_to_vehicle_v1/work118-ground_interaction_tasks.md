# Work 118: Ground interaction, stopping and direction control

Thai companion: `work118-ground_interaction_tasks.th.md`

Status: Planned

Original Work 106 package: 117

Dependencies: Work 114, Work 116

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Evaluate physical ground interaction and required motion functions without fixing a wheel or steering architecture.

Moving/contact models and material applicability; freeze the external surface/environment for each comparison.

## 2. Proposed files

- `src/formula_ultimate/simulation/ground_interaction_tasks.py`
- `config/development/ground_interaction_tasks_v1.json`
- `scripts/development/run_ground_interaction_tasks.py`
- `tests/test_ground_interaction_tasks.py`

## 3. Implementation sequence

1. Define ground-contact ports, surface properties and force/moment sign conventions.
2. Implement a verified bounded contact/friction route with explicit applicability.
3. Evaluate propulsion reaction, direction change and stopping with all dissipated power recorded.
4. Exercise different contact placements/geometry and return loads to local part models.

## 4. Experiment

- IV: Contact geometry/placement, surface condition, slip state and commanded motion.
- DV: Traction, stopping distance/time, directional response, loss and contact stability.
- Controls: Same external route, initial state, surface and energy opportunity.

## 5. Tests and falsification

Zero-friction limit, lift-off, reverse motion, saturation and disconnected actuation; no ground force without an allowed physical interaction.

## 6. Registration and acceptance

Freeze surface data/range, contact resolution, force/loss errors and numerical stability criteria.

Reference behavior and conservation/refinement checks pass; unsupported tire or non-tire behavior stays unresolved rather than receiving a generic coefficient.

## 7. Deliverables and handoff

Contact/motion histories, force and loss maps, stopping/direction tests and coverage limits.

Feeds whole-candidate transient Work 123 and detailed assembly Work 126.

## 8. Risks and non-goals

A simple friction law does not validate tires, soft soil or arbitrary locomotion. Split new interaction domains into verified adapters; no wheel-count rule.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_ground_interaction_tasks tests.test_repository_contract -v
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_a
python scripts/development/run_ground_interaction_tasks.py --config config/development/ground_interaction_tasks_v1.json --output-root artifacts/work118/run_b --replay-reference artifacts/work118/run_a/result.json
```
