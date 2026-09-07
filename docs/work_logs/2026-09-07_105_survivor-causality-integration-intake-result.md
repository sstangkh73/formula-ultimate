# Work 105 Result: Survivor Causality and Whole-Vehicle Integration Intake V1

Thai companion: `2026-09-07_105_survivor-causality-integration-intake-result.th.md`

Date: 2026-09-07 (Asia/Bangkok)

Status: Completed

## Outcome

Work 105 completed the first bounded implementation phase toward the roadmap Work 101 milestone. It added a fail-closed intake that verifies the exact Work 100 V2 deterministic identity, aggregates finest-level mechanical and thermal flow by original edge, removes inactive appendages from an identifier-independent active-topology identity, compares each candidate with the paired fixed control, and reports technology-neutral capability/evidence coverage.

The intake result is correctly negative: `blocked_incomplete_capability_and_evidence_coverage`, with `work101_program_exit = false`. All ten Work 100 subsystem survivors remain preserved and typed as possible `load_structure` inputs, but no whole-vehicle candidate was created and none was promoted.

## Causal findings

- `functional_mechanism_candidate_count = 0`.
- Four graph/joint candidates are `declared_topology_only_inactive_appendage`: each retained three active coupled edges and added one inactive edge. Their response differences from paired fixed controls were only about `1e-14`.
- Four candidates are shape-response variants with unchanged active topology: both morphology-only and both random-control cases.
- `RANDOM_CONTROL`, seed `7`, had a meaningful absolute utilization difference `+0.0586275358`. Since utilization is minimized, this is a worsening, not an improvement.
- The other detectable shape differences were below the frozen meaningful threshold `0.05`.
- The preferred hypothesis that a Work 100 survivor contained a task-relevant active-topology mechanism was falsified at this intake fidelity. Local feasibility and geometry-response evidence remain intact.

Whole-vehicle coverage contains only `load_structure`. Eight capabilities are missing: braking, controller, direction control, energy converter, energy storage, ground propulsion, heat rejection and power transmission. Seven program-exit evidence classes are missing: contact, coupled transient, energy, failure, independent higher fidelity, optimized baseline and safety. Work 100 holdout evidence is preserved, but its shared-runtime formula reference is not relabeled independent higher fidelity.

## Files changed

- `src/formula_ultimate/experiments/integration_intake.py`
- `config/experiments/work101_integration_intake_v1.json`
- `scripts/experiments/run_integration_intake.py`
- `tests/test_integration_intake.py`
- `docs/contracts/WHOLE_VEHICLE_INTEGRATION_INTAKE_V1.md` and Thai companion
- this plan/result pair and Thai companions

Generated reports under `artifacts/work105/` remain ignored by Git; `run_c` and `run_d` are the final-source exact pair.

## Exact validation evidence

1. `python -m unittest tests.test_integration_intake -v`
   - Exit `0`; `Ran 9 tests in 0.005s`; `OK`.
2. Work 105 final-source run C and independent exact replay D
   - Both exit `0`.
   - Both report ten candidates, zero mechanism candidates, blocked intake and `work101_program_exit = false`.
   - Exact result SHA-256: `559fb55a4513003af35e302ddff9120ece830b88d8f19f62188a052c3411229e`.
3. Targeted Works 098-100, functional vehicle, release/promotion and whole-mechanical audit regression
   - Exit `0`; `Ran 114 tests in 25.563s`; `OK`.
4. `python -m compileall -q src scripts tests`
   - Exit `0`.
5. `python -m unittest discover -s tests -q`
   - Exit `0`; `Ran 794 tests in 332.058s`; `OK (skipped=8)`.

## Decisions, limitations and follow-up

- Active means relative mechanical and thermal flow greater than `1e-8`; equality is inactive. No post-result threshold change occurred.
- Canonicalization is exact for unlabelled simple graphs up to eight active nodes. It deliberately ignores source/sink coloring, direction and parallel-edge multiplicity, so it is an intake descriptor rather than complete mechanism proof.
- The input is prior admitted Work 100 evidence; Work 105 adds analysis, not new physical evidence.
- A negative intake is the correct fail-closed result and does not make the work item `Stopped`.
- The next bounded phase should produce or admit additional typed subsystem survivors with causal active paths before attempting assembly. It should not force a conventional layout or reuse the blocked whole-mechanical candidate without new geometry/evidence.

The validated commit hash is reported in the final handoff after the mandatory exact-scope commit succeeds.
