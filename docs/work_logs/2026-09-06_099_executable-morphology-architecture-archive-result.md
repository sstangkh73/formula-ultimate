# Work 099 Result: Executable Morphology, Architecture and Archive Search

Thai companion: `2026-09-06_099_executable-morphology-architecture-archive-result.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Outcome and files changed

Implemented the bounded Work 099 executable-morphology deliverable after reviewing completed Work 098 commit `ec0004b`. Numerical swept-solid genes now execute in CadQuery, architecture operators split/merge parts and rewire typed interfaces, measured geometry and terminal ancestry enter the Work 098 ledger, and a bounded multi-disposition archive replays deterministically. No completed Work 098 file or historical roadmap was changed.

Intended commit scope is 11 files:

- `src/formula_ultimate/search/executable_morphology.py`
- `src/formula_ultimate/search/morphology_archive.py`
- `config/experiments/executable_morphology_qd_v1.json`
- `scripts/experiments/run_executable_morphology_qd.py`
- `tests/test_executable_morphology_qd.py`
- `docs/contracts/EXECUTABLE_MORPHOLOGY_ARCHIVE_V1.md` and `.th.md`
- this result, the matching plan and both Thai languages' companion files

Generated evidence is retained under ignored `artifacts/work099/`, including final `run_a`, `run_b`, `full_suite.txt` and `full_suite.exit.txt`, plus preserved developmental pilots.

## Implemented decisions and behavior

- Added a strict `executable_swept_network_v1` genotype with finite SI-metre node/radius fields, connected material regions, typed interfaces, terminal ancestry and optional controller genes. Bounds are explicit and fail closed.
- Added deterministic `perturb_node`, `grow_branch`, `split_part`, `rewire_interface`, `merge_parts`, `mutate_radius_field` and `mutate_controller` operators. Every child records exact parameters and parent/child identities. Geometry and architecture changes are declared separately.
- `split_part` cannot move terminal or existing interface endpoints. `merge_parts` unifies the consumed interface nodes and rewrites dependent terminals/interfaces while preserving lineage.
- CadQuery executes spheres and swept cylinders from the numerical genes, validates each connected region, exports canonicalized STEP and measures volume, area, bounds, centre, solid/face/edge counts, per-region measurements and terminal positions.
- Every registered geometry operator must change both STEP digest and at least one measured field. Identifier or controller-only changes cannot satisfy that gate.
- Work 098 candidate, reservation, start and settlement events charge every proposal/attempt. Geometry and boundary identities seal separately; an injected zero-length specimen remains `representation_invalid`, while one valid-CAD ambiguous-terminal fixture remains `boundary_unresolved`.
- The archive uses part count, interface cycle rank, branch-node count and terminal-domain count. Each niche separately bounds morphology-fixture `feasible`, `failed` and `unresolved` records. Novelty cannot erase failure or expand claim scope.
- Variable CPU/wall timings stay in ledger/report evidence. Deterministic archive ordering uses registered opportunity counters, preventing runtime noise from changing cross-run decisions.

## Executed CAD and replay evidence

Both final runs produced:

- 18 candidate records across seeds `7` and `19`;
- 10 explicit geometry-change proofs;
- 6 distinct bounded functional signatures;
- 3 archive niches retaining 5 feasible, 1 failed and 1 unresolved software-fixture records;
- 120 append-only ledger rows per run;
- zero scientific survivors and `physical_validation: false`.

The shared deterministic evidence SHA-256 is `727b75d305bb6e0ae7111d553c73ee9fc8f4cae059e7d5a8602abbfcd2d4515d`. The final archive SHA-256 is `5c9d0ec677f936dbb64be16da749e85512c61bf21c8cf3f6aefdafce17024091`. Cross-run execution comparison was `identity_exact: true`, with maximum observed absolute and relative geometry-measurement differences both `0.0`; timing was reported separately and not treated as identity.

Each ledger reopened exactly at its trusted head. Because actual CPU/wall observations differ, ledger head/state hashes legitimately differ between independent executions; exact decision replay applies to reopening each immutable event stream, while cross-run execution replay applies registered geometry/measurement tolerances.

Example decomposition evidence:

- seed `7` split: STEP `0cbc1f5b7b48338acfb91b9eaf4bdd82895401f1c2c69ae257dcb4dbaa6dfd1b`, 3 solids, 29 faces, 61 edges;
- seed `7` merge: STEP `1979f64530fde895138bbc503371d9b4fd0561ba5a782ac9b86c5f7cfce4b6e1`, 2 solids, 28 faces, 63 edges;
- seed `19` split: STEP `782371b0298f58560a7408c3578a3f4e8b25e1742bf61d7dae27dc4864f6ce7c`, 3 solids, 28 faces, 60 edges;
- seed `19` merge: STEP `a4c3f091bba36c69cd33dc2d171296f1c021cbef72f2c93d35236a2fbd878030`, 2 solids, 27 faces, 63 edges.

These are CAD morphology/decomposition observations, not structural or functional physics evidence.

## Exact validation commands and observed results

Pure contract suite:

```powershell
python -m unittest tests.test_executable_morphology_qd -v
# initial: exit 0; 10 passed, 1 CadQuery test skipped

python -m unittest tests.test_executable_morphology_qd -q
# after seed-19 split regression: exit 0; Ran 12 tests; OK (skipped=1)
```

The first CadQuery-suite invocation exited `1` before loading tests because that isolated environment did not include repository `src` on `sys.path`: `ModuleNotFoundError: No module named 'formula_ultimate'`. It was rerun with an explicit `PYTHONPATH`, without changing installed packages:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' -m unittest tests.test_executable_morphology_qd -v
# final current-code run: exit 0; Ran 12 tests in 3.140s; OK
```

Final real-CAD fixture commands:

```powershell
$env:PYTHONPATH = (Join-Path $PWD 'src')
& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_a
# exit 0; 18 candidates; 6 signatures; exact decision replay

& '.tools/cadquery-mcp/Scripts/python.exe' scripts/experiments/run_executable_morphology_qd.py --output-dir artifacts/work099/run_b --replay-reference artifacts/work099/run_a/result.json
# exit 0; same deterministic SHA-256; identity exact; measurement differences 0.0
```

Targeted regression and compile gates:

```powershell
python -m unittest tests.test_discovery_contract tests.test_topology_genome tests.test_topology_mutation tests.test_freeform_solid_grammar tests.test_repository_contract -q
# exit 0; Ran 91 tests in 18.437s; OK (skipped=2)

python -m compileall -q src scripts tests
# exit 0
```

The full suite preserved its own exit status:

```powershell
python -m unittest discover -s tests -q *> artifacts/work099/full_suite.txt
$work099FullSuiteExit = $LASTEXITCODE
Set-Content -LiteralPath artifacts/work099/full_suite.exit.txt -Value $work099FullSuiteExit
exit $work099FullSuiteExit
# exit 0; Ran 771 tests in 301.188s; OK (skipped=8)
```

The skipped tests are environment-dependent and include the real-CAD Work 099 test under the repository Python; that same test passed under the pinned CadQuery environment above.

## Defects found and retained evidence

The first full runner pilot stopped on seed `19` with `interface node is missing`. Its `split_part` selector allowed an existing interface leaf to be moved to a new region, leaving the original interface stale. The selector now excludes both external-terminal and interface endpoints, with a direct all-registered-seeds regression. The failed pilot remains at `artifacts/work099/pilot_failed_interface_endpoint/`.

The next cross-run pilot stopped with `replay archive differs`. Actual wall time had been used as the unresolved/archive cost tie-break, allowing runtime noise to alter archive identity. Archive cost now uses deterministic attempt/geometry/CAD opportunity counters; actual CPU/wall time remains charged and reported separately. The pre-fix evidence remains under `pilot_pre_deterministic_cost/` and `pilot_failed_archive_replay/`.

No failed run was relabeled as passing and no evidence was deleted to make replay succeed.

## Falsification, confidence and limitations

Supporting evidence includes adversarial non-finite, short-edge, stale-interface, missing-ancestry, claim-scope, overwrite and archive-cap tests; two seeds; actual CAD execution; exact trusted-head reopening; and an independent repeated execution with identical geometry evidence.

Contradicting/missing evidence is decisive for claims beyond Work 099: there is no stress, thermal, flow, contact, motion or energy field solve; no process evaluator; no vehicle task; no race baseline; and no statistical archive-retention comparison. Archive `feasible` means executable morphology-fixture success only. The functional signature is bounded color refinement and may collide for some non-isomorphic graphs.

Alternative explanation for success: the chosen swept-solid representation and mutations are well suited to the CadQuery fixture. This does not establish that arbitrary geometry is executable, that the archive improves search, or that any candidate has useful physical behavior. Confidence is high for the exercised software/CAD invariants and limited to them.

Work 100 must add independently validated geometry-derived local/coupled evidence and preregistered contrasts. Work 101 remains responsible for complete-vehicle integration and stronger promotion. No admitted experiment, physical/discovery claim, external publication, push or history rewrite occurred.

Final documentation QA passed: 3 bilingual pairs retained their English-source names, numbered sections, executable commands, technical claim-boundary tokens and valid local links. `python -m unittest tests.test_repository_contract -q` passed 6 tests in `0.640s`, and `git diff --check` exited `0` with no output. Explicit staging listed exactly the 11 intended files; `git diff --cached --check` exited `0` with no output. Git's LF/CRLF notices describe a possible later checkout conversion, not a validation failure. The verified commit hash is reported in the handoff because a commit cannot contain its own hash.
