"""Validate Work 017 aerodynamic-map and cooling-flow reference behavior."""

from __future__ import annotations

from dataclasses import asdict
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.aerodynamics import (  # noqa: E402
    AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,
    AerodynamicEvidence,
    AerodynamicOperatingPoint,
    AerodynamicReference,
    AerodynamicStateGrid,
    evaluate_aerodynamics,
)


SPEEDS = (0.0, 20.0, 40.0)
HEIGHTS = (0.04, 0.08)
YAWS = (-0.1, 0.0, 0.1)


def sample(state: str, height: float, yaw: float) -> AerodynamicCoefficientSample:
    opened = state == "cooling_open"
    return AerodynamicCoefficientSample(
        (0.72 if opened else 0.60) + 0.4 * abs(yaw) + 0.5 * (0.08 - height),
        0.7 * yaw,
        (1.10 if opened else 1.20) + 1.5 * (0.08 - height) - 0.2 * abs(yaw),
        0.05 + 0.5 * (height - 0.06),
        0.2 * yaw,
        (0.80 if opened else 0.40) - 0.3 * abs(yaw) + 0.2 * (height - 0.04),
    )


def grid(state: str) -> AerodynamicStateGrid:
    return AerodynamicStateGrid(
        state,
        tuple(
            sample(state, height, yaw)
            for _speed in SPEEDS
            for height in HEIGHTS
            for yaw in YAWS
        ),
    )


def map_() -> AerodynamicCoefficientMap:
    return AerodynamicCoefficientMap(
        "work017-reference",
        SPEEDS,
        HEIGHTS,
        YAWS,
        (grid("nominal"), grid("cooling_open")),
        AerodynamicEvidence(
            "work017-synthetic",
            "synthetic_reference",
            "analytical validator fixture; not geometry-derived",
        ),
    )


REFERENCE = AerodynamicReference(1.5, 3.0, 0.08, 1_005.0, 0.7)


def point(speed: float, state: str = "nominal") -> AerodynamicOperatingPoint:
    return AerodynamicOperatingPoint(speed, 1.2, 0.06, 0.05, state, 300.0, 360.0)


def main() -> int:
    coefficient_map = map_()
    low = evaluate_aerodynamics(
        coefficient_map=coefficient_map,
        reference=REFERENCE,
        operating_point=point(20.0),
    )
    high = evaluate_aerodynamics(
        coefficient_map=coefficient_map,
        reference=REFERENCE,
        operating_point=point(40.0),
    )
    opened = evaluate_aerodynamics(
        coefficient_map=coefficient_map,
        reference=REFERENCE,
        operating_point=point(20.0, "cooling_open"),
    )
    replay = evaluate_aerodynamics(
        coefficient_map=coefficient_map,
        reference=REFERENCE,
        operating_point=point(20.0),
    )
    outside = evaluate_aerodynamics(
        coefficient_map=coefficient_map,
        reference=REFERENCE,
        operating_point=AerodynamicOperatingPoint(
            41.0, 1.2, 0.06, 0.05, "nominal", 300.0, 360.0
        ),
    )

    if low.status != "ok" or high.status != "ok" or opened.status != "ok":
        raise RuntimeError("reference aerodynamic point failed")
    force_ratio = high.drag_force_n / low.drag_force_n  # type: ignore[operator]
    flow_ratio = (
        high.cooling_air_mass_flow_kg_per_s
        / low.cooling_air_mass_flow_kg_per_s  # type: ignore[operator]
    )
    if abs(force_ratio - 4.0) > 1.0e-12:
        raise RuntimeError("drag did not follow speed-squared scaling")
    if abs(flow_ratio - 2.0) > 1.0e-12:
        raise RuntimeError("cooling mass flow did not follow linear speed scaling")
    if opened.drag_force_n <= low.drag_force_n:  # type: ignore[operator]
        raise RuntimeError("open cooling state did not expose drag increase")
    if opened.cooling_air_mass_flow_kg_per_s <= low.cooling_air_mass_flow_kg_per_s:  # type: ignore[operator]
        raise RuntimeError("open cooling state did not expose flow increase")
    if low != replay:
        raise RuntimeError("identical evaluation did not replay exactly")
    if outside.status != "invalid":
        raise RuntimeError("out-of-envelope point was silently accepted")

    print(
        json.dumps(
            {
                "evidence": asdict(coefficient_map.evidence),
                "interior_point": {
                    "status": low.status,
                    "interpolation": asdict(low.interpolation),
                    "coefficients": asdict(low.coefficients),
                    "dynamic_pressure_pa": low.dynamic_pressure_pa,
                    "drag_force_n": low.drag_force_n,
                    "downforce_n": low.downforce_n,
                    "pitching_moment_n_m": low.pitching_moment_n_m,
                    "longitudinal_centre_of_pressure_m": low.longitudinal_centre_of_pressure_m,
                    "cooling_air_mass_flow_kg_per_s": low.cooling_air_mass_flow_kg_per_s,
                    "cooling_effective_conductance_w_per_k": low.cooling_effective_conductance_w_per_k,
                    "cooling_heat_rejection_w": low.cooling_heat_rejection_w,
                    "residuals": asdict(low.residuals),
                },
                "scaling": {
                    "drag_40_to_20_ratio": force_ratio,
                    "mass_flow_40_to_20_ratio": flow_ratio,
                },
                "active_state_tradeoff": {
                    "nominal_drag_force_n": low.drag_force_n,
                    "open_drag_force_n": opened.drag_force_n,
                    "nominal_mass_flow_kg_per_s": low.cooling_air_mass_flow_kg_per_s,
                    "open_mass_flow_kg_per_s": opened.cooling_air_mass_flow_kg_per_s,
                },
                "replay_equal": low == replay,
                "outside_envelope": {
                    "status": outside.status,
                    "reason": outside.reason,
                },
                "claim_boundary": "synthetic Level-0 map; not geometry-derived or physically validated",
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
