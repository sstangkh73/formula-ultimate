# Work 083 Plan: Ground-Interaction Candidate 001

Thai companion: `2026-09-03_083_ground-interaction-candidate-001-plan.th.md`

## Status

Status: Completed

## Objective

Create one inspectable, replayable multi-part mechanical candidate that transfers normal, longitudinal, and lateral ground forces to a structural mount; carries drive and braking torque to contact; permits a declared vertical translation and contact-body rotation; and fails observably when a critical path is broken.

This is one generated candidate, not a prescribed vehicle architecture. The work may complete its software and CAD verification while its design-admission verdict remains negative because the available material/process evidence is synthetic.

## Scope and frozen experiment

- Freeze a five-part candidate before evaluation: structural mount, guide frame, translating carrier, axle, and annular contact roller.
- Use SI values in the declaration and convert to millimetres only at the CadQuery boundary.
- Calculate assembly mobility from explicit joint constraint rows: fixed mount, fixed guide, prismatic carrier, fixed axle, and revolute roller.
- Evaluate declared vertical travel, exact-part clearance at travel extrema, positive normal force, force/moment closure, drive/brake energy closure, and continuous mount/torque paths.
- Run controls for mirror symmetry, rigid/no-travel, disconnected mount, blocked translation, seized rotation, broken torque path, undersized capacity, and contact loss.
- Reuse the exact Work 082 structural-mount coupling evidence as a bounded structural witness; do not generalise it to the other parts.
- Generate each part and the complete assembly as canonical STEP, and save a FreeCAD FCStd witness containing separate imported solids.
- Execute two clean CAD/replay runs and compare declaration, part, assembly, FreeCAD summary, and evaluation identities.

Independent variables are topology, part geometry, joint type/location, travel, contact radius, force vector, torque, angular speed, efficiencies, connection state, capacity scale, and mirror state. Dependent variables are part count and identities, mobility, travel, clearance, normal force, transmitted wrench, torque, power/work, equilibrium and energy residuals, structural-witness state, subsystem state, control response, and replay identity. The reference candidate and frozen mirror are the positive controls; every injected fault is a falsification control.

## Planned files

- `config/candidates/ground_interaction_candidate_001.json`
- `src/formula_ultimate/subsystems/__init__.py`
- `src/formula_ultimate/subsystems/ground_interaction.py`
- `scripts/candidates/build_ground_interaction_candidate_001.py`
- `scripts/candidates/inspect_ground_interaction_freecad.py`
- `tests/test_ground_interaction_candidate_001.py`
- `docs/contracts/GROUND_INTERACTION_CANDIDATE_001.md` and Thai companion
- this plan and Thai companion
- matching result and Thai companion after validation
- ignored generated evidence under `artifacts/work083/`

## Validation

1. Run the candidate builder twice in the pinned CadQuery environment.
2. Import each exact part and the assembly through FreeCAD without repair, save FCStd, and measure separate solids.
3. Compare exact replay identities and run all declared functional/failure controls.
4. Run focused unit and repository-contract tests, compile all Python sources, then run the full test suite.
5. Stage only Work 083 files, inspect the staged scope, run `git diff --cached --check`, commit, and repeat focused post-commit validation.

## Success criteria

- Five separate valid part solids and one assembly STEP/FCStd witness are present.
- Calculated mobility is exactly two DOF: one declared vertical translation and one contact-body rotation.
- Reference travel and geometric clearance pass without hidden repair or interference suppression.
- A unique continuous force path reaches the mount and a unique torque path reaches contact.
- Force and moment residuals are each `<=1e-5`; energy residual is `<=1e-4`.
- Structural evidence is exact-identity coupled and remains explicitly synthetic-only.
- Every required injected fault causes the declared measurable change; critical disconnection or contact loss causes `DNF`.
- Two runs reproduce the declaration, part STEP, assembly STEP, evaluation, and canonical FreeCAD summary hashes.
- The candidate verdict is `not_admitted_synthetic_evidence`, never a real-world validation claim.

## Risks

- Assembly placement or tolerance may create unintended overlap through travel.
- STEP or FCStd serialization may contain timestamps; only explicitly canonicalised evidence may be used for exact replay.
- Simple quasi-static equations can verify bookkeeping but cannot establish tyre/contact, fatigue, bearing, or dynamic performance.
- Reused Work 082 evidence covers only its exact bracket/load family and uses synthetic material properties.

## Explicit non-goals

- No claim of a validated suspension, wheel, tyre, steering, brake, bearing, production part, safety case, fatigue life, or physical test.
- No topology preference is added to the general evaluator from this single candidate.
- No hidden repair, force clipping, overlap suppression, result-conditioned geometry mutation, or synthetic-to-design evidence relabelling.
- No Work 084 energy converter, Work 085 integrated load structure, or Work 086 whole vehicle.
