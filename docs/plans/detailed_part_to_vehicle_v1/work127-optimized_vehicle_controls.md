# Work 127: Optimized vehicle controls and causal substitution

Thai companion: `work127-optimized_vehicle_controls.th.md`

Status: Planned

Original Work 106 package: 126

Dependencies: Work 123, Work 126

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Establish whether a candidate's system benefit survives optimized baselines, controller adaptation and transferred burdens.

Work 126 exact candidate assembly and Work 123 harness; Work 124 accounting and registration requirements.

## 2. Proposed files

- `src/formula_ultimate/experiments/optimized_vehicle_controls.py`
- `config/development/optimized_vehicle_controls_v1.json`
- `scripts/development/run_optimized_vehicle_controls.py`
- `tests/test_optimized_vehicle_controls.py`

## 3. Implementation sequence

1. Define fair fixed-topology and random/reference arms without constraining the open arm to their layout.
2. Optimize all arms under matched task, library opportunity and complete compute budget.
3. Substitute the proposed mechanism using a common controller, then matched-budget retuning.
4. Account for changed cooling, containment, supports, energy and manufacturing assumptions.

## 4. Experiment

- IV: Vehicle/search arm, subsystem substitution and controller treatment.
- DV: Completion/time, total energy/mass, failure margins and combined search/tuning cost.
- Controls: Same external race, energy, environment, safety scope, materials and random seed policy.

## 5. Tests and falsification

Untuned baseline, free controller effort, omitted cooling mass and unequal source energy must invalidate fairness claims.

## 6. Registration and acceptance

Freeze baseline families, optimization opportunity, paired comparison, meaningful system effect and uncertainty method.

All arms receive registered opportunity and complete costs. A system-benefit claim requires improvement beyond uncertainty without shifted hidden burdens.

## 7. Deliverables and handoff

Optimized baseline artifacts, substitution matrix, controller ledgers and signed system-effect analysis.

Freezes finalists and comparison logic for held-out race Work 128.

## 8. Risks and non-goals

A conventional baseline is a control, not a required answer. Invalid fairness requires a new registration; no external novelty claim.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_optimized_vehicle_controls tests.test_repository_contract -v
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_a
python scripts/development/run_optimized_vehicle_controls.py --config config/development/optimized_vehicle_controls_v1.json --output-root artifacts/work127/run_b --replay-reference artifacts/work127/run_a/result.json
```
