# Bounded Main Campaign Runner and Ledger Contract

Thai companion: `BOUNDED_MAIN_CAMPAIGN_RUNNER_LEDGER.th.md`

Status: Implemented and preparation-verified; campaign execution remains locked.

## Purpose and evidence boundary

This component makes the frozen `FU-BMC-001` opportunity budget deterministic, append-only, and recoverable. It does not make a Level-0 result physically valid and it does not authorize burn-in or admitted main-seed execution. Synthetic unit-test evaluations are software fixtures only and cannot be used as campaign observations.

## Transaction order

For every treatment/seed stream, the runner performs one irreversible logical transaction:

1. reconstruct the search agent from all prior reservations and terminal training results;
2. propose the exact next candidate and RNG checkpoint;
3. append and `fsync` one `attempt_reserved` row, consuming one opportunity;
4. invoke the evaluator;
5. append and `fsync` exactly one `training_result` row;
6. feed that terminal result back to the reconstructed agent.

A process interruption between steps 3 and 5 leaves one visible pending reservation. Resume must reproduce the identical candidate, ancestry, and RNG checkpoint, evaluate that reservation once, and must not reserve another opportunity first. A reserved attempt is consumed even if the evaluator later returns a failure state.

## Ledger integrity

The budget and result ledgers use canonical JSONL schema `chained_campaign_jsonl_v1`. Each row contains the protocol ID, campaign ID, evidence class, ledger kind, zero-based sequence, previous-row SHA-256, payload, and its own SHA-256. The first previous hash is 64 zeroes.

The record hash is:

```text
record_sha256 = SHA256(canonical_json(row_without_record_sha256))
```

Replay fails closed on malformed or blank rows, sequence gaps, previous-hash mismatch, record mutation, cross-ledger identity mismatch, duplicate reservation/result, unreserved result, reordered attempt, more than one pending reservation in a stream, candidate identity mismatch, evaluation identity mismatch, or non-finite numeric evidence. This chain detects accidental or local content alteration; it is not an external signature and cannot prove who produced the data.

## Deterministic recovery

`reconstruct_training_agent` regenerates every proposal from the frozen protocol, treatment, and paired seed. It checks the entire candidate object, including variable ordering and values, parent candidate ID, and pre-proposal RNG checkpoint. Completed results are observed in attempt order. Any disagreement stops execution instead of silently repairing state.

The execution target is monotonic. It cannot exceed the frozen per-treatment/seed budget and cannot be set below opportunities already consumed. Main-campaign evidence requires a non-empty authorization matching campaign ID, evidence class, and seed; admitted-campaign execution additionally requires the explicit main-execution flag.

## Promotion rule

Promotion selection reads terminal `training` records only. For each treatment/seed it sorts feasible candidates by ascending training objective and then candidate ID, selects at most the frozen cap of two, and records any shortfall. A shortfall is not borrowed from another treatment or seed. Holdout/refined evidence is rejected as input to this selection step.

## Work 056 verification and limitations

The Work 056 command initializes separate `PREP-FU-BMC-001` ledgers with evidence class `preparation_only`, replays their exact empty fingerprint, and proves an unauthorized execution request is rejected before the evaluator is called. Its required outcome is `runner_prepared_campaign_locked` with `candidate_evaluations=0`, `burn_in_evaluations=0`, and `main_seed_evaluations=0`.

Remaining evidence for a later work item includes the CalculiX evaluation adapter, STEP/FreeCAD finalist adapter, real process-interruption exercise, burn-in acceptance, and admitted campaign execution. No result in Work 056 supports a race-performance, material-strength, fatigue, fracture, or whole-vehicle physical-validation claim.
