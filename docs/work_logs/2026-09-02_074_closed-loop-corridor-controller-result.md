# Work 074 Result: Closed-Loop Corridor Controller

Status: Completed

Thai companion: `2026-09-02_074_closed-loop-corridor-controller-result.th.md`

## Outcome and files

Implemented a deterministic centreline projection and bounded feedback steering controller around the unchanged Work 073 physical plant. Added analytical left/right circle and straight fixtures, configuration, simulation module/exports, runner, tests, bilingual research, and this result. The requested Work 075/076 bilingual plans were also preregistered before their implementation. Evidence is ignored under `artifacts/work074/`.

## Decisions and evidence

The controller retains feed-forward, feedback, raw/applied steer, saturation, signed tracking error, desired heading, progress, widths, and downstream physical evidence per sampled step. Departure is explicit. Correct feedback reduced final error from the zero-feedback control's `0.3772375000371769 m` to `0.02307508195600006 m`; wrong-sign feedback worsened it to `0.46591408662822736 m`. Reference saturation was retained at `348/500` steps as a limitation. Minimum load was `290.149480377666 N`; maximum travel was `0.011457919570257338 m`.

Work 073 hash remained `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`. Work 074 result/canonical evidence/file hashes are `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`, `9572a793e45713ee9768d3bca7ead9460ce3d1fe1824d6cee273b89e7737efea`, and `B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B`.

## Validation record

```text
python -m unittest tests.test_closed_loop_corridor_controller -q
Exit: 0
Ran 9 tests — OK

python scripts/experiments/run_closed_loop_corridor_controller.py --config config/vehicle/closed_loop_corridor_controller_v1.json --vehicle-root config/vehicle --output artifacts/work074/experiment_evidence.json
Exit: 0; status=passed

same command with --output artifacts/work074/replay/experiment_evidence.json
Exit: 0; byte-identical SHA-256 B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B

python -m unittest discover -s tests -q
Exit: 0
Ran 463 tests in 197.111s — OK
```

Full regression, repository contract, compilation, scoped commit, and post-commit replay are recorded in the final handoff after execution.

## Limitations and follow-up

This short-horizon controller is heavily saturated and uses sampled synthetic geometry. It has no longitudinal control or real-circuit evidence. Work 075 next adds explicit linkage motion ratio; Work 076 must retune and falsify sustained one-lap integration rather than extrapolate this result.
