# Detailed Vehicle Closure V1

Thai companion: `DETAILED_VEHICLE_CLOSURE_V1.th.md`

Status: Implemented by Work 126 as a deterministic G3-registry closure gate.

## Evidence boundary

Every registered external function has one or more explicit component owners, and every required structure, ground-port, actuator, energy-store, controller, cooler, fastener, support, seal, signal, thermal-link and load-link role must be installed. Material-region identities are unique. Mass, center, diagonal inertia and occupied volume are recomputed from SI component records; declared ledgers must match within the frozen tolerance.

Energy, signal, heat and load paths must connect their registered source and sink. Component bounds must remain inside the final subsystem envelope without static or sampled swept-motion interference. Removing required hardware, duplicating region ownership, creating an out-of-envelope void, interference, an open path or stale envelope fails closed.

G3 registry means explicit deterministic component bounds, placements, ownership and interface graphs. It is not native CAD. Purchased parts are attributed rather than claimed as generated discoveries. Exact replay requires the same result SHA-256. Essential material, surface, tolerance, manufacturing and physical-test gaps remain observable and force `detailed_exploratory`; this contract cannot permit vehicle promotion or physical validation.
