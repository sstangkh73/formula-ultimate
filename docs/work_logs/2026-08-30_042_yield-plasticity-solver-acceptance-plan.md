# Work 042 Plan: Yield and Plasticity Solver Acceptance

Status: Completed

Thai companion: `2026-08-30_042_yield-plasticity-solver-acceptance-plan.th.md`

## Objective

Verify that the installed CalculiX route changes from elastic to declared bilinear elastic-plastic response at yield, accumulates plastic strain, and retains residual deformation after unloading instead of providing unlimited linear-elastic strength.

## Scope and claim boundary

- Use a synthetic, rate-independent, isotropic bilinear material with `E=70 GPa`, `nu=0.3`, `sigma_y=250 MPa`, and declared total post-yield tangent `Et=1 GPa`.
- Use a uniform prismatic tension coupon and homogeneous end loading with SI units.
- Compare solver onset, post-yield tangent, plastic strain, residual strain, reactions, work partition, and two mesh levels against an independently implemented closed-form uniaxial reference.
- Include a below-yield negative control, an unload-to-zero sequence, reversed loading within the declared isotropic-hardening limitation, and exact rejection of missing material provenance or malformed laws.

This work verifies the numerical material-law route only. The synthetic material is not a real-alloy allowable and does not establish temperature/rate effects, cyclic plasticity, fracture, fatigue, component strength, or vehicle safety.

## Experiment design

- independent variables: load amplitude, loading direction/history, hardening declaration, and structured mesh density;
- dependent variables: axial stress/strain, yield-onset load, tangent stiffness, equivalent plastic strain, residual displacement/strain, reaction closure, elastic energy, plastic work, external work, convergence, hashes, and replay identity;
- controls: coupon geometry, material identity, temperature/rate declaration, boundary surfaces, integration rule, solver executable, parser, and absolute load schedule;
- preferred hypothesis: all declared onset/tangent/residual/energy/equilibrium and mesh gates pass for the synthetic law;
- falsification: retain below-yield and post-yield cases, reject non-finite/missing step evidence, and do not infer a pass from analytical values when solver output is absent.

## Planned implementation and files

- versioned `config/structural/yield_plasticity_acceptance_v1.json`;
- elastic-plastic record, analytical reference, structured mesh/deck generator, and multi-step parser under `src/formula_ultimate/structural/`;
- Work 042 runner/launcher and ignored evidence under `artifacts/work042/`;
- focused negative and analytical tests;
- bilingual physics report and matching result records.

The admitted solver deck will use the CalculiX `*PLASTIC` convention of yield stress versus equivalent plastic strain. The configured total tangent `Et` will be converted to plastic hardening modulus `H=E Et/(E-Et)` so the uniaxial total stress-strain tangent remains `Et`.

## Validation and success criteria

- yield-onset error `<=2%`, post-yield tangent error `<=5%`, residual-strain error `<=5%`;
- reaction residual `<=1e-5`, energy-ledger residual `<=1e-4`, and negligible below-yield plastic strain;
- last-two-mesh nominal-response change `<=5%`;
- deterministic event/step identity and fail-closed invalid material/provenance controls;
- focused tests, live installed-solver run, full tests, compile checks, staged-diff check, explicit commit, and clean-tree replay all pass.

## Risks and explicit non-goals

CalculiX output names and multi-step table structure must be observed and then frozen in parser tests. Load-controlled unloading may require sufficient load steps to integrate work without hiding the bilinear corner. No element deletion, fracture, fatigue, kinematic hardening, ratcheting, arbitrary CAD component, whole vehicle, push, or publication is included.
