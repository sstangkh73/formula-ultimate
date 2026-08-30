# Work 048 Plan: Whole-Vehicle Load Cases and Structural Coupling

Status: Completed

Thai companion: `2026-08-30_048_whole-vehicle-load-cases-plan.th.md`

## Objective

Transform frozen Level 0 vehicle snapshots into traceable, balanced quasi-static structural load cases for the admitted Work 047 assembly, then couple bounded interface demand to the Work 046 structural-failure contract without silently inventing unsupported evidence.

## Scope and planned files

- Add a versioned load-case manifest under `config/vehicle/` containing training and holdout snapshots, frame definitions, immutable evidence identities, and structural limits.
- Add a load-case module under `src/formula_ultimate/simulation/` for snapshot validation, rigid-body wrench balance, component/interface load transfer, analytical bounded structural response, failure-coupling inputs, and deterministic identities.
- Add an acceptance runner and `scripts/run_work048.ps1` that write ignored evidence under `artifacts/work048/`.
- Add focused tests, a bilingual physics report, and matching bilingual result records.

## Experiment definition

- Independent variables: frozen case identifier and partition, translational acceleration, gravity, aerodynamic wrench, external contact wrenches, component mass state, and declared interface capacity.
- Dependent variables: component and interface six-axis wrenches, global and local force/moment residuals, demand/capacity ratio, structural state/event, and manifest/replay hashes.
- Controls: exact Work 047 declaration and STEP identities, one immutable snapshot per case, SI units, one assembly frame, fixed load-path graph, fixed Work 046 failure-policy identity, frozen training/holdout membership, and unchanged thresholds.
- Falsification controls: unbalanced external wrench, missing evidence, altered geometry identity, unsupported dynamic/contact evidence, duplicate partition membership, and deliberately overloaded interface.

## Validation

1. Unit tests for frame/wrench algebra, residuals, partitions, identity rejection, overload coupling, and exact replay.
2. Acceptance run across straight acceleration, braking, cornering, combined manoeuvre, bump, aero extreme, and a holdout mass-state extreme.
3. Require global and every interface force/moment residual `<= 1e-5` in SI units.
4. Require mapped mass/inertia agreement with Work 047 FreeCAD evidence within `1e-6` relative.
5. Require unsupported or incomplete evidence to reject promotion with no neutral numeric substitution.
6. Run the full repository test suite, compile checks, repository-contract checks, and Git whitespace checks.

## Success criteria

- Every applied wrench traces to one frozen snapshot and exact geometry/material/failure-policy identity.
- Training and holdout partitions are immutable, disjoint, and hashed before Work 050.
- All admitted nominal cases balance and produce deterministic structural results; the deliberate overload produces the expected degraded/failed state or `DNF` through the bounded coupling contract.
- Repeated runs preserve exact result hashes and provenance.

## Risks

The Work 047 grammar has translation-only primitives and idealized interfaces. Quasi-static equivalent loads can balance algebraically while omitting transient, contact, vibration, or local stress effects. Analytical interface demand is a bounded adapter, not arbitrary whole-vehicle FEA or physical validation.

## Explicit non-goals

No transient crash, vibration, random road, CFD, tyre-test calibration, contact/preload/friction, arbitrary free-form FEA, physical-track validation, design search, push, or publication is included.
