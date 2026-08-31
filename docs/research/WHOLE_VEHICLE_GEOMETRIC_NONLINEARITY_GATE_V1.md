# Whole-Vehicle Geometric-Nonlinearity Gate v1

Thai companion: `WHOLE_VEHICLE_GEOMETRIC_NONLINEARITY_GATE_V1.th.md`

## Purpose and boundary

`whole_vehicle_geometric_nonlinearity_gate_v1` is a fail-closed post-refinement sensitivity gate for the bounded Work 062 vehicle-frame grammar. It reruns each frozen finalist geometry and both Work 048 holdout loads using CalculiX B31 beams with `*STEP,NLGEOM`, then compares the result with the exact Work 062 fine-mesh linear reference.

The gate tests whether geometric nonlinearity materially amplifies a candidate's response inside the existing beam idealization. It is not a buckling certificate: v1 adds no initial imperfection, eigenvalue extraction, branch-following, contact, solid mesh, or material plasticity. The material remains synthetic and linear elastic.

## Frozen inputs

- Inclusion rule: all and only the 51 Work 062 candidates whose holdout, Work 053 refinement, and STEP/FreeCAD witness passed.
- Load cases: `aero_extreme` and `holdout_combined` from the frozen Work 048 holdout partition.
- Geometry: exact candidate variables/declaration from immutable Work 062 evidence; no repair or optimization.
- Mesh: 16 B31 subdivisions per branch, matching the Work 062 fine reference.
- Material: `synthetic_linear_elastic_aluminium_like_v1`, `E = 70 GPa`, Poisson ratio `0.3`, nominal yield stress `250 MPa`; this is not a certified allowable.
- Solver evidence: exit code zero plus stdout containing `nonlinear geometric`; absence fails closed.

## Outputs and falsification

For each candidate/load-case pair, the gate records nonlinear displacement, surface von Mises stress, their ratios to the linear reference, nonlinear yield margin, process status, confirmation status, failure codes, and a canonical SHA-256 result identity.

A case passes only when all conditions hold:

- nonlinear displacement amplification `<= 1.10`;
- nonlinear stress amplification `<= 1.15`;
- nonlinear yield margin `>= 1.10`;
- all numeric evidence is finite and positive;
- process and solver-confirmation checks pass.

A candidate passes only with exactly one hash-valid terminal result for each required holdout case and both cases passing. Duplicate, missing, extra, tampered, nonterminal, non-finite, or identity-mismatched evidence is rejected rather than repaired.

## Implementation validation

The existing linear B31 deck remains byte-structure compatible at its step header because geometric nonlinearity is opt-in. A live CalculiX 2.22 smoke run accepted the nonlinear deck, reported geometric-nonlinearity activation, exited zero, and produced parseable displacement, stress, and section-force evidence. Unit tests cover threshold boundaries, invalid configuration, missing confirmation, process failure, non-finite values, exact case sets, duplicate cases, tamper detection, and deterministic replay.

Work 063 freezes and commits the adapter only. Applying it to Work 062 finalists requires a separate clean-tree execution record so candidate outcomes cannot influence the implementation or thresholds.
