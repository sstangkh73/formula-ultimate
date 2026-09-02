# Work 081 Plan: STEP to FreeCAD Geometry Witness V2

Status: Completed

Thai companion: `2026-09-03_081_step-freecad-geometry-witness-v2-plan.th.md`

## Objective and scope

Independently import the exact five canonical Work 078 STEP artifacts with FreeCAD 1.1, without healing or geometry substitution, and produce deterministic SI geometry witnesses for topology, volume, bounding boxes, centres of mass, full inertia tensors, principal moments/axes, circular-feature signatures, and uniquely recoverable semantic interfaces. Compare the FreeCAD measurements against the frozen CadQuery exporter records and bind every result to the exact STEP bytes.

Work 081 will regenerate the frozen Work 078 artifacts with the pinned CadQuery environment into ignored `artifacts/work081/source_step/`, verify their exact preregistered SHA-256 values, then invoke FreeCAD as a separate process. This is an independent import/measurement route but remains a `toolchain_cross_check` because CadQuery and FreeCAD can share OCCT technology.

## Experiment design

- Independent variables: canonical part family, exact STEP bytes, measurement route, interface geometric signature, mapping-key order, and deliberate hash/topology/signature/expected-value mutations.
- Dependent variables: STEP SHA-256, shape/solid count, validity, volume, bounding box, centre of mass, inertia tensor, principal properties, recovered circular interface count/position/axis/diameter, residuals against frozen exporter evidence, and canonical report identity.
- Controls: all five Work 078 parts; key-order replay; changed STEP bytes; wrong expected hash; extra/missing solid; ambiguous or missing circular signature; changed expected volume; invalid/no-repair flag; and repeated FreeCAD runs.
- Preferred hypothesis: exact artifacts produce one valid unrepaired solid each, directly comparable global properties agree within `1e-6` relative, required semantic interface signatures are recovered uniquely without face numbers, and repeated runs have identical canonical report identities.
- Falsification: accepting altered bytes, repairing invalid geometry, using face indices, copying expected values instead of measuring, hiding unsupported measurements, or changing result identity under mapping-key permutation.

## Planned files

- `config/cad/step_freecad_geometry_witness_v2.json`
- `src/formula_ultimate/components/geometry_witness.py`
- `scripts/cad/inspect_geometry_witness_v2_freecad.py`
- `scripts/cad/compare_geometry_witness_v2.py`
- `tests/test_geometry_witness_v2.py`
- `docs/contracts/STEP_FREECAD_GEOMETRY_WITNESS_V2.md` and Thai companion
- matching Work 081 result files
- ignored evidence under `artifacts/work081/`

The existing Work 079 material/process fixture will remain synthetic unless the exact bracket measurements satisfy its full witness schema. Work 081 will not relabel unsupported manufacturing measurements as independent evidence.

## Validation and success criteria

- exact STEP hashes match the frozen Work 078 hashes for all five parts;
- FreeCAD reports one valid solid, positive finite SI volume, finite bounds/centre/inertia, and `hidden_geometry_repair=false` for every part;
- directly comparable FreeCAD/CadQuery volume and bounding-box relative residuals are `<=1e-6`;
- configured circular interface signatures are recovered uniquely by geometry class, radius, centre, and axis tolerances, never face number;
- malformed configs and hash/value/signature/topology mutations fail closed with causal codes;
- two independent FreeCAD report runs and comparison runs replay exactly;
- focused tests, repository-contract tests, compilation, and the full regression pass before a scoped commit.

## Risks and explicit non-goals

FreeCAD and CadQuery may share OCCT, so agreement is not physical validation. STEP does not preserve causal feature names; V2 therefore supports only measurable geometric signatures and explicitly reports unsupported wall/section/clearance claims. Full arbitrary wall-thickness minima, torsion constants, exact part-to-part interference, moving assembly clearance, manufacturing capability, material allowables, strength, fatigue, safety, and production approval are non-goals. If an interface cannot be recovered uniquely without face indices or exact bytes do not replay, Work 081 stops rather than relaxing the gate.
