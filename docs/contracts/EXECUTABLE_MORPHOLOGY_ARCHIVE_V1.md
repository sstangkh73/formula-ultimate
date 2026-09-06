# Executable Morphology, Architecture and Archive Contract V1

Thai companion: `EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.th.md`

Status: Implemented by Work 099

## 1. Scope and claim boundary

This contract implements a bounded executable morphology loop on top of the Work 098 discovery ledger. It proves that numerical genes can instantiate real CadQuery solids, change measured geometry, change part/interface decomposition, retain typed terminal ancestry and populate deterministic bounded archives. Its evidence scope is `software_fixture_with_executed_cad` / `morphology_software_fixture_only`.

The output is not physical feasibility, manufacturing feasibility, race performance, technology novelty or physical validation. No field solver runs. Archive names `feasible`, `failed` and `unresolved` describe this registered morphology software fixture only; they must not be relabeled as Work 100 physics states or scientific survivors. The reused Work 098 registration has evidence class `software_fixture`, and the runner requires the scientific survivor count to remain zero.

## 2. Executable representation

`src/formula_ultimate/search/executable_morphology.py` defines `executable_swept_network_v1`. A genotype contains:

- variable-length material regions/parts;
- finite SI-metre node positions and bounded radius fields;
- connected swept-solid edges within each part;
- typed part interfaces with endpoint-node and ancestry records;
- external terminals with role, domains and ancestry;
- an optional registered controller gene.

The implementation permits up to 8 parts, 24 nodes per part, 32 edges per part, 16 interfaces and 12 terminals under the committed fixture. Radius is bounded to `[0.002, 0.04] m`, coordinates to `±0.5 m`, and edge length must be at least `0.002 m`. Every part and the part-interface architecture must be connected. Source and sink terminals are mandatory. Non-finite values, stale node references, missing ancestry and disconnected graphs fail before CAD.

This V1 is a swept sphere/cylinder solid-network representation, not arbitrary CAD. It supports multiple physical regions; it does not require one universal single solid or prescribe a conventional vehicle layout.

## 3. Registered operators and lineage

The exact operator schedule is:

1. `perturb_node`
2. `grow_branch`
3. `split_part`
4. `rewire_interface`
5. `merge_parts`
6. `mutate_radius_field`
7. `mutate_controller`

Every call pins parent/child genotype digests, parent/child functional signatures, seed, step, numerical parameters and whether geometry or architecture is declared to change. `split_part` may only move a non-terminal, non-interface leaf into a new material region; it adds a typed interface with split ancestry. `merge_parts` consumes an interface, unifies its endpoint nodes and rewrites affected terminals/interfaces without erasing ancestry. A controller-only change is never labeled geometry change.

The functional signature is ID-invariant and refines part labels from internal node degree, terminal role/domain/ancestry and typed neighboring interfaces. It is a deterministic diversity signature for this bounded representation, not a general proof of graph isomorphism or functional novelty.

## 4. CAD execution and measurement

`scripts/experiments/run_executable_morphology_qd.py` creates one sphere at each node and one cylinder for every edge, fuses each connected part and exports the parts as a STEP compound. Export timestamps are canonicalized before hashing. No automatic geometry healing is allowed.

For every successful genotype the runner records:

- STEP SHA-256 and measurement SHA-256;
- volume in `m^3`, surface area in `m^2`, bounds and centre in `m`;
- solid, face and edge counts;
- per-part volume/area;
- terminal positions, roles, domains and ancestry;
- boundary identity derived from measured terminals and declared interfaces.

Every declared geometry operator must change the STEP digest and at least one measured field relative to its parent. `split_part` and `merge_parts` may demonstrate decomposition change through solid/topology counts even when total occupied material is otherwise similar. Transform-only or identifier-only changes are not registered geometry operators.

## 5. Work 098 ledger integration

Each genotype is appended as a Work 098 candidate with immutable parent links and mutation trace. Geometry validation/CAD execution and terminal binding are separately reserved, started and settled. Successful execution seals `geometry_sha256`; successful terminal binding seals `boundary_sha256`. A zero-length injected specimen becomes `representation_invalid`. One valid CAD specimen receives an injected, explicitly synthetic ambiguous-terminal diagnostic and becomes `boundary_unresolved`. Neither is collapsed into a physical failure.

Observed CPU/wall time and CAD/attempt counters are charged to the Work 098 ledger. The archive uses deterministic opportunity cost (`attempts + geometry_executions + cad_calls`) for ordering, while variable CPU/wall timing remains separate evidence. This prevents runtime noise from changing cross-run archive identity without hiding actual measured timing.

The ledger is reopened with its trusted head. Exact decision replay means the same stored events reproduce the same state and accounting. Cross-run execution replay compares genotype, functional, STEP and measurement identities, numerical fields under registered tolerances, and archives; timing is reported but not compared for identity.

## 6. Bounded quality-diversity archive

Niches use causal/topological descriptors rather than visual curvature:

- part count;
- part-interface cycle rank;
- internal branch-node count;
- terminal-domain count.

Each niche has separately bounded `feasible: 2`, `failed: 1` and `unresolved: 1` slots. Feasible records rank by fixture quality then novelty/cost; failed records rank by measured margin then novelty/cost; unresolved records prefer lower deterministic opportunity cost. Stable candidate-ID tie-breaking makes decisions replayable. Novelty cannot change a record's disposition, erase failure or broaden evidence scope.

The per-niche reproduction caps are one record from each disposition. This demonstrates bounded stepping-stone permissions, not an empirical claim that failed or unresolved reproduction improves discovery. Evicted archive entries remain immutable in the Work 098 ledger even though the active archive stays bounded.

## 7. Commands and evidence

Run pure contract tests with the repository Python:

```powershell
python -m unittest tests.test_executable_morphology_qd -v
```

Run all tests including actual CadQuery execution, then two independent fixtures:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' -m unittest tests.test_executable_morphology_qd -v
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_a
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_b --replay-reference artifacts/work099/run_a/result.json
```

The final verified runs contain 18 candidates, 10 explicit geometry-change proofs, 6 functional signatures and 3 archive niches. Each ledger contains 120 append-only rows and reopens exactly at its trusted head. Cross-run deterministic evidence SHA-256 is `727b75d305bb6e0ae7111d553c73ee9fc8f4cae059e7d5a8602abbfcd2d4515d`; all compared geometry measurements differed by `0.0` in the observed rerun. The active bounded archive retained 5 feasible, 1 failed and 1 unresolved fixture records. These counts characterize the software fixture, not search performance.

## 8. Limitations and next work

This implementation has no geometry-derived stress, thermal, flow, contact, motion or energy field solver; no manufacturing process evaluator; no vehicle task; no optimization baseline; and no statistical archive-retention experiment. CAD validity and reproducibility do not establish usefulness. The functional signature can collide for some non-isomorphic graphs because it is a bounded refinement signature rather than an exhaustive isomorphism solver.

Work 100 must introduce independently validated, geometry-derived local/coupled evaluators and preregistered contrasts before any `physically_feasible` or `candidate_survivor` interpretation. Work 101 remains responsible for complete-vehicle integration, holdout/independent promotion and fair optimized baseline evidence.
