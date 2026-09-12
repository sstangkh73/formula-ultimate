# Coupled Vehicle Transient V1

Thai companion: `COUPLED_VEHICLE_TRANSIENT_V1.th.md`

Status: Implemented by Work 123 for bounded exploratory Level-0 integration.

## Identity, state and exchange boundary

This contract pins exact Work 117–122 contracts/results. Position/velocity, stored energy, temperature and controller-delay states each have one declared owner. The route-X frame and signs for traction work, drag work, storage draw, generated heat and removed cooling are immutable; mismatches fail closed.

The reduced trial couples controller force demand, Work 118 ground capacity, Work 119 output-power ceiling, Work 120 initial energy, Work 121 drag/cooling and Work 122 controller load. Within each step, a fixed-point iteration resolves the speed-dependent power cap. Traction work partitions into kinetic-energy change and drag work; storage decrease partitions into traction work, actuation loss and controller energy. Residuals remain observable.

Time steps are `0.02`, `0.01` and `0.005 s`. Maximum step residual is `1e-8 J`, global residual `1e-7 J`, and last-two state change `0.005` relative. A target event occurs at `2 s`; histories retain event and coupling-iteration evidence.

## Controls and promotion boundary

Mismatched signs, double-counted power, delayed event, depleted energy, out-of-range reduced flow state and a decoupled run are mandatory controls. Successful integration remains `passed_exploratory_only` with `promotion_allowed: false`.

Complete candidate geometry, measured material, validated ground device, full aerodynamics, structural failure and physical validation remain unresolved. This harness does not establish a complete vehicle, race completion, readiness or physical performance.
