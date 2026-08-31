# Work 063 Plan: Whole-Vehicle Geometric-Nonlinearity Gate

Status: Completed

Thai companion: `2026-08-31_063_whole-vehicle-nonlinear-gate-plan.th.md`

## Objective

Build and validate the reusable adapter required to bridge Work 062 linear-beam finalist evidence to a stricter candidate-derived geometric-nonlinearity check. Freeze its inputs, outputs, thresholds, and replay contract before any Work 062 finalist is evaluated; candidate execution will be a separately planned successor work item using the committed adapter.

## Experimental design

- Independent variable in later application: Work 062 finalist geometry; no geometry will be modified or optimized.
- Dependent variables: nonlinear solver convergence, maximum displacement and surface von Mises stress, nonlinear-to-linear displacement/stress amplification, and nonlinear yield margin for both frozen holdout load cases.
- Controls: exact Work 062 candidate declaration, Work 048 holdout loads, Work 053 synthetic material, fine mesh subdivision `16`, identical boundary conditions, CalculiX executable identity, and one frozen threshold configuration.
- Falsification: a candidate fails if any required process is missing/nonzero, geometric-nonlinearity confirmation is absent, outputs are invalid, displacement amplification exceeds `1.10`, stress amplification exceeds `1.15`, or nonlinear yield margin falls below `1.10`.
- Future selection contract: all and only Work 062 CAD-witness-passed candidates are included; outcomes cannot change the inclusion set.

## Scope and planned files

- Add `config/structural/whole_vehicle_nonlinear_gate_v1.json`.
- Add a reusable fail-closed nonlinear gate module under `src/formula_ultimate/structural/` and export it.
- Extend the B31 deck builder without changing its default linear output.
- Add unit/integration tests for deck identity, threshold boundaries, missing evidence, non-finite evidence, solver confirmation, and deterministic aggregation.
- Add bilingual gate-contract and result documentation.

## Validation and success criteria

Success requires a frozen versioned configuration, unchanged default linear deck output, deterministic fail-closed adjudication and fingerprinting, focused and full tests, compilation, bilingual documentation, and a scoped commit. The successor execution work must use this committed implementation and independently verify exact inclusion, terminal records, and replay.

## Risks and explicit non-goals

Risks include CalculiX nonlinear convergence, parser ambiguity across increments, dependence on beam idealization, and low-load responses too small to expose instability. This work does not run Work 062 finalists; that requires a separate post-commit work item. It also does not add initial imperfections, contact, solid elements, material plasticity, fracture, fatigue spectra, crash propagation, calibrated material data, manufacturing tolerances, hardware validation, independent replication, or a physical-safety claim. It is a geometric-nonlinearity sensitivity gate, not a buckling certificate or physical validation.
