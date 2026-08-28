# Central Energy and Health Coupling

Thai companion: `CENTRAL_ENERGY_HEALTH_COUPLING.th.md`

## Boundary

Work 027 couples declared wheel work, auxiliary demand, regeneration, brake heat, aerodynamic cooling conductance, lumped thermal state, degradation, damage, and seeded reliability. It remains a Level-0 evidence and event-localization model, not calibrated physical validation.

## Energy Ownership

- Positive applied local contact force produces no-slip `drive_wheel_energy_j = F_x r omega dt`.
- Drive source demand is `drive_wheel_energy_j / drive_efficiency`.
- Auxiliary demand is `auxiliary_power_w * dt`.
- Recovered storage energy, conversion loss, and mechanical brake heat come from Work 025 and must close against wheel energy removed.
- Available recovered energy is used before primary energy. Recovery arriving during the interval participates in the declared average-rate store balance.
- Recovered capacity overflow is invalid; the solver does not clip it.

Three independent typed energy audits cover the propulsion chain, auxiliary chain, and aggregate braking/recovery boundary. Five `ResidualEntry` records expose central-store, contact-braking, and audit residuals.

## Event Localization

Work 025 first reruns every contact to the earliest positive contact failure. The central energy solver then analytically localizes depletion from the net demand rate. The health solver constructs candidates for energy depletion, contact failure, component thermal failure, degradation/damage limits, and per-component seeded reliability hazard.

`arbitrate_event_candidates` chooses the earliest time and uses declared priority only for tolerance ties. Energy, component thermal state, degradation, damage, motion, and final time are recomputed or localized to the chosen duration.

For constant acceleration inferred from the Work 026 candidate, motion localization uses the corresponding kinematic equations. Race-distance progress is proportionally localized within the prospective step. If a central event occurs earlier than already-evaluated contact physics, persistent contact state remains at its start value rather than being falsely interpolated; the terminal event is observable and no later step may continue it.

## Thermal and Cooling Contract

Each central component declares lumped `ThermalParameters`, base heat generation, loss/cooling shares, degradation and damage laws, limits, and reliability hazard. Loss and cooling fractions each sum to one.

Mechanical brake heat remains owned by the contact brake thermal model and is not added to central components. Aerodynamic `conductance_w_per_k` replaces active component conductance according to declared shares. `heat_rejection_w` is retained as reference evidence, not subtracted again. Ambient temperature is mandatory configuration; no neutral default is inserted.

## Seed Contract

Each component receives a deterministic SHA-256-derived random stream from `(random_seed, step_index, component_id)`. Component registration order cannot change draws. Same-seed replay is exact; different seeds change draw evidence but need not change the winning event when an earlier deterministic event dominates.

## Architecture

`coupled-level0-reference-v3` preserves v2 and adds `energy.residuals` plus `state.motion_candidate` to the health stage. Energy and health adapter versions are `work027-central-energy-v1` and `work027-central-health-v1`.

## Validator Evidence

- `900 J` wheel work at efficiency `0.9` requires `1000 J` source energy; `100 J` auxiliary demand leaves `900 J` from a `2000 J` primary start.
- `1000 J` braking closes as `700 J` recovered + `100 J` conversion loss + `200 J` mechanical heat.
- A `550 J` store under `1100 W` net demand depletes at `0.5 s` with zero negative energy.
- A thermal fixture reaches `302 K` at `0.2 s`; motion localizes to `x = 2 m` and replay is exact.

## Limitations

Wheel work assumes no slip. Component heat and degradation are lumped. Reliability hazards are synthetic and uncalibrated. Cooling is conductance-based, not CFD. Central-event truncation retains start contact state when exact Work 018 rerun inputs are unavailable. These limits prevent physical-validation or safety claims.
