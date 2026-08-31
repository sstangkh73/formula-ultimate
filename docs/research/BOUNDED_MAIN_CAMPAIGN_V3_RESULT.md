# Bounded Main Campaign v3 Result

Thai companion: `BOUNDED_MAIN_CAMPAIGN_V3_RESULT.th.md`

## Decision

Protocol `bounded_whole_vehicle_main_campaign_v3`, campaign `FU-BMC-003`, completed with status `completed_with_supported_finishers`. All `2,880` attempted evaluations reached terminal results with equal budgets: 80 attempts for each of 36 treatment/seed streams, 960 attempts per treatment, no pending reservations, and 960 unique GRID proposals. Exact clean-tree replay passed.

This is comparative evidence only inside the frozen five-variable geometry grammar, synthetic-material assumptions, load partitions, Level-0 evaluator, linear-beam refinement, and STEP/FreeCAD witness route. It is not physical validation, safety certification, manufacturability evidence, arbitrary-topology validation, or proof of algorithm superiority.

## Experimental design

- Independent variable: proposal treatment `GRID`, `RANDOM`, or `EVOLUTION`.
- Paired experimental units: seeds `55001` through `55012`; individual attempts are not independent replicates.
- Controls: identical 80-attempt budgets, candidate bounds, training evaluator, frozen training/holdout partitions, promotion count, Work 053 refinement gates, and `3D -> STEP -> FreeCAD` witness requirements.
- Dependent variables: supported-finisher presence per treatment/seed, seed-level best frozen-holdout time, failure distribution, refinement survival, and CAD-witness completion.
- Primary falsification rule: a non-positive EVOLUTION-minus-RANDOM supported-finisher-rate difference contradicts the preferred direction. Algorithm superiority additionally requires independent replication under a new protocol.

## Execution evidence

Training produced `2,107` feasible and `773` structural-failure outcomes. All 36 streams selected two candidates, so 72 candidates entered frozen holdout with zero promotion shortfall. Every promoted candidate was feasible on holdout. Work 053 refinement passed 51 and rejected 21 as `refined_disagreement`; the latter were recorded and their CAD stage was `not_run`. All 51 refinement survivors produced valid four-solid STEP assemblies and passed FreeCAD 1.1.3 inspection with no hidden geometry repair.

The stage ledger contains one refinement benchmark, 36 promotion records, 72 holdout records, 72 refinement records, and 72 CAD-witness records. It records 1,299 CalculiX processes, 51 CadQuery generation processes, and 51 FreeCAD inspection processes. The admitted invocation elapsed `10,327.025 s`; external-process wall time recorded in stage evidence sums to `239.847 s`.

## Preregistered outcomes

| Treatment | Supported seeds | Rate |
| --- | ---: | ---: |
| GRID | 10/12 | 0.8333 |
| RANDOM | 9/12 | 0.7500 |
| EVOLUTION | 11/12 | 0.9167 |

For the primary EVOLUTION-minus-RANDOM comparison, the paired rate difference was `+0.1667`, with two EVOLUTION-only pairs, zero RANDOM-only pairs, exact two-sided McNemar `p = 0.5`, and paired-bootstrap 95% interval `[0.0000, 0.4167]`. The observed direction supports the preferred hypothesis descriptively, but the exact test does not establish a statistically significant difference.

On the nine seeds where both treatments produced supported finishers, the EVOLUTION-minus-RANDOM paired median best-time difference was `-2.232959 s`; exact two-sided sign-flip `p = 0.0625`, with paired-bootstrap 95% interval `[-2.564327, -1.546702] s`. This favors EVOLUTION in this bounded run but does not cross a conventional `0.05` significance threshold. GRID comparisons remain descriptive by preregistration.

## Replay identities

- Protocol fingerprint: `9ef748f2719923632a05ef5fcbba95b8f2fa1b4156d2dbbf6cb9b4fbd02d4c36`.
- Training fingerprint: `503917192f3029c66e27cec2a2ef1f7521ebfba9c2872e3541945bf35a281176`.
- Stage fingerprint: `9e2554f865788b98c21cff736063d46857eff888e022299256222fad186e1182`.
- Analysis fingerprint: `f6a86288b3653b75d1d5c56f62b948344884911d946b91ef8ddbfc6e46dbef19`.
- Execution source commit: `bfa33a29bc92890628df0429351cef3e6eed017e`.
- Worktree dirty during run: `false`.

## Scientific review

Supporting evidence is equal opportunity allocation, immutable consumed failures, frozen holdout separation, exact chained-ledger replay, terminal downstream evidence for every promotion, and 51 derivable STEP/FreeCAD survivors. Contradicting evidence is the non-significant primary exact test and 21/72 refined disagreements despite Level-0 holdout feasibility. The preferred interpretation may depend on the frozen five-variable grammar rather than general search quality.

Confidence is high that the bounded campaign executed and replayed as preregistered, moderate that EVOLUTION was faster within common-success seeds in this campaign, and low for transfer outside this evaluator domain. Missing evidence includes independent replication, solid/contact/nonlinear whole-vehicle analysis, calibrated physical material properties, manufacturing tolerances, fatigue spectra, crash/failure propagation, and hardware tests.
