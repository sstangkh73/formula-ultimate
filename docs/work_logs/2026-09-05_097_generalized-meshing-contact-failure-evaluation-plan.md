# Work 097 Plan: Generalized Meshing, Contact, and Failure Evaluation

Thai companion: `2026-09-05_097_generalized-meshing-contact-failure-evaluation-plan.th.md`

## Status

Status: Completed

## Objective

Implement a bounded geometry-witness-driven benchmark evaluator so curved, tapered, hollow, branching, ribbed, bearing-seat, and contact-pair cases are not rejected merely because they are non-primitive. Each case must expose model selection, discretization refinement, independent reference comparison, equilibrium/energy residuals, typed contact law, failure checks, solver-invalid states, and propagation to a typed connection edge.

## Scope and planned files

- `config/structural/generalized_geometry_benchmarks_v1.json`
- `src/formula_ultimate/structural/generalized_geometry_benchmarks.py`
- `src/formula_ultimate/structural/__init__.py`
- `scripts/structural/run_generalized_geometry_benchmarks.py`
- `tests/test_generalized_geometry_benchmarks.py`
- `docs/contracts/GENERALIZED_GEOMETRY_BENCHMARKS_V1.md` and Thai companion
- this plan/result and Thai companions
- ignored deterministic pilot/replay/control evidence under `artifacts/work097/`

## Independent/dependent variables and controls

- Independent inputs: exact Work 096 report/comparison identities; benchmark family and source candidate; support/load/contact region IDs; declared load, torque, pressure, temperature change, material and failure domains; model-selection rules; contact law; discrete levels; and residual/convergence thresholds.
- Dependent outputs: selected beam/shell/solid/contact model and justification; geometry inputs from Work 096; reference and discrete responses; effective element/sample counts; last-two change and observed order; force, moment, and energy residuals; bending/torsion/buckling/yield/plasticity/fracture/fatigue/thermal indicators; contact state; solver-valid/invalid state; and typed connection-edge transition/affected functional paths.
- Controls: source/report hash mutation, primitive-only case substitution, missing semantic region, model-selection mismatch, non-refining levels, non-finite response, excessive equilibrium/energy residual, non-convergence, contact-law mutation, severed edge with nonzero transmission, hidden geometry repair, failure evidence after result observation, and exact replay mutation.

## Seven benchmark adapters

1. `curved_cantilever`: Work 092 curved branch, beam bending reference and midpoint strain-energy integration.
2. `tapered_beam`: tapered open shell geometry under a declared beam idealization, piecewise section reference and discrete integration.
3. `hollow_shell`: tapered hollow duct, membrane reference and polygonized circumference refinement.
4. `branched_joint`: organic/branching geometry, parallel branch bending reference and discrete integration.
5. `lattice_rib_junction`: ribbed gusset geometry, axial rib-network reference and discrete spring assembly.
6. `bearing_seat`: bored hub geometry, annular radial-compliance reference and radial ring integration.
7. `contact_pair`: four-solid revolved member identity, Hertz normal-contact reference and bounded Newton refinement with declared friction/preload state.

The analytical/reduced reference and independent discrete implementation are separate code paths. They are benchmark adapters driven by measured geometry summaries, not general-purpose FEA.

## Model, mesh, contact, and failure rules

- Model selection uses benchmark load dimensionality plus Work 096 solid count, path/section evidence, thickness ratio, and contact-pair declaration. Any expected/selected mismatch rejects.
- Discrete levels strictly refine and report effective elements/samples/iterations. Curvature, thickness, section gradients, interface-region count, and stress-gradient class contribute to the declared refinement justification.
- Contact laws admitted in V1 are `bonded`, `sliding_friction`, `bearing_preload`, and `hertz_frictional`; every case must declare one. This does not solve arbitrary 3D nonlinear contact.
- Every fine result evaluates bending, torsion, Euler buckling, yield/plasticity, fracture-domain, synthetic fatigue damage, thermal stress, and contact validity, while marking non-applicable mechanisms explicitly.
- Failure status updates a declared typed connection edge. A severed edge must transmit zero force/moment and identify affected paths; divergence and invalid states remain results rather than receiving fallback values.

## Success criteria

- All seven required benchmark families bind to exact non-primitive Work 096 candidates and mandatory semantic regions.
- Every admitted baseline passes its declared response-reference, last-two refinement, observed-order/exact-match, equilibrium, moment, energy, contact, and failure-domain gates.
- Beam, shell, solid, and contact model selections all occur with machine-readable justification; all four contact-law families occur across the suite.
- Injected divergence, residual, missing-region, model mismatch, hidden repair, invalid contact law, and noncausal severed-edge controls fail visibly.
- Same clean runs reproduce the complete ordered evidence and result SHA-256.
- Focused tests, compilation, repository contracts, pilot/replay, and full regression pass.

## Risks and explicit non-goals

These reduced benchmark adapters cannot resolve arbitrary 3D stress concentrations, local shell modes, plastic redistribution, crack growth, fretting, real S-N data, nonlinear material/contact history, or mesh geometry from STEP. Work 096 scalar/section sampling can miss local extrema. Passing proves the seven frozen benchmark paths and failure bookkeeping, not arbitrary topology, real-material capacity, design admission, manufacturability, safety, or physical validation. Independent Gmsh/CalculiX promotion remains required for candidate claims beyond this benchmark level.
