# Ground-Interaction Candidate 001 Contract

Thai companion: `GROUND_INTERACTION_CANDIDATE_001.th.md`

## Claim boundary

This contract admits one bounded software/CAD verification specimen. It does not prescribe a general vehicle topology and does not validate a suspension, wheel, tyre, steering system, brake, bearing, production part, fatigue life, safety case, or physical behaviour.

The candidate verdict must remain `not_admitted_synthetic_evidence` and `design_use_allowed=false` while its material/process chain is `synthetic_verification`. A passing software result cannot override that evidence gate.

## Frozen candidate

The candidate contains five separate solids:

1. `structural_mount`: exact Work 081 `bracket_001.step`, also used by the Work 082 structural witness;
2. `guide_frame`: fixed guide with a pin entering the mount's cylindrical interface;
3. `carrier`: translating clevis-like carrier;
4. `axle`: force/torque transfer member; and
5. `contact_roller`: annular rotating contact body.

This is one candidate selected for inspectability. The evaluator's general admissible topology is not restricted to this arrangement or to historically conventional vehicle layouts.

## Kinematic contract

The SI frame is `+x` forward, `+y` left, and `+z` up. Five bodies provide `30` unconstrained spatial DOF. Fixed, fixed, prismatic, fixed, and revolute joints contribute `6 + 6 + 5 + 6 + 5 = 28` independent declared constraint rows, leaving exactly `2 DOF`:

- carrier-group vertical translation from `-0.007 m` to `+0.007 m`;
- contact-roller rotation about `+y`.

The CAD runner evaluates exact B-rep intersection volume and forbidden-pair distance at minimum, reference, and maximum travel. It does not suppress or repair intersections. Maximum overlap is `1e-12 m3`; minimum forbidden clearance is `0.0005 m`.

## Force, moment, torque, and energy contract

The reference ground force on the candidate is `[320, 180, 1250] N` at `[-0.04, 0, -0.139] m`. Its `+z` component must be strictly positive. The ground-force graph must contain exactly one continuous path:

`contact_roller -> axle -> carrier -> guide_frame -> structural_mount`

The drive/braking graph must contain exactly one `axle -> contact_roller` path. Reference drive torque is `42 Nm` at `80 rad/s` for `0.25 s`, with efficiency `0.92`. Reference braking torque is `-30 Nm`, opposing positive rotation. Force and moment reactions are explicit; drive work is split into delivered work and loss. Force and moment residuals must each be `<=1e-5`, and the energy residual must be `<=1e-4`. Non-finite values, efficiency outside `[0,1]`, or non-positive reference normal force fail closed.

## Geometry and structural evidence

CadQuery `2.8.0` generates four parts and imports the exact frozen mount. Every part is exported as a canonical STEP byte stream. The subsystem STEP must import as five separate valid solids. FreeCAD independently imports each exact part STEP, imports the assembly, records validity/volume/bounds, and saves an FCStd document containing five named `Part::Feature` objects. No healing call or hidden geometry repair is allowed.

The structural witness is exact-identity coupled to Work 082 result `3b5d82a7a60f68a8420f1fe5bea9915e494cc29f98bf568e1862903e929b805a` and bracket STEP `b06e3141f7a1fcad8017537d3680a787164d3190d4503417d3f6c1c98ed1ba89`. It covers only that bracket and load family. Its synthetic material identity must remain `72a1b5527e4aede10c6de73523c54835f11458f80100c6383d2a304d4d912097`, with `design_use_allowed=false`.

## Required falsification controls

- `mirror`: lateral force and force-direction angle change sign; normal force remains unchanged.
- `rigid_no_travel`: declared translation becomes zero and mobility falls to one.
- `disconnected_mount`: force-path count and transmitted force become zero; state is `dnf`.
- `blocked_translation`: realized travel becomes zero and state is degraded.
- `seized_rotation`: angular speed and delivered mechanical power become zero.
- `broken_torque_path`: torque-path count and delivered torque become zero.
- `undersized_capacity`: utilization must exceed one and state becomes `dnf`.
- `contact_loss`: normal, longitudinal, and lateral contact forces become zero; state is `dnf`.

Every control must remain present and produce its preregistered measurable consequence. A missing or ineffective control fails evaluation.

## Replay and failure semantics

Two clean runs compare the declaration, every part STEP, assembly STEP, geometry manifest, canonical FreeCAD report, evaluation, structural evidence, and result identities. STEP timestamps are replaced with the fixed value `1970-01-01T00:00:00`; FCStd bytes are not treated as deterministic evidence because its container metadata may vary. The canonical FreeCAD measurement report is the replay identity for the FCStd witness.

Any schema extension, changed identity, missing solid, invalid shape, clearance/overlap violation, broken reference path, ledger residual above its gate, relabelled synthetic evidence, non-causal fault control, or replay mismatch fails closed. There is no result-conditioned geometry repair.
