# Fracture-Initiation Acceptance

Thai companion: `FRACTURE_INITIATION_ACCEPTANCE.th.md`

## Outcome and claim boundary

Work 043 passed a narrow, independently verified LEFM initiation evaluator. It preserves explicit crack identity, toughness provenance, thickness/material-state domain checks, deterministic first-crossing events, and fail-closed invalid cases. It does not claim a CalculiX crack-tip field because the current route has no independently validated contour-integral parser.

This is ideal center-crack initiation arithmetic only. It is not real toughness, crack propagation/path, fracture-energy dissipation, element deletion, fatigue crack growth, component strength, or crashworthiness.

## Model and domain

For an infinite plate with a center crack of total length `2a` under uniform remote tension,

```text
K_I = sigma sqrt(pi a)
sigma_initiation = K_IC / sqrt(pi a)
```

The synthetic record uses `K_IC=15 MPa sqrt(m)`, `sigma_y=250 MPa`, `E=70 GPa`, width `0.2 m`, and thickness `0.012 m`. Admission also requires full crack/width `<=0.1`, `B>=2.5(K_IC/sigma_y)^2`, plane-strain plastic-zone ratio `r_p/a<=0.1`, and initiation below yield. The toughness record is explicitly prohibited from design fitness.

The formula is supported by NASA fracture-mechanics references for an ideal infinite plate. The thickness rule is a screening criterion; it does not transform the synthetic record into a valid measured `K_IC`.

## Results

| Half-crack `a` (m) | Initiation stress (MPa) | Initiation force (N) | `r_p/a` | Localized load error |
|---:|---:|---:|---:|---:|
| 0.003 | 154.5097 | 370,823.23 | 0.06366 | 0 |
| 0.005 | 119.6827 | 287,238.44 | 0.03820 | 0 |
| 0.008 | 94.6175 | 227,081.93 | 0.02387 | 0 |

Every case used load factors `0.8`, `1.0`, and `1.2` of its analytical initiation force. The localized first crossing is exact for this linear evaluator. Representation levels `8`, `16`, and `32` segments per half crack preserve exact tagged tip coordinates, so last-two `K_I` change is zero. Reaction and gross elastic work-ledger residuals are zero.

Six negative controls were rejected with their intended reason: insufficient thickness, excessive finite-width ratio, missing flaw, missing toughness, missing provenance, and material yield preceding LEFM initiation.

## Falsification review

Supporting evidence is exact closed-form reproduction across three crack lengths, deterministic event identity, representation-invariant crack tips, explicit material/domain gates, and complete negative-control rejection. No admitted evidence contradicts the preferred evaluator hypothesis.

The principal alternative explanation is also the key limitation: `Y=1` removes finite-geometry complexity and the work ledger is a gross linear-elastic accounting control, not fracture-energy evidence. Missing evidence includes finite-body geometry factors, crack-tip FEA/J-integral agreement, measured toughness uncertainty, physical coupons, propagation, path, and dissipated fracture energy. Confidence is high for arithmetic and rejection behavior, low beyond ideal initiation.

## Reproduction

```powershell
.\scripts\run_work043.ps1
py -3.14 -m unittest tests.test_fracture_initiation -v
```

Machine-readable evidence is written to ignored `artifacts/work043/experiment_summary.json`.
