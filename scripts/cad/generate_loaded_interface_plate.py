"""Generate the exact Work 045 plate and STEP evidence with CadQuery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.structural import loaded_interface_spec_from_mapping  # noqa: E402


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def canonicalize_step_header(path: Path) -> None:
    """Remove the OCCT wall-clock field while preserving all STEP geometry."""
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(
        r"(FILE_NAME\('[^']*',)'[^']*'",
        r"\1'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    if count != 1:
        raise RuntimeError("STEP FILE_NAME timestamp was missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-step", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()
    payload = json.loads(args.config.read_text(encoding="utf-8"))
    spec = loaded_interface_spec_from_mapping(payload)
    mm = 1000.0
    result = cq.Workplane("XY").box(spec.length_m * mm, spec.width_m * mm, spec.thickness_m * mm, centered=(False, True, False))
    result = result.faces(">Z").workplane().pushPoints([(item.center_x_m * mm, item.center_y_m * mm) for item in spec.interfaces]).hole(2.0 * spec.interfaces[0].radius_m * mm)
    shape = result.val()
    if not shape.isValid() or len(shape.Solids()) != 1:
        raise RuntimeError("loaded-interface CAD is not one valid solid")
    args.output_step.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(result, str(args.output_step), exportType="STEP")
    canonicalize_step_header(args.output_step)
    manifest = {
        "protocol_id": spec.protocol_id, "generator": "CadQuery",
        "cadquery_version": cq.__version__, "solid_count": len(shape.Solids()), "is_valid": shape.isValid(),
        "volume_m3": shape.Volume() * 1e-9,
        "interfaces": [{"interface_id": item.interface_id, "role": item.role, "surface": "cylinder_z", "center_m": [item.center_x_m, item.center_y_m, spec.thickness_m / 2], "radius_m": item.radius_m, "expected_area_m2": 2 * 3.141592653589793 * item.radius_m * spec.thickness_m} for item in spec.interfaces],
        "step": {"path": str(args.output_step), "sha256": sha(args.output_step), "bytes": args.output_step.stat().st_size},
    }
    args.manifest.write_text(json.dumps(manifest, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(json.dumps({"status": "passed", "step_sha256": manifest["step"]["sha256"], "volume_m3": manifest["volume_m3"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
