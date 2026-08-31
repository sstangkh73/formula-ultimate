# Work 070 Result: Differential and Independent Driven-Wheel Dynamics

English result for `2026-08-31_070_differential-independent-wheel-dynamics-plan.md`.

Status: Completed

Thai companion: `2026-08-31_070_differential-independent-wheel-dynamics-result.th.md`

## Outcome

Implemented an ideal open-differential carrier and independent left/right driven-wheel state on the unchanged Work 069 v3 geometry. The model closes common/modal inertia without double counting, consumes the declared `0.98` branch connection efficiencies, exposes connection/slip/differential heat, maintains the carrier-average constraint, and propagates branch overspeed to `DNF`.

Symmetric grip retained identical branch speeds and zero modal energy. Admitted split grip completed with branch speeds `141.05601957062677` and `74.25341080361065 rad/s`; the mirrored control exchanged them exactly. Zero energy produced no motion. A `25 rad/s` operational limit caused the expected `differential_branch_overspeed` terminal event.

## Files changed

- `config/vehicle/functional_differential_drive_v1.json`
- `src/formula_ultimate/simulation/differential_drive_coupling.py`
- `src/formula_ultimate/simulation/__init__.py`
- `scripts/experiments/run_differential_drive.py`
- `tests/test_differential_drive_coupling.py`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.md`
- `docs/research/DIFFERENTIAL_INDEPENDENT_WHEEL_DYNAMICS_V1.th.md`
- matching bilingual Work 070 plan/result records

Ignored evidence is under `artifacts/work070/`, including the materialized architecture, canonical experiment JSON, and exact replay copies.

## Evidence

- Common inertia closure: `2.2393151654985397 + 2(0.13034241725073026) = 2.5 kg m^2`.
- Driven-contact static load: `701.6810927158073 N` per branch, derived from Work 069 equilibrium.
- Symmetric final vehicle speed: `11.68448249437216 m/s`; equal branch speed `103.15502526901471 rad/s`; modal energy `0 J`.
- Split final vehicle speed: `9.96057727044386 m/s`; left/right `141.05601957062677/74.25341080361065 rad/s`; modal speed `-33.401304383508055 rad/s`.
- Split maximum modal energy: `324.1158550756573 J`; connection heat `599.8816054535888 J`; differential heat `60.115830964968396 J`.
- Split maximum interface residual: `1.9071116214020023e-12 J`; global relative residual `1.0060348957777023e-8`.
- Mirror aggregate and exchanged-branch residuals: exactly `0` for selected values.
- Maximum half-step difference: `0.00023334677638767642`, below `0.02`.
- Reference result SHA-256: `c23eea2641b6863da2d63eb8a2ca3b7ae5ad94a53822c70bffd8fa1bffb1b92a`.
- Split result SHA-256: `eee844e411d194c5d2205e5467ce42d3877867b013863fd4cd0772bda2be4879`.
- Evidence SHA-256: `bc23719a3fbd0d343898488f263bf805d8aae8152acc6de4ef23ff2d410cd79a`.
- Architecture bytes match Work 069 exactly; no new CAD solid was claimed.

## Exact validation commands and status

```powershell
python -m unittest tests.test_differential_drive_coupling -v
# exit 0; Ran 9 tests; OK

python scripts/experiments/run_differential_drive.py --config config/vehicle/functional_differential_drive_v1.json --vehicle-root config/vehicle --materialized-architecture artifacts/work070/materialized_architecture_v3.json --output artifacts/work070/experiment_evidence.json
# exit 0; status passed

# Repeated with outputs under artifacts/work070/replay.
# evidence_exact=true, architecture_bytes_exact=true,
# reference_exact=true, split_exact=true.

python -m compileall -q src scripts tests
# exit 0

python -m unittest discover -s tests
# exit 0; Ran 421 tests in 39.066s; OK
```

## Decisions, limitations, and follow-up

The split-grip admitted control was frozen at `mu=(1.0,1.2)`. Exploratory `mu=(0.35,1.2)` reached architecture branch overspeed before `2 s`, so it was not mislabeled as a completed admissible run. Overspeed remains explicit failure evidence.

This is a synthetic lumped open differential, not resolved internal geometry or hardware validation. It retains fixed static loads and omits shaft elasticity per branch, backlash, bearings, lubrication, limited-slip behavior, reverse rotation, tyre thermal/wear state, and suspension transients.

The next work should combine independent branch states with planar steering/yaw and transient normal-load transfer, followed by internal transmission geometry and structural/thermal evidence.
