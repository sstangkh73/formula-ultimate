# Yield and Plasticity Solver Acceptance

Thai companion: `YIELD_PLASTICITY_ACCEPTANCE.th.md`

## Outcome and claim boundary

Work 042 passed the declared synthetic uniaxial bilinear material-law acceptance. CalculiX produced zero below-yield plastic strain, a resolved elastic-to-plastic tangent change, nonzero equivalent plastic strain at `270 MPa`, residual strain after unloading, elastic reverse response, closed reactions, and an internal-energy ledger consistent with external work.

This validates only the declared numerical route. It is not a real-alloy allowable, physical coupon validation, cyclic plasticity, fracture, fatigue, component strength, or vehicle safety evidence.

## Declared law and fixture

The prismatic coupon has `L=0.1 m` and area `1e-4 m^2`. The synthetic material uses `E=70 GPa`, `nu=0.3`, `sigma_y=250 MPa`, and total post-yield tangent `Et=1 GPa`. CalculiX `*PLASTIC` requires stress versus equivalent plastic strain, so the tabular hardening slope is

```text
H = E Et / (E - Et) = 1.0144927536 GPa
epsilon = sigma/E                         for sigma <= sigma_y
epsilon = sigma_y/E + (sigma-sigma_y)/Et for sigma > sigma_y
epsilon_p = epsilon - sigma/E
```

The absolute stress history is `200, 250, 270, 0, -200, 0 MPa`. It includes a below-yield control, the bilinear corner, post-yield loading, unload, reverse-elastic loading, and final zero load. The two deterministic C3D8 meshes contain `8` and `16` elements. CalculiX output `PEEQ` and `ELSE` semantics follow the CalculiX user manual.

## Results

| Metric, fine mesh | Result | Gate |
|---|---:|---:|
| yield-onset error | `1.0145e-9` relative | `<=0.02` |
| post-yield tangent error | `5.0000e-8` relative | `<=0.05` |
| peak `PEEQ` error | `2.1739e-7` relative | `<=0.05` |
| residual-strain error | `2.1739e-7` relative | `<=0.05` |
| below-yield `PEEQ` | `0` | `<=1e-10` |
| maximum reaction residual | `1.0840e-16` relative | `<=1e-5` |
| maximum energy-ledger residual | `2.7508e-7` relative | `<=1e-4` |
| maximum last-two-mesh response change | `0` | `<=0.05` |

The analytical peak total strain is `0.0235714286`; the residual plastic strain is `0.0197142857`. The fine solver residual is `0.0197142900`. Reversing to `-200 MPa` remains elastic under the enlarged isotropic yield surface; this is a control, not a cyclic-plasticity validation.

## Falsification review

Supporting evidence includes solver-emitted multi-step displacement, reactions, stress, strain, `PEEQ`, and `ELSE`; exact below-yield behavior; residual deformation; work-energy closure; and mesh-independent homogeneous response. The first exploratory run was not admitted because default print frequency emitted every increment and exposed an incorrect parser heading; output frequency and the observed exact heading were then frozen and tested.

No admitted result contradicts the preferred hypothesis. Alternative explanations are that a homogeneous coupon suppresses stress concentrations and the synthetic bilinear curve is substantially simpler than processed real material. Missing evidence includes sourced material allowables, physical coupons, temperature/rate effects, cyclic hardening/ratcheting, multiaxiality, fracture, and fatigue. Confidence is high only for this local synthetic uniaxial solver-law route.

## Reproduction

```powershell
.\scripts\run_work042.ps1
py -3.14 -m unittest tests.test_plasticity_acceptance -v
```

Machine-readable evidence is written to ignored `artifacts/work042/experiment_summary.json`; the accepted clean replay must identify the committed implementation and a clean worktree.
