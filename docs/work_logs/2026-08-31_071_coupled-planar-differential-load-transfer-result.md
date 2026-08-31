# Work 071 Result: Coupled Planar Differential and Per-Step Load Transfer

Status: Completed

Thai companion: `2026-08-31_071_coupled-planar-differential-load-transfer-result.th.md`

## Outcome

The Work 069 three-contact planar vehicle and Work 070 independent-wheel differential now execute in one deterministic Level-0 loop. Each admitted step couples normal-load redistribution, longitudinal slip, lateral slip angle, combined tyre-force projection, powertrain load, differential modal motion, body translation, yaw, work, heat, and global energy. The reference and controls passed their declared gates; deliberate excessive steering terminated as an observable `contact_lift` DNF.

This is software-level coupled feasibility evidence only. It is not physical validation or race readiness.

## Files changed

- `config/vehicle/coupled_planar_differential_v1.json`
- `src/formula_ultimate/simulation/coupled_planar_differential.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_coupled_planar_differential.py`
- `tests/test_coupled_planar_differential.py`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.md`
- `docs/research/COUPLED_PLANAR_DIFFERENTIAL_LOAD_TRANSFER_V1.th.md`
- this bilingual plan/result record set

Ignored deterministic evidence was regenerated under `artifacts/work071/`.

## Decisions and implementation evidence

- Kept the Work 069 v3 materialized geometry unchanged with SHA-256 `cf78a1c499790aed6c8b117c8f583a427a9d91a9fb36605e2b7038b2907b1418`.
- Used both front contacts as powered/steered branches and kept the rear support passive for propulsion.
- Solved acceleration-dependent quasi-static normal loads inside each step's fixed-point loop. Negative load remains visible and terminal; no clipping is allowed.
- Projected requested longitudinal and lateral forces together through the contact friction ellipse and retained saturation/unserved demand.
- Used midpoint-consistent body and differential integration so Coriolis exchange and modal damping close in the energy ledger.
- Matched initial wheel/carrier/converter speeds to `10 m/s`. Body and rotating kinetic energy are deducted from storage, making total initial accounted energy exactly `50,000,000 J` rather than creating hidden initial energy.
- Kept convergence failure, non-finite state, contact lift, limit failure, and energy failure explicit and fail closed.

## Experiment result

Reference command: steer `+0.01 rad`, throttle `0.3`, duration `0.5 s`, `dt = 0.001 s`.

- Status/outcome: `passed/finished`, 500 steps.
- Final position: `(5.370504659073167, 0.1338516705920943) m`.
- Final heading/yaw rate: `0.09777375911939074 rad`, `0.3638034159613838 rad/s`.
- Final branch speeds: left `95.16937580718059 rad/s`, right `83.57249258481846 rad/s`.
- Minimum normal load: `282.9427858151486 N`.
- Maximum combined contact utilization: `1.0000000000000002`.
- Saturated steps: `302`.
- Maximum absolute load-balance residual: `4.547473508864641e-13`.
- Maximum body-energy residual: `1.4557244298885053e-11 J`.
- Maximum global-energy residual: `0.25046080350875854 J`; relative `5.009216070175171e-9`.
- Maximum half-step relative difference: `0.002683761648435663`, below `0.02`.

Zero steer preserved exact straight-line symmetry. Opposite steering and the split-grip/spatial-mirror controls recorded zero selected mirror mismatch. The excessive `+0.04 rad` control reached minimum load `-0.14156334912604507 N` at attempted step 443 and terminated at `0.442 s` with `DNF: contact_lift`.

Primary and replay evidence files were byte-identical. File SHA-256: `3D9BF89250E57EC818B785797F3854F4A729BDBAEEBEB8313DD31EE5A2726359`. Canonical evidence payload SHA-256: `935eaec117ab5835e7af8b47cf50f63ec79cfa30e0d57cccad79b5ba1629a6ba`.

## Validation record

An initial `python -m pytest tests/test_coupled_planar_differential.py -q` environment probe exited `1` because the system Python has no `pytest`; the repository's declared `unittest` runner was then used. This was a runner-selection issue, not a failed physics assertion.

```text
python -m unittest tests.test_coupled_planar_differential -v
Exit: 0
Ran 10 tests in 13.528s — OK

python scripts/experiments/run_coupled_planar_differential.py --config config/vehicle/coupled_planar_differential_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work071/materialized_architecture_v3.json --output artifacts/work071/experiment_evidence.json
Exit: 0
status=passed; evidence_sha256=935eaec117ab5835e7af8b47cf50f63ec79cfa30e0d57cccad79b5ba1629a6ba

python scripts/experiments/run_coupled_planar_differential.py --config config/vehicle/coupled_planar_differential_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work071/replay/materialized_architecture_v3.json --output artifacts/work071/replay/experiment_evidence.json
Exit: 0
primary SHA-256 = replay SHA-256 = 3D9BF89250E57EC818B785797F3854F4A729BDBAEEBEB8313DD31EE5A2726359

python -m unittest discover -s tests -v
Exit: 0
Ran 431 tests in 48.203s — OK
```

The final repository-contract, compilation, staged-diff, commit, and post-commit replay checks are recorded in the final handoff after they execute.

## Limitations and follow-up

Normal-load redistribution is quasi-static. The model has no resolved spring/damper stroke, roll-centre geometry, unsprung mass, wheel hop, tyre relaxation, temperature/wear, camber, aligning moment, measured tyre data, aero map coupling, road roughness, driver/path controller, track boundary, or lap timing. Internally consistent residuals do not demonstrate real-world accuracy.

The next work should add transient wheel/suspension state and its contact-loss/travel/energy contracts, followed by closed-loop path and circuit integration. Physical correlation remains required before any physical-validation claim.
