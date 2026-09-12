# Ground Interaction Tasks V1

Thai companion: `GROUND_INTERACTION_TASKS_V1.th.md`

Status: Implemented by Work 118 as bounded Level-0 reference evidence.

## Scope, ports and applicability

This contract pins Work 114 moving/contact evidence and Work 116 material-scope evidence. Ground interaction is represented by named contact ports with positions, prescribed normal loads and longitudinal/lateral force requests; no contact technology, steering mechanism or contact count is required. Positive longitudinal force follows the route direction, positive lateral force follows the registered transverse direction, and positive yaw moment is `x*F_lateral - y*F_longitudinal`.

The only implemented adapter is a disclosed synthetic `rigid_dry_coulomb` surface with coefficient `0.8`, registered coefficient range `0-1`, normal-load range `0-6000 N` per port and speed range `-30` to `30 m/s`. The resultant tangential force cannot exceed `mu*N`. Zero or negative normal load gives lift-off; disconnection or absence of an allowed physical interaction gives zero ground force. Unsupported tire, soft-soil and non-tire behavior must remain unresolved rather than inherit this coefficient.

## Stopping, direction and gates

The stopping reference uses a `300 kg` rigid body at `20 m/s`, total prescribed normal load `3000 N`, and time steps `0.1`, `0.05` and `0.025 s`. It records contact work and dissipated power and compares stopping time, distance and kinetic-energy loss with constant-force analytic references. Energy residual must be at most `1e-12` relative and last-two refinement change at most `1e-10`.

Force-circle saturation, zero friction, lift-off, reverse motion, disconnected actuation, absent interaction and changed contact placement are mandatory causal controls. Maximum port resultant and yaw moment are returned as local part-model loads while the Work 116 material claim remains blocked. This contract does not validate tires, soft soil, arbitrary locomotion, load transfer, compliant contact, control stability, wear/thermal evolution, full-vehicle behavior or physical performance.
