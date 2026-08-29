# Integration Falsification and Promotion Gate

Status: Work 030 Level-0 release review

Thai companion: `INTEGRATION_FALSIFICATION_PROMOTION_GATE.th.md`

## Purpose

Work 030 closes the coupled implementation queue by separating three questions:

1. Does the transaction reject deliberate integration defects?
2. Is the analytical reference stable under the declared timestep refinement?
3. Is there enough independent evidence to promote a candidate beyond Level 0?

The answers for the current repository are **yes**, **yes within a narrow steady analytical control**, and **no**. The release status is therefore `level0_experimentation_ready_promotion_blocked`.

## Gate Protocol

`config/simulation/integration_promotion_gate_v1.json` fingerprints:

- six required fault cases and expected failure codes;
- refinement timesteps `(2000, 1000, 500) s`, seed `17`, common `128`-step budget, and tolerances;
- minimum ten-profile completion;
- required real-circuit admission;
- independent evidence at `level1` or higher;
- six required cross-model evidence types; and
- `automatic_discovery_claim = false`.

Unknown fields, implicit budget types, duplicate requirements, unsupported fidelity levels, and automatic discovery are rejected.

## Deliberate Fault Matrix

The control transaction commits. Every injected defect returns an invalid transaction and no committed state:

| Fault | Expected/observed code | Rollback |
|---|---|---|
| adapter omitted | `adapter_coverage` | yes |
| model version corrupted | `adapter_version_mismatch` | yes |
| residual identity duplicated | `evidence_identity_duplicate` | yes |
| numerical residual forced to fail | `residual_failure` | yes |
| undeclared output emitted | `adapter_exception` | yes |
| next-state time regressed | `time_regression` | yes |

These synthetic adapters isolate the atomic transaction enforcement. Earlier Work 023-029 domain fixtures separately exercise the physical adapters, invalid corridors, energy depletion, thermal failure, missing evidence, and budget exhaustion.

## Baseline Evidence Identity v2

Promotion cannot trust a visible field and an unrelated stale hash. Work 030 therefore upgrades the campaign evidence model to `work029-baseline-campaign-v2`:

- every run field except its fingerprint field is hashed;
- every campaign result field except its fingerprint field is hashed;
- run and aggregate counts/flags are recomputed;
- run protocol/control/architecture identities must match the campaign; and
- top-level real-circuit admission must agree with every run.

The validated v2 campaign result fingerprint is `79a03587e6bbeb17101c89a59c7fe61053571f493a29fbe356322418726d2a9b`.

## Timestep Refinement

One calibration and one holdout profile run at all three timesteps under seed `17` and a common `128`-step maximum. Six samples finish with all residuals passed.

- maximum relative finish-time variation: `0.0`;
- maximum relative primary-energy variation: `1.5466148595436325e-14`;
- maximum absolute finish-distance residual: `0.0 m`;
- attempted steps per profile: `16`, `31`, and `62`.

The energy variation is floating-point scale. Nevertheless, `convergence_order_estimated = false`: a steady drag-balanced analytical solution cannot establish convergence order, nonlinear circuit behavior, quantified model uncertainty, or higher-fidelity agreement.

## Cross-Model Promotion Requirements

Promotion requires independent passing evidence at `level1` or higher for:

1. `geometry-mass-inertia`
2. `surveyed-circuit-corridor`
3. `cross-model-aerodynamics`
4. `structural-safety`
5. `thermal-reliability`
6. `quantified-uncertainty`

The current candidate provides none of these and has no real-circuit admission. Its promotion status is `blocked` with all seven reasons retained. A test-only complete evidence fixture under a relaxed real-admission requirement reaches only `eligible_for_independent_review`; discovery and automatic promotion remain false.

## Release Decision

The repository is ready for **gated Level-0 experimentation** because:

- the 30-run/ten-profile baseline finishes within controls;
- campaign identities and aggregates verify;
- all six transaction faults fail closed; and
- the bounded timestep sensitivity gate passes.

The following claims remain forbidden:

- real-circuit performance or lap time;
- discovery or technological superiority;
- physical validation;
- safety; and
- manufacturability.

Level-0 autonomous candidate generation may now use these contracts as an early selection environment, but every candidate must remain behind the same fair-compute, evidence-identity, falsification, refinement, and cross-model gates.

## Evidence Fingerprints

- gate: `ad629075e69001b17eaf8b8e9371ecb72fc52a4e07a762c4546096daf9d23814`;
- falsification suite: `a6c0b5a1a30abda519ed230114ca5c49b5754bb2bd763e505ae0f2f77ec15f4b`;
- refinement: `fdb02195f1a77709b9f43f5d1b1d86736f73e0862dbb9d605f56017a28462af2`;
- blocked promotion decision: `bf78fcb402c43e633399342d3e93a3473d3f2c4defa2e1447163bc34d059400f`;
- release review: `783e156bb2a8d8dcad356033b6767fb2b2cbef9b9f0f3d1f94df13a83ab94f29`.

## Remaining Research Work

Completing Work 030 closes the software implementation queue, not the research program. The next research phase must acquire or derive geometry-linked physical evidence, measured circuit corridors/conditions, calibrated or independent models, uncertainty bounds, and physical testing. Those are evidence prerequisites rather than conventional design prescriptions; the vehicle architecture search remains open-ended.
