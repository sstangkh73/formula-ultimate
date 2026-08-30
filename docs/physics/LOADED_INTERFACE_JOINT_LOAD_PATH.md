# Loaded Interface and Joint Load Path

Thai companion: `LOADED_INTERFACE_JOINT_LOAD_PATH.th.md`

## Outcome and claim boundary

Work 045 completed a solver-backed load-path experiment through one loaded cylindrical interface and two bonded support interfaces. CAD/STEP/FreeCAD/mesh/result identity, force closure, moment closure, internal/external energy, and last-two-mesh compliance gates passed. The preferred combined hypothesis was nevertheless **rejected** because changing from two rigid support holes to one changed compliance by `299.021%`, far above the `10%` transferability gate.

The result proves a load path only for this exact bonded-interface fixture. It does not validate bolts, pins/contact, bearing failure, welds, adhesives, friction, preload, tolerances, nonlinear failure, arbitrary joints, or a vehicle chassis.

## Geometry and identity chain

`loaded_interface_plate_v1` is a `0.12 x 0.08 x 0.008 m` plate with three `5 mm`-radius through holes:

- `load_port`: `(x,y)=(0.09,0) m`, loaded by `(+1000,0,0) N` distributed over its complete cylindrical surface;
- `support_upper`: `(0.03,+0.02) m`;
- `support_lower`: `(0.03,-0.02) m`.

CadQuery 2.8.0 generated one valid solid. FreeCAD 1.1.3 independently imported the STEP and identified each cylindrical face by ID, center, radius, axis, and area `0.0002513274122872 m^2`. Gmsh then mapped each geometric signature to nonzero boundary triangles/nodes. On the fine mesh every interface mapped to `90` triangles and `56` nodes.

OCCT initially inserted wall-clock time into the STEP `FILE_NAME` header, changing raw hashes despite identical geometry. The exporter now canonicalizes only that header timestamp. Two independent probes then produced the same STEP SHA-256, `6f20d310970723738abafb19fa212264f14a5147880144280c2dbe92502c4aee`, and the same hash survived CadQuery manifest, FreeCAD import, and all mesh runs.

## Solver results

| Mesh | Nodes | C3D4 | Compliance (m/N) | Max von Mises (Pa) | Force residual | Moment residual | Energy residual |
|---|---:|---:|---:|---:|---:|---:|---:|
| 6 mm | 1,110 | 3,228 | `2.13581e-9` | `5.29453e6` | `1.35e-8` | `3.49e-9` | `4.61e-8` |
| 4 mm | 2,115 | 7,059 | `2.14778e-9` | `5.78391e6` | `3.28e-8` | `9.19e-10` | `3.28e-9` |
| 3 mm | 4,178 | 15,293 | `2.16273e-9` | `5.59884e6` | `4.14e-9` | `1.08e-9` | `2.28e-8` |

The last-two compliance change was `0.6959%` and integrated reaction-resultant change was `2.70e-8`, passing their `5%` gates. Symmetry split the axial reaction equally between the two supports. The fine baseline external and internal energies were `0.0010813635116 J` and `0.0010813634869 J`.

With only `support_lower` active, compliance rose from `2.16273e-9` to `8.62973e-9 m/N` and maximum von Mises rose from `5.60` to `27.61 MPa`. The sensitivity solve still closed force, moment, and energy, so this is a real boundary-condition effect inside the model, not a failed solve. Transferability is therefore rejected.

Six negative controls failed closed: missing support, duplicated support selection, zero-area interface, duplicated load ID, broken outer ligament, and disconnected solid.

## Falsification review

Supporting evidence includes one canonical STEP, independently matched interfaces, three connected meshes, complete field coverage, consistent surface loading, equilibrium/energy closure, converged compliance, symmetric load share, and all negative-control rejections. Contradicting evidence is the `299.021%` support-policy sensitivity, which rejects the preferred transferability hypothesis.

Rigid bonded hole constraints are a plausible alternative explanation for the sensitivity and may dominate compliance compared with real pin/contact behavior. Missing evidence includes contact pressure, clearance, friction, preload, support compliance, plastic bearing, bolt/weld/adhesive mechanics, manufacturing tolerance, and yield/fracture/fatigue coupling. Confidence is high for this declared solver load path and low for transfer to other joints.

## Reproduction

```powershell
.\scripts\run_work045.ps1
py -3.14 -m unittest tests.test_loaded_interface -v
```

Machine-readable evidence is written to ignored `artifacts/work045/experiment_summary.json`.
