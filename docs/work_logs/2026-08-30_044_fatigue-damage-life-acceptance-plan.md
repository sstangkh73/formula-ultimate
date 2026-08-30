# Work 044 Plan: Fatigue Damage and Life Acceptance

Status: Completed

Thai companion: `2026-08-30_044_fatigue-damage-life-acceptance-plan.th.md`

## Objective

Convert explicit stress histories into deterministic counted cycles, mean-stress-corrected S-N lives, an append-only Miner damage ledger, and the first observable fatigue-failure crossing without clipping, resetting, or silently extrapolating damage.

## Scope and claim boundary

- Use an immutable synthetic Basquin S-N record with explicit alternating-stress domain, ultimate strength, Goodman mean-stress correction, and life-scatter factor.
- Implement deterministic rainflow counting for declared reversal histories and exact constant/variable-amplitude fixtures.
- Preserve every damage contribution and localize the first `D>=1` crossing, including fractional cycle position when required.
- Reject below-domain, above-domain, invalid mean-stress, missing curve/provenance, and non-finite histories rather than assigning zero or extrapolated damage.

This work validates deterministic Miner/S-N accounting only. It is not crack-growth validation, multiaxial/non-proportional fatigue, spectrum/environment validation, real component service life, or physical material evidence.

## Experiment design

- independent variables: constant/variable amplitude history, mean stress, cycle count, block sequence, and curve declaration;
- dependent variables: rainflow ranges/means/counts, corrected amplitude, life per bin, incremental/cumulative damage, predicted crossing cycle, event identity, and uncertainty interval;
- controls: turning-point convention, rainflow algorithm version, Goodman rule, temperature/process declaration, exact floating-point order, and no damage clipping;
- preferred hypothesis: exact cycle fixtures and constant-amplitude damage pass `<=1%`, same input replay is exact, Miner arithmetic is exact, and failure is emitted at the first crossing;
- falsification: deliberate overload, under-domain history, invalid mean stress, malformed curve, permutation/replay, and a sequence pair with equal final Miner damage but different event positions.

## Planned implementation and files

- `config/structural/fatigue_damage_acceptance_v1.json`;
- immutable fatigue record, rainflow counter, Goodman correction, life evaluator, damage ledger, uncertainty, and event contract;
- Work 044 runner/launcher and ignored evidence under `artifacts/work044/`;
- focused exact-cycle, arithmetic, replay, negative-domain, and event tests;
- bilingual report and matching result records.

## Validation and success criteria

- exact declared cycle-count fixtures and constant-amplitude damage error `<=1%`;
- exact replay identity and exact cumulative arithmetic for the same record/order;
- first crossing emitted at `D>=1` without clipping/reset; unsupported curve-domain requests fail closed;
- uncertainty is emitted explicitly and synthetic provenance remains prohibited from design fitness;
- focused/full tests, compile/static checks, staged-diff check, explicit commit, and clean-tree replay pass.

## Risks and explicit non-goals

Rainflow endpoint half cycles and block boundaries must remain explicit; blocks will not be concatenated in a way that invents transition cycles. Miner sequence independence is a model limitation, while first-crossing chronology is still preserved. No strain-life, plastic hysteresis, crack growth, multiaxial critical plane, physical coupon, vehicle fitness, push, or publication is included.
