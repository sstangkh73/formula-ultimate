"""Validate and replay the Work 079 material/manufacturing binding."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.engineering_contracts import (  # noqa: E402
    validate_engineering_assignment,
)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    raw = json.loads(args.config.read_text(encoding="utf-8"))
    expected = {
        "protocol_version",
        "material",
        "manufacturing_process",
        "geometry_witness",
        "assignment",
    }
    if set(raw) != expected:
        raise ValueError(
            f"root keys mismatch; missing={sorted(expected - set(raw))}, "
            f"unknown={sorted(set(raw) - expected)}"
        )
    if raw["protocol_version"] != "engineering_material_manufacturing_binding_v1":
        raise ValueError("protocol_version mismatch")
    result = validate_engineering_assignment(
        raw["assignment"],
        raw["material"],
        raw["manufacturing_process"],
        raw["geometry_witness"],
    )
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(result, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": result["status"],
                "part_id": result["part_id"],
                "material_record_sha256": result["material"]["record_sha256"],
                "process_record_sha256": result["manufacturing_process"]["record_sha256"],
                "manufacturing_report_sha256": result["manufacturing_witness"]["report_sha256"],
                "result_sha256": result["result_sha256"],
                "design_use_allowed": result["design_use_allowed"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
