# Work 112 Result: Physical Interface Graph

Thai companion: `2026-09-10_112_physical-interface-graph-result.th.md`

Date: 2026-09-10 (Asia/Bangkok)

Status: Completed

## Outcome and evidence

Work 112 implemented a six-terminal, four-edge typed multigraph bound to Work 108 regions. It retained two parallel mechanical paths and three disconnected physical-domain components. Identifier-only renaming was invariant; source/sink reversal, removal of one parallel edge, owner regrouping and disconnection remained distinct.

Result SHA-256 is `45e821a075f98258a8fbe5c1a954def9e12b561db1c0e5f1d8f6d21ffe901b37`; `run_b/replay.json` is exact. Maximum exchange residual was `0`. The corpus contained `6` terminals, `4` edges, `1` additional parallel edge and `3` connected components. Unit, surface, rigid/moving and exchange-imbalance controls were rejected. Unambiguous split transfer changed the region and invalidated dependent evidence; ambiguous split retained the binding and emitted invalidation. Nine terminals produced explicit `unresolved` identity above the frozen bound of eight.

Changed: implementation, config, runner and tests at their Work 112 proposed paths; bilingual `PHYSICAL_INTERFACE_GRAPH_V1` contract; and this bilingual plan/result. `artifacts/work112/run_a|run_b` remain ignored.

## Validation

```powershell
python -m unittest tests.test_physical_interface_graph -v
# exit 0; 6 tests passed
python -m py_compile src/formula_ultimate/assembly/physical_interface_graph.py scripts/development/run_physical_interface_graph.py
# exit 0
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_a
# exit 0; result SHA-256 above
python scripts/development/run_physical_interface_graph.py --config config/development/physical_interface_graph_v1.json --output-root artifacts/work112/run_b --replay-reference artifacts/work112/run_a/result.json
# exit 0; exact replay
```

```powershell
python -m unittest tests.test_spatial_material tests.test_physical_interface_graph tests.test_repository_contract -v
# exit 0; 19 tests passed
python -m compileall -q src scripts tests
# exit 0
git diff --check
# exit 0
git diff --cached --name-status
# exit 0; exactly the 10 declared Work 112 files
git diff --cached --check
# exit 0
```

The identity bound and declared surface frames limit generalization; no contact mechanics, general mechanism discovery or physical validation is claimed. The verified commit hash is reported in the final handoff.
