# Coupled-Vehicle Implementation Queue — Work 021–030

Status: Active sequential queue

Thai companion: `COUPLED_VEHICLE_IMPLEMENTATION_QUEUE.th.md`

## Execution rule

Work items execute strictly in numeric order. Only one item may be `In progress`.
Every item requires a bilingual plan before changes, implementation and
falsification evidence, bilingual result after validation, explicit staged
scope, `git diff --cached --check`, and one verified commit. A material problem
requires a separate bilingual report and resolution or explicit bound before
completion.

| Work | Status | Deliverable | Completion gate |
|---:|---|---|---|
| 021 | Completed | Unified experiment manifest, topology-neutral shared state, deterministic coupling architecture compiler, residual ledger, and event arbitration | Reference architecture compiles/fingerprints identically under permutation; invalid dependencies/states/residuals/ties are explicit |
| 022 | Completed | Atomic coupled-step transaction and adapter execution protocol | Adapters read one immutable start state, write declared outputs only, and either commit one complete next state or return observable invalidity without partial mutation |
| 023 | Completed | Circuit, environment, weather, traffic, and strategy input adapters | Ten circuit profiles produce deterministic typed step inputs; missing spatial/weather evidence remains explicit and cannot become neutral silently |
| 024 | Queued | Aerodynamic force/cooling to chassis force-moment and normal-load coupling | Aero forces/moments alter shared chassis/contact loads with closed force/moment residuals and unsupported map queries invalidate the step |
| 025 | Queued | Per-contact tyre, suspension, mechanical braking, and regeneration coupling | Arbitrary contact sets share normal loads, combined tyre capacity, travel, brake torque/heat, and central recovery requests without hidden redistribution |
| 026 | Queued | Coupled longitudinal, lateral, yaw, and race-distance state integration | One motion state advances from summed contact/aero forces and moments; analytical references, timestep refinement, and corridor failures remain observable |
| 027 | Queued | Central energy, thermal, cooling, degradation, damage, and reliability state coupling | Typed transfers close through the independent audit; recovery, heat, derating, damage, seeded failure, and earliest event truncate the same step |
| 028 | Queued | Deterministic whole-race coupled orchestrator and replay telemetry | One fixed-topology reference executes all coupled stages until finish/depletion/failure/timeout/invalid with exact same-seed replay and complete provenance |
| 029 | Queued | Ten-circuit fixed-topology baseline campaign and fair compute controls | At least one defensible reference family completes all ten profiles under pinned energy, component opportunity, evaluation budget, seeds, and holdout policy |
| 030 | Queued | Integration falsification, numerical refinement, cross-model promotion gate, and release review | Deliberate coupling defects fail; convergence/uncertainty evidence is recorded; unsupported candidates cannot be promoted or called discovered |

## Dependency path

```text
021 contracts and architecture
  -> 022 atomic adapter transactions
  -> 023 circuit/environment inputs
  -> 024 aero/chassis/load coupling
  -> 025 contact/suspension/brake coupling
  -> 026 shared vehicle motion
  -> 027 energy/thermal/health coupling
  -> 028 coupled whole-race orchestration
  -> 029 fair fixed-topology baselines
  -> 030 falsification and promotion gate
```

## Shared definition of done

1. Every signal/state field has declared identity, unit/meaning, producer,
   consumer, timing semantics, and invalid-state behavior.
2. Physics modules exchange state only through the versioned coupling contract.
3. Force, moment, energy, distance, thermal, and event residuals remain
   observable and are never silently corrected.
4. Arbitrary valid contact/component topologies remain possible; reference
   fixed topology is a controlled integration treatment, not a design mandate.
5. Same inputs, versions, architecture, artifacts, and seed replay exactly.
6. Full repository tests, work validator, compilation, whitespace, staged-scope,
   and commit checks pass.
7. Level-0 success never by itself becomes physical validation, safety,
   manufacturability, discovery, or real-race superiority.

The queue builds the missing central simulator in falsifiable stages. It does
not authorize autonomous whole-vehicle evolution before Work 030 closes the
integrated reference and promotion gates.
