"""Validate Work 010 analytical corridors and real-circuit coverage."""

from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.physics.corridor import (  # noqa: E402
    VehicleEnvelope,
    assess_vehicle_corridor,
    closure_residual,
    load_corridors,
)


def main() -> int:
    corridors = load_corridors(
        ROOT / "config" / "circuits" / "corridor_schema_v1.json"
    )
    vehicle = VehicleEnvelope(
        width_m=2.0,
        wheelbase_m=3.0,
        front_overhang_m=1.0,
        rear_overhang_m=1.0,
        max_steering_angle_rad=0.7,
    )
    results = {
        corridor.corridor_id: assess_vehicle_corridor(corridor, vehicle)
        for corridor in corridors
    }
    expected = {
        "synthetic_full_circle_pass": "verification_passed",
        "synthetic_overhang_reject": "rejected",
        "synthetic_steering_reject": "rejected",
    }
    actual = {key: value.status for key, value in results.items()}
    if actual != expected:
        raise RuntimeError(f"fixture status mismatch: {actual!r}")

    real_circuits = load_circuit_catalog(
        ROOT / "config" / "circuits" / "real_circuits_v1.json"
    )
    coverage = {
        profile.circuit_id: assess_vehicle_corridor(
            None, vehicle, circuit_id=profile.circuit_id
        ).status
        for profile in real_circuits
    }
    if len(coverage) != 10 or set(coverage.values()) != {"indeterminate"}:
        raise RuntimeError(f"unexpected real-circuit coverage: {coverage!r}")

    closure = closure_residual(corridors[0])
    output = {
        "schema_version": "1.0",
        "fixture_statuses": actual,
        "full_circle_closure_residual": {
            "horizontal_m": closure.horizontal_m,
            "vertical_m": closure.vertical_m,
            "heading_rad": closure.heading_rad,
        },
        "real_circuit_coverage": coverage,
        "real_circuit_summary": {
            "total": len(coverage),
            "admitted": sum(value == "admitted" for value in coverage.values()),
            "indeterminate": sum(
                value == "indeterminate" for value in coverage.values()
            ),
        },
    }
    print(json.dumps(output, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
