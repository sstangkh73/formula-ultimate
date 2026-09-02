"""Execute the Work 078 feature corpus and export canonical STEP evidence."""

from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.components.brep_grammar import (  # noqa: E402
    brep_declaration_sha256,
    validate_brep_grammar,
)


MM = 1000.0


class BrepExecutionError(RuntimeError):
    """Raised when a declared feature fails in the CAD kernel."""


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(
        r"(FILE_NAME\('[^']*',)'[^']*'",
        r"\1'1970-01-01T00:00:00'",
        text,
        count=1,
    )
    if count != 1:
        raise BrepExecutionError("STEP FILE_NAME timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def _shape_state(shape: cq.Shape, feature_id: str) -> cq.Shape:
    solids = shape.Solids()
    volume = shape.Volume()
    if not shape.isValid():
        raise BrepExecutionError(f"feature {feature_id} produced an invalid shape")
    if not solids or not math.isfinite(volume) or volume <= 0.0:
        raise BrepExecutionError(f"feature {feature_id} produced an empty shape")
    # OCCT operations such as shell may wrap one valid solid in a Compound.
    # Unwrap only this representation-preserving case; never fuse or repair
    # multiple solids implicitly.
    return solids[0] if len(solids) == 1 else shape


def _profile_workplane(profile: dict[str, Any]) -> cq.Workplane:
    parameters = profile["parameters"]
    kind = parameters["profile_type"]
    cx = parameters["center_x_m"] * MM
    cy = parameters["center_y_m"] * MM
    a = parameters["size_a_m"] * MM
    b = parameters["size_b_m"] * MM
    workplane = cq.Workplane("XY").center(cx, cy)
    if kind == "rectangle":
        return workplane.rect(a, b)
    if kind == "circle":
        return workplane.circle(a)
    if kind == "annulus":
        return workplane.circle(a).circle(b)
    raise BrepExecutionError(f"profile {kind} cannot be extruded")


def _execute_feature(
    feature: dict[str, Any], states: dict[str, Any]
) -> Any:
    feature_id = feature["feature_id"]
    operator = feature["operator"]
    parameters = feature["parameters"]
    inputs = [states[item] for item in feature["inputs"]]
    try:
        if operator == "sketch_profile":
            return {"kind": "profile", "parameters": dict(parameters)}
        if operator == "extrude":
            result = _profile_workplane(inputs[0]).extrude(parameters["distance_m"] * MM).val()
        elif operator == "revolve":
            profile = inputs[0]["parameters"]
            if profile["profile_type"] != "shaft_section":
                raise BrepExecutionError("revolve V1 requires shaft_section")
            radius = profile["size_a_m"] * MM
            length = profile["size_b_m"] * MM
            angle = math.degrees(parameters["angle_rad"])
            result = (
                cq.Workplane("XZ")
                .moveTo(0.0, 0.0)
                .lineTo(radius, 0.0)
                .lineTo(radius, length)
                .lineTo(0.0, length)
                .close()
                .revolve(angle, (0.0, 0.0), (0.0, 1.0))
                .val()
            )
        elif operator == "pocket_cut":
            source = inputs[0]
            bounds = source.BoundingBox()
            width = parameters["width_m"] * MM
            height = parameters["height_m"] * MM
            depth = parameters["depth_m"] * MM
            if width >= bounds.xlen or height >= bounds.ylen or depth >= bounds.zlen:
                raise BrepExecutionError("pocket_cut would erase or split the bounded blank")
            cutter = (
                cq.Workplane("XY")
                .box(width, height, depth, centered=(True, True, True))
                .translate(
                    (
                        parameters["center_x_m"] * MM,
                        parameters["center_y_m"] * MM,
                        bounds.zmax - depth / 2.0,
                    )
                )
                .val()
            )
            result = source.cut(cutter)
        elif operator == "through_hole":
            source = inputs[0]
            bounds = source.BoundingBox()
            cutter = cq.Solid.makeCylinder(
                parameters["diameter_m"] * MM / 2.0,
                bounds.zlen + 2.0,
                cq.Vector(
                    parameters["center_x_m"] * MM,
                    parameters["center_y_m"] * MM,
                    bounds.zmin - 1.0,
                ),
                cq.Vector(0.0, 0.0, 1.0),
            )
            result = source.cut(cutter)
        elif operator == "stepped_bore":
            source = inputs[0]
            bounds = source.BoundingBox()
            cx = parameters["center_x_m"] * MM
            cy = parameters["center_y_m"] * MM
            through = cq.Solid.makeCylinder(
                parameters["through_diameter_m"] * MM / 2.0,
                bounds.zlen + 2.0,
                cq.Vector(cx, cy, bounds.zmin - 1.0),
                cq.Vector(0.0, 0.0, 1.0),
            )
            depth = parameters["counterbore_depth_m"] * MM
            if depth >= bounds.zlen:
                raise BrepExecutionError("counterbore depth must be below part height")
            counter = cq.Solid.makeCylinder(
                parameters["counterbore_diameter_m"] * MM / 2.0,
                depth + 1.0,
                cq.Vector(cx, cy, bounds.zmax - depth),
                cq.Vector(0.0, 0.0, 1.0),
            )
            result = source.cut(through.fuse(counter))
        elif operator == "shaft_shoulder":
            source = inputs[0]
            shoulder = cq.Solid.makeCylinder(
                parameters["diameter_m"] * MM / 2.0,
                parameters["length_m"] * MM,
                cq.Vector(0.0, 0.0, parameters["offset_z_m"] * MM),
                cq.Vector(0.0, 0.0, 1.0),
            )
            result = source.fuse(shoulder)
        elif operator == "rib_web":
            result = (
                cq.Workplane("XY")
                .box(
                    parameters["length_m"] * MM,
                    parameters["width_m"] * MM,
                    parameters["height_m"] * MM,
                    centered=(True, True, False),
                )
                .translate(
                    (
                        parameters["center_x_m"] * MM,
                        parameters["center_y_m"] * MM,
                        parameters["base_z_m"] * MM,
                    )
                )
                .val()
            )
        elif operator == "shell_wall":
            source = inputs[0]
            result = (
                cq.Workplane(obj=source)
                .faces(">Z")
                .shell(-parameters["wall_thickness_m"] * MM)
                .val()
            )
        elif operator == "linear_pattern":
            seed = inputs[0]
            axes = {
                "x": (1.0, 0.0, 0.0),
                "y": (0.0, 1.0, 0.0),
                "z": (0.0, 0.0, 1.0),
            }
            axis = axes[parameters["direction"]]
            spacing = parameters["spacing_m"] * MM
            result = seed
            for index in range(1, parameters["count"]):
                offset = tuple(index * spacing * item for item in axis)
                result = result.fuse(seed.translate(offset))
        elif operator == "circular_pattern":
            seed = inputs[0]
            result = seed
            step_degrees = math.degrees(parameters["angle_rad"]) / parameters["count"]
            for index in range(1, parameters["count"]):
                result = result.fuse(
                    seed.rotate((0.0, 0.0, 0.0), (0.0, 0.0, 1.0), index * step_degrees)
                )
        elif operator == "fillet_chamfer":
            source = inputs[0]
            selector = "|Z" if parameters["selector"] == "vertical" else "%CIRCLE"
            selected = cq.Workplane(obj=source).edges(selector)
            if parameters["mode"] == "fillet":
                result = selected.fillet(parameters["size_m"] * MM).val()
            else:
                result = selected.chamfer(parameters["size_m"] * MM).val()
        elif operator == "boolean_union":
            result = inputs[0].fuse(inputs[1])
        elif operator == "boolean_subtract":
            result = inputs[0].cut(inputs[1])
        elif operator == "boolean_intersect":
            result = inputs[0].intersect(inputs[1])
        else:  # pragma: no cover - parser blocks this route
            raise BrepExecutionError(f"unsupported operator {operator}")
    except BrepExecutionError:
        raise
    except Exception as exc:
        raise BrepExecutionError(f"feature {feature_id} ({operator}) failed: {exc}") from exc
    return _shape_state(result, feature_id)


def _execute_candidate(candidate: dict[str, Any]) -> tuple[cq.Shape, list[dict[str, Any]]]:
    states: dict[str, Any] = {}
    trace: list[dict[str, Any]] = []
    for feature in candidate["features"]:
        state = _execute_feature(feature, states)
        states[feature["feature_id"]] = state
        trace.append(
            {
                "feature_id": feature["feature_id"],
                "operator": feature["operator"],
                "status": "passed",
                "solid_count": None if isinstance(state, dict) else len(state.Solids()),
            }
        )
    final = states[candidate["final_feature_id"]]
    if isinstance(final, dict):
        raise BrepExecutionError("final feature is a profile, not a solid")
    if len(final.Solids()) != 1:
        raise BrepExecutionError(
            f"candidate {candidate['candidate_id']} final state must contain exactly one solid"
        )
    return final, trace


def _canonical_hash(value: Any) -> str:
    encoded = json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    grammar_validation = validate_brep_grammar(raw)
    args.output_root.mkdir(parents=True, exist_ok=True)
    records: list[dict[str, Any]] = []
    for candidate in raw["candidates"]:
        shape, trace = _execute_candidate(candidate)
        step_path = args.output_root / f"{candidate['candidate_id']}.step"
        cq.exporters.export(shape, str(step_path), exportType="STEP")
        _canonicalize_step(step_path)
        bounds = shape.BoundingBox()
        records.append(
            {
                "candidate_id": candidate["candidate_id"],
                "family": candidate["family"],
                "final_feature_id": candidate["final_feature_id"],
                "feature_trace": trace,
                "valid": shape.isValid(),
                "solid_count": len(shape.Solids()),
                "volume_m3": shape.Volume() * 1.0e-9,
                "bounding_box_m": {
                    "minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM],
                    "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM],
                },
                "step_file": step_path.name,
                "step_bytes": step_path.stat().st_size,
                "step_sha256": _sha256(step_path),
            }
        )
    draft = {
        "status": "passed",
        "grammar_version": raw["grammar_version"],
        "grammar_declaration_sha256": brep_declaration_sha256(raw),
        "cadquery_version": cq.__version__,
        "hidden_geometry_repair": False,
        "grammar_validation": grammar_validation,
        "candidates": records,
    }
    manifest = {**draft, "manifest_sha256": _canonical_hash(draft)}
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(
        json.dumps(manifest, sort_keys=True, indent=2, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    print(
        json.dumps(
            {
                "status": "passed",
                "candidate_count": len(records),
                "manifest_sha256": manifest["manifest_sha256"],
                "step_sha256": {
                    record["candidate_id"]: record["step_sha256"] for record in records
                },
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
