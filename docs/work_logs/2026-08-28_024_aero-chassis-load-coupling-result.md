# Work 024 Result: Aerodynamic Chassis and Normal-Load Coupling

Status: Completed

Thai companion: `2026-08-28_024_aero-chassis-load-coupling-result.th.md`

## Outcome

Work 024 now turns typed weather/motion into a Work 017 aerodynamic result,
translates force/moment and cooling evidence to the chassis centre of mass, and
balances normal loads over arbitrary contact topology. Both architecture
adapters emit exact declared signals and fail closed on invalid map/load states.

## Files and decisions

- Added `aero_load_coupling.py`, exports, 10 focused tests, validator, and
  bilingual model/plan/result documentation.
- Updated Work 023 weather contract and validator to require `local_enu` wind.
- Used body axes `x` forward, `y` left, `z` up and `M_com=M_map+r x F`.
- Generalized vertical/pitch/roll equilibrium without clipping negative loads.
- Retained raw residuals and observable numerical node-snap evidence.
- Preserved topology neutrality; analytical three-contact and four-contact cases
  pass.

## Problems resolved

Separate bilingual reports cover missing wind coordinate frame, exact-node
roundoff after ENU rotation, and an imbalanced rounded three-contact fixture.
All were corrected before completion.

## Validation

```powershell
python -m unittest tests.test_aero_load_coupling -v
# exit 0; Ran 10 tests in 0.003s; OK
python -m unittest discover -s tests -v
# exit 0; Ran 196 tests in 1.607s; OK
python scripts/validate_aero_load_coupling.py
# exit 0; drag -525.9915 N; downforce -1051.9830 N
# front 2978.4915 N each; rear 2452.5 N each
# residuals passed; outside map invalid with 0 writes
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
```

## Review and limitations

Evidence supports signs, moment translation, load shift, conservation closure,
replay, topology neutrality, and invalid boundaries. Synthetic map/weather remain
an alternative explanation for clean results; no real aero accuracy is claimed.
Acceleration feedback, contact force, suspension/brake, and motion remain
missing. Work 025 is next. No push was performed.
