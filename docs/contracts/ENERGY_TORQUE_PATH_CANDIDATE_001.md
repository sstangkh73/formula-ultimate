# Energy Conversion and Torque-Path Candidate 001 Contract

Thai companion: `ENERGY_TORQUE_PATH_CANDIDATE_001.th.md`

## Claim boundary

This contract admits one bounded software and CAD verification specimen. It does not validate a motor, engine, battery, fuel system, transmission, coupling, bearing, lubrication system, or cooling system, and it establishes no technology superiority, manufacturing readiness, safety case, or physical behaviour.

The candidate verdict must remain `not_admitted_synthetic_evidence` with `design_use_allowed=false` while its material, process, and measurement chain is `synthetic_verification`. A passing software result cannot override that evidence gate.

The declared technology is one candidate selection. The evaluator accepts any declaration satisfying the typed interfaces; it does not require or reward a historically conventional powertrain layout.

## Frozen candidate

Seven separate solids in the frozen order `energy_store`, `converter_housing`, `converter_rotor`, `input_shaft`, `ratio_drum`, `output_shaft`, `support_block`:

1. `energy_store`: sealed hollow vessel with a fill port; its measured cavity volume, the declared medium density, and the declared specific energy produce the onboard pre-race primary energy. It is also the Work 084 reaction terminal shell and must be replaced by the Work 085 load structure.
2. `converter_housing`: box with a `+y` through bore, two `+y` coolant passages, one lubrication feed port opening into the bore, and four cooling fins.
3. `converter_rotor`: rotating converter output body inside the bore with `0.001 m` running clearance.
4. `input_shaft`: rotor-side torque member whose outer radius is the drive traction radius.
5. `ratio_drum`: driven traction radius and torque transformation body.
6. `output_shaft`: coaxial member terminating at the frozen Work 083 axle outboard end plane.
7. `support_block`: reaction support carrying the output-group bearing bore.

## Kinematic contract

The SI frame is `+x` forward, `+y` left, `+z` up. Seven bodies provide `42` unconstrained spatial DOF. The constraint tree contributes `6 + 6 + 6 + 5 + 6 + 5 + 6 = 40` rows and every part is a tree child exactly once. One separately declared loop-closing rolling coupling contributes `1` row, leaving exactly `1 DOF` about `+y`.

The torque ratio is `driven_radius / drive_radius = 0.030 / 0.010 = 3.0`, taken from the same two frozen radii that generate the B-rep. It is never a free scalar. The rolling coupling is declared with a `0.0002 m` radial engagement gap; teeth, belts, and friction preload are **not modelled**, so the ratio is a declared no-slip kinematic relation rather than a validated engagement.

## Clearance contract

Every one of the twenty-one part pairs carries an exact B-rep clearance and intersection-volume record classified as `forbidden`, `contact`, or `coupling`. Forbidden pairs must hold at least `0.0005 m`; contact and coupling pairs must not exceed the `0.0005 m` mate gap. Maximum permitted intersection volume is `1e-12 m3` everywhere. There is no overlap suppression, healing, or repair.

The transformation body must stay above the frozen Work 083 contact plane `z = -0.139 m`.

## Torque, reaction, energy, and thermal contract

The torque graph must contain exactly one continuous path

`converter_rotor -> input_shaft -> ratio_drum -> output_shaft -> w083_axle -> w083_contact_roller`

and the reaction graph exactly one continuous path

`converter_housing -> energy_store -> structure_terminal`

with `support_block -> energy_store` present. Adding the `converter_rotor -> energy_store` return edge must yield exactly one recovery path from the contact body to the store.

The reference drive case is `8.0 Nm` rotor torque at `300 rad/s` for `4.0 s` with converter efficiency `0.90`. Mechanism efficiency is **derived** from the declared `1.2 Nm` support drag torque, not declared independently. The reference brake case is `-12.0 Nm` at `100 rad/s` for `3.0 s` with recovery efficiency `0.60`, drawing from a declared `60000 J` conserved kinetic source.

Enforced invariants:

- external primary-energy inflow is exactly `0 J`;
- every efficiency lies inside `[0,1]` and at or below the declared maximum `0.99`, so a positive loss is mandatory;
- recovered energy never exceeds its declared braking source;
- the reference sequence never ends above its onboard pre-race energy;
- torque and reaction residuals are each `<=1e-5`; energy and thermal residuals are each `<=1e-4`.

The thermal model solves each quasi-steady segment with two parallel rejection routes: coolant-wall conductance from the geometry-derived wetted passage area, and fin-air conductance from the geometry-derived fin-added area. Coolant temperature rise, coolant velocity through the geometry-derived passage cross-section, and housing temperature must each stay inside the declared domain. Nothing is clipped.

## Geometry evidence

CadQuery `2.8.0` generates all seven parts and exports each as a canonical STEP byte stream with the timestamp fixed to `1970-01-01T00:00:00`. The assembly STEP must import as seven separate valid solids. FreeCAD independently imports every exact part STEP and the assembly, records validity, volume, area, and bounds, and saves an FCStd document containing seven named `Part::Feature` objects. No healing call or hidden geometry repair is allowed.

Two surface quantities are cross-checked against the frozen build parameters at `1e-6` relative tolerance: the coolant passage area is measured as the CadQuery surface-area difference across the passage cut, and the fin area as the difference across the fin fusion. A cut or fusion that did not occur fails closed.

Part mass must equal the CadQuery volume times the single declared synthetic material density; a typed mass fails closed.

## Work 083 interface

The candidate is exact-identity coupled to Work 083 result `a061d0b2de7b01eb31233cd3ed1ab9945eb5dbc015ca478c26fb9b77fbfaded3`, assembly STEP `57dc477bbec58da05a0908d1b9b8de04c57a482f710c2362980fed8c51ccb135`, and axle STEP `b44add5cc5a31471947d2dbf614ae78c4187384059677e7107dd7151b4e470ef`. Work 083 must still report `not_admitted_synthetic_evidence` and `design_use_allowed=false`.

The measured `output_shaft` inboard end plane, axis, and radius must match the frozen axle at `1e-6 m`. **No fastener is modelled**, so torque and radial transfer across this butt interface is a declared interface continuity claim, not a validated joint.

## Required falsification controls

Each control re-runs the same physics with an injected change and must produce its preregistered computed consequence:

- `mirror`: reflected `y` positions reproduce the reference support reaction exactly; the rotation axis sign flips.
- `locked_converter`: zero rotor speed gives zero delivered work and state `no_delivered_power`.
- `seized_support`: drag equal to the transformed torque gives zero delivered work and drives the housing past its temperature domain.
- `broken_coupling`: removing the traction edge yields `open_torque_path` and zero delivered work.
- `zero_loss_exploit`: unit converter efficiency with zero drag yields `declared_efficiency_exceeds_maximum`.
- `efficiency_over_one`: `1.05` yields `efficiency_outside_unit_interval`.
- `reversed_torque`: negative rotor torque yields `undeclared_energy_source`.
- `overspeed`: `900 rad/s` yields `speed_domain_exceeded` and `surface_speed_domain_exceeded`.
- `inadequate_cooling`: reduced coolant flow yields `coolant_temperature_rise_exceeded_brake`.
- `disconnected_housing_reaction`: removing the housing mount edge yields `open_reaction_path`.

A missing or ineffective control fails the evaluation.

## Structural evidence class

Structural margins for `output_shaft_combined`, `input_shaft_combined`, `support_block_bearing`, and `converter_housing_mount` are analytic, geometry-derived, and labelled `analytic_synthetic_verification` with `meshed_solver_evidence=false`. Declaring meshed evidence fails closed. Fatigue, fracture, buckling, contact, thermal stress, and meshed stress fields are recorded as unsupported modes.

**The Work 084 meshed structural completion gate is not met by this contract.** A separately numbered remedial work must add a generalised meshed torsion, bearing, and housing route before Gate B or Work 085 may be claimed.

## Replay and failure semantics

Two clean runs compare the declaration, every part STEP, the assembly STEP, the geometry manifest, the canonical FreeCAD report, the evaluation, the Work 083 evidence, and the result identities. STEP timestamps are canonicalised; FCStd bytes are not treated as deterministic evidence because the container carries volatile metadata.

Any schema extension, changed identity, missing solid, invalid shape, clearance or overlap violation, misclassified pair, broken reference path, area cross-check mismatch, ledger residual above its gate, domain violation, relabelled synthetic evidence, non-causal control, or replay mismatch fails closed. There is no result-conditioned geometry repair.
