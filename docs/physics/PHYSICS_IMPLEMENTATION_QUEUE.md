# Physics Implementation Queue — Work 010–019

Status: Active sequential queue

Thai companion: `PHYSICS_IMPLEMENTATION_QUEUE.th.md`

## Execution rule

Work items execute strictly in numeric order. Only one item may be `In progress`.
Each item requires its own bilingual plan, implementation, validation, full
bilingual result report, and verified commit. If a material problem is found,
create a separate bilingual report under `docs/problem_reports/`, resolve or
explicitly bound the problem, rerun validation, and only then complete and
commit the item. The next item must not begin before the preceding commit is
verified.

| Work | Status | Deliverable | Completion gate |
|---:|---|---|---|
| 010 | Completed | Versioned 3D circuit corridor and whole-vehicle swept-envelope admission | Reject static-fit/swept-fail and steering-fail cases; unsupported real geometry stays indeterminate |
| 011 | Completed | Tyre-road longitudinal/lateral force and saturation boundary | Analytical friction-circle/ellipse tests; requested and saturated forces both observable |
| 012 | Completed | Typed energy and powertrain component graph | Source, converter, transmission, and tyre ports compile deterministically with SI/sign contracts |
| 013 | Completed | Independent energy-conservation audit | Lossless/lossy reference chains close within scaled tolerance; hidden or double-counted energy invalidates run |
| 014 | Completed | Lumped thermal, cooling, derating, and failure physics | Heating/cooldown references pass; temperature is never silently clipped |
| 015 | Completed | Deterministic full-race completion loop | Finish, depletion, timeout, invalidity, and failure outcomes replay identically across circuit profiles |
| 016 | Queued | Lateral/yaw dynamics, load transfer, and combined tyre force | Reference steady-state and transient cases converge and conserve declared balances |
| 017 | Queued | Aerodynamic force, balance, and cooling-flow model | Drag/downforce/moment maps validate across speed, ride height, yaw, and active state envelopes |
| 018 | Queued | Suspension, mechanical braking, and regenerative braking | Wheel loads, travel, brake energy, regen limits, and failure events remain physically accounted |
| 019 | Queued | Reliability, traffic, weather, degradation, and race strategy | Multi-lap/multi-event digital race completes with deterministic strategy controls and uncertainty-aware failures |

## Shared definition of done

Every item must satisfy all of the following:

1. SI assumptions, model boundary, independent/dependent variables, controls,
   success criteria, and failure criteria are declared before implementation.
2. Every implemented law has analytical or independently checkable tests.
3. Numerical invalidity, conservation residuals, saturation, depletion,
   derating, and missing evidence remain observable.
4. The preferred hypothesis is actively challenged by at least one falsifying
   reference case.
5. English and Thai Markdown companions remain synchronized.
6. Full repository tests, work-specific validator, compilation, and whitespace
   checks pass.
7. Explicit staged scope and `git diff --cached --check` pass.
8. The item has one verified local commit whose hash is recorded in the final
   handoff. Remote push is outside this queue unless separately requested.

## Dependency path

```text
010 circuit corridor
  -> 011 tyre/contact
  -> 012 energy graph
  -> 013 conservation audit
  -> 014 thermal/cooling
  -> 015 race loop
  -> 016 lateral/yaw/load transfer
  -> 017 aerodynamics
  -> 018 suspension/braking/regen
  -> 019 digital race reliability and strategy
```

The queue is a staged evidence plan, not a claim that queued physics already
exists. Level-0 or reduced-order success never by itself establishes physical
validation, safety, manufacturability, or real-world superiority.
