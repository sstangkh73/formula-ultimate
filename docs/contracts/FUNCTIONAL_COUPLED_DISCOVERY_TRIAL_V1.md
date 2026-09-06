# Functional and Coupled Discovery Trial V1

Thai companion: `FUNCTIONAL_COUPLED_DISCOVERY_TRIAL_V1.th.md`

Status: Implemented and executed under Work 100 registration V2

## Claim boundary

This trial evaluates only a bounded source-to-sink subsystem represented as a scalar axial-force network and a steady-state thermal-resistance network. A `candidate_survivor` means the registered morphology passed refined numerical physics, a computational process envelope, an untouched holdout task and exact ledger replay. It does not establish full three-dimensional structural behavior, complete-vehicle feasibility, race performance, technology novelty, manufacturing feasibility, `promotion_ready` status or physical validation.

The material properties are a declared linear isotropic study model, not certified properties. The process gate checks minimum diameter, part count and coordinate span only; it is not a manufacturing demonstration. The passive controller gene is recorded but has no causal path in this solver and receives no performance credit.

## Geometry, fields and equations

Every genome edge is a straight member of length `L` with linearly varying endpoint radii `r_a` and `r_b`. Its circular cross-section is `A(x) = pi r(x)^2`. Fixed interfaces carrying both `load` and `thermal` domains merge coincident network nodes. Exactly one source and one sink terminal are bound by registered ancestry; every part material identifier must match the registered study model.

The primary evaluator divides each edge into `n` midpoint segments. For a segment of length `Delta x` and area `A_i`, mechanical and thermal resistances are:

```text
R_mechanical,i = Delta x / (E A_i)
R_thermal,i    = Delta x / (k A_i)
```

The assembled conductance matrix fixes the source potential to zero and applies force `F` or heat rate `Q` at the sink. Nodal displacement/temperature, segment force/heat flow, source reaction, free-node residual, global equilibrium residual and energy residual are stored at all three registered refinements. Maximum axial stress uses each original edge's minimum endpoint area as a conservative section. The coupled utilization is:

```text
U = max(displacement / displacement_limit,
        maximum_axial_stress / yield_strength,
        temperature_rise / temperature_limit)
```

`U <= 1` is `physically_feasible` only inside this model. Numerical admission additionally requires last-two-refinement relative change, conservation residual and primary/reference disagreement to stay within their registered limits.

The separate reference implementation integrates a linearly varying circular radius exactly:

```text
R_exact = L / (coefficient pi r_a r_b)
```

It independently assembles edge resistances but shares the same declared equations, geometry genotype and NumPy linear-algebra runtime. It is cross-method corroboration, not an independent software stack or experiment.

Geometry-derived volume uses the conical-frustum expression `V = L pi (r_a^2 + r_a r_b + r_b^2) / 3`; mass and fraction of the declared 800 kg reference vehicle are feedback only. CAD execution independently establishes geometry identity and measurements, but the network is constructed from the exact genes that generate that CAD rather than from a volumetric finite-element mesh.

## Registered trial

- Treatments: `FIXED_TOPOLOGY`, `RANDOM_CONTROL`, `GRAPH_ONLY`, `MORPHOLOGY_ONLY`, `JOINT_MORPHOLOGY_CONTROLLER`.
- Paired seeds: `7`, `19`; `n = 2` is descriptive and cannot support a superiority inference.
- Training task: `5000 N`, `30 W`, displacement limit `0.0002 m`, temperature-rise limit `160 K`.
- Holdout task: `6000 N`, `35 W`, the same registered limits, and no holdout feedback.
- Proxy refinements: `[1, 2, 4]`; refined/holdout refinements: `[4, 8, 16]`.
- Limits: refinement change `0.005`, exact-reference error `0.005`, conservation residual `1e-10`, coupled utilization `1.0`.
- Study material: density `2700 kg/m^3`, `E = 70 GPa`, yield strength `250 MPa`, conductivity `170 W/(m K)`.
- Process envelope: diameter at least `0.004 m`, no more than `8` parts, coordinate span no more than `0.5 m`.
- Runtime: Python `3.12.14`, CadQuery `2.8.0`, NumPy `2.5.2`, one serial worker.

Registration V1 SHA-256 `aa5012d3b0a85b9f6c42b1ede5561681713cb9c9832577f6d2bf88e09d96a871` stopped without holdout or survivor outcomes because eight proxy labels were unresolved and the inherited audit reporter required Boolean proxy labels. Its partial ledger was not resumed. Registration V2 SHA-256 `2c3aaa21ffb6ed36da532493c82c6e1f0195b13990180dc5d055c75fb47bdd45` preserved all scientific thresholds, tasks, treatments, seeds and selection rules, while prospectively defining an explicit not-estimable audit result for unresolved proxy labels.

## Admitted outcome

Independent V2 runs A and B produced the same deterministic evidence SHA-256 `652ba7d9db9d76ed841d5b2c24af421075cc2d266a9098bc065fe4a8ac45da61`. All ten candidates passed the refined training task, process envelope, holdout task and replay gate, so the ledger recorded ten scoped `candidate_survivor` decisions with admissible accounting. All refined errors were below `0.000536`; holdout utilization remained below `0.696`.

The audit sampled all ten treatment/seed/representation strata. Only two proxy labels were Boolean and eight stayed `numerically_unresolved`, so false-negative and false-positive rates are `null`, not zero. All ten refined references were feasible. This is a proxy-resolution limitation, not evidence that the proxy is accurate or inaccurate.

Graph-only and joint treatments produced signatures distinct from the fixed topology, satisfying the registered survivor-success condition. Their primary response differed from the fixed control only at floating-point round-off (`mean difference about -1.51e-14`) because the added branch carried essentially zero source-to-sink flow. Morphology-only paired differences had opposite signs and mean `-0.00312`; random-control mean difference was `+0.01593`. Consequently, this trial demonstrates executable distinct architectures and scoped feasible survivors, but no functional superiority, new useful load-path effect, race advantage or technology discovery.

## Reproduction

```powershell
$env:PYTHONPATH = Join-Path $PWD 'src'
python -m unittest tests.test_functional_discovery -v
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_functional_discovery.py --output-dir artifacts/work100/run_v2_a
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_functional_discovery.py --output-dir artifacts/work100/run_v2_b --replay-reference artifacts/work100/run_v2_a/result.json
```

Generated evidence under `artifacts/work100/` is intentionally ignored by Git. The committed registration, source, tests, contract and work logs preserve the reproducible specification and exact reported identities.
