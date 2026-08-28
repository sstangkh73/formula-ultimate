# Work 025 Plan: Contact, Suspension, Brake, and Regeneration Coupling

Status: Completed

Thai companion: `2026-08-28_025_contact-suspension-brake-coupling-plan.th.md`

## Objective

Resolve each arbitrary ground contact from Work 024 normal load through explicit
drive/brake allocation, suspension travel, mechanical braking, regeneration,
and the combined tyre ellipse. Preserve requested, applied, unserved, heat, and
energy values without hidden redistribution.

## Scope

- Define topology-neutral contact coupling specs and exact allocation weights.
- Reject contact-ID mismatch, duplicate/missing states, negative wheel speed,
  conflicting throttle/brake, and allocation sums that do not close.
- Evaluate the existing Work 018 suspension/brake/regen model per contact.
- Limit regen by the central recovery request before mechanical allocation.
- Resolve combined longitudinal/lateral tyre capacity per contact.
- Emit typed `contact.force_moment`, `contact.energy_transfers`, and
  `contact.health_inputs` with raw residuals and failure evidence.
- Prove arbitrary three/four-contact behavior, saturation, zero recovery,
  storage/power limits, replay, no redistribution, and adapter failure.
- Add tests, validator, bilingual docs/result, bug reports, validation, commit.

## Experiment definition

- Hypothesis: explicit per-contact allocation plus independent capacity models
  can close torque/energy accounting without reallocating unmet demand.
- Independent variables: topology, loads, commands, wheel speeds, subsystem
  states/parameters, allocation weights, recovery fraction, and tyre capacity.
- Dependent variables: contact forces/moments, travel/failure, recovered energy,
  heat/loss, unserved demand, saturation, residuals, and adapter status.
- Controls: Work 011 tyre ellipse, Work 018 suspension/brake model, Work 024
  contact loads, one immutable start state, exact signal contract.
- Success: per-contact and summed evidence closes; missing demand remains
  unserved; three-contact topology passes; injected invalidity produces no writes.
- Failure: hidden redistribution, double-counted braking/regen, load mismatch,
  lost failure event, residual correction, topology prescription, or commit fail.

## Risks and non-goals

This Level-0 adapter uses declared control allocations and configured subsystem
state; it is not an optimal controller or calibrated tyre/suspension. Work 026
owns motion integration. No whole race, optimizer, physical validation, README
change, or remote push is included.

## Validation

```powershell
python -m unittest tests.test_contact_coupling -v
python -m unittest discover -s tests -v
python scripts/validate_contact_coupling.py
python -m compileall -q src scripts tests
git diff --check
git diff --cached --check
```
