"""Generate the Work 141 survey declaration from the Work 135 vehicle.

Every part class is assigned by a rule over the occurrence classes the vehicle
itself declares, so the mapping is auditable and reproducible rather than
hand-picked part by part.
"""

from __future__ import annotations

import argparse
import collections
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]

#: Requirements are engineering minimums, not a fit to the current vehicle. A
#: plain box has 6 faces and 12 edges, so the structural minimum sits above it.
PART_CLASSES = {
    "fastener_or_seal": {"minimum_faces": 12, "minimum_curved_faces": 4, "minimum_distinct_feature_scales": 3, "minimum_edges": 20},
    "rotating_or_bearing": {"minimum_faces": 8, "minimum_curved_faces": 3, "minimum_distinct_feature_scales": 2, "minimum_edges": 14},
    "electronics_module": {"minimum_faces": 8, "minimum_curved_faces": 1, "minimum_distinct_feature_scales": 2, "minimum_edges": 14},
    "fluid_or_conductor_route": {"minimum_faces": 4, "minimum_curved_faces": 2, "minimum_distinct_feature_scales": 2, "minimum_edges": 6},
    "structure_or_housing": {"minimum_faces": 8, "minimum_curved_faces": 0, "minimum_distinct_feature_scales": 2, "minimum_edges": 14},
}

#: First matching rule wins, so a fastener is never reclassified as structure.
CLASS_RULES = (
    ("fastener_or_seal", {"fastener", "nut", "washer", "gasket", "seal"}),
    ("rotating_or_bearing", {"bearing", "shaft", "axle", "transmission_element", "coupling", "ground_body", "fan", "pump", "actuator", "converter"}),
    ("electronics_module", {"controller_module", "sensor", "connector", "switching"}),
    ("fluid_or_conductor_route", {"coolant_tube", "conductor", "power_harness", "signal_harness", "fluid_void"}),
)
DEFAULT_CLASS = "structure_or_housing"


def classify(occurrence_classes: set[str]) -> str:
    for class_id, members in CLASS_RULES:
        if occurrence_classes & members:
            return class_id
    return DEFAULT_CLASS


def build(vehicle: dict[str, Any], mesh_size_factor: float) -> dict[str, Any]:
    roles: dict[str, set[str]] = collections.defaultdict(set)
    for instance in vehicle["instances"]:
        roles[instance["definition_id"]].update(instance["occurrence_classes"])

    parts = []
    excluded = []
    for definition in vehicle["definitions"]:
        definition_id = definition["definition_id"]
        if definition["material_id"] == "void":
            excluded.append(definition_id)
            continue
        parts.append({
            "part_id": definition_id,
            "part_class": classify(roles[definition_id]),
            "source": f"work135_native_detailed_vehicle:{definition_id}",
            "geometry": {"kind": "step_file", "path": f"artifacts/work135/run_a/cad/parts/{definition_id}.step"},
        })
    parts.sort(key=lambda item: item["part_id"])

    identity = {"translation_m": [0.0, 0.0, 0.0], "rotation_deg_xyz": [0.0, 0.0, 0.0]}
    return {
        "protocol_version": "part_resolution_gate_v1",
        "units": "SI_m",
        "runtimes": [
            {"runtime_id": "cadquery_python", "path": ".tools/cadquery-mcp/Scripts/python.exe", "version": "3.12.14"},
            {"runtime_id": "gmsh", "path": "C:/Program Files/FreeCAD 1.1/bin/gmsh.exe", "version": "4.15.0"},
        ],
        "resolution": {
            "minimum_feature_m": 5e-05,
            "minimum_elements_across_feature": 1,
            "mesh_size_factor": mesh_size_factor,
        },
        "part_classes": PART_CLASSES,
        "parts": parts,
        "joints": [{
            "joint_id": "work135_pack_threaded",
            "technology": "threaded",
            "parts": ["bolt", "nut"],
            "placement": {"bolt": identity, "nut": identity},
            "fit_range_m": [0.0, 0.0005],
            "minimum_overlap_area_m2": 1e-06,
        }],
        "controls": [
            "sliver_below_manufacturing_floor",
            "primitive_below_resolution_requirement",
            "mesh_too_coarse_for_feature",
            "joint_without_measurable_interface",
            "fit_outside_declared_range",
            "technology_outside_registry",
            "no_discovery_claim",
            "exact_replay",
        ],
        "experiment": {
            "independent_variables": ["part class as assigned by the vehicle's own occurrence classes"],
            "dependent_variables": ["face, edge and curved-face counts", "smallest feature", "modelled feature scale", "registered part status"],
            "controls": ["sliver floor", "resolution requirement", "mesh adequacy", "empty interface", "out-of-range fit", "unregistered technology", "claim boundary", "replay"],
            "success_criteria": ["every material definition carries one registered status", "all controls rejected", "exact replay"],
            "failure_criteria": ["a definition dropped from the survey", "a requirement relaxed after seeing a result"],
            "excluded_void_definitions": excluded,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--vehicle", type=Path, default=ROOT / "config/development/native_detailed_vehicle_v1.json")
    parser.add_argument("--output", type=Path, default=ROOT / "config/development/vehicle_part_resolution_v1.json")
    parser.add_argument("--mesh-size-factor", type=float, default=0.15)
    args = parser.parse_args()

    vehicle = json.loads(args.vehicle.read_text(encoding="utf-8"))
    declaration = build(vehicle, args.mesh_size_factor)
    args.output.write_text(json.dumps(declaration, indent=2) + "\n", encoding="utf-8", newline="\n")
    counts = collections.Counter(part["part_class"] for part in declaration["parts"])
    print(json.dumps({
        "status": "generated",
        "part_count": len(declaration["parts"]),
        "excluded_void_definitions": declaration["experiment"]["excluded_void_definitions"],
        "class_counts": dict(sorted(counts.items())),
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
