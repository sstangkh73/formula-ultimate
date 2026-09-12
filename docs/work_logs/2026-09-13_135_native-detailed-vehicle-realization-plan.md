# Work 135 Plan: Native Detailed Vehicle Realization

Thai companion: `2026-09-13_135_native-detailed-vehicle-realization-plan.th.md`

Date: 2026-09-13 (Asia/Bangkok)

Status: Completed

## Objective

Execute the approved Work 135 detailed plan by realizing one exact candidate as inspectable native OCCT B-rep part solids and a physically connected assembly. Replace the Work 126 box registry as geometry evidence while retaining it only as an architecture-neutral function checklist.

## Scope and planned files

- Pin the consumed commits, contract/result hashes, installed geometry runtimes, candidate identity, task/energy/safety boundary, complete required-occurrence inventory and deterministic thresholds.
- Implement `src/formula_ultimate/assembly/native_detailed_vehicle.py` for strict declaration parsing, semantic identities, occurrence completeness, assembly/interface/tolerance/motion validation, ledgers, physics-boundary ownership and falsification controls.
- Add `config/development/native_detailed_vehicle_v1.json` for the frozen candidate and admitted gates.
- Add `scripts/cad/build_native_detailed_vehicle.py` for deterministic native parts, per-definition STEP files and separate-solid assembly STEP.
- Add `scripts/cad/inspect_native_detailed_vehicle_freecad.py` for exact no-repair FreeCAD import, native-property cross-checks and FCStd witness generation.
- Add `scripts/development/run_native_detailed_vehicle.py` for admitted orchestration, artifacts, all negative controls and clean replay comparison.
- Add `tests/test_native_detailed_vehicle.py` and bilingual `docs/contracts/NATIVE_DETAILED_VEHICLE_V1.md` / `.th.md`.
- Create the matching bilingual Work 135 result. Update other maintained files only when required by an explicit repository contract, recording each addition in the result.

Generated evidence is restricted to ignored `artifacts/work135/{pilot,run_a,run_b,negative_controls}` paths.

## Validation

Run the exact CadQuery builder and FreeCAD inspector, admitted `run_a`, clean `run_b`, the Work 135 unit/negative-control suite, affected geometry/assembly/motion/energy/flow/control regressions, compilation, repository contract and Git whitespace/staged-scope gates. Each command must retain its own exit status.

## Success criteria

- Required physical-occurrence coverage is exactly `1.0`, with zero unknown essential occurrence and no unsupported purchased proxy.
- Every material occurrence is a valid native solid with unique ownership; required voids, routes, interfaces, fasteners, seals, supports and service relations are explicit.
- CadQuery/FreeCAD relative volume and mass residuals are `<= 1e-8`, center residual is `<= 1e-7 m`, componentwise inertia residual is `<= 1e-7`, and counts/signatures survive exact import without hidden repair.
- Mating residual is `<= 1e-6 m`, non-contact penetration is `<= 1e-12 m^3`, motion uses at least 101 samples with refinement convergence `<= 1e-5 m`, and preview chord is `<= 0.00025 m`.
- All eighteen falsification controls are rejected for their declared reason; `run_a` and clean `run_b` evidence hashes match exactly.
- The final admitted status is `passed_native_detailed_geometry`. This status is only a geometry/assembly gate.

## Risks and explicit non-goals

Missing exact geometry, incomplete occurrence ownership, unresolved assembly, lost semantic boundaries or replay drift stops completion; none may be hidden with bounding boxes or manual aggregate properties. CadQuery and FreeCAD share OCCT and therefore provide a cross-application witness, not independent-kernel validation.

This work does not prescribe a conventional vehicle layout, prove performance benefit, rerun downstream structural/thermal/flow/energy/control physics, establish manufacturing readiness or safety, authorize fabrication, perform physical validation, push or rewrite history. Downstream physics revalidation belongs to a separate Work 136.
