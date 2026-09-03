# Work 082 Plan: Geometry-to-Structural Physics Coupling V1

Status: Completed

Thai companion: `2026-09-03_082_geometry-structural-coupling-v1-plan.th.md`

## Objective and scope

Implement a fail-closed coupling from an exact Work 081 STEP identity and recovered geometric regions into a three-level meshed CalculiX structural experiment. The bounded reference will use one canonical Work 078/081 part, immutable support/load signatures, explicit SI load provenance, exact Work 079 material identity, solver-result parsing, convergence/residual gates, failure classification, and causal connection-state propagation.

Because Work 079 material/process evidence remains synthetic, Work 082 is limited to `synthetic_verification`. Completion means the geometry-to-mesh-to-solver-to-failure software path and its controls are verified; it must return `design_use_allowed=false` and cannot establish real-part capacity.

## Experiment design

- Independent variables: exact STEP hash, mesh characteristic length, support/load region signatures, load magnitude/direction, synthetic material identity/properties, section geometry, connection criticality, and injected solver/material/path faults.
- Dependent variables: node/element counts, displacement, stress, reactions, strain energy, force/moment/energy residuals, last-two refinement change, failure class, transmitted wrench, connection state, subsystem state, and deterministic identities.
- Controls: three frozen mesh levels, key-order replay, reversed load, thicker analytical control, changed STEP hash, missing support/load surface, disconnected mesh/path, below-yield reference, yield/ultimate-domain overload, unsupported fracture/fatigue domain, critical versus redundant connection, and solver non-convergence injection.
- Preferred hypothesis: exact geometry and region identities reach all solver artifacts, reactions and energy close inside declared gates, admitted response converges, and a critical structural failure removes the transmitted wrench and creates deterministic `DNF`.
- Falsification: substituting typed dimensions for geometry, accepting a stale STEP/report hash, hiding non-convergence, silently clipping stress/failure, transmitting load after connection failure, or approving synthetic material for design use.

## Planned files

- `config/structural/geometry_structural_coupling_v1.json`
- `src/formula_ultimate/structural/geometry_coupling.py`
- `scripts/structural/run_geometry_structural_coupling.py`
- `tests/test_geometry_structural_coupling.py`
- `docs/contracts/GEOMETRY_STRUCTURAL_COUPLING_V1.md` and Thai companion
- matching Work 082 result records
- ignored meshes, decks, solver outputs, parsed evidence, and replay records under `artifacts/work082/`

## Validation and success criteria

- exact Work 081 part/report/interface identities must bind into every mesh-level record;
- three mesh refinements execute through the pinned local Gmsh/CalculiX toolchain without geometry mutation;
- integrated reaction force/moment relative residual is `<=1e-5` and strain-energy/work relative residual is `<=1e-4`;
- last-two admitted displacement/compliance and non-singular stress changes are `<=5%`;
- negative controls reject stale identity, missing region/path, unsupported evidence, invalid/numerical state, and failed residual/convergence;
- failure causally changes connection state and transmitted wrench; declared critical failure yields deterministic `DNF`;
- exact replay, focused tests, repository contract, compilation, and full regression pass before a scoped commit.

## Risks and explicit non-goals

Pointwise peak stress near idealized constraints may be singular and is not an admitted metric; use declared non-singular/integrated metrics. Shared OCCT geometry paths are not physical validation. Synthetic material values cannot support real allowable, fatigue/fracture life, crashworthiness, safety, or production claims. If the solver does not converge, residuals do not close, mesh response does not refine, or the structural event does not change the connection graph, Work 082 stops rather than substituting a lower-fidelity result.
