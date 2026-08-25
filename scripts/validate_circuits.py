"""Validate and summarize the real-circuit Level-0 catalogue."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from formula_ultimate.physics.circuit import load_circuit_catalog


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_CATALOG = ROOT / "config" / "circuits" / "real_circuits_v1.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--catalog", type=Path, default=DEFAULT_CATALOG)
    parser.add_argument("--vehicle-width-m", type=float, default=2.0)
    parser.add_argument("--clearance-per-side-m", type=float, default=0.5)
    args = parser.parse_args()

    profiles = load_circuit_catalog(args.catalog)
    if len(profiles) != 10:
        raise SystemExit(f"expected exactly 10 circuits, found {len(profiles)}")

    assessments = [
        profile.assess_static_width(
            vehicle_width_m=args.vehicle_width_m,
            clearance_per_side_m=args.clearance_per_side_m,
        )
        for profile in profiles
    ]
    summary = {
        "catalog": str(args.catalog),
        "circuit_count": len(profiles),
        "vehicle_width_m": args.vehicle_width_m,
        "clearance_per_side_m": args.clearance_per_side_m,
        "width_evidence_count": sum(
            profile.published_width is not None for profile in profiles
        ),
        "status_counts": {
            status: sum(item.status == status for item in assessments)
            for status in ("screen_passed", "rejected", "indeterminate")
        },
        "circuits": [
            {
                "circuit_id": profile.circuit_id,
                "status": assessment.status,
                "minimum_width_m": assessment.available_published_width_m,
                "isa_air_density_kg_per_m3": profile.isa_air_density_kg_per_m3,
                "race_start_offset_m": profile.race_start_offset_m,
            }
            for profile, assessment in zip(profiles, assessments, strict=True)
        ],
    }
    print(json.dumps(summary, ensure_ascii=False, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
