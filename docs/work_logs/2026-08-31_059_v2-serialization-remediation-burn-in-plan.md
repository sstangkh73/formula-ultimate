# Work 059 Plan: Protocol v2 Serialization Remediation and Fresh Burn-In

Status: Completed

Thai companion: `2026-08-31_059_v2-serialization-remediation-burn-in-plan.th.md`

## Objective

Supersede stopped protocol `bounded_whole_vehicle_main_campaign_v1` with a new protocol/campaign identity, correct only the promotion JSON representation boundary exposed by Work 057, add a write/read regression control, freeze the corrected implementation, and run a fresh excluded-seed burn-in from empty v2 ledgers.

## Preserved failure evidence

Work 057 stopped after `240/240` training records and before holdout because stored JSON `candidate_ids` lists were compared with in-memory tuples. The preserved v1 ledger hashes are recorded in the Work 057 result. Those ledgers remain immutable and cannot be imported into v2.

## Scope and planned files

- Add `config/experiments/bounded_whole_vehicle_main_campaign_v2.json` with new protocol ID `bounded_whole_vehicle_main_campaign_v2`, campaign ID `FU-BMC-002`, frozen source commit `b43c69fd9b52acf4888c9bb3abec8b4c179c8424`, and an explicit remediation link to the stopped v1 evidence.
- Extend strict protocol validation for the exact v2 identity while retaining v1 validation.
- Canonicalize promotion selections by a JSON-compatible round trip before append/replay comparison; do not change candidate generation, evaluation, partitions, budgets, physics, thresholds, or analysis.
- Add an append/reload regression test proving tuple/list representation cannot stop equal evidence and altered values still fail.
- Add Work 059/060 wrappers, fresh ignored artifacts, bilingual research/result evidence, validation, and a dedicated commit.

## Variables, controls, and metrics

The scientific independent/dependent variables and controls remain exactly those preregistered in v1. The remediation variable is only serialization representation (`tuple` before JSON versus `list` after JSON). Controls compare semantically equal round-tripped selection evidence and a mutated candidate ID. Metrics are exact stage replay, `240` terminal burn-in opportunities, `80/80/80` stream counts, promotion shortfall, terminal downstream counts, tool/implementation hashes, and zero v1/main-ledger reuse.

## Success criteria

1. v2 validates with all scientific rules equal to v1 except identities, frozen commit, and remediation provenance.
2. Regression test passes after append/reload and rejects altered selection content.
3. Fresh v2 process-resume probe returns exactly `1/1/0` reservation/result/pending.
4. Fresh burn-in returns `burn_in_accepted_for_admitted_main_campaign` with `240` terminal training attempts, exact replay, complete terminal downstream evidence, and no implementation/config change after observation.
5. Work 059 is committed and clean-tree verify-only replay updates admission evidence to that commit before Work 060.

## Failure criteria

Stop successor main execution on any new serialization mismatch, identity drift, ledger reuse, budget inequality, GRID repeat, leakage, missing downstream terminal, unavailable solver/CAD tool, or required post-burn-in change. Do not repair and continue under v2 after observation.

## Validation

Run focused regression/protocol/runner tests, full tests, compilation, fresh process-resume probe, fresh burn-in, verify-only replay, explicit staged checks, commit, and clean-tree verify-only replay. Inspect exact artifact counts, fingerprints, implementation/tool identities, and decision.

## Non-goals

No scientific rule, threshold, material, load, topology grammar, hypothesis, seed, budget, or claim boundary changes. No main seed in Work 059. No physical-validation, safety, superiority, push, or publication claim.
