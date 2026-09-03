# Work 084 Plan: Energy Conversion and Torque-Path Candidate 001

Thai companion: `2026-09-03_084_energy-torque-path-candidate-001-plan.th.md`

## Status

Status: Partial

## Objective

Replace the abstract energy-converter box and scalar drive ratio with one
inspectable, replayable multi-part candidate that carries a declared onboard
primary energy store through a converter, a geometry-realised torque
transformation, reaction supports, and a housing with cooling and lubrication
interfaces, into the frozen Work 083 ground-interaction torque interface.

The candidate declares a specific energy technology without making the evaluator
prefer a historically conventional powertrain layout. As in Work 083, the
software and CAD work may complete while the design-admission verdict stays
negative, because the available material, process, and measurement evidence is
`synthetic_verification`.

## Scope and frozen experiment

Freeze a seven-part candidate before evaluation:

1. `energy_store` — hollow vessel carrying the declared pre-race primary energy;
2. `converter_housing` — bore, mount interface, cooling fins, two coolant
   passages, and one lubrication feed port;
3. `converter_rotor` — rotating converter output body inside the housing bore;
4. `input_shaft` — rotor-side torque member and drive traction radius;
5. `ratio_drum` — driven traction radius and torque transformation body;
6. `output_shaft` — coaxial member terminating at the Work 083 axle interface;
7. `support_block` — reaction support carrying the output-group bearing bore.

Frozen rules for the work:

- SI in the declaration; millimetres only at the CadQuery boundary; frame is
  `+x` forward, `+y` left, `+z` up, identical to Work 083.
- Mobility is calculated from an explicit constraint tree of seven joints plus
  one separately declared loop-closing rolling coupling row. The declared and
  calculated result must be exactly `1 DOF` about `+y`.
- The kinematic ratio is `driven_radius / drive_radius` taken from the two
  frozen radii that also generate the B-rep, never a free scalar.
- Exact B-rep clearance and interference are evaluated for every part pair.
  Joined and coupled pairs are declared separately from forbidden pairs; no
  overlap suppression or healing is allowed anywhere.
- The torque graph must contain exactly one continuous path from
  `converter_rotor` to the Work 083 `contact_roller`, crossing the Work 083
  `axle` node, and the Work 083 leg must be identity-coupled to the frozen
  Work 083 result and assembly hashes.
- The reaction graph must contain exactly one continuous path from
  `converter_housing` to the declared structure terminal.
- The energy ledger enforces onboard pre-race primary energy, zero external
  primary inflow, efficiencies inside `[0,1]`, and a recovered-energy source
  that traces to a declared conserved braking source.
- The thermal ledger uses the geometry-derived housing mass, the geometry-derived
  fin-added convective area, and the geometry-derived coolant passage
  cross-section. Coolant velocity, coolant temperature rise, and housing
  temperature must each stay inside declared domains without clipping.
- Structural margins for `output_shaft`, `support_block`, and
  `converter_housing` are analytic and geometry-derived, and are labelled
  `analytic_synthetic_verification`. They are explicitly not a meshed solve.

Independent variables are declared technology, topology, traction radii, shaft
and support sections, support spacing, speed and torque schedule, converter and
mechanism efficiencies, recovery efficiency, coolant declaration, housing
geometry, connection state, and mirror state. Dependent variables are part
identities, mobility, ratio, clearances, transmitted torque, reaction wrench,
delivered power, energy and thermal residuals, coolant velocity and temperature
rise, housing temperature, analytic structural margins, subsystem state, control
response, and replay identity. The reference candidate and its frozen mirror are
positive controls; every injected fault is a falsification control.

## Declared controls

`mirror`, `locked_converter`, `seized_support`, `broken_coupling`,
`zero_loss_exploit`, `efficiency_over_one`, `reversed_torque`, `overspeed`,
`inadequate_cooling`, and `disconnected_housing_reaction`. Each must produce its
preregistered measurable consequence; a missing or ineffective control fails the
evaluation.

## Planned files

- `config/candidates/energy_torque_path_candidate_001.json`
- `src/formula_ultimate/subsystems/energy_torque_path.py`
- `src/formula_ultimate/subsystems/__init__.py` (export update)
- `scripts/candidates/build_energy_torque_path_candidate_001.py`
- `scripts/candidates/inspect_energy_torque_path_freecad.py`
- `tests/test_energy_torque_path_candidate_001.py`
- `docs/contracts/ENERGY_TORQUE_PATH_CANDIDATE_001.md` and Thai companion
- this plan and Thai companion
- matching result and Thai companion after validation
- ignored generated evidence under `artifacts/work084/`

## Validation

1. Run the candidate builder twice in the pinned CadQuery environment under
   separate output roots.
2. Import every exact part STEP and the assembly STEP through FreeCAD without a
   healing call, save an FCStd witness holding seven named solids, and emit a
   canonical measurement report.
3. Compare declaration, part, assembly, FreeCAD report, evaluation, and result
   identities between the two runs.
4. Run the focused unit tests and `tests.test_repository_contract`, compile all
   Python sources, then run the full test suite.
5. Stage only Work 084 files, inspect the staged scope, run
   `git diff --cached --check`, commit, and repeat focused post-commit
   validation.

## Success criteria

- Seven separate valid part solids and one seven-solid assembly STEP and FCStd
  witness exist.
- Calculated mobility is exactly `1 DOF`; the calculated ratio equals
  `driven_radius / drive_radius` exactly.
- The single torque path reaches the frozen Work 083 contact body and the single
  reaction path reaches the declared structure terminal.
- Torque and reaction residuals are each `<=1e-5`; the energy residual and the
  thermal residual are each `<=1e-4`.
- Efficiencies stay inside `[0,1]`; external primary inflow is exactly `0 J`;
  final store energy does not exceed initial store energy; recovered energy
  traces to the declared conserved braking source with its loss recorded.
- Coolant velocity, coolant temperature rise, and housing temperature stay
  inside declared domains, and the housing temperature rise is derived from the
  CadQuery housing volume rather than a typed constant.
- Every declared control produces its preregistered measurable consequence.
- Two runs reproduce every canonical identity exactly.
- The candidate verdict is `not_admitted_synthetic_evidence`.

## Known gate that this work does not close

The Work 084 completion gate in `WORKS_080_086_DETAILED_EXECUTION_PLAN.md`
requires that shaft, support, and housing structural cases pass Work 082 gates
or fail observably. The Work 082 evaluator maps its loaded region as a
`z`-axis cylindrical hole and its support as a constant-`x` plane, so it cannot
accept this candidate's `y`-axis bores, torsional loading, or bearing reactions
without changing the frozen Work 082 configuration identity. Program rule 4.1
forbids that change, and `WORK_PROTOCOL.md` forbids silently expanding the
current work item.

Work 084 therefore delivers analytic geometry-derived torsion, bearing, and
housing margins and records the meshed structural gate as **not met**. If the
declared validation otherwise passes, this work closes as `Partial`, not
`Completed`, and a separately numbered remedial work must add a generalised
meshed torsion/bearing/housing route before Gate B or Work 085 may be claimed.

## Risks and controls

- A large driven radius could place the drum below the Work 083 contact plane.
  Control: freeze `driven_radius_m` below the Work 083 roller radius and report
  the resulting ground clearance as measured evidence.
- Exactly tangent traction cylinders make B-rep intersection numerically
  fragile. Control: declare a finite radial engagement gap, treat the traction
  pair as a coupling pair rather than a forbidden pair, and state that the
  engagement elements are not modelled.
- The coupling to Work 083 is a coaxial butt interface with no modelled fastener.
  Control: verify coaxiality, radius, and end-plane coincidence from geometry
  and record the absent fastener as a limitation, not as a validated joint.
- Algebraically paired ledgers can return near-zero residuals without physical
  content. Control: derive rejection from the independent coolant declaration
  and housing geometry so that closure is a check rather than an identity, and
  record the remaining circularity.
- STEP and FCStd containers may carry volatile metadata. Control: canonicalise
  the STEP timestamp and treat only the canonical FreeCAD report as replay
  evidence for the FCStd witness.

## Explicit non-goals

- No claim of a validated motor, engine, battery, fuel, transmission, clutch,
  bearing, coupling, lubrication system, or cooling system.
- No claim of technology superiority, efficiency realism, manufacturing
  readiness, safety, fatigue life, or physical validation.
- No meshed structural solve for the shaft, support, or housing.
- No modelled speed decay during the braking segment.
- No packaging, service-path, or vehicle-scale interference resolution; that is
  Work 085.
- No hidden repair, force or temperature clipping, overlap suppression,
  result-conditioned geometry mutation, or synthetic-to-design evidence
  relabelling.
- No Work 085 integrated load structure and no Work 086 whole vehicle.
