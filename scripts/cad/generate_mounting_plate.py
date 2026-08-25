"""Generate one constrained Work 006 mounting plate with CadQuery."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.components.grammar import (  # noqa: E402
    GrammarViolation,
    MountingPlateSpec,
)


def _candidate_payload(config: dict[str, Any], candidate_id: str) -> dict[str, Any]:
    candidates = [*config["valid_candidates"], config["invalid_candidate"]]
    candidate = next(
        (item for item in candidates if item["candidate_id"] == candidate_id),
        None,
    )
    if candidate is None:
        raise GrammarViolation(f"candidate_id is not declared: {candidate_id!r}")
    spec = {
        **config["common_spec"],
        "lightening_radius_m": candidate["lightening_radius_m"],
        "material": config["material"],
        "grammar_version": config["grammar_version"],
    }
    return {
        "candidate_id": candidate_id,
        "seed": config["seed"],
        "spec": spec,
    }


def _build(spec: MountingPlateSpec) -> cq.Workplane:
    mm = 1000.0
    result = (
        cq.Workplane("XY")
        .box(
            spec.length_m * mm,
            spec.width_m * mm,
            spec.thickness_m * mm,
            centered=(True, True, False),
        )
        .edges("|Z")
        .fillet(spec.corner_radius_m * mm)
        .faces(">Z")
        .workplane()
        .pushPoints(
            [(x_m * mm, y_m * mm) for x_m, y_m in spec.mounting_hole_centres_m]
        )
        .hole(spec.mounting_hole_diameter_m * mm)
    )
    if spec.lightening_radius_m > 0.0:
        result = (
            result.faces(">Z")
            .workplane()
            .hole(2.0 * spec.lightening_radius_m * mm)
        )
    return result


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def _write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--candidate-id", required=True)
    parser.add_argument("--output-step", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--failure-json", type=Path, required=True)
    args = parser.parse_args()

    try:
        config = json.loads(args.config.read_text(encoding="utf-8"))
        payload = _candidate_payload(config, args.candidate_id)
        spec = MountingPlateSpec.from_mapping(payload["spec"])
    except (GrammarViolation, KeyError, TypeError, ValueError) as exc:
        failure = {
            "candidate_id": args.candidate_id,
            "error_type": type(exc).__name__,
            "message": str(exc),
            "stage": "grammar_validation_before_cad",
            "cadquery_executed": False,
        }
        _write_json(args.failure_json, failure)
        print(json.dumps(failure, sort_keys=True), file=sys.stderr)
        return 2

    result = _build(spec)
    shape = result.val()
    if not shape.isValid():
        raise RuntimeError("CadQuery produced an invalid shape")
    solid_count = len(shape.Solids())
    if solid_count != 1:
        raise RuntimeError(f"CadQuery produced {solid_count} solids instead of one")

    args.output_step.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(result, str(args.output_step), exportType="STEP")
    bounds = shape.BoundingBox()
    centre = shape.Center()
    manifest = {
        **payload,
        "generator": {
            "cadquery_version": cq.__version__,
            "script": str(Path(__file__).relative_to(ROOT)),
            "script_sha256": _sha256(Path(__file__)),
            "grammar_source_sha256": _sha256(
                ROOT / "src/formula_ultimate/components/grammar.py"
            ),
        },
        "cadquery_measurement": {
            "source": "CadQuery generated B-rep",
            "volume_m3": shape.Volume() * 1.0e-9,
            "volume_mm3": shape.Volume(),
            "solid_count": solid_count,
            "is_valid": shape.isValid(),
            "bounds_m": [
                bounds.xlen * 1.0e-3,
                bounds.ylen * 1.0e-3,
                bounds.zlen * 1.0e-3,
            ],
            "centre_of_mass_m": [
                centre.x * 1.0e-3,
                centre.y * 1.0e-3,
                centre.z * 1.0e-3,
            ],
        },
        "analytical_volume_m3": spec.analytical_volume_m3,
        "analytical_mass_kg": spec.analytical_mass_kg,
        "step": {
            "path": str(args.output_step),
            "bytes": args.output_step.stat().st_size,
            "sha256": _sha256(args.output_step),
            "header": args.output_step.read_text(
                encoding="ascii", errors="replace"
            ).splitlines()[0],
        },
    }
    _write_json(args.manifest, manifest)
    print(
        json.dumps(
            {
                "candidate_id": args.candidate_id,
                "solid_count": solid_count,
                "volume_mm3": shape.Volume(),
                "step_sha256": manifest["step"]["sha256"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
