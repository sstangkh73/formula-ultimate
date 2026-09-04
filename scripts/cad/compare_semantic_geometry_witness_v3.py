#!/usr/bin/env python3
"""Compare a Work 096 FreeCAD report with the frozen semantic contract."""
from __future__ import annotations

import argparse
import json
from pathlib import Path

from formula_ultimate.components.semantic_geometry_witness import compare_report


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--report", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args(); config = json.loads(args.config.read_text(encoding="utf-8")); report = json.loads(args.report.read_text(encoding="utf-8"))
    result = compare_report(config, report); args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")
    if args.replay_reference and json.loads(args.replay_reference.read_text(encoding="utf-8")) != result: raise RuntimeError("semantic witness comparison replay mismatch")
    print(json.dumps({"status": result["status"], "candidate_count": result["candidate_count"], "comparison_sha256": result["comparison_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
