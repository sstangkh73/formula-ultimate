# Work 015 Problem Report: Exact Event Tie Becomes Numerical Energy Overspend

Status: Resolved

Thai companion: `2026-08-26_015_event-tie-energy-overspend.th.md`

## Problem

A falsifying test constructs a race where finish, primary-energy depletion, and
timeout occur at the same analytical time (`10 s`). The declared tie priority
requires `finished`. The initial implementation instead returned `invalid`:

```text
runtime numerical failure: event ordering overspent onboard energy by
0.000244140625 J
```

The energy scale was `1354976035920.0 J`, so the overspend was a relative
floating-point residual of approximately `1.8e-16`, not a material undeclared
energy source.

## Root cause and impact

Finish localization uses the first-true bisection bound while depletion uses the
last non-overspending bound. At an exact physical tie those adjacent floating-
point bounds can straddle the mathematical event. Selecting finish then
evaluates source energy on the upper bound, producing a tiny negative remaining
energy. The unconditional negative-energy guard converted the declared tie into
`invalid` and contradicted deterministic event semantics.

Without a fix, candidates at a finish/energy boundary can receive a result that
depends on representational rounding rather than declared race rules.

## Planned resolution

1. Add explicit absolute/relative energy-event tolerances to race controls and
   replay metadata.
2. Preserve the raw signed boundary residual in step and terminal telemetry.
3. When a higher-priority `finished` or `failed` event exceeds available energy
   only within scaled tolerance, set remaining usable energy to zero while
   retaining the negative raw residual as evidence.
4. Keep any overspend beyond tolerance as `invalid`.
5. Require the exact triple-tie test to return `finished`, nonnegative remaining
   energy, and the observable `-0.000244140625 J` boundary residual.
6. Rerun all Work 015 and repository validation before marking this report
   resolved.

This tolerance addresses numerical event coincidence only. It does not permit
energy replenishment or hide a physically meaningful deficit.

## Resolution evidence

The controls, replay metadata, step telemetry, and terminal result now expose
the energy-event tolerances and signed boundary residual. The exact triple tie
returns `finished`, remaining usable energy `0.0 J`, and residual
`-0.000244140625 J`. Repeating it with both tolerances set to zero returns
`invalid` with the overspend reason. Work-specific tests (`10`) and the full
repository suite (`110`) pass. The validator reproduces the resolved tie and
reports zero replenishment events.
