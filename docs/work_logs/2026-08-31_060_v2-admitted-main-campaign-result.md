# Work 060 Result: Protocol v2 Admitted Main Campaign

Status: Stopped before execution

Thai companion: `2026-08-31_060_v2-admitted-main-campaign-result.th.md`

## Outcome

Committed Work 059 admission and clean-tree burn-in replay passed at commit `83d10b3c08844369a794d3c61e02f549a4ca2957`. Before initializing main ledgers, the Work 060 admission preflight compared the v2 admission `protocol_sha256` with a hard-coded v1 config path and returned `admission protocol identity differs`. The lock failed closed. No Work 060 budget, result, or stage ledger was created; main reservations/evaluations remain exactly zero.

## Exact command

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work060.ps1
```

Exit status: `1`. Failed stage: `admission`. Exact message: `admission protocol identity differs`.

## Review

Supporting evidence: the error occurred before ledger construction and no main opportunity was consumed. The burn-in evidence itself remains exact and immutable.

Contradicting evidence: Work 059 regression coverage tested v2 scientific equivalence and downstream serialization, but did not invoke the main-admission path with a non-v1 protocol file.

Alternative explanation rejected: protocol content and fingerprint matched; the mismatch was the command's hard-coded v1 file path, not a changed scientific rule or corrupt admission artifact.

Missing evidence: all v2 main opportunities and outcomes.

Confidence: high in the zero-main boundary and blocker identity.

## Follow-up

Protocol v2 cannot be modified after accepted burn-in. A successor protocol must pass the active protocol path/hash into admission validation, add a regression test that exercises successor admission before ledger initialization, run a fresh excluded-seed burn-in, commit clean admission, and only then open successor main ledgers.
