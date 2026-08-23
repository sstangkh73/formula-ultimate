# Project Instructions for Formula Ultimate

## Mandatory Work-Log Protocol

Before any task-specific code, configuration, research document, or experiment
change:

1. Create `docs/work_logs/YYYY-MM-DD_NNN_<slug>-plan.md`.
2. State objective, scope, planned files, validation, success criteria, risks,
   and explicit non-goals.
3. Mark its status `In progress` before starting the task.

After the work and before its final commit:

1. Create the matching
   `docs/work_logs/YYYY-MM-DD_NNN_<slug>-result.md`.
2. Record files changed, decisions, exact test commands, exit status, relevant
   output, limitations, and follow-up work.
3. Change the plan status to `Completed` only after validation passes, or to
   `Stopped` with the reason when the task cannot be completed.

Plans and result records are append-oriented evidence. Do not rewrite an older
record to make a later outcome look planned; create a new numbered work item.

## Engineering Rules

- Work from explicit physics assumptions and SI units.
- Separate feasibility validation from simulation and scientific validation.
- Treat conservation residuals, numerical failures, and invalid states as
  observable outputs, never silent corrections.
- Never call a design physically validated from Level-0 simulation alone.
- Keep fixed-topology baselines and free-topology experiments comparable by
  compute budget, component library, constraints, and random seeds.
- Preserve deterministic replay metadata for every experiment.
- Add tests with every implemented physical law or component model.

## Review Discipline

For experiment changes, explicitly define independent variables, dependent
variables, controls, metrics, success criteria, and failure criteria. Attempt to
falsify the preferred hypothesis and record supporting evidence, contradicting
evidence, alternative explanations, missing evidence, and confidence.
