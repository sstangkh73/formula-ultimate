# Work 117: Bidirectional architecture and part tasks

Thai companion: `work117-architecture_part_feedback.th.md`

Status: Planned

Original Work 106 package: 116

Dependencies: Work 112, Work 114, Work 115

Mandatory common requirements: [index and execution rules](README.md). Numbers, files and CLI below are proposed, not implemented.

## 1. Outcome and inputs

Demonstrate a closed exploratory loop where assembly feedback changes local tasks and regenerates geometry.

Work 112 terminals and Work 114/115 coupled assembly models; external task remains immutable.

## 2. Proposed files

- `src/formula_ultimate/experiments/architecture_part_feedback.py`
- `config/development/architecture_part_feedback_v1.json`
- `scripts/development/run_architecture_part_feedback.py`
- `tests/test_architecture_part_feedback.py`

## 3. Implementation sequence

1. Define versioned internal task proposals with loads, heat, motion, envelopes and unknowns.
2. Generate local candidates from assembly-derived conditions rather than manually favorable loads.
3. Integrate explicit reduced/incomplete models and return changed requirements to the generator.
4. Run a bounded regeneration loop and invalidate stale local evidence after task changes.

## 4. Experiment

- IV: Architecture/part edits, decomposition and feedback enabled versus frozen local tasks.
- DV: Assembly quality, transferred mass/heat, feasibility margins and cost per iteration.
- Controls: Same external task, model coverage, initial candidates and compute opportunity.

## 5. Tests and falsification

Change assembly load and require local re-evaluation; merge multifunctional regions without duplicate mass; block invented missing coefficients.

## 6. Registration and acceptance

Freeze iteration/resource caps, task-change schema, uncertainty intervals and decision/stop rules.

At least one traced feedback/regeneration cycle executes with causally updated evidence. Improvement is tested, not required to make a negative experiment legitimate.

## 7. Deliverables and handoff

Task ancestry, before/after geometry, coupling ledger and positive/negative comparative result.

Provides the co-design loop for subsystem expansion and Work 124 search.

## 8. Risks and non-goals

Do not restore the isolated-survivor-only gate. Unresolved models can explore, but cannot justify complete feasibility or change the race rules.

## 9. Proposed validation commands

Implement the runner/CLI and freeze configuration before use. These commands were not executed by this planning work. For physical-test packages the runner analyzes recorded data only; it does not operate equipment.

```powershell
python -m unittest tests.test_architecture_part_feedback tests.test_repository_contract -v
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_a
python scripts/development/run_architecture_part_feedback.py --config config/development/architecture_part_feedback_v1.json --output-root artifacts/work117/run_b --replay-reference artifacts/work117/run_a/result.json
```
