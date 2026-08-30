# Work 059 Result: Protocol v2 Serialization Remediation and Fresh Burn-In

Status: Completed

Thai companion: `2026-08-31_059_v2-serialization-remediation-burn-in-result.th.md`

## Outcome

Created protocol `bounded_whole_vehicle_main_campaign_v2` / campaign `FU-BMC-002`, linked it to the immutable stopped v1 evidence, and verified that all scientific rules equal v1. Corrected only the tuple/list serialization representation boundary and added append/reload regression coverage. Fresh process recovery and fresh excluded-seed burn-in passed. Decision: `burn_in_accepted_for_admitted_main_campaign`.

## Files changed

- New v2 protocol config and exact successor validation.
- JSON-compatible promotion canonicalization in the generic campaign command.
- Protocol-selectable process probe and Work 059/060 wrappers.
- Regression and scientific-equivalence tests.
- Bilingual Work 059/060 plans, v2 admission research record, and Work 059 result.

## Exact commands and results

1. Focused tests:

   ```powershell
   py -3.14 -m unittest tests.test_main_campaign_protocol tests.test_campaign_physics tests.test_campaign_runner -q
   ```

   Exit status: `0`; `Ran 26 tests in 0.415s`; `OK`.

2. Fresh process probe and burn-in:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work059.ps1
   ```

   Exit status: `0`. Process probe `1/1/0`. Burn-in: attempts `240`, promotions `6`, refinement passed `6`, witness passed `6`, supported streams `3`, replay exact, decision accepted.

3. Verify-only replay:

   ```powershell
   py -3.14 scripts/experiments/run_bounded_main_campaign.py --kind burn-in --protocol config/experiments/bounded_whole_vehicle_main_campaign_v2.json --artifact-root artifacts/work059 --verify-only
   ```

   Exit status: `0`; counts and fingerprints identical; no evaluator or solver process invoked.

4. Full suite:

   ```powershell
   py -3.14 -m unittest discover -s tests -q
   ```

   Exit status: `0`; `Ran 369 tests in 26.151s`; `OK`.

5. Compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts tests
   ```

   Exit status: `0`.

## Evidence

- Protocol fingerprint: `d09e33dd0ff0438f379ccadfac5b8bcde3e611f2bf71bde3c74ced2697d58123`.
- Training reservations/results/pending: `240/240/0`; counts `80/80/80`; GRID unique `80`.
- Training feasible/structural failure: `189/51`.
- Promotions/shortfall: `6/0`; holdout/refinement/CAD terminal: `6/6/6`; passed refinement/CAD: `6/6`.
- Training combined fingerprint: `52de5c3a44423b126e6e05b50c594a0a70c4956d084bc4bc2a02b3c4fa9b3054`.
- Stage fingerprint: `cd019afbe7b85b10e6fc5bc744314b16b281e4dd1701b0eab0c94681f7978e97`.
- Refinement benchmark result: `185b3749575325ff7c6be9aee2553abf37ac44320b222a330b802b90da21a038`.
- External process evidence: 123 processes, cumulative recorded wall time `37.7205395991914 s`.

## Review and limitations

Supporting evidence: scientific equivalence test, new identity/provenance checks, exact process recovery, equal opportunity accounting, benchmark, all downstream terminal records, and exact verify-only replay.

Contradicting evidence: v1 exposed a missing serialization-boundary test; v2 does not erase that failure. The physical evaluator remains bounded and linear-elastic.

Alternative explanation: successful burn-in can reflect simple primitive geometry and does not imply arbitrary-vehicle robustness.

Missing evidence: v2 main campaign, independent replication, solid/contact/nonlinear analysis, physical material calibration, manufacturing tolerance, and hardware tests.

Confidence: high for v2 admission under the exact committed software/tool environment; low outside the frozen domain.

Staged-scope checks, commit hash, and post-commit clean-tree replay are reported in the final Work 059 handoff because the commit does not yet exist when this record is written.
