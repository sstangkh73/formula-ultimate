# Generalized Geometry Benchmarks V1

Thai companion: `GENERALIZED_GEOMETRY_BENCHMARKS_V1.th.md`

## Purpose

This contract admits seven frozen non-primitive Work 096 geometry witnesses to reduced-order structural benchmark evaluation. It prevents unfamiliar geometry from being rejected solely because only primitive-specific evaluators exist. It does not claim a general finite-element solver.

## Source identity

`config/structural/generalized_geometry_benchmarks_v1.json` binds the exact Work 096 semantic configuration, FreeCAD report, and strict comparison SHA-256 identities. The runner rejects any identity change, missing candidate, missing `support_region`/`load_region`/`contact_region`, or `hidden_geometry_repair: true`.

The seven frozen source candidates are:

1. `curved_branch_001`
2. `tapered_open_shell_001`
3. `tapered_hollow_duct_001`
4. `organic_load_bridge_001`
5. `ribbed_gusset_bridge_001`
6. `bored_chamfered_hub_001`
7. `revolved_intersection_member_001`

Primitive substitution is not admitted by this version.

## Evaluation paths

Each case selects and justifies one of `beam`, `shell`, `solid`, or `contact`. Selection consumes the Work 096 solid count, sampled section properties, thickness-to-path ratio, semantic regions, and path witness. Expected and selected models must agree.

The separate reference/discrete paths are curved bending versus midpoint integration, tapered bending versus refined section integration, membrane response versus polygonized circumference, parallel-branch bending versus discrete integration, rib network versus assembled springs, annular compliance versus radial integration, and Hertz contact versus bounded Newton refinement.

Every case declares one typed contact/interface law from `bonded`, `sliding_friction`, `bearing_preload`, or `hertz_frictional`. V1 records the active law and validity but does not solve arbitrary three-dimensional nonlinear contact history.

## Evidence gates

Exactly three discretization levels must double strictly. Fine response, last-two change, observed order or exact discrete match, scalar constitutive equilibrium/energy consistency, and scalar solver convergence must pass. Non-finite values and divergence are invalid outputs; no fallback response is allowed. Work 103 corrects the earlier force/moment/energy gate description: these reduced adapters do not recover independent field reactions.

`evaluator_version=generalized_geometry_equations_v2` distinguishes corrected outputs from historical Work 097. `force_residual_relative`, `moment_residual_relative` and `energy_residual_relative` are now `null`, with `field_balance_status=not_computed_no_independent_field_reactions` and `full_balance_validated=false`. This is missing field evidence, not a zero residual or a passed balance gate. Adjudication rejects legacy zeros, missing fields, changed scope/version, forged energy/reference errors and incorrect refinement ordering.

Scalar evidence uses q = K*u^p, where K comes from the model/discrete compliance before solving u, never from q/u afterward. `generalized_equilibrium_residual_relative` is abs(K*u^p-q)/q. `constitutive_energy_residual_relative` compares stored energy K*u^(p+1)/(p+1) with prescribed quasistatic ramp work q*u/(p+1). The latter assumes the ramp has the same power-law shape, not an independently measured load history. These are two consistency checks on the same scalar law, not independent validation. Existing force/energy tolerances bound these scalar checks; the legacy moment tolerance cannot establish a moment balance. Newton reports actual residual history/iteration effort and convergence requires residuals <= 1e-12; an exhausted budget remains invalid.

For linear adapters p = 1. For the normal Hertz proxy p = 3/2, E* = E/[2(1-nu^2)], K = (4/3)*E*sqrt(R*), a = (3*F*R*/(4*E*))^(1/3), and p0 = 3*F/(2*pi*a^2). Indentation and contact pressure share E* and R*. R* is the declared sampled bend-radius proxy, or sampled thickness only when radius is absent; it is not silently clamped to thickness. Equal isotropic elastic materials and a small, frictionless normal-contact patch are assumed. The typed frictional interface does not add a solved tangential contact law. See [CompuTiX Hertz theory](https://computix.gitlabpages.inria.fr/computix/db/d6e/group__Hertz.html).

Integrating F = K*delta^(3/2) gives U = (2/5)*K*delta^(5/2), or (2/5)*F*delta at equilibrium, not (1/2)*F*delta. This derivation assumes quasistatic elastic loading without dissipation. Force-based energy is in J; shell pressure-based work is in J/m^2, because pressure times displacement is energy per area. It is not total shell energy. Newton starts from half the analytical indentation solely as a bounded iteration benchmark; it is not an independent contact solver.

The evaluator records bending, torsion, axial, hoop, contact, and fully constrained thermal stress screens; Euler buckling, yield/plastic-strain proxy, fracture-domain ratio, and synthetic fatigue damage. These are bounded verification indicators using a synthetic material, not certified material allowables.

Failure changes the declared typed connection edge from `intact` to `failed`, zeros transmitted force and moment, and lists affected functional paths. The severed-edge control rejects any nonzero transmitted load. Failure thresholds and the prohibition on post-observation repair are frozen in configuration.

## Reproduction

```powershell
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work103/run_b/result.json --replay-reference artifacts/work103/run_a/result.json
python -m unittest tests.test_generalized_geometry_benchmarks -v
```

## Claim boundary

Keep historical Work 097 outputs unchanged; reproducing their exact identity requires the historical implementation. Input configuration, loads, thresholds and Work 096 source identities remain unchanged in Work 103.

Passing establishes only deterministic behavior for the seven frozen reduced-order cross-method benchmarks and their failure bookkeeping. It does not validate arbitrary future topology, local STEP-derived stress concentrations, shell instability, nonlinear material redistribution, crack growth, fretting, real fatigue data, manufacturability, vehicle safety, or design admission. Candidate promotion beyond this level requires independent geometry-derived meshing and higher-fidelity Gmsh/CalculiX or equivalent evidence.
