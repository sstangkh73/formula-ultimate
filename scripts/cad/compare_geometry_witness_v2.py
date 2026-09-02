"""Compare a Work 081 FreeCAD report against the frozen witness config."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from formula_ultimate.components.geometry_witness import compare_geometry_witness


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--report", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    config = json.loads(args.config.read_text(encoding="utf-8"))
    report = json.loads(args.report.read_text(encoding="utf-8"))
    result = compare_geometry_witness(config, report)
    rendered = json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n"
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(rendered, encoding="utf-8")
    print(json.dumps({"status": result["status"], "part_count": result["part_count"], "comparison_sha256": result["comparison_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
