#!/usr/bin/env python3
"""Audit Work 100 survivors for causal function and Work 101 integration intake."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.discovery_registration import strict_json  # noqa: E402
from formula_ultimate.experiments.integration_intake import (  # noqa: E402
    IntegrationIntakeViolation,
    audit_work100_result,
)


def _write(path: Path, value: object) -> None:
    if path.exists():
        raise IntegrationIntakeViolation("output already exists")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/work101_integration_intake_v1.json")
    parser.add_argument("--work100-result", type=Path, default=ROOT / "artifacts/work100/run_v2_a/result.json")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    try:
        config = strict_json(args.config.read_text(encoding="utf-8"))
        source = strict_json(args.work100_result.read_text(encoding="utf-8"))
        result = audit_work100_result(config, source)
        if args.replay_reference is not None:
            reference = strict_json(args.replay_reference.read_text(encoding="utf-8"))
            if result != reference:
                raise IntegrationIntakeViolation("exact replay differs")
        _write(args.output, result)
        print(json.dumps({"status": result["integration_intake"]["status"], "candidate_count": result["summary"]["candidate_count"], "mechanism_candidate_count": result["summary"]["functional_mechanism_candidate_count"], "result_sha256": result["result_sha256"], "work101_program_exit": result["integration_intake"]["work101_program_exit"]}, sort_keys=True))
        return 0
    except (IntegrationIntakeViolation, OSError, ValueError, KeyError) as error:
        print(f"Work 105 failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
