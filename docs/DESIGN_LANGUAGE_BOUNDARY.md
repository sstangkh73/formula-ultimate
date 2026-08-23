# Design Language Boundary

## Why This Document Exists

"No prescribed architecture" cannot mean "no assumptions." Search can only
discover designs expressible by its representation and component library. This
document makes that inductive bias visible and versionable.

## Phase-1 Fixed Experimental Boundary

To isolate powertrain topology as the independent variable, Phase 1 fixes:

- one vehicle body represented by mass and longitudinal coefficients;
- four abstract tyre contact patches at fixed positions;
- a one-dimensional track coordinate and prescribed track profile;
- ambient conditions per experiment;
- component catalog version;
- budget, starting energy, and race-completion rules;
- search/evaluation budget and random-seed set.

These restrictions do not define the final Formula Ultimate vehicle. They are
controls for the first causal experiment.

## Topology Freedom in Phase 1

Candidates may vary:

- energy-source count and type;
- converter count, type, and connection;
- presence or absence of gearing and mechanical differentials;
- actuator count and assignment to permitted tyre endpoints;
- series, parallel, and mixed energy paths;
- component parameters within declared envelopes;
- regenerative paths when supported by the selected components.

No component is mandatory except what is logically required to move, remain
within constraints, and complete the race.

## Typed Physical Domains

Every connection uses an explicit domain and conjugate effort/flow variables:

| Domain | Effort | Flow | Power convention |
|---|---|---|---|
| Electrical DC | voltage (V) | current (A) | `V * A` |
| Mechanical rotational | torque (N m) | angular speed (rad/s) | `tau * omega` |
| Mechanical translational | force (N) | velocity (m/s) | `F * v` |
| Chemical fuel | specific energy (J/kg) | mass flow (kg/s) | model-defined |
| Thermal | temperature (K) | heat flow (W) | signed heat transfer |
| Control | command/state | signal rate | carries no physical power |

Control edges cannot create energy. Components must expose losses and rejected
heat rather than hiding efficiency deficits.

## Graph Validity Gates

A candidate graph is rejected before race simulation when it has:

- incompatible port domains or directions;
- dangling required ports;
- an energy-consuming path with no reachable source;
- unbounded source, sink, or state values;
- duplicate exclusive connections;
- a forbidden algebraic loop without a declared solver strategy;
- parameters outside component envelopes;
- static mass, cost, or volume above the experimental budget;
- no path capable of applying longitudinal force to a tyre endpoint.

Passing graph validation means representationally valid, not performant,
stable, safe, or physically certified.

## Versioning Requirement

Every experiment record must contain:

- design-language version;
- component-catalog version and hash;
- simulator version and Git commit;
- configuration hash;
- random seed;
- search algorithm and evaluation budget.

Comparisons across design-language versions are separate experiments unless a
documented compatibility analysis shows otherwise.
