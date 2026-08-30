# Work 043 Plan: Fracture-Initiation Evidence

Status: Completed

Thai companion: `2026-08-30_043_fracture-initiation-evidence-plan.th.md`

## Objective

Implement and validate a deterministic fracture-initiation evaluator that turns an explicit crack, nominal load, material toughness, thickness regime, and material state into an observable initiation event without treating a singular finite-element peak stress or arbitrary element deletion as physical proof.

## Scope and claim boundary

- Use the ideal infinite-plate center-crack LEFM fixture `K_I=sigma*sqrt(pi*a)` with declared half-crack length `a`, gross nominal stress, and `Y=1`.
- Require a finite-width approximation-domain declaration, plane-strain thickness check `B>=2.5(K_IC/sigma_y)^2`, and small-scale-yielding check before admitting a result.
- Use a synthetic toughness/material record with explicit prohibition from design fitness; Work 042 supplies only the yield-state contract, not toughness.
- Evaluate crack-length cases, load levels bracketing initiation, deterministic event localization, exact reaction and work ledger controls, and representation-refinement invariance.

This work validates analytical LEFM initiation arithmetic and evidence contracts only. It does not validate crack-tip FEA, stable/unstable propagation, crack path, fracture-energy dissipation, real material toughness, crashworthiness, or element deletion.

## Experiment design

- independent variables: crack half-length, nominal tensile load, representation resolution, toughness, thickness regime, and declared geometry-factor domain;
- dependent variables: `K_I`, utilization, initiation load, event identity/load fraction, reaction residual, work residual, domain margins, and replay hash;
- controls: geometry convention, gross stress area, `Y=1`, material state, load sequence, SI units, and no crack healing;
- preferred hypothesis: the evaluator reproduces the closed-form initiation load within `5%`, representation last-two change is `<=5%`, ledgers close, and every invalid-domain fixture fails closed;
- falsification: include below/at/above initiation loads, too-thin, excessive finite-width ratio, missing provenance, missing flaw, and yielding-before-fracture controls.

## Planned implementation and files

- `config/structural/fracture_initiation_acceptance_v1.json`;
- immutable fracture record, cracked-coupon grammar, domain validator, evaluator, and event contract;
- Work 043 deterministic runner/launcher and ignored evidence under `artifacts/work043/`;
- focused analytical, identity, replay, and invalid-domain tests;
- bilingual report and matching result records.

## Validation and success criteria

- initiation-load error `<=5%` in the admitted LEFM domain;
- last-two representation change `<=5%` for `K_I`, not raw peak stress;
- reaction residual `<=1e-5`, work-ledger residual `<=1e-4`, and deterministic first-crossing identity;
- exact rejection for missing crack/toughness/provenance/thickness regime and for material yield preceding the claimed LEFM initiation;
- focused/full tests, compile/static checks, staged-diff check, explicit commit, and clean-tree replay pass.

## Risks and explicit non-goals

The infinite-plate fixture is intentionally narrow and will reject finite-width or nonlinear material states outside its preregistered domain. Current CalculiX evidence has no independently validated fracture contour-integral route, so no solver crack-tip field is claimed. No propagation, cohesive zone, XFEM, fatigue crack growth, physical coupon, vehicle component, push, or publication is included.
