"""Validate and fingerprint one Work 077 geometry-causal part declaration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.part_contract import PartContract  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    contract = PartContract.from_mapping(raw)
    result = {
        "status": "passed",
        "contract_version": raw["contract_version"],
        "part_id": contract.part_id,
        "canonical_byte_count": len(contract.canonical_json),
        "declaration_sha256": contract.declaration_sha256,
    }
    encoded = json.dumps(result, sort_keys=True, indent=2) + "\n"
    if args.output is not None:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(encoded, encoding="utf-8")
    print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
