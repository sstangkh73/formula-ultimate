# Held-Out Race Robustness V1

Thai companion: `HELDOUT_RACE_ROBUSTNESS_V1.th.md`

Status: Implemented by Work 128 as a sealed synthetic holdout gate.

## Evidence boundary

Finalist, controller, evaluator, rules and holdout identities are sealed before exposure. Training and holdout condition identifiers must be disjoint. Every finalist runs every registered condition, and incomplete or stopped trajectories remain in telemetry. Post-exposure tuning, repair, source changes or threshold changes invalidate the admitted comparison.

The registered estimand is fixed-finalist time minus open-finalist time for paired finishers. Robust superiority additionally requires the lower uncertainty interval to reach the registered time improvement, every finalist to meet completion rate, and all source-energy, thermal and structural gates to pass. Numerical uncertainty is added to the paired statistical interval rather than silently corrected.

Exact replay requires the same result SHA-256. These trajectories are deterministic synthetic evidence; numerical race completion does not establish manufactured behavior, external novelty, vehicle promotion or physical validation.
