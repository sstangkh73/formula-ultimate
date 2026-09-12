# Material Failure Scope V1

Thai companion: `MATERIAL_FAILURE_SCOPE_V1.th.md`

Status: Implemented by Work 116 as an applicability and reference-law gate.

## Evidence boundary

This contract pins Work 111 stress, Work 114 dynamic-history and Work 115 temperature evidence. Every material record declares property units, source, evidence class, temperature/rate bounds, process, uncertainty and allowed uses. Synthetic or analytic records cannot be relabelled as measured survival evidence. Out-of-range temperature/rate/process, missing units and unregistered mixtures fail closed.

First-yield uses the lower uncertainty-adjusted yield stress. Pinned-column buckling uses `pi^2 E I / (K L)^2`; the bounded imperfection fixture reduces capacity by `1 + imperfection/radius_of_gyration`. These are mathematical verification fixtures, not universal constitutive or collapse laws.

The candidate aluminium record is synthetic and therefore permits diagnostic margins only. Fatigue, fracture and wear remain `unresolved_missing_tested_data`. Missing measured process-qualified properties, geometry-applicable member mapping, manufacturing variability and physical correlation block physical-survival claims regardless of a positive diagnostic margin.

Exact replay requires the same result SHA-256. This contract does not establish fatigue life, fracture resistance, wear, manufacturing qualification, safety certification or complete physical survival.
