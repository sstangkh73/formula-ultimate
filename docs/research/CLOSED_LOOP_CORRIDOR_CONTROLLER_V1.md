# Closed-Loop Corridor Controller V1

Thai companion: `CLOSED_LOOP_CORRIDOR_CONTROLLER_V1.th.md`

## Claim boundary

Work 074 closes steering feedback around the Work 073 drivetrain, planar, sprung-body, suspension, tyre, and road plant. It is a deterministic `0.5 s` synthetic Level-0 tracking specimen, not autonomous racing, an optimal racing line, or real-circuit validation.

## Method

A declared `CircuitCorridor` is sampled at at most `0.1 m` spacing. The vehicle position is orthogonally projected to each polyline interval, retaining signed cross-track error `e_y`, desired heading, curvature, widths, and centreline progress. For geometry-derived contact wheelbase `L`, steering is:

```text
delta_ff = atan(L kappa)
delta_raw = delta_ff - K_heading e_heading - K_cross e_y
delta = clamp(delta_raw, -0.03 rad, +0.03 rad).
```

Clamping is never silent: every saturated command is counted and its unclipped value remains in evidence. The applied command is passed into Work 073 before each physical step. Corridor departure occurs when signed centreline error exceeds the applicable side width minus the declared `0.65 m` half-envelope.

## Experiment and results

The reference uses a synthetic `50 m`-radius left circle, `0.25 m` initial lateral disturbance, `0.03 rad` initial heading disturbance, `K_heading = 0.8`, and `K_cross = 0.2 rad/m`.

- initial/final cross-track error: `0.24999987503241972 m` / `0.02307508195600006 m`;
- zero-feedback final error: `0.3772375000371769 m`;
- wrong-sign final error: `0.46591408662822736 m`;
- maximum absolute tracking error: `0.2620130810314983 m`;
- progress in `0.5 s`: `5.39206238640666 m`;
- minimum actual normal load: `290.149480377666 N`;
- maximum suspension travel: `0.011457919570257338 m`;
- maximum combined relative energy residual: `4.73869100213051e-9`;
- mirror residual: `1.1102230246251565e-16`;
- half-step difference: `0.0003151468688774861`.

The reference saturated for `348/500` steps. This is an observable control-authority limitation, not hidden success: feedback still reduced final error by about `94%` relative to zero feedback over the short horizon, but the high saturation count argues against treating the controller as tuned for a lap. The explicit saturation control saturated all `500` steps. The initial-departure control returned `DNF: corridor_departure` before executing a plant step. Straight and right-circle mirror controls passed.

The unchanged fixed-steer Work 073 result retained SHA-256 `802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973`. Work 074 result SHA-256 is `a400e8a9c1c0768d11647aa6c2fde3855a5d12898b548edef0b2fd6911244374`; canonical evidence SHA-256 is `9572a793e45713ee9768d3bca7ead9460ce3d1fe1824d6cee273b89e7737efea`; byte-identical primary/replay file SHA-256 is `B21A66201270C99CB0177CA6A4BF82755DDF734C6F1EACFF46ACB7A78C84FE5B`.

## Interpretation and limitations

Correct-sign feedback outperforming both zero feedback and wrong-sign feedback supports the causal controller hypothesis. Mirror, straight, replay, and half-step controls reduce sign and numerical explanations. The high saturation count is contradicting evidence against adequate authority/tuning for sustained racing.

The sampled-polyline projection is approximate and may select an ambiguous station at a closed-loop seam. There is no speed controller, braking, actuator model, latency, noise, estimator, look-ahead optimization, obstacle/traffic response, real corridor survey, or learning. Work 076 must not award a lap from scalar distance alone; it must check spatial containment and the seam explicitly.
