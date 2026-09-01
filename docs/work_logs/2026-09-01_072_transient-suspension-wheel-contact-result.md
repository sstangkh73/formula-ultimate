# Work 072 Result: Transient Suspension, Wheel Load, and Contact Coupling

Status: Completed

Thai companion: `2026-09-01_072_transient-suspension-wheel-contact-result.th.md`

## Outcome

Work 071 now accepts an optional deterministic normal-load transform without changing its untransformed result. Work 072 uses that hook to solve one geometry-identified spring/damper/effective-mass state per contact inside the acceleration/load-transfer fixed point. Actual transient load drives tyre capacity; target load, travel, velocity, boundary work, damper heat, residuals, contact loss, and travel failure remain explicit.

The reference and controls passed the declared Level-0 gates. This is coupled software feasibility evidence, not physical validation or race readiness.

## Files changed

- `config/vehicle/transient_suspension_coupling_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/transient_suspension_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_transient_suspension_coupling.py`
- `tests/test_transient_suspension_coupling.py`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.md`
- `docs/research/TRANSIENT_SUSPENSION_WHEEL_CONTACT_V1.th.md`
- this bilingual Work 072 plan/result record set

Ignored deterministic evidence was regenerated under `artifacts/work072/`.

## Decisions and implementation evidence

- Preserved the Work 069 v3 materialized architecture SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`.
- Derived per-contact effective mass from each ground component: powered contacts `13.30024665823775 kg`; passive rear support `4.342937684322531 kg`.
- Used an implicit-midpoint oscillator and passed actual midpoint spring/damper load into the Work 071 tyre calculation within the same fixed point.
- Kept boundary work from omitted sprung-body vertical modes explicit instead of assigning it silently to the drivetrain.
- Deducted initial suspension perturbation energy from storage, preserving the `50,000,000 J` initial budget.
- Treated actual load `<= 0 N` as uncommitted terminal `contact_loss`; retained over-travel as committed boundary-step `suspension_travel`. No load or travel clipping is used.
- Preserved the untransformed Work 071 result SHA-256 `f8f3d888b23a9e21b7bb9ad8b7153ecd5bd4752c7937ebf8cc42a952b64c9cdd`.

## Experiment result

Reference command: steering `+0.01 rad`, throttle `0.3`, duration `0.5 s`, `dt = 0.001 s`.

- Status/outcome: `passed/finished`, 500 steps.
- Final position: `(5.369677667803904, 0.13391224133502547) m`.
- Final yaw rate: `0.3637589747733689 rad/s`.
- Actual load range: `282.92044294869817` to `1597.6137536723597 N`.
- Maximum target/actual load difference: `96.89914047704144 N`.
- Maximum travel/vertical speed: `0.011753827694854656 m`, `0.19365997408307992 m/s`.
- Boundary work/damper heat: `4.606168739325264 J`, `0.9238099457339569 J`.
- Maximum force residual: `3.979039320256561e-13 N`.
- Maximum suspension-energy residual: `8.296586074402201e-16 J`.
- Maximum total global relative energy residual: `5.010984838008881e-9`.
- Maximum half-step relative difference: `0.008650825751444935`, below `0.02`.

Zero steer remained exactly symmetric. Opposite steer exchanged left/right vertical states and mirrored selected planar/yaw states with zero mismatch. Zero damping produced exactly zero damper heat. Half stiffness increased maximum travel to `0.02332339540361481 m`.

The contact-loss control preserved `-329.1330469175954 N` and returned `DNF: contact_loss` on attempted step 1 without committing the transaction. The travel control preserved `0.05068991458357319 m` and returned `DNF: suspension_travel` after step 2. Both retained the exact `50,000,000 J` initial total.

Primary and replay evidence files were byte-identical. File SHA-256: `E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719`. Canonical evidence payload SHA-256: `25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b`.

## Validation record

```text
python -m unittest tests.test_transient_suspension_coupling -v
Exit: 0
Ran 11 tests in 19.231s — OK

python scripts/experiments/run_transient_suspension_coupling.py --config config/vehicle/transient_suspension_coupling_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work072/materialized_architecture_v3.json --output artifacts/work072/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=25b269082eb921efc54c334c6dc3d9623bcb7d6fa91beb9d2ea9b4083270b97b

python scripts/experiments/run_transient_suspension_coupling.py --config config/vehicle/transient_suspension_coupling_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work072/replay/materialized_architecture_v3.json --output artifacts/work072/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = E48CA5034D8361C5E45AAF2D88BA5FC1349015AAD4144345CB5CBFD2AE66B719

python -m unittest discover -s tests -v
Exit: 0
Ran 442 tests in 84.210s — OK

python -m compileall -q src scripts/experiments/run_transient_suspension_coupling.py tests/test_transient_suspension_coupling.py
Exit: 0

python -m unittest tests.test_transient_suspension_coupling tests.test_coupled_planar_differential -q
Exit: 0
Ran 21 tests in 40.284s — OK
```

The final bilingual repository contract, staged-diff check, commit, and post-commit replay are reported in the final handoff after execution.

## Limitations and follow-up

This model omits sprung-body heave/pitch/roll inertia, tyre vertical compliance, road displacement, linkage geometry, motion ratio, roll centres, anti-dive/squat, bump stops, hysteresis, measured coefficients, aero load, and exact sub-step event localization. Geometry supplies identity and component mass but does not yet supply spring/damper behaviour. Internal energy closure does not demonstrate real-world predictive accuracy.

The next work should resolve sprung-body vertical modes and road/tyre compliance before, or as a prerequisite to, the closed-loop path and circuit gate.
