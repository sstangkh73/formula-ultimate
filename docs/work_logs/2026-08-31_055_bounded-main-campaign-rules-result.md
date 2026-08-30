# Work 055 Result: Bounded Main-Campaign Rules

Status: Completed

Thai companion: `2026-08-31_055_bounded-main-campaign-rules-result.th.md`

## Outcome

The first bounded main-campaign rules are preregistered and machine-validated. Decision: `rules_frozen_campaign_not_run`. Work 055 evaluated `0` candidates.

The frozen declaration uses 12 new paired seeds, 80 attempted evaluations per treatment/seed, `960` attempts per treatment, and `2,880` total attempts. GRID consumes `960` unique opportunities from its `4^5=1,024` capacity without wrapping. Up to two candidates per treatment/seed may advance, for a maximum of 72 promotions.

The preferred primary hypothesis compares seed-level refined-supported-finisher probability for `EVOLUTION` versus `RANDOM`. The paired seed—not each attempt—is the inferential unit. Holdout leakage, silent repair, neutral failure substitution, retries, cross-seed budget borrowing, mutable refined thresholds, and winner eligibility without `3D -> STEP -> FreeCAD` evidence are prohibited.

## Files changed

- `config/experiments/bounded_whole_vehicle_main_campaign_v1.json`
- `src/formula_ultimate/experiments/main_campaign_protocol.py` and experiment package exports
- `scripts/experiments/validate_main_campaign_protocol.py` and `scripts/run_work055.ps1`
- `tests/test_main_campaign_protocol.py`
- `docs/research/BOUNDED_WHOLE_VEHICLE_MAIN_CAMPAIGN_PROTOCOL.md` and `.th.md`
- matching Work 055 bilingual plan/result records

Ignored validation evidence is under `artifacts/work055/`.

## Decisions and evidence

- Main seeds are `55001..55012`; pilot seeds `101/202/303` and burn-in seed `55999` are excluded.
- Every failure/DNF consumes one opportunity and remains observable.
- GRID is a fixed discrete calibration treatment; its distributional difference from RANDOM/EVOLUTION must be reported.
- Primary endpoints are seed-level supported-finisher presence and seed-level best frozen-holdout time.
- Candidate eligibility requires frozen holdout, Work 053 refined evidence, provenance/exploit checks, and the final STEP/FreeCAD witness.
- Algorithm superiority requires both a positive primary supported-finisher-rate effect and independent replication under a new protocol.
- Protocol config SHA-256 is `f42b9f59a0006ffb87e6607099de3446b03b559a38fe1b719bdd775a1d1a31ab`; canonical protocol fingerprint is `a332852d75da1c4c22caba78105062eb1a6859db3ec484dc14ec0f3aec844ceb`.

## Observed non-admitted failures

The first focused test run failed because the validator incorrectly applied a 64-character artifact SHA-256 rule to the 40-character Git commit identity. A separate commit-ID validator corrected the type distinction without changing campaign rules. The next run had one negative-fixture expectation failure: changing the attempt budget was correctly rejected by the earlier exact-budget rule before reaching GRID capacity. The fixture was changed to corrupt declared GRID capacity directly; the protocol and thresholds were unchanged.

## Exact validation

```powershell
py -3.14 -m unittest tests.test_main_campaign_protocol -q
# initial exit 1; Git commit identity was incorrectly validated as SHA-256
# intermediate exit 1; one GRID negative fixture reached an earlier exact-budget guard
# final exit 0; Ran 7 tests; OK

powershell -NoProfile -ExecutionPolicy Bypass -File scripts/run_work055.ps1
# exit 0; status=passed
# decision=rules_frozen_campaign_not_run; candidate_evaluations=0
# paired_seeds=12; total_attempts=2880
# grid_unique=960; maximum_promotions=72; replay=exact

py -3.14 -m unittest tests.test_main_campaign_protocol tests.test_refined_readiness tests.test_whole_vehicle_search tests.test_repository_contract -q
# exit 0; Ran 21 tests; OK

py -3.14 -m unittest discover -s tests -q
# exit 0; Ran 350 tests in 31.939s; OK

py -3.14 -m compileall -q src scripts tests
# exit 0
```

Repository-contract checks, staged `git diff --cached --check`, the explicit scoped commit, and clean-tree Work 055 replay are verified after this result exists and are reported in the final handoff.

## Supported and unsupported claims

Supported: the declaration is internally consistent, pins the bounded upstream evidence, balances treatment opportunities, avoids GRID repetition, defines falsifiable seed-level outcomes, and validates deterministically without running the campaign.

Unsupported: no campaign outcome, candidate merit, treatment effect, algorithm superiority, discovery, physical validation, safety, manufacturability, or race performance has been established.

## Limitations and next work

Twelve seeds do not guarantee power for small effects. The five-variable grammar and current physics domain limit transfer. Work 056 should implement the two-stage campaign runner and append-only ledgers against this exact protocol. Work 057 should use only excluded seed `55999` for burn-in; any rule change after burn-in requires a new protocol ID.
