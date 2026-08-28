# Work 027 Result: Central Energy and Health Coupling

Status: Completed

Thai companion: `2026-08-29_027_central-energy-health-coupling-result.th.md`

## Outcome

Implemented central propulsion/recovery energy accounting, independent audits, component thermal/degradation/damage updates, deterministic reliability streams, persistent contact state, and earliest-event localization.

## Files Changed

- Added architecture v3, central energy/health source, 12 focused tests, validator, and bilingual model records.
- Extended shared contact state and Work 025 energy/event contracts.
- Added six bilingual problem reports covering every defect found during Work 027.

## Resolved Problems

1. Missing drive-wheel energy transfer.
2. Non-persistent contact subsystem state.
3. Peer contacts not truncated at the earliest contact failure.
4. Missing energy/motion inputs to health stage.
5. Hidden `300 K` thermal ambient default.
6. Validator assumption that every different seed must change the winning event time.

## Decisions

- Preserve architecture v1/v2 and add v3.
- Use recovered energy before primary energy and reject capacity overflow.
- Audit drive, auxiliary, and recovery boundaries independently.
- Keep brake heat in the contact model to prevent double counting.
- Derive component reliability streams from seed, step index, and component ID.
- Retain start contact state on an earlier central terminal event rather than fabricate interpolation.

## Validation Commands and Evidence

All commands returned exit status `0`:

```powershell
$env:PYTHONPATH='src'
python -m unittest tests.test_contact_coupling tests.test_energy_health_coupling
python -m unittest discover -s tests
python scripts/validate_energy_health_coupling.py
python -m compileall -q src scripts tests
git diff --check
```

- focused Work 025/027 regression: 24 passed in `0.015 s`;
- full repository suite: 232 passed in `0.622 s`;
- validator exit `0`;
- architecture fingerprint: `a3782a246e27997984ece4afc1c2f7b0924d8b9e67e602bb46889399ba565a38`;
- drive/aux primary state: `2000 J -> 900 J` with all residuals passed;
- recovery boundary: `1000 = 700 + 100 + 200 J`, residual `0 J`;
- depletion time: `0.5 s`, end primary `0 J`;
- thermal winner: `0.2 s`, `302 K`, localized `x = 2 m`;
- same-seed replay exact and different seed changes reliability draw.

## Limitations

Level-0 only. No calibrated reliability, CFD cooling, battery chemistry, material fatigue, full 3D contact constraints, or physical validation. Work 028 must supply explicit environment/configuration and stop terminal states.

## Follow-up

Work 028 will implement the deterministic whole-race coupled transaction loop, final race-progress merge, terminal outcomes, and replay/provenance telemetry.
