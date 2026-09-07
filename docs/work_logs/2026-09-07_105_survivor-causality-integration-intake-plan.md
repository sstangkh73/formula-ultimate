# Work 105 Plan: Survivor Causality and Whole-Vehicle Integration Intake V1

Thai companion: `2026-09-07_105_survivor-causality-integration-intake-plan.th.md`

Date: 2026-09-07 (Asia/Bangkok)

Status: Completed

## Objective and milestone boundary

Advance the roadmap's Work 101 program milestone with its first bounded implementation phase. Work 100 produced ten scoped axial/thermal subsystem survivors, but graph-only and joint candidates differed from the fixed topology mainly through a branch carrying essentially zero source-to-sink flow. Work 105 will distinguish declared graph diversity from task-relevant functional causality, admit only typed subsystem evidence into a whole-vehicle intake registry, and fail closed when required vehicle functions or stronger promotion evidence are absent.

This work item will not assemble or claim a complete vehicle. The roadmap Work 101 exit condition remains unmet unless a later complete candidate supplies every required functional domain, causal path, geometry/material applicability, transient/energy/contact/failure evidence, holdout, independent higher fidelity, safety and fair optimized-baseline comparison.

## Scope and planned files

- `src/formula_ultimate/experiments/integration_intake.py`: strict intake config/result validation; aggregate mechanical/thermal edge flow; prune inactive branches; derive active-path identities; compare paired candidates with the fixed control; preserve survivor evidence while classifying functional-mechanism, shape-response and inactive-topology cases; compute technology-neutral vehicle capability coverage and blockers.
- `config/experiments/work101_integration_intake_v1.json`: frozen Work 100 registration/result identities, flow/activity tolerances, meaningful-effect threshold, capability vocabulary, evidence requirements and claim boundary.
- `scripts/experiments/run_integration_intake.py`: read the ignored Work 100 admitted result, verify identities, emit deterministic intake evidence, reject overwrite and support exact replay.
- `tests/test_integration_intake.py`: tests for nonzero-flow aggregation, dangling-branch pruning, paired fixed comparison, tampering, incomplete capability coverage, missing stronger evidence, false whole-vehicle admission and deterministic replay.
- `docs/contracts/WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.md` and `.th.md`: definitions, decision rules, evidence result and limitations.
- This bilingual plan and the matching bilingual result. Generated reports remain ignored under `artifacts/work105/`.

## Variables, controls and falsification

- Independent evidence: treatment and paired seed from Work 100; declared versus active edge topology; candidate capability declarations; availability of survivor, independent, safety, transient, energy, contact, failure, holdout and optimized-baseline evidence.
- Dependent evidence: edge flow fractions, active mechanical/thermal/coupled edge sets, active-path identity, response difference from paired fixed control, mechanism classification, capability coverage, missing evidence classes, integration status and Work 101 milestone readiness.
- Controls: exact Work 100 V2 registration/deterministic identities, no mutation of source candidates, same registered load/heat tasks, fixed activity tolerance, fixed minimum meaningful effect, existing technology-neutral `REQUIRED_CAPABILITIES`, no holdout feedback and deterministic ordering.
- Preferred hypothesis: at least one Work 100 survivor contains a task-relevant active-path change and can enter whole-vehicle integration as a supported typed subsystem.
- Competing explanations: apparent novelty is a zero-flow appendage, identifier-only graph change, continuous-radius response variation below the meaningful-effect threshold, numerical noise, or incomplete vehicle capability/evidence coverage.
- Falsification: inject a high-flow added edge and require the active identity to change; inject only a zero-flow branch and require pruning; alter source identity and require rejection; remove a required capability/evidence class and require integration to remain blocked; never turn a subsystem survivor into `promotion_ready` or whole-vehicle admission.

## Frozen decision rules

An original edge is active in a domain only when its maximum absolute segment flow divided by the registered applied input exceeds the frozen relative activity tolerance. A coupled active edge must be active in both mechanical and thermal fields. Active-path identity excludes refinement node labels and zero-flow appendages. A graph-diverse survivor is a functional-mechanism candidate only if its active coupled topology differs from its paired fixed control and its registered response difference exceeds the frozen meaningful-effect threshold. Same-active-topology geometry with a measurable but sub-threshold response remains a shape-response variant, not a new mechanism.

Whole-vehicle intake uses functional capabilities rather than prescribed component names or vehicle layouts. The Work 100 subsystem may contribute only `load_structure`; axial conduction does not by itself prove `heat_rejection`. Missing energy storage/conversion/transmission, ground propulsion, direction control, braking, heat rejection and controller capabilities block assembly. Missing independent, safety, transient, energy, contact, failure and optimized-baseline evidence also blocks stronger promotion even when local survivor gates passed.

## Validation and success criteria

1. Run focused unit tests for causality, identity, tamper rejection, coverage and replay.
2. Execute Work 105 reports A and B from the exact Work 100 V2 admitted result; require byte-identical deterministic evidence.
3. Run targeted regressions for Works 098-100, functional vehicle architecture and integration/promotion contracts.
4. Run `python -m compileall -q src scripts tests` and the full repository suite.
5. Validate bilingual companions, Markdown links, JSON/config identities, `git diff --check`, exact staged scope and `git diff --cached --check`.

Work 105 succeeds when the gate makes the Work 100 causal distinction and integration blockers explicit, replayable and fail-closed. A negative intake result is expected and valid if the evidence shows no active-topology mechanism or complete capability set. It must not weaken thresholds to manufacture an integration-ready candidate.

## Risks and non-goals

Risks are treating tiny floating-point flow as function, confusing geometry response with mechanism novelty, prescribing conventional hardware through capability labels, reusing a local artifact without identity checks, or calling a coverage audit whole-vehicle physics. Controls are relative flow thresholds, paired fixed controls, technology-neutral functional roles, content-addressed input evidence and explicit missing-evidence output.

Non-goals: new CAD generation, candidate mutation, whole-vehicle assembly, transient lap execution, FEA/contact/CFD, material/process certification, performance optimization, baseline superiority, prior-art novelty, `promotion_ready`, complete-vehicle research admission, physical validation, external publication or push.
