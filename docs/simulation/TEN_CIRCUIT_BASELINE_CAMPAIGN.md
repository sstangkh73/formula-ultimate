# Ten-Circuit Fixed-Topology Baseline Campaign

Status: Work 029 Level-0 analytical proxy baseline

Thai companion: `TEN_CIRCUIT_BASELINE_CAMPAIGN.th.md`

## Purpose and Boundary

Work 029 runs one immutable fixed-topology reference family through the Work 028 eight-stage whole-race orchestrator for every versioned circuit profile and seed. It establishes reproducible integration baselines and fair opportunity controls before any free-topology candidate comparison.

The campaign uses official profile identity, lap length, race distance, width evidence, source metadata, and design-pressure metadata. It does **not** have surveyed local centreline/corridor geometry or event-time weather. The local path and weather are explicit analytical controls; therefore every run has evidence grade `profile-distance-analytical-proxy` and `real_circuit_admitted = false`.

## Pinned Protocol

`config/simulation/fixed_topology_baseline_protocol_v1.json` pins:

- campaign: `work029-ten-circuit-fixed-topology-v1`;
- architecture: `coupled-level0-reference-v4`;
- family: `fixed-four-steady-drag-v1`;
- four fixed contacts and the Work 025-027 component library;
- mass `1000 kg`, width `1.8 m`, speed `10 m/s`;
- reference area `1.5 m^2` and analytical drag coefficient `0.5`;
- primary energy `50,000,000 J`, drive efficiency `0.9`, and recovered capacity `5,000,000 J`;
- maximum drive force `1000 N` and `steady-drag-balance-v1` strategy;
- synthetic dry-track control at `300 K`, `101325 Pa`, zero wind/precipitation, and a `50 m` proxy half corridor;
- timestep `1000 s`, timeout `40000 s`, and maximum `64` steps per run;
- design-evaluation budget `1`;
- seeds `(17, 29, 43)`; and
- a fixed seven-profile calibration / three-profile holdout split.

Unknown protocol fields and implicit integer coercion are rejected. The complete protocol, controls, component opportunity, architecture, each run, and the campaign result have SHA-256 identities.

## Reference Physics

The analytical aerodynamic map has nonzero drag and zero side force/downforce. On every step the pinned strategy requests drive force equal to the current calculated aerodynamic drag. Contact force, aerodynamic drag, motion, drive-wheel work, drive efficiency loss, central energy state, component heat, health, and race progress therefore pass through the real coupled adapters.

This is stronger than a frictionless zero-energy coast, but it remains incomplete: rolling resistance, real cornering, gradients, braking zones, traffic, changing weather, measured aero, tyre degradation, and circuit-local geometry are absent.

## Fairness and Holdout Rules

- Every circuit/seed run receives the same architecture, vehicle/component opportunity, initial energy, strategy law, timestep, timeout, and maximum step budget.
- Shorter races may consume fewer steps; the maximum opportunity is identical and no run receives an extension.
- Calibration and holdout IDs are disjoint, complete, and fingerprinted before execution.
- Holdout results are reported but cannot mutate the family or controls.
- Seed identity remains in replay metadata even when disabled stochastic hazards make performance metrics identical.
- Static published-width screening is retained. `indeterminate` means width evidence is unresolved, not passed.

## Validated Result

All `30/30` runs (`10 profiles × 3 seeds`) finished with all residuals passed and no run exceeding `31/64` steps. Each seed produced the same controlled performance metrics for a circuit while retaining a distinct replay identity.

| Circuit | Partition | Distance (m) | Time (s) | Primary energy used (MJ) | Steps | Static width |
|---|---|---:|---:|---:|---:|---|
| Bahrain 2025 | holdout | 308238 | 30823.8 | 15.012090 | 31 | indeterminate |
| Hungaroring 2026 | calibration | 306630 | 30663.0 | 14.933776 | 31 | indeterminate |
| Mexico City 2025 | holdout | 305354 | 30535.4 | 14.871631 | 31 | indeterminate |
| Monaco 2026 | calibration | 260286 | 26028.6 | 12.676688 | 27 | screen_passed |
| Monza 2026 | calibration | 306720 | 30672.0 | 14.938159 | 31 | screen_passed |
| Sao Paulo 2025 | holdout | 305879 | 30587.9 | 14.897200 | 31 | screen_passed |
| Silverstone 2026 | calibration | 306198 | 30619.8 | 14.912736 | 31 | indeterminate |
| Singapore 2025 | calibration | 306143 | 30614.3 | 14.910058 | 31 | indeterminate |
| Spa 2026 | calibration | 308052 | 30805.2 | 15.003032 | 31 | indeterminate |
| Suzuka 2026 | calibration | 307471 | 30747.1 | 14.974735 | 31 | screen_passed |

Campaign evidence:

- architecture fingerprint: `abf3148cfba2063f8fdba23951239b2b0a4a899c391503d3e46db69fd203618d`;
- protocol fingerprint: `4c1c93a21c8ada5d8859eebbce1adb11f750787b2f522ba671f30be08ea6f2a6`;
- controls fingerprint: `9c6a168a90a1e8d7cf33f72f3410e8d193cfd4edffddf7a136c84a1bed0371c9`;
- result fingerprint: `44dc7f85fac097b8ecbb38c04ff14a595702e8e4a0b9134ba70403fc451bfa98`.

## Falsification

Tests reject overlapping/incomplete partitions, hidden protocol fields, float values in integer budgets, real-circuit admission on proxy evidence, unsupported evidence grades, and mutated component opportunity. An insufficient one-step budget produces observable timeout results rather than silent extension. Catalog order permutation replays exactly under a reduced controlled campaign.

## Interpretation

The result proves that the central Level-0 software can execute one energy-consuming fixed-topology reference consistently across all ten profile distances under pinned opportunity. It does not prove that the reference can drive those physical circuits, that its times are plausible, or that it is optimized. It is a comparison-control artifact, not a discovery.

Work 030 must still attempt deliberate integrated defects, numerical refinement, uncertainty/claim review, and cross-model promotion gating. Free-topology candidates remain blocked from discovery or real-race claims until higher-fidelity independent evidence exists.
