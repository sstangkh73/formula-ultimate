# Research Charter

## Working Thesis

Formula Ultimate investigates whether engineering architectures can be
discovered without prescribing a conventional vehicle layout, while retaining
explicit physical, safety, resource, and task constraints.

## Primary Research Question

When vehicle architecture is not prescribed, does topology-evolving design
search rediscover conventional race-car architectures, or produce distinct
solutions adapted to different racing environments?

## Phase-1 Question

Under matched resource and search budgets, can a typed-graph topology search
discover valid one-dimensional powertrain architectures that match or exceed
optimized fixed EV, ICE, and hybrid baselines?

## Falsifiable Hypotheses

### H1: Feasible topology discovery

Free-topology search produces physically valid, race-completing candidates at a
rate materially above unguided random graph generation.

### H2: Competitive performance

At equal evaluation budgets, at least one discovered topology is non-dominated
against tuned fixed-topology baselines on race time, energy, cost, mass, and
reliability.

### H3: Environment-dependent specialization

Different track/energy regimes produce architecture families whose topology
distributions differ across repeated seeds and transfer asymmetrically between
regimes.

### H4: Fidelity survival

The ordering of promoted candidates remains sufficiently stable when evaluated
at the next fidelity level; otherwise Level 0 is not a trustworthy search gate.

## Alternative Explanations to Test

- Apparent innovation is a numerical or objective-function exploit.
- Topology differences come from unequal compute budgets.
- Convergence is caused by component-library bias rather than physics.
- Surrogate uncertainty hides poor high-fidelity performance.
- A topology appears specialized because parameters, not connections, differ.

## Current Phase

Repository bootstrap and Level-0 physics-system design. No discovery or
performance hypothesis has yet been tested.

## Explicit Non-Goals for the Initial Simulator

- Full 3D geometry generation
- CFD or detailed external aerodynamics
- FEA or crash certification
- Detailed tyre transients and contact-patch mechanics
- Free wheel count or wheel placement
- Active suspension
- Driver/control-policy learning
- Claims of manufacturability or real-world safety

These are future fidelity or scope expansions, not silently approximated
features of Level 0.
