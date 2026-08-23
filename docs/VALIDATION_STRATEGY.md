# Validation Strategy

## Evidence Ladder

Validation claims are limited to the strongest completed layer:

1. **Structural:** files, schemas, and package boundaries are present.
2. **Unit:** individual equations/components match analytical references.
3. **Invariant:** conservation, bounds, and dimensional contracts hold.
4. **Integration:** connected components and race loop behave coherently.
5. **Regression:** named reference cases remain stable across changes.
6. **Numerical:** results converge under timestep/solver refinement.
7. **Cross-model:** promoted candidates agree with an independent model.
8. **Empirical:** simulation agrees with measured data and uncertainty bounds.

The initial commit targets only structural validation.

## Required Physics Tests

Before Level 0 may be used for research conclusions, it must include:

- zero-input rest state;
- constant-force analytical acceleration;
- drag-only coast-down;
- grade equilibrium case;
- tyre-force saturation;
- source depletion at a known energy draw;
- ideal lossless energy-chain balance;
- lossy chain with heat accounting;
- thermal rise and passive cooldown references;
- component envelope rejection;
- graph invalidity cases;
- deterministic replay;
- timestep refinement/convergence;
- NaN/infinity/negative-state rejection.

## Experiment Controls

- Same component catalog and constraints across topology treatments.
- Same number of candidate evaluations or measured compute budget.
- Predeclared random seeds and sufficient independent repeats.
- Fixed-topology baselines tuned with competitive optimization effort.
- Holdout tracks/configurations not used during search.
- Surrogate predictions reported with uncertainty and periodically audited by
  the authoritative simulator.

## Evidence Preservation

Every result report records:

- exact command;
- start/end or duration when relevant;
- exit code;
- concise output;
- generated artifact paths and hashes when material;
- Git commit/configuration/seed for experiments;
- failed tests and unresolved limitations.

Generated large artifacts belong outside Git under `artifacts/` or `runs/`;
their manifest and hashes should be preserved in the corresponding result log.

## Claim Language

- "Structurally validated" does not mean physics works.
- "Simulation-valid" does not mean manufacturable or safe.
- "Promoted" means worthy of a stronger model, not proven optimal.
- "Discovered" must identify the design-language version and comparison
baseline.
- "Novel" requires comparison against known architectures and cannot be based
  on appearance alone.
