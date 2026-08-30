# Work 060 Plan: Protocol v2 Admitted Main Campaign

Status: In progress; execution remains blocked until the Work 059 acceptance commit and clean-tree replay complete

Thai companion: `2026-08-31_060_v2-admitted-main-campaign-plan.th.md`

## Objective

Execute and analyze successor campaign `FU-BMC-002` using the exact committed v2 implementation admitted by Work 059. This plan replaces stopped Work 058 without reusing any v1 campaign observation.

## Design and scope

The independent variable, 12 paired seeds `55001`–`55012`, `GRID`/`RANDOM`/`EVOLUTION` treatments, 80 opportunities per treatment/seed, `2,880` total opportunities, two-promotion cap, frozen holdouts, Work 053 refinement, STEP/FreeCAD witness, outcomes, analysis seed `551337`, statistical methods, winner rule, prohibited claims, and failure policies are unchanged from Work 058/v1.

Work 060 will reuse committed Work 059 code without modification, write fresh ignored ledgers/evidence under `artifacts/work060/`, analyze every preregistered outcome, write bilingual result/research evidence, validate, and commit. Any needed post-admission code/config change stops `FU-BMC-002`.

## Admission and success criteria

Admission requires a clean committed Work 059 summary with decision `burn_in_accepted_for_admitted_main_campaign`, protocol ID `bounded_whole_vehicle_main_campaign_v2`, campaign ID `FU-BMC-002`, exact implementation/upstream/tool identities, and exact replay.

Success requires exactly `2,880` terminal opportunities, `80` per treatment/seed, `960` per treatment, unique GRID opportunities, complete terminal evidence for every selected candidate, exact replay, full preregistered paired-seed analysis, and one allowed final campaign status. A non-positive preferred effect or no supported finisher remains a valid result.

## Stop criteria and evidence discipline

Stop on identity, fairness, partition, ledger, replay, mutation-after-burn-in, or infrastructure violations. Never retry or replace a consumed opportunity. Report supporting and contradicting evidence, alternative explanations, missing evidence, confidence, compute cost, failure counts, and the bounded claim level.

## Validation and non-goals

Run admission check, campaign, verify-only replay, full tests, compilation, bilingual documentation checks, explicit staging, `git diff --cached --check`, commit, and clean-tree replay. Do not claim physical validation, real safety, manufacturability, race or algorithm superiority, novelty, discovery, or certified material performance. Do not push or publish.
