# Contact, Suspension, Brake, and Regeneration Coupling

Thai companion: `CONTACT_SUSPENSION_BRAKE_COUPLING.th.md`

## Boundary

Work 025 consumes Work 024 normal loads, the typed strategy command, and shared
contact state. It evaluates each uniquely identified contact through explicit
drive/brake allocation, Work 018 suspension/brake/regen, and the Work 011
combined tyre ellipse. No wheel count, axle, symmetry, or driven-contact layout
is prescribed.

## Explicit allocation and no redistribution

Drive and brake allocation fractions are declared per contact and each set must
sum to `1` within `1e-12`. Global drive force and brake torque requests are split
once. If one contact saturates, its unmet force/torque remains attached to that
contact; spare capacity elsewhere is not used silently.

Simultaneous nonzero throttle and brake is rejected because no blending policy
is declared. Contact IDs across specs, loads, shared state, and subsystem state
must match exactly. Negative wheel speed requires a future explicit reverse
model and is not converted with `abs()`.

## Per-contact sequence

1. Apply the central recovery fraction as a cap on available regen torque.
2. Evaluate subsystem torque capacity and suspension response.
3. Convert available longitudinal torque to contact force and combine with the
   lateral request through the tyre ellipse.
4. If combined saturation reduced brake force, rerun brake/regen/thermal at the
   projected torque so energy and temperature match road-transmitted torque.
5. Rotate contact-local forces by declared steer angle and calculate
   `Mz = x*Fy - y*Fx`.
6. Retain applied/unserved force, recovered energy, conversion loss, mechanical
   heat, storage margin, travel/failure state, and raw residuals.

Physical suspension/thermal failure is health evidence rather than numerical
invalidity. Malformed input or failed conservation residual returns atomic
invalidity with zero writes.

## Outputs and evidence

The adapter emits exactly `contact.force_moment`, `contact.energy_transfers`,
and `contact.health_inputs`. Residuals cover suspension force, brake torque, and
brake energy for every contact.

Work 027 extends the energy evidence with applied positive drive-wheel work and
requested/executed duration. If one contact reaches a positive failure time
first, all contacts are deterministically rerun to that common duration.
Persistent suspension velocity, brake temperature, recovered contact-store
energy, and latched failure flags are carried by `ContactRuntimeState`; an
external subsystem snapshot must match that shared state exactly.

The validator uses an arbitrary three-contact topology. Its low-load front
contact leaves force unserved without redistribution. Combined braking/steering
shows per-contact wheel energy exactly matching applied longitudinal force times
effective radius, angular speed, and duration. Replay is exact.

## Limitations

The tyre is a friction ellipse, suspension is lumped, and allocation is declared
rather than optimized. Work 027 centrally commits the persistent contact state,
but a central event earlier than the contact calculation retains the terminal
start contact state rather than inventing interpolation. Level-0 success is not
physical validation or real-race evidence.
