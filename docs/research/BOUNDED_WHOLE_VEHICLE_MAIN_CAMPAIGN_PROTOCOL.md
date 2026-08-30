# Bounded Whole-Vehicle Main Campaign Protocol v1

Thai companion: `BOUNDED_WHOLE_VEHICLE_MAIN_CAMPAIGN_PROTOCOL.th.md`

Protocol ID: `bounded_whole_vehicle_main_campaign_v1`

Campaign ID: `FU-BMC-001`

Status: `preregistered_not_run`

## Purpose and claim boundary

This protocol freezes the rules for the first main comparative campaign after Work 054 returned `ready_for_bounded_whole_vehicle_campaign`. The campaign asks whether proposal treatment affects the seed-level ability to produce an evidence-supported finisher under equal attempted-evaluation opportunity.

The admissible claim is comparative evidence inside the exact Work 047 assembly grammar, Work 048 load partitions, Work 049 baseline, Work 053 linear-elastic beam/refined evaluator, synthetic material, and current Level 0 domain. It cannot establish physical validation, safety, manufacturability, real-race superiority, algorithm superiority from one campaign, novelty, engineering discovery, arbitrary-topology transfer, or certified material allowables.

## Hypotheses

Primary `H1_EVOLUTION_SUPPORTED_FINISHER_RATE`:

- Preferred hypothesis: with equal opportunity, `EVOLUTION` has a higher paired-seed probability of producing at least one refined-supported finisher than `RANDOM`.
- Null: the paired-seed rate difference `EVOLUTION - RANDOM` is zero.
- Falsification: a non-positive observed rate difference contradicts the preferred hypothesis. Attempt-level feasible rate cannot replace this seed-level endpoint.

Secondary questions:

- On common-success seeds, does `EVOLUTION` produce a lower seed-level best frozen-holdout time than `RANDOM`?
- How does the fixed discrete `GRID` calibration treatment behave descriptively? GRID is not treated as having the same proposal distribution as the continuous treatments.

## Treatments, seeds, and opportunity budget

| Rule | Frozen value |
|---|---:|
| Treatments | `GRID`, `RANDOM`, `EVOLUTION` |
| Paired main seeds | `55001` through `55012` |
| Excluded pilot seeds | `101`, `202`, `303` |
| Excluded burn-in seed | `55999` |
| Attempts per treatment/seed | `80` |
| Attempts per treatment | `960` |
| Total attempted evaluations | `2,880` |
| Promotions per treatment/seed | `2` maximum |
| Total promotion cap | `72` |

Every invalid declaration, invalid geometry, numerical failure, structural or energy failure, exploit rejection, holdout failure, refined disagreement, or DNF consumes one opportunity. A failed attempt cannot be retried, replaced, assigned a neutral numeric score, or borrowed across seeds.

The five candidate bounds remain identical to Work 050. GRID uses four levels across five variables, so its capacity is `4^5=1,024`. The `12 x 80=960` planned GRID opportunities are unique. Wrap or repetition is prohibited.

`EVOLUTION` uses 20 initial random attempts per seed, mutation sigma `0.12` of each declared range, and the best training-feasible candidate as parent, falling back to the best observed record. Bound clamping must be recorded. `RANDOM` samples each variable independently and uniformly within the same bounds.

## Frozen evaluation sequence

```text
declaration and identity
  -> candidate proposal
  -> grammar/geometry and training Level 0
  -> seed-level training selection
  -> frozen holdout Level 0
  -> Work 053 refined stress/deformation
  -> finalist 3D -> STEP -> FreeCAD witness
  -> eligibility and analysis
```

Holdout information may never reach parent selection, training ranking, mutation, or retry decisions. Up to two training-feasible candidates per treatment/seed are selected by minimum training finish time and then candidate ID. A shortfall of zero or one is recorded without replacement or cross-seed borrowing.

A candidate becomes winner-eligible only when it passes both frozen holdouts, the exact Work 053 refined evaluator, provenance and exploit checks, and the final STEP/FreeCAD witness without hidden geometry repair. Refined thresholds are immutable during the campaign.

## Outcomes and analysis

The paired seed is the inferential unit. The 80 attempts inside one seed are dependent search opportunities, not 80 independent replicates.

Primary outcomes per treatment/seed:

1. whether at least one refined-supported finisher exists;
2. best frozen-holdout time among eligible finishers.

When no supported finisher exists, presence is `false` and best time is `null`. The seed remains in supported-finisher-rate analysis and the absence remains explicit in time-availability reporting.

The primary comparison is `EVOLUTION - RANDOM`. The protocol calls for paired rate difference, exact McNemar analysis, and a 95% paired-bootstrap interval. Common-success best time uses paired median difference, exact sign-flip analysis, and a 95% paired-bootstrap interval. Analysis RNG seed is `551337`. GRID comparisons and every preregistered secondary metric must be reported without selective suppression.

Candidate winner ordering is:

1. all eligibility gates passed;
2. minimum frozen-holdout time;
3. ascending candidate ID tie-break.

Even a positive primary effect cannot establish algorithm superiority without independent replication under a new protocol.

## Stop/go and immutability

Stop before an admitted run if any upstream/protocol identity differs, GRID repeats, treatment opportunities differ, holdout leaks into training, Work 053 is unavailable, or ledger/replay is not exact. Burn-in changes require a new protocol ID. Changes after admitted start require a new campaign ID. Result and budget ledgers are append-only and must retain RNG checkpoints and ancestry.

Allowed final statuses are:

- `completed_with_supported_finishers`
- `completed_without_supported_finisher`
- `stopped_protocol_violation`
- `stopped_infrastructure_failure`

Completing without a supported finisher is a valid research result, not permission to relax a gate.

## Current validation state

Work 055 validates only the declaration. It performed `0` candidate evaluations. The machine-readable source is `config/experiments/bounded_whole_vehicle_main_campaign_v1.json`; ignored validation evidence is written to `artifacts/work055/protocol_validation.json`. Campaign-runner implementation and burn-in belong to later work items.
