# Work 025 Result: Contact, Suspension, Brake, and Regeneration Coupling

Status: Completed

Thai companion: `2026-08-28_025_contact-suspension-brake-coupling-result.th.md`

## Outcome

Work 025 couples arbitrary contact loads to explicit drive/brake allocation,
suspension, mechanical braking, regeneration, combined tyre capacity, body force
and yaw moment. Requested/applied/unserved values, energy, heat, travel, failure,
and residuals remain per-contact and are never redistributed silently.

## Files and decisions

- Added `contact_coupling.py`, public exports, 11 focused tests, validator, and
  bilingual model/plan/result documentation.
- Allocation fractions must close independently for drive and brake.
- Central recovery fraction caps regen before mechanical allocation.
- Combined brake/steer saturation uses a two-pass subsystem evaluation so
  thermal and energy evidence matches road-transmitted torque.
- Physical contact failure is retained as health evidence; malformed or
  conservation-invalid input atomically emits zero signals.
- Three/four-contact layouts pass without prescribed axle topology.

## Problem resolved

The initial implementation overcounted brake/regen energy after the combined
tyre ellipse reduced longitudinal force. The separate bilingual report records
the defect and two-pass correction. A regression now closes applied force,
torque, angular speed, duration, and wheel energy per contact.

## Validation

```powershell
python -m unittest tests.test_contact_coupling -v
# exit 0; Ran 11 tests in 0.005s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 207 tests in 0.368s; OK
python scripts/validate_contact_coupling.py
# exit 0; 3 contacts; replay equal; 9 residuals passed
# requested drive 3000 N; applied 2100 N; front unserved 900 N
# brake wheel energy 85.3178 J; recovered 68.2542 J
# per-contact energy/force consistency true; redistribution false
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review and limitations

Evidence supports explicit allocation, saturation, no redistribution, energy
closure, failure retention, replay, and topology neutrality. Results still use
reduced-order tyre/suspension/brake fixtures, not calibration. Subsystem state is
not centrally committed and summed force has not advanced motion. Work 026 owns
that integration. No push was performed.
