# Realized Actuation Chain V1

Thai companion: `REALIZED_ACTUATION_CHAIN_V1.th.md`

Status: Implemented by Work 119 as bounded Level-0 reference evidence.

## Realized route and evidence boundary

This contract pins Work 114 motion/load, Work 115 thermal and Work 116 material-scope identities. One disclosed synthetic coaxial rotary reduction route connects torque/speed input and output ports through two cylindrical transfer members, four supports, a containment shell and a coupler. Their registered geometry determines mass, torsional stiffness/stress and reaction loads. The route is an admitted reference, not a permanent requirement for gears, shafts, motors or any other proposal.

The ratio is `3.5`; input limits are `80 N*m`, `300 rad/s` and `280-360 K`. A disclosed synthetic loss law assigns fractional, fixed, speed, torque and temperature losses. At every admitted operating point, accepted input power must equal output power plus heat/loss within `1e-10 W`. Output work and loss energy use a registered `5 s` interval.

## Controls and limitations

The response map contains three speeds, three torques and two temperatures. Disconnected, locked-output, reverse, saturated-demand, removed-support and missing-transfer-member controls are mandatory. A disconnected route admits no input/output energy; a locked output sends admitted power to modeled heat; reverse operation preserves power/loss magnitudes; missing supports or hardware fail closed.

Alternative conversion routes require their own verified laws and hardware coverage. Work 116 material eligibility remains blocked. This contract does not establish measured efficiency, material survival, fatigue/wear, detailed bearing/fastener behavior, controller hardware, a preferred technology or physical validation.
