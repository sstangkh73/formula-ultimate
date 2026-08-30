# Whole-Vehicle Section-Force Refined Evaluator

Thai companion: `WHOLE_VEHICLE_SECTION_FORCE_REFINED_EVALUATOR.th.md`

## Bounded claim

Work 053 establishes `project_frame6dof_plus_calculix_b31_section_force_v2` as an independent refined evaluator for the bounded Work 047 beam-network grammar, frozen Work 048 holdout wrenches, and declared synthetic linear-elastic material. It derives stiffness, deformation, reactions, section resultants, surface equivalent stress, and yield margin from candidate geometry. It does not use the Work 050 structural capacity factors.

This is numerical beam-network evidence, not complete-vehicle physical validation. It does not establish local solid stress, real-joint behavior, nonlinear yield, fracture, fatigue life, buckling, crash response, or hardware safety.

## Why Work 052 stopped

CalculiX B31 expands beams for material-stress output. `*EL PRINT` stress is sampled at expanded-element integration points, while the analytical cantilever reference `6 F L/b^3` is extreme-fiber stress at the root. Comparing these directly produced a false location mismatch. The [CalculiX beam documentation](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node60.html) distinguishes integration-point output from section-force output, and the [cantilever example](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node20.html) discusses integration-point, extrapolated-node, and section-force representations.

Work 053 instead requests `*EL FILE,SECTION FORCES`. Its six resultants follow the [CalculiX section-force component definition](https://www.feacluster.com/CalculiX/ccx_2.18/doc/ccx/node265.html): two shears, normal force, torque, and two bending moments. For a rectangular section, the evaluator computes

```text
sigma_surface = |N|/A + |M1| c1/I1 + |M2| c2/I2
tau_surface   = 1.5 sqrt(V1^2 + V2^2)/A + |T| cmax/J
sigma_vm      = sqrt(sigma_surface^2 + 3 tau_surface^2)
```

Each unlike section is requested in a separate full coupled CalculiX run so shared-node averaging cannot mix section properties. All section-output runs must replay the same displacement.

## Experimental result

The frozen refinement series was `4/8/16` B31 elements per branch. At 16 subdivisions the maximum analytical error across both solvers and both displacement/stress metrics was `3.4276%`. Project-frame equilibrium residual never exceeded `2.2293e-11` relative over 54 candidate states. Seven of nine Work 050 promotions passed both holdouts; among those seven, maximum last-two change was `2.0489%`, maximum fine cross-model difference was `5.0207%`, minimum yield margin was `379.45`, and maximum displacement was `6.1326e-6 m`.

Two candidates failed only the preregistered `8%` fine stress-difference gate:

- `candidate-9b03158dc541df18`: `16.69%` and `17.66%` stress difference.
- `candidate-372db49a7cbceba5`: `32.24%` and `33.51%` stress difference.

Their large calculated yield margins do not override the disagreement. They remain rejected because formulation sensitivity is itself contradicting evidence.

## Decision and remaining evidence

Decision: `independent_refined_evaluator_available`; candidate set: `partially_supported` (`7/9`). This closes the evaluator-availability blocker but does not retroactively make the two rejected candidates valid.

Still missing are solid/contact stress concentrations, nonlinear material response, local buckling, fatigue calibration, vibration, crash, physical material records, manufacturing variation, and hardware tests. Any next whole-vehicle pilot must admit only candidates that pass this refined gate and must retain the same evidence boundary.
