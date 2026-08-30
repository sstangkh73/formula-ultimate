# Work 057 Result: Campaign Physical Adapter and Burn-In

Status: Stopped

Thai companion: `2026-08-31_057_campaign-physical-adapter-burn-in-result.th.md`

## Outcome

The separate-process pending-reservation recovery control passed exactly. The excluded burn-in seed `55999` then consumed and recorded all `240` frozen training opportunities (`80` per treatment) with no pending record. During downstream replay, the command stopped before holdout evaluation because serialized promotion `candidate_ids` were JSON lists while the freshly computed dataclass representation retained tuples. The values matched, but the strict structural comparison correctly failed closed with `CampaignPhysicsError: stored promotion selection differs from training-only replay`.

No main seed was reserved or evaluated. No burn-in admission was issued. Under the frozen v1 immutability rule, this implementation cannot be repaired and continued under the same protocol after burn-in observations exist; remediation requires a new protocol ID.

## Files changed

- Initial campaign adapter and analysis implementation in `src/formula_ultimate/experiments/campaign_physics.py`.
- Public evidence decoding additions in `campaign_runner.py` and exports in `experiments/__init__.py`.
- Generic campaign command, process-resume probe, and Work 057/058 wrappers under `scripts/`.
- Focused campaign-physics tests.
- Work 057 and conditional Work 058 bilingual plans and stopped-result records.

These files preserve the exact failed implementation for reproducibility. The serialization defect is intentionally not corrected in this work item.

## Exact validation and execution record

1. Compilation:

   ```powershell
   py -3.14 -m compileall -q src scripts
   ```

   Exit status: `0`.

2. Focused tests:

   ```powershell
   py -3.14 -m unittest tests.test_campaign_physics tests.test_campaign_runner -q
   ```

   Exit status: `0`; `Ran 16 tests in 0.413s`; `OK`.

3. Separate-process reservation phase:

   ```powershell
   py -3.14 scripts/experiments/probe_campaign_process_resume.py --action reserve --artifact-root artifacts/work057/process_resume_probe
   ```

   Intentional exit status: `75`. Candidate `candidate-52a6df50771f058c`; reservations/results/pending = `1/0/1`.

4. Separate-process resume phase:

   ```powershell
   py -3.14 scripts/experiments/probe_campaign_process_resume.py --action resume --artifact-root artifacts/work057/process_resume_probe
   ```

   Exit status: `0`; decision `separate_process_resume_exact`; reservations/results/pending = `1/1/0`; no second opportunity was allocated.

5. Burn-in:

   ```powershell
   powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work057.ps1
   ```

   Exit status: `1`. Failed stage: `downstream`. Exact message: `stored promotion selection differs from training-only replay`.

## Preserved ignored evidence

- Training budget/result rows: `240/240`; stage rows: `4` (one passed refinement benchmark and three treatment/seed promotion declarations); holdout rows: `0`; main-seed rows: `0`.
- Budget-ledger file SHA-256: `53874fdfc878d0a23b0868797cf59556a08e5106d06fd5a3bfe339ccc8abf005`.
- Result-ledger file SHA-256: `0c79ae667631a93c95f6872b8e79e65c0337636e2a3316dc31b3c0fd036bfeb9`.
- Stage-ledger file SHA-256: `dcb6b2fd5918800402d3c01d4a5d5b060fc7bf03f16bc711f22d3b2b8aac8f0f`.
- Failure-record SHA-256: `faa7b387b33003c3f4321aabd50d631ad4186ec95898f400847cd4e8ccb31b41`.

## Review discipline

Supporting evidence: opportunity accounting, candidate reconstruction, process-boundary resume, physical input identity, and the CalculiX refinement benchmark worked before the stop.

Contradicting evidence: downstream replay was not representation-canonical across the JSON boundary. Existing unit tests did not exercise a write/read comparison of promotion selection tuples and lists.

Alternative explanation rejected: this was not a scientific treatment outcome or a candidate physics failure; it was an infrastructure serialization-contract defect.

Missing evidence: holdout, candidate refinement, STEP/FreeCAD finalist witnesses, burn-in acceptance, all main-seed evidence, and statistical analysis.

Confidence: high in the recorded stop cause and zero-main-seed boundary; no confidence claim is made for downstream campaign completion.

## Follow-up

Create a new numbered work item and a new protocol/campaign identity. Canonicalize promotion selection representations at the serialization boundary, add a regression test that appends and reloads stage evidence, freeze the corrected implementation identity, rerun excluded burn-in from empty new ledgers, and admit main execution only after acceptance.
