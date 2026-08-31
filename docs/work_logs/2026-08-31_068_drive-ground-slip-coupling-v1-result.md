# Work 068 Result: Drive-to-Ground Slip Coupling v1

Thai companion: `2026-08-31_068_drive-ground-slip-coupling-v1-result.th.md`

Status: Completed

## Outcome

Implemented a deterministic coupling from Work 067 powertrain output through Work 066 geometry-bound ground units to slip-limited longitudinal force and vehicle translation. The reference accelerated while satisfying geometry, inertia, contact, torque, interface-power, and global-energy gates. Zero-input controls produced no motion, and a drive-path failure propagated to subsystem failure and `DNF` with zero output drive torque.

## Files changed

- `src/formula_ultimate/simulation/drive_ground_coupling.py`
- exports in `src/formula_ultimate/simulation/__init__.py`
- `config/vehicle/functional_drive_ground_coupling_v1.json`
- `scripts/experiments/run_drive_ground_coupling.py`
- `tests/test_drive_ground_coupling.py`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.md`
- `docs/research/DRIVE_GROUND_SLIP_COUPLING_V1.th.md`
- this bilingual Work 068 plan/result set

Ignored evidence is `artifacts/work068/drive_ground_evidence.json`.

## Decisions

- Ground radius, axial inertia, mass, and contact limits are checked against Work 066 rather than re-entered without provenance.
- Geometry-derived ground inertia plus explicit other reflected inertia closes the Work 067 output inertia, preventing double counting.
- Positive slip uses a bounded synthetic `tanh` law; nonpositive slip requests zero drive force because regeneration is outside v1.
- Work 067 useful work is replaced in the global ledger by vehicle kinetic energy, aerodynamic/rolling work, and slip heat.
- Powertrain terminal failure immediately becomes drive subsystem `failed` and race outcome `DNF`.

## Exact validation commands and evidence

```powershell
py -3.14 -m unittest tests.test_drive_ground_coupling -v
```

Exit status `0`; `Ran 8 tests ... OK`.

```powershell
py -3.14 scripts/experiments/run_drive_ground_coupling.py --config config/vehicle/functional_drive_ground_coupling_v1.json --vehicle-root config/vehicle --output artifacts/work068/drive_ground_evidence.json
```

Exit status `0`; status `passed`; evidence SHA-256 `747d7ab1fbc7b73093151cf685e444160aa55fade6c385e1a5fb5c1f8c4d1b0f`; reference SHA-256 `b7311a924e74bc412c611f261e11928745dec381f093c13085814b05624a3070`; final speed/distance `14.399690385591617 m/s` and `16.45505131092282 m`; maximum contact utilization `0.8831466159464643`; maximum global relative energy residual `1.0215881764888763e-08`; maximum refinement difference `4.969084181339372e-05`; deliberate failure outcome `DNF`, reason `shaft_connection_failure`.

Reference energy evidence: source used `65239.388932965 J`; vehicle kinetic `28257.0273591386 J`; slip heat `1791.64460139612 J`; aerodynamic work `984.746997658385 J`; rolling work `659.722558888986 J`; maximum ground force `2832.59764718983 N`; maximum torque residual `0 N m`; maximum interface residual `1.81721304670646e-12 J`; maximum global residual `0.510794088244438 J`.

```powershell
py -3.14 -m unittest discover -s tests -q
py -3.14 -m compileall -q src scripts tests
git diff --check
```

Exit statuses `0`; full regression `Ran 404 tests ... OK`; compilation and diff checks emitted no errors.

## Falsification, limitations, and follow-up

Zero throttle and zero energy produced zero motion. High positive slip remained below contact capacity. Negative slip produced no undeclared regeneration. A reduced shaft limit caused `DNF` at `0.002 s`; the terminal output drive torque was `0 N m`. Invalid radius, axial inertia, force/normal-load limits, inertia closure, tolerance, and non-finite friction failed closed.

No contradiction occurred inside the declared model. The slip curve, friction, normal loads, drag, and rolling values remain synthetic. Common wheel speed, static loads, straight-line translation, and explicit fixed steps cannot validate a differential, suspension, steering, real tyre, lap time, or safety.

Work 069 should implement dynamic normal-load transfer and independent left/right wheel states, then couple steering and combined slip for planar motion while retaining exact energy/failure evidence.
