"""Run the Work 080 reference assembly and emit canonical JSON evidence."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from formula_ultimate.assembly.joint_kernel import evaluate_assembly


ROOT = Path(__file__).resolve().parents[2]
DEFAULT_CONFIG = ROOT / "config/assembly/mechanical_assembly_joint_kernel_v1.json"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    declaration = json.loads(args.config.read_text(encoding="utf-8"))
    result = evaluate_assembly(declaration)
    rendered = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    print(rendered, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
