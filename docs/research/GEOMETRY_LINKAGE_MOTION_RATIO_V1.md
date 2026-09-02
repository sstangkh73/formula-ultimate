# Geometry-Derived Linkage Motion Ratio V1

Thai companion: `GEOMETRY_LINKAGE_MOTION_RATIO_V1.th.md`

## Claim boundary and equations

Work 075 replaces Work 073's implicit one-to-one spring/wheel displacement with a small-angle rigid-rocker transform derived from declared 3D points and directions. It is geometry-causal Level-0 evidence, but the points are synthetic declarations rather than STEP/FreeCAD joint measurements.

For unit rocker rotation axis `a`, pickup arm `r`, and unit displacement direction `d`, the projected lever is:

```text
l = d dot (a cross r)
motion ratio R = l_spring / l_wheel
k_wheel = k_spring R^2
c_wheel = c_spring R^2
travel_wheel = travel_spring / R.
```

The sign must be positive so declared spring compression agrees with wheel compression. Zero projected arms, opposite signs, missing contacts, and non-finite geometry fail closed. Axis and direction vectors are normalized; a user cannot change the ratio by scaling a direction vector.

## Experiment and results

The selected powered-contact geometry uses `0.16 m` spring and `0.20 m` wheel projected arms, deriving `R = 0.7999999999999999`. The rear contact derives `R = 1.0`. Powered wheel-coordinate stiffness and damping therefore scale by `0.64`, while available wheel travel scales by `1.25`.

The transformed Work 073 reference finished with:

- maximum heave `0.0008656698982980348 m`;
- maximum suspension travel `0.019278824606844512 m`;
- minimum actual normal load `266.8789268655951 N`;
- maximum combined relative energy residual `5.0778645277023315e-9`.

Unit-ratio geometry preserved Work 073 result SHA-256 exactly at `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`. Changing one spring pickup from `0.16 m` to `0.18 m` changed both application and coupled-result identities. Axis scaling, linkage permutation, and mirrored geometry preserved the derived ratio; degenerate and direction-opposed cases were rejected.

The selected application SHA-256 is `51b6255347e4a6a59428ee309f4f78c8e981baa437386bdcf3505df9d8403487`; coupled result SHA-256 is `7fd4af71e95dc49be5330762efe284a20a0ac86bc73b19df6a17c41d0e0b552a`; canonical evidence SHA-256 is `69d4ad48f82026fdca4134a0c00519f9dc4df837cb43c2ad0608b7eafe16c939`; byte-identical primary/replay file SHA-256 is `37864D0AE558AFBEB4E2E90B63DE1A48D84C17D4C6B8EC6EB106414E02A2DE64`.

## Interpretation and missing evidence

The unit-ratio preservation and geometry mutation support correct virtual-work coupling rather than a decorative geometry field. However, the current transform is local and linear. It omits finite-angle arcs, pushrod articulation, joint/bearing compliance, backlash, friction, collision, anti-dive/squat, structural loads, and extraction from actual CAD topology. Confidence is high in the declared small-angle transform and low that its synthetic points represent a buildable suspension.
