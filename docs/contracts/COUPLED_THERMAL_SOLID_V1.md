# Coupled Thermal-Solid V1

Thai companion: `COUPLED_THERMAL_SOLID_V1.th.md`

Status: Implemented by Work 115 for bounded Level-0 coupling evidence.

## Scope and geometry evidence

This contract pins the Work 111 and Work 113 commits/contracts and the exact Work 113 threaded-reference result and male/female STEP hashes. Male/female region volumes are `9.803770506463375e-7` and `2.6351823298910333e-6 m3`. Contact area `1.2073261309882398e-4 m2` is re-derived from the registered eight-turn helix geometry rather than treated as a free fit parameter.

Two lumped thermal regions use disclosed synthetic density, heat capacity, expansion and temperature-dependent modulus records valid only from `250-400 K`. A `10 W` source heats the male for `5 s`; the female has a prescribed `0.5 W/K` ambient-boundary conductance. Contact conductance begins from an unmeasured synthetic `20000 W/m2/K` law and varies with interface area and the square root of preload ratio. This boundary is not validated convection, radiation or fluid cooling.

## Bidirectional coupling and gates

At each explicit step, contact heat transfer changes both temperatures. Temperature changes free expansion and Young's modulus; differential expansion changes preload through the registered clamp sensitivity; preload returns a changed contact conductance to the next heat balance. A decoupled control holds conductance independent of returned mechanical state.

Time steps are `0.02`, `0.01` and `0.005 s`. Energy residual must not exceed `1e-10`; last-two relative changes of both temperatures, preload and contact conductance must each be at most `0.01`. A single-temperature reduced model is accepted only when its temperature-rise error is at most `0.2`. Leaving the property range, non-positive modulus/preload, stale geometry or missing contact area fails closed.

Insulated energy rise, zero-source equilibrium, free/constrained expansion, removed heat path and doubled interface area are mandatory causal controls. Exact replay requires the same result SHA-256. Lumped regions do not resolve spatial gradients or thermal stress fields; this contract does not establish certified properties, validated cooling, fatigue/loosening, vehicle cooling adequacy or physical validation.
