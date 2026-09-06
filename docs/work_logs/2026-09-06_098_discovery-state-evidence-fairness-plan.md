# Work 098 Plan: Discovery State, Evidence and Fairness Contract

Thai companion: `2026-09-06_098_discovery-state-evidence-fairness-plan.th.md`

Date: 2026-09-06 (Asia/Bangkok)

Status: Completed

## Objective and starting evidence

Implement the Work 098 software contract required by `WHOLE_VEHICLE_TECHNOLOGY_DISCOVERY_PROTOCOL_V1_2026-09-06.md`, starting at clean revision `7afb91e`. Keep historical Work 095/097 benchmarks and the original campaign runner unchanged. This is a software contract work item, not a new physical model or an admitted discovery experiment.

## Scope and planned files

- `src/formula_ultimate/experiments/discovery_registration.py`: strict versioned registration, coverage and budget validation, immutable identity and admission boundary.
- `src/formula_ultimate/experiments/discovery_evidence.py`: candidate/context identity, orthogonal state outcomes, scoped evidence and exploratory/promotion admission, conservative legacy adapters.
- `src/formula_ultimate/experiments/discovery_ledger.py`: append-only event ledger, deterministic reduction/replay, candidate ancestry, resource reservation/settlement/recovery and cache rules.
- `src/formula_ultimate/experiments/discovery_audit.py`: deterministic stratified sampling, inclusion probabilities and per-stratum proxy error accounting, selection and numerical replay comparison.
- `config/experiments/discovery_contract_fixture_v1.json`: complete explicitly synthetic software registration, not an admitted campaign.
- `scripts/experiments/run_discovery_contract.py`: executable mixed-ledger fixture and exact replay evidence, with safe output handling.
- `tests/test_discovery_contract.py`: adversarial acceptance cases plus integration/resume coverage.
- `docs/contracts/DISCOVERY_STATE_EVIDENCE_FAIRNESS_V1.md` and `.th.md`: implemented interface, commands, acceptance mapping and limitations.
- This bilingual plan and matching bilingual result. Retain generated evidence under ignored `artifacts/work098/`.

## Implementation decisions to validate

- Separate states by representation, boundary, physics domain/fidelity, manufacturing process and intended use. Preserve previous attempts rather than overwrite failures.
- Bind evidence to all causal identities and a frozen registration. Fixtures cannot contribute to scientific survivor counts. Trusted evaluator provenance remains explicit; a hash is integrity evidence, not proof of physical truth.
- Use a bounded single-writer, serial scheduling implementation. Partition resources per treatment/seed and budget pool; reserve before operations, charge retries/lost results and retain overshoot as a campaign-stop condition. No claim of a process-killing watchdog or distributed execution.
- Keep registration numerical requirements explicit; synthetic fixture values are software test values only. Incomplete or changed declarations cannot execute under an old registration identity.
- Distinguish exact decision replay from numerical execution comparison. Audit unknown reference labels remain unknown; report rates within strata with inclusion probabilities and uncertainty information.

## Validation and success criteria

1. Run `python -m unittest tests.test_discovery_contract -v`; cover all 10 acceptance requirements in the governing protocol, including negative promotion, stale identity, tampering, crash/retry, cache, budget, score-independent audit and legacy semantics.
2. Run targeted regressions: `python -m unittest tests.test_constructive_validity tests.test_generalized_geometry_benchmarks tests.test_campaign_runner tests.test_repository_contract -q`.
3. Execute the fixture runner twice in separate artifact directories and compare deterministic ledger/report hashes; reopen a ledger and verify replay/recovery in tests. Fixture observations are not admitted science.
4. Run `python -m compileall -q src scripts tests` and `python -m unittest discover -s tests -q` as final regression gates. Preserve failures and environment-dependent skips in the result.
5. Verify bilingual files, run `git diff --check`, inspect explicit staged scope, run `git diff --cached --check`, commit only this work, and report the verified hash.

Success requires executable state/accounting/admission behavior with falsification tests and replay artifacts, not just schema labels or a hand-authored ledger. A failed gate stops the commit. Unexpected blockers leave the work `In progress` or `Stopped` with their exact reason.

## Risks, controls and non-goals

Risks: synthetic evidence masquerading as physics, invalid metadata changing a result class, uncharged retry/cache work, incomplete admissions, and overclaiming hash-chain security. Controls: strict evidence classes and causal identities, frozen rules, adversarial tests, explicit cost recovery, trusted checkpoint verification and documented provenance boundary.

Non-goals: Works 099–101, morphology/CAD/field-solver implementation, new physical laws, statistical discovery conclusions, optimized race comparison, unrestricted concurrency, external publication or push. No edits to the dated governing protocol or its backups are planned.
