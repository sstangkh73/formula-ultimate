"""Validate Work 011 tyre-road analytical references."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.tyre import (  # noqa: E402
    TyreContactParameters,
    TyreForceRequest,
    resolve_tyre_force,
)


def result_dict(result):
    return {
        "status": result.status,
        "requested_force_n": [
            result.requested_longitudinal_force_n,
            result.requested_lateral_force_n,
        ],
        "applied_force_n": [
            result.applied_longitudinal_force_n,
            result.applied_lateral_force_n,
        ],
        "residual_force_n": [
            result.residual_longitudinal_force_n,
            result.residual_lateral_force_n,
        ],
        "requested_utilization": result.requested_utilization,
        "applied_utilization": result.applied_utilization,
        "saturation_scale": result.saturation_scale,
        "saturated": result.saturated,
    }


def main() -> int:
    circle = TyreContactParameters(1.0, 1.0)
    outside = resolve_tyre_force(
        parameters=circle,
        normal_load_n=4_000.0,
        request=TyreForceRequest(3_000.0, 4_000.0),
    )
    if outside.status != "saturated":
        raise RuntimeError("outside-circle reference was not saturated")
    expected = (2_400.0, 3_200.0, 1.0)
    actual = (
        outside.applied_longitudinal_force_n,
        outside.applied_lateral_force_n,
        outside.applied_utilization,
    )
    if any(abs(a - b) > 1.0e-12 for a, b in zip(actual, expected)):
        raise RuntimeError(f"circle analytical mismatch: {actual!r}")

    zero_load = resolve_tyre_force(
        parameters=circle,
        normal_load_n=0.0,
        request=TyreForceRequest(100.0, -50.0),
    )
    if zero_load.status != "no_normal_load" or not zero_load.saturated:
        raise RuntimeError("zero-load request did not remain an observable failure")

    inside = resolve_tyre_force(
        parameters=TyreContactParameters(1.5, 1.0),
        normal_load_n=4_000.0,
        request=TyreForceRequest(3_000.0, 2_000.0),
    )
    if inside.status != "within_limit" or inside.saturated:
        raise RuntimeError("inside-ellipse reference changed unexpectedly")

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "outside_circle": result_dict(outside),
                "inside_ellipse": result_dict(inside),
                "zero_normal_load": result_dict(zero_load),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
