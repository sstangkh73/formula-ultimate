# Load Structure Integration Candidate 001

Thai companion: `LOAD_STRUCTURE_INTEGRATION_001.th.md`

## Boundary

This contract evaluates one synthetic vehicle-scale packaging fixture. It requires exact Work 083, Work 084, and Work 086 identities, seventeen separate STEP/FreeCAD solids, geometry-derived mass properties, pairwise interference evidence, service/routing clearance, load/thermal bookkeeping, motion-interface compatibility, causal controls, and replay. It does not validate a chassis, monocoque, crash structure, cooling package, or production assembly.

## Geometry and paths

Twelve frozen subsystem parts are imported unchanged. Five generated solids provide an upper bridge, two mounts, and two coolant routes. Every unordered pair is measured. Undeclared overlap above `1e-12 m3` or clearance below `0.5 mm` is a visible blocker; it is never suppressed. Routing/service clearance must be at least `2 mm`, and new integration geometry must remain at least `5 mm` above the frozen contact plane.

Mass, centre of mass, and full inertia are calculated from exact B-rep volume/centres/inertia with synthetic density and parallel-axis translation. These values are not physical measurements.

## Ledgers, controls, and verdict

Six load cases pair every applied force/torque with an explicit structure reaction. Force/moment residuals must be `<=1e-5`. Generated heat must equal coolant plus air rejection within `1e-4`; external primary inflow is zero. Required controls reject disconnected/weak mounts, blocked service, routing collision, inadequate rejection, asymmetric load, and thin structure; mirror and replay remain explicit.

Work 083 permits `+/-7 mm` vertical axle travel, while Work 084 declares a rigid coaxial butt interface with `1e-6 m` alignment tolerance. The evaluator must expose the resulting motion mismatch rather than silently add a joint. Any blocker yields `integration_status=partial`, `candidate_verdict=not_admitted`, and `design_use_allowed=false`.
