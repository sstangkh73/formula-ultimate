# Topology-Neutral Whole-Vehicle Assembly Grammar

Thai companion: `TOPOLOGY_NEUTRAL_VEHICLE_ASSEMBLY.th.md`

## Claim and outcome

Work 047 validates one complete multi-solid vehicle declaration through a topology-neutral assembly contract. The contract does not prescribe a conventional body, wheel count, contact count, powertrain layout, or component count. It requires explicit geometry, material density, interfaces, connections, ground contacts, energy paths, external-load paths, envelope, keep-outs, and Work 046 failure-contract identity.

The admitted fixture contains four solids and one ground contact. This unusual fixture demonstrates that the schema does not require a four-wheel automobile. It is geometric admission only, not evidence of structural feasibility, aerodynamics, cooling, manufacturing, safety, race completion, novelty, or superiority.

## Grammar v1

The initial library contains `box` and `cylinder_z` solids in SI units with translation-only placement. Component functions are tags rather than geometry names. The fixture declares:

- `source`: `energy_source`;
- `core`: `external_load_receiver`;
- `propulsor`: `propulsion`;
- `contact_alpha`: one explicit `ground_contact`.

The energy graph is `source -> core -> propulsor`. The external-load graph is `core -> contact_alpha`. Coincident point interfaces connect the solids. Positive-volume overlap is forbidden; face/point contact is allowed. Every component must lie inside the envelope and outside protected keep-outs.

## Deterministic CAD evidence

CadQuery `2.8.0` generated one STEP file per component and one four-solid compound STEP. OCCT wall-clock fields were canonicalized without changing geometry. Two independent exports produced identical component and assembly hashes.

The canonical assembly STEP SHA-256 is:

```text
f60bb686dfaca51c06bed8b1b086418c5f9ce2208d861b5b2ff18d8f845f18b9
```

The canonical declaration SHA-256 is:

```text
041057afd245bd4a10482837672d474b0e310ebbfc38fdca4c40408f1f441170
```

STEP application labels are not treated as persistent identity. Identity comes from the immutable declaration, per-component file/hash, material ID, and measured geometric signature.

## FreeCAD cross-check

FreeCAD `1.1.3` independently imported every component STEP and the assembly STEP. It found four valid solids. Analytical component summation and FreeCAD gave:

```text
mass = 30.657168026350796 kg
centre of mass = (-0.01875580939197546,
                   0.002656151458968935,
                   0.14557308090171845) m
```

The analytical assembly inertia tensor components `(Ixx,Iyy,Izz,Ixy,Ixz,Iyz)` were:

```text
(0.12214756112199837,
 0.8039434564567454,
 0.8490539916188957,
-0.0015272870889071375,
 0.002545478481511896,
 0.00778252377477898) kg*m^2
```

The maximum relative difference across mass, centre, and inertia comparisons was `1.7042240975184457e-15`, below the preregistered `1e-6` limit. The maximum connection-interface position residual was `1.3877787807814457e-17 m`.

## Falsification and defect evidence

Eight controls rejected a floating component, protected-volume overlap, unmatched interface, disconnected energy path, zero-size solid, massless energy source, envelope violation, and undeclared ground position.

The first exploratory cylinder export used CadQuery `both=True`, producing twice the declared height. FreeCAD measured mass `32.01433605270158 kg` instead of the analytical `30.657168026350796 kg`, a `4.43%` discrepancy. That run was not admitted. The generator was corrected to create exactly `h` from `-h/2` to `+h/2`, and the frozen declaration was rerun. This demonstrates that the independent mass evidence can detect a plausible CAD-generator defect.

Supporting evidence is exact replay, valid-solid inspection, explicit graph reachability, tight mass-property agreement, and fail-closed controls. Alternative explanations include the simplicity of analytic primitives. Missing evidence includes arbitrary rotations, free-form geometry, joint/contact physics, FEA load cases, aerodynamics, thermal paths, manufacturing, and physical measurements.

Confidence is high for this v1 primitive fixture and low outside its declared grammar.

## Reproduction

```powershell
.\scripts\run_work047.ps1
py -3.14 -m unittest tests.test_vehicle_assembly tests.test_repository_contract -q
py -3.14 -m unittest discover -s tests -q
```

Machine-readable evidence and STEP files are under `artifacts/work047/` and intentionally ignored by Git. A clean-tree replay is required after commit.
