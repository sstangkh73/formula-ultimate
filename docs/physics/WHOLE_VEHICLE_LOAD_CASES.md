# Whole-Vehicle Load Cases and Structural Coupling

Thai companion: `WHOLE_VEHICLE_LOAD_CASES.th.md`

## Evidence boundary

Work 048 admits a deterministic quasi-static rigid-component cut-load adapter for the exact Work 047 primitive assembly. It does not admit whole-vehicle stress FEA, arbitrary geometry, transient response, contact mechanics, or physical strength. The adapter's purpose is narrower: prove that a frozen Level 0 state can produce complete, traceable, balanced interface wrenches and can trigger the already bounded Work 046 failure-state policy.

## Frozen identities

- assembly protocol: `topology_neutral_vehicle_v1`
- declaration SHA-256: `041057afd245bd4a10482837672d474b0e310ebbfc38fdca4c40408f1f441170`
- assembly STEP SHA-256: `f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9`
- structural failure contract: `structural_failure_coupling_v1`
- frame: right-handed SI, `x` forward, `y` left, `z` up

The acceptance runner regenerates the STEP file and asks FreeCAD to measure mass, centre of mass, and inertia. A hash or mass-property mismatch rejects the load-case protocol.

## Equilibrium model

For component `i`, the body force in the accelerating vehicle frame is

```text
F_i = m_i (g - a)
```

and its moment about the assembly centre of mass is

```text
M_i = (r_i - r_COM) x F_i
```

The frozen aerodynamic and contact wrenches are added without correction. Their global sum must close within the declared force and moment tolerances. The assembly connection graph is a tree rooted at the declared ground-contact component. For every non-root subtree `S`, the connection wrench acting on that subtree is

```text
W_connection = -sum(W_external,i), i in S
```

This construction is audited again at every component. It does not estimate local stress; it preserves force and moment transfer at a common reference origin.

## Cases and partitions

The training partition was frozen before search with five cases: straight acceleration, braking, steady cornering, combined manoeuvre, and bump extreme. The holdout partition was frozen with aero extreme and a second combined manoeuvre. A separate deliberately overloaded control is never training or holdout evidence.

- training partition SHA-256: `d19f8e33c1259e64632e6e89f9768fddeb8c6e54f4a204994e200037c6beba38`
- holdout partition SHA-256: `5045fd461c740e4edc461a702dc96bf3e93fba0b4dbb0bbeeca8adcaf4d5cf41`

Every snapshot must declare exact dynamics, contact, aerodynamics, and mass-state evidence classes. Missing evidence is an error; the adapter never substitutes zero.

## Results

All seven nominal training/holdout cases remained `running`. Their maximum declared interface utilization ranged from approximately `0.37` to `0.72`. The deliberate overload reached approximately `1.30`, failed the critical `core_contact` path and another non-critical capacity through its physical moment arm, and the Work 046 contract returned `DNF`.

- maximum global residual: `1.5631940186722204e-13`
- maximum component residual: `2.2737367544323206e-13`
- maximum interface action/reaction residual: `0`
- maximum FreeCAD mass-property relative error: `1.7042240975184457e-15`
- exact replay result-set SHA-256: `da4848de71c19f9d76cad00cdf5013791e5b0d6f5b544293dcf9e094d782bb03`
- negative controls rejected: `7`

## Falsification record

The implementation initially serialized typed connection loads too early; a focused test exposed the lost type and the result/JSON boundary was corrected. The next test showed that the overload also exceeded `energy_core` moment capacity. That was retained as physical evidence rather than hidden by changing capacity; the test was narrowed to the preregistered expectation that `core_contact` fails and the vehicle becomes `DNF`.

The strongest contradicting evidence is the absence of a whole-vehicle stress solver. Algebraic balance cannot exclude local stress concentration, joint flexibility, contact separation, vibration, buckling, or nonlinear material response. Work 049 may consume this adapter as a bounded load-path stage, but must not label it FEA or physical validation.

## Reproduction

```powershell
.\scripts\run_work048.ps1
py -3.14 -m unittest tests.test_vehicle_load_cases -v
```
