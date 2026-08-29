# Work 029 Plan: Ten-Circuit Fixed-Topology Baseline Campaign

Status: Completed

Thai companion: `2026-08-29_029_ten-circuit-baseline-campaign-plan.th.md`

## Objective

Run at least one declared fixed-topology Level-0 reference family across all ten versioned circuit profiles under identical energy, component-opportunity, seed, evaluation-budget, architecture, and holdout controls, while keeping analytical proxy completion distinct from real-circuit physical evidence.

## Scope

- Define a strict, fingerprinted baseline campaign protocol.
- Pin one reference vehicle family, component library, strategy, energy profile, timestep, per-run step budget, design-evaluation opportunity, seed set, and calibration/holdout split.
- Execute the Work 028 eight-stage whole-race orchestrator for every circuit/seed pair.
- Use official profile race distance and lap length while declaring local corridor and weather inputs as analytical controls, not observations.
- Record per-run outcome, time, distance, energy, residual, replay, evidence grade, width screen, compute use, and partition.
- Aggregate circuit/family completion without selecting on holdout results.
- Prove protocol/catalog permutation invariance and reject unfair, overlapping, incomplete, or mutated controls.
- Record and resolve each discovered defect in a separate bilingual problem report.

## Planned Files

- `config/simulation/fixed_topology_baseline_protocol_v1.json`
- `src/formula_ultimate/simulation/baseline_campaign.py`
- `src/formula_ultimate/simulation/__init__.py`
- `src/formula_ultimate/simulation/step_inputs.py` if analytical-control evidence requires a typed contract correction
- `tests/test_baseline_campaign.py`
- related step-input regression tests if required
- `scripts/validate_baseline_campaign.py`
- `docs/simulation/TEN_CIRCUIT_BASELINE_CAMPAIGN.md`
- `docs/simulation/TEN_CIRCUIT_BASELINE_CAMPAIGN.th.md`
- Work 029 problem reports if required
- implementation queue, this plan, and matching bilingual result records

## Experiment Definition

- Independent variables: circuit profile and declared random seed.
- Dependent variables: finish status/time/distance, energy consumed, attempted/committed steps, residual pass count, replay fingerprint, width-screen status, and compute use.
- Controls: architecture/model versions, fixed topology, component library, strategy law, aerodynamic map, initial state/energy, timestep, maximum steps, design-evaluation budget, analytical environment policy, and partition assignment.
- Metrics: ten-profile completion, all-seed completion, finish residual, failed residual count, per-run step-budget compliance, control-identity equality, permutation invariance, and holdout isolation.
- Success criteria: all declared circuit/seed runs finish within one common budget; all residuals pass; controls remain identical; every profile appears exactly once in the calibration/holdout partition; replay is deterministic; proxy evidence is never labeled real-circuit admission.
- Failure criteria: a run uses extra energy/components/evaluations, a holdout changes the protocol, a missing profile is silently dropped, failed residuals are ignored, or analytical controls are presented as measured evidence.
- Falsification attempt: duplicate/overlapping/missing partitions, unknown circuits, zero/duplicate seeds, altered component opportunity, insufficient step budget, protocol/catalog permutation, and tampered evidence grade.

## Validation

1. Focused Work 023/028/029 tests.
2. Entire repository test suite.
3. Standalone Work 029 validator.
4. Python bytecode compilation.
5. `git diff --check` and `git diff --cached --check`.
6. Explicit staged-scope review before commit.

## Success Criteria

- At least one fixed-topology family completes all ten profile distances for all pinned seeds.
- Every run uses the same declared opportunity and compute/energy controls.
- Holdout assignment is immutable and not used to tune the reference.
- Results retain complete Work 028 provenance and deterministic fingerprints.
- Analytical proxy results remain ineligible for real-circuit or discovery claims.
- English and Thai documentation agree.
- Work 029 is committed as one validated commit.

## Risks

- Work 023 reports zero profiles with measured local spatial/weather evidence.
- Large official race distances can make the campaign expensive without a justified timestep/budget.
- Current weather status vocabulary may force synthetic controls to be mislabeled as observations.
- A frictionless or zero-energy reference would be a weak fairness baseline.
- Identical seed outcomes can be correct when all stochastic hazards are disabled; identity must still retain the seed.

## Explicit Non-goals

- No claim that proxy completion predicts real lap time or vehicle ranking.
- No topology optimization or autonomous candidate search.
- No use of holdout outcomes to change baseline configuration.
- No higher-fidelity CFD, FEA, surveyed 3D corridor, calibrated reliability, safety, or physical validation.
- No candidate promotion; Work 030 owns that gate.
