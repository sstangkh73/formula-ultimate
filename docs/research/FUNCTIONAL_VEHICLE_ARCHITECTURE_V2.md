# Functional Vehicle Architecture v2

Thai companion: `FUNCTIONAL_VEHICLE_ARCHITECTURE_V2.th.md`

## Outcome and boundary

Work 066 replaces the four-solid visual fixture as the next research input with a technology-neutral, typed functional architecture. The fixed reference candidate contains 10 independently derivable solids, 48 ports, 23 connections, and two bounded ground contacts. It represents the minimum functional paths needed to ask whether a candidate can transmit energy, torque, heat, commands, and structural load without accepting a propulsion label as evidence of force.

This is an architecture and CAD-evidence result, not a complete vehicle simulation. The reference still uses primitive boxes and cylinders. It has no detailed gears, shafts, bearings, windings, cells, fasteners, suspension links, tyre model, fluid passages, driver volume, crash structure, or manufacturing tolerances.

## Technology-neutral contract

Every admitted candidate must provide capabilities equivalent to energy storage, energy conversion, power transmission, ground propulsion, direction control, braking, load structure, heat rejection, and control. The grammar recognizes capabilities from function tags and compatible connected ports rather than names or a prescribed engine, motor, gearbox, wheel count, body shape, or layout.

The reference evidence graph is:

```text
energy_store --electrical--> energy_converter --mechanical_rotary-->
torque_transmission --mechanical_rotary--> left_ground_unit/right_ground_unit

vehicle_controller --control--> converter/direction_actuator/brake_actuator
heat sources --thermal--> heat_rejector
all components --structural--> load_spine --> both ground units --> ground
```

The physical domains are `structural`, `electrical`, `mechanical_rotary`, `thermal`, `control`, and `ground`. Each port has a domain, direction, local 3D position, and finite limits in SI units. Connections must use existing compatible ports and cannot exceed their declared length. Electrical and mechanical efficiency must remain in `(0, 1]`; conversion and transmission declarations cannot create undeclared power or torque. Control connectivity cannot replace an energy path.

## Reference candidate

Candidate `fu-functional-reference-0001` contains:

| Component | Required role | Geometry evidence |
| --- | --- | --- |
| `load_spine` | load-bearing structure | separate box solid |
| `energy_store` | stored energy | separate box solid |
| `energy_converter` | energy-to-rotary conversion and heat source | separate box solid |
| `torque_transmission` | bounded torque transmission and heat source | separate box solid |
| `left_ground_unit` | left ground propulsion/contact | separate transverse cylinder |
| `right_ground_unit` | right ground propulsion/contact | separate transverse cylinder |
| `direction_actuator` | direction control | separate box solid |
| `brake_actuator` | braking and heat source | separate box solid |
| `heat_rejector` | heat rejection | separate box solid |
| `vehicle_controller` | command source | separate box solid |

The declared architecture passes with mass `272.55249331647553 kg`, centre of mass `(-0.024952088769517506, 0.0, 0.2793091493604943) m`, maximum connection length `0.842140130857092 m`, declaration SHA-256 `aab2aa83b794cbee8f1cdfa897c875bcf440394672e0013805d31f4bd20d9990`, and validation SHA-256 `d29f5d51a9b23db2dce9c33f93539cb71afaa020709fc5bcb69b2b6ebaa27677`.

## CAD and independent inspection

CadQuery 2.8.0 generated one STEP file per component plus a ten-solid assembly without geometry repair. The assembly identity is SHA-256 `983902b813ab6ee3fd69c703521ee32206e224b98013f430d1aeee7249ac75da`. FreeCAD 1.1.3 independently reopened every component and the assembly, confirmed 10 valid solids, and recomputed the mass properties.

The FreeCAD comparison produced relative residuals:

- mass: `2.0855952616365914e-16`;
- centre: `1.2421529906547113e-17`;
- inertia: `7.979411838121619e-18`.

All are below the frozen `1e-6` limit. A second generation in a separate directory reproduced the assembly hash and all 10 component hashes exactly.

## Falsification evidence

Seven focused tests include deliberate controls for a missing storage-to-converter path, incompatible domain, invalid direction, unknown port, disconnected structure, missing heat path, uncontrolled brake, efficiency above one, created power, created torque, nonpositive limits, overlapping solids, a port outside its solid, ground contact away from `z = 0`, excessive connection length, and incorrect transverse-cylinder inertia. Each invalid case fails closed instead of being silently repaired.

The complete repository regression passed `388` tests. This supports deterministic schema, graph, primitive geometry, and STEP/FreeCAD evidence plumbing. It does not validate the physical adequacy of the selected component sizes or limits.

## What must follow

The next research layer should add transient component laws before optimizing a detailed car: storage state and power limits; converter torque-speed-efficiency and heat loss; transmission ratio, inertia, compliance, and failure; ground-force/slip and braking limits; steering kinematics; thermal capacity and temperature state; and bidirectional coupling to the structural/failure system. Only after those laws pass analytical and negative controls should the architecture enter whole-vehicle dynamics, higher-fidelity structural analysis, or race optimization.
