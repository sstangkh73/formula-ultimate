# Work 103 Plan: Correct Benchmark Equations and Balance Evidence

Thai companion: `2026-09-05_103_correct-benchmark-equations-plan.th.md`

Status: Completed

## Objective and scope

Correct the Work 102 findings in the generalized geometry benchmark: constructed-zero residuals, unconditional convergence, Hertz energy and inconsistent effective modulus/radius between indentation and contact stress. Starting revision: `1b6e93c`. Do not retune loads or thresholds to make corrected results pass.

Compute scalar constitutive residuals using stiffness/compliance defined before the response. Distinguish these from unavailable 3D field force/moment/energy balance with nulls and explicit status. Hertz uses E* = E/[2(1-nu^2)], one effective radius, F = K*delta^(3/2), and U = (2/5)*K*delta^(5/2) under quasistatic loading. Disclose equal-material and radius-proxy assumptions; do not claim STEP-derived contact solving.

## Planned files

- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` and `.th.md`
- Bilingual Work 103 plans/results; new outputs under `artifacts/work103/` (artifacts not committed)

## Validation and success criteria

Test independently calculated Hertz values, integrated force energy and dU/ddelta = F, load/material scaling, perturbed responses producing nonzero residuals, exhausted Newton budget/invalid domains, and rejection of forged/incomplete evidence. Run `python -m unittest tests.test_generalized_geometry_benchmarks -v`, the runner into run_a and replay run_b, and `python -m unittest discover -s tests -q`. Check bilingual companions, staged scope and `git diff --cached --check`, then commit only this work.

Independent variables: equation implementation, refinement/iterations and perturbations. Dependent variables: response, residual, energy, contact pressure, convergence/failure and replay identity. Controls: unchanged config, material, geometry and loads. Success requires passing regressions, agreement with independent equations and replay. Failure includes accepting incorrect responses or hidden repair. If corrected physics rejects an old baseline, report it without changing the load.

## Risks and non-goals

Results/identities may change and cannot replay against historical Work 097. Add evaluator versioning and preserve historical evidence. No general FEM, whole-vehicle repair or physical-validation promotion from scalar checks. Independent meshing/reaction extraction remains separate follow-up work.
