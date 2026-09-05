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

Exactly three discretization levels must double strictly. The fine response, last-two change, observed order or exact discrete match, force residual, moment residual, energy residual, and solver-convergence gates must all pass. Non-finite values and divergence are invalid outputs; no fallback response is allowed.

The evaluator records bending, torsion, axial, hoop, contact, and fully constrained thermal stress screens; Euler buckling, yield/plastic-strain proxy, fracture-domain ratio, and synthetic fatigue damage. These are bounded verification indicators using a synthetic material, not certified material allowables.

Failure changes the declared typed connection edge from `intact` to `failed`, zeros transmitted force and moment, and lists affected functional paths. The severed-edge control rejects any nonzero transmitted load. Failure thresholds and the prohibition on post-observation repair are frozen in configuration.

## Reproduction

```powershell
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_a/result.json
python scripts/structural/run_generalized_geometry_benchmarks.py --config config/structural/generalized_geometry_benchmarks_v1.json --output artifacts/work097/run_b/result.json --replay-reference artifacts/work097/run_a/result.json
python -m unittest tests.test_generalized_geometry_benchmarks -v
```

## Claim boundary

Passing establishes only deterministic behavior for the seven frozen reduced-order cross-method benchmarks and their failure bookkeeping. It does not validate arbitrary future topology, local STEP-derived stress concentrations, shell instability, nonlinear material redistribution, crack growth, fretting, real fatigue data, manufacturability, vehicle safety, or design admission. Candidate promotion beyond this level requires independent geometry-derived meshing and higher-fidelity Gmsh/CalculiX or equivalent evidence.
