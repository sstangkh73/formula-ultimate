"""Import Work 084 exact STEP artifacts, retain separate solids, and save FCStd."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import sys

import FreeCAD as App
import Part


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.subsystems.energy_torque_path import canonical_sha256  # noqa: E402


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _bounds(shape) -> dict:
    bounds = shape.optimalBoundingBox(True, False)
    return {
        "minimum": [bounds.XMin * 1.0e-3, bounds.YMin * 1.0e-3, bounds.ZMin * 1.0e-3],
        "maximum": [bounds.XMax * 1.0e-3, bounds.YMax * 1.0e-3, bounds.ZMax * 1.0e-3],
    }


def _read_exact(path: Path, expected_sha256: str):
    if not path.is_file() or _sha256(path) != expected_sha256:
        raise RuntimeError(f"STEP identity mismatch: {path.name}")
    shape = Part.Shape()
    shape.read(os.fspath(path))
    return shape


def main() -> int:
    manifest_path = Path(os.environ["FORMULA_ULTIMATE_W084_MANIFEST"])
    step_root = Path(os.environ["FORMULA_ULTIMATE_W084_STEP_ROOT"])
    output_report = Path(os.environ["FORMULA_ULTIMATE_W084_FREECAD_REPORT"])
    output_fcstd = Path(os.environ["FORMULA_ULTIMATE_W084_FCSTD"])
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

    document = App.newDocument("EnergyTorquePathCandidate001")
    records = []
    for part in manifest["parts"]:
        path = step_root / part["step_file"]
        shape = _read_exact(path, part["step_sha256"])
        solids = shape.Solids
        if len(solids) != 1 or not shape.isValid():
            raise RuntimeError(f"{part['part_id']} is not one valid imported solid")
        obj = document.addObject("Part::Feature", part["part_id"])
        obj.Label = part["part_id"]
        obj.Shape = solids[0]
        records.append(
            {
                "part_id": part["part_id"],
                "step_file": part["step_file"],
                "step_sha256": part["step_sha256"],
                "valid": bool(shape.isValid()),
                "solid_count": len(solids),
                "volume_m3": float(shape.Volume) * 1.0e-9,
                "surface_area_m2": float(shape.Area) * 1.0e-6,
                "bounding_box_m": _bounds(shape),
            }
        )

    assembly_info = manifest["assembly"]
    assembly_path = step_root / assembly_info["step_file"]
    assembly_shape = _read_exact(assembly_path, assembly_info["step_sha256"])
    if len(assembly_shape.Solids) != len(records) or not assembly_shape.isValid():
        raise RuntimeError("assembly did not preserve seven valid separate solids")

    document.recompute()
    output_fcstd.parent.mkdir(parents=True, exist_ok=True)
    document.saveAs(os.fspath(output_fcstd))
    if not output_fcstd.is_file() or output_fcstd.stat().st_size <= 0:
        raise RuntimeError("FCStd witness was not saved")

    version = App.Version()
    body = {
        "source_manifest_sha256": manifest["manifest_sha256"],
        "freecad_version": ".".join(str(item) for item in version[:3]),
        "occt_version": str(getattr(Part, "OCC_VERSION", "unavailable")),
        "hidden_geometry_repair": False,
        "parts": records,
        "assembly": {
            "step_file": assembly_info["step_file"],
            "step_sha256": assembly_info["step_sha256"],
            "valid": bool(assembly_shape.isValid()),
            "solid_count": len(assembly_shape.Solids),
            "volume_m3": float(assembly_shape.Volume) * 1.0e-9,
            "bounding_box_m": _bounds(assembly_shape),
        },
    }
    report = {**body, "report_sha256": canonical_sha256(body)}
    output_report.parent.mkdir(parents=True, exist_ok=True)
    output_report.write_text(
        json.dumps(report, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    App.Console.PrintMessage(
        json.dumps(
            {
                "status": "passed",
                "part_count": len(records),
                "assembly_solid_count": len(assembly_shape.Solids),
                "report_sha256": report["report_sha256"],
            },
            sort_keys=True,
        )
        + "\n"
    )
    App.closeDocument(document.Name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
