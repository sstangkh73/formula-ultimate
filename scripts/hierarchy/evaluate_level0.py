#!/usr/bin/env python3
"""Race a generated vehicle package on the existing Level-0 kernel.

    python evaluate_level0.py --manifest DIR/manifest.json --out RESULT.json

Uses the manifest root mass, a drag area bounded by the leaf-mesh frontal box
and the versioned config ``config/hierarchy/level0_race_v1.json``. The output
is deterministic. Outcome evidence only, not physical validation.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.hierarchy.level0 import (  # noqa: E402
    evaluate_manifest,
    load_config,
    result_bytes,
)

DEFAULT_CONFIG = ROOT / "config" / "hierarchy" / "level0_race_v1.json"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    args = parser.parse_args(argv)
    result = evaluate_manifest(args.manifest, load_config(args.config), ROOT)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_bytes(result_bytes(result))
    print(f"{result['outcome']} race_time_s={result['race_time_s']:.3f} mass_kg={result['mass_kg']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
