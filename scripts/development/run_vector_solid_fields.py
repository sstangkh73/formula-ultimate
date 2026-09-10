"""Execute Work 111 vector solid mechanics evidence package."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
from typing import Any

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.search.freeform_material_generator import generate_source, grid_spec  # noqa: E402
from formula_ultimate.structural.geometry_mesh_bridge import build_mesh  # noqa: E402
from formula_ultimate.structural.vector_solid_fields import (  # noqa: E402
    VectorSolidViolation,
    canonical_sha256,
    element_kinematics,
    patch_strain,
    solve,
    validate_protocol,
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def require_dependency(raw: dict[str, Any]) -> None:
    dependency = raw["dependency"]
    contract = ROOT / dependency["contract_path"]
    if file_sha256(contract) != dependency["contract_sha256"]:
        raise VectorSolidViolation("stale Work 110 contract")
    check = subprocess.run(
        ["git", "cat-file", "-e", dependency["work110_commit"] + "^{commit}"],
        cwd=ROOT,
        capture_output=True,
    )
    if check.returncode:
        raise VectorSolidViolation("missing Work 110 dependency commit")


def rectangular_mesh(length: float, width: float, height: float, resolution: float) -> dict[str, Any]:
    dimensions = tuple(int(round(value / resolution)) for value in (length, width, height))
    if any(abs(dimensions[i] * resolution - value) > 1e-12 for i, value in enumerate((length, width, height))):
        raise VectorSolidViolation("reference dimensions must be integral multiples of resolution")
    field = {(i, j, k): "synthetic_isotropic_elastic" for i in range(dimensions[0]) for j in range(dimensions[1]) for k in range(dimensions[2])}
    mesh = build_mesh(
        field,
        {"minimum": (0.0, 0.0, 0.0), "maximum": (length, width, height), "resolution": resolution, "dimensions": dimensions},
        maximum_elements=500_000,
    )
    return relabel_x_faces(mesh, 0.0, length)


def relabel_x_faces(mesh: dict[str, Any], minimum_x: float, maximum_x: float) -> dict[str, Any]:
    tolerance = max(1e-12, abs(maximum_x - minimum_x) * 1e-10)
    nodes = np.asarray(mesh["nodes"], dtype=float)
    for triangle in mesh["triangles"]:
        xs = nodes[np.asarray(triangle["nodes"], dtype=int) - 1, 0]
        if np.all(np.abs(xs - minimum_x) <= tolerance):
            triangle["set"] = "load_surface"
        elif np.all(np.abs(xs - maximum_x) <= tolerance):
            triangle["set"] = "contact_surface"
        else:
            triangle["set"] = "external_surface"
    return mesh


def stripped_result(result: dict[str, Any], field_file: str) -> dict[str, Any]:
    compact = {key: value for key, value in result.items() if key not in {"displacements_m", "element_stresses"}}
    compact["field_file"] = field_file
    return compact


def run_and_store(mesh: dict[str, Any], material: dict[str, Any], load_spec: dict[str, Any], path: Path) -> dict[str, Any]:
    result = solve(mesh, material, load_spec)
    write_json(path, {
        "displacements_m": result["displacements_m"],
        "element_stresses": result["element_stresses"],
        "displacement_sha256": result["displacement_sha256"],
        "stress_sha256": result["stress_sha256"],
        "reaction_field_sha256": result["reaction_field_sha256"],
    })
    return stripped_result(result, path.name)


def assert_gates(result: dict[str, Any], tolerances: dict[str, float]) -> None:
    for key in ("force_residual_relative", "moment_residual_relative", "energy_residual_relative"):
        if result[key] > tolerances[key]:
            raise VectorSolidViolation(f"{key} exceeded registered tolerance")
    if result["minimum_diagonal_condition_proxy"] < tolerances["minimum_diagonal_condition_proxy"]:
        raise VectorSolidViolation("diagonal conditioning proxy fell below registered minimum")


def relative_change(a: float, b: float) -> float:
    return abs(a - b) / max(abs(a), abs(b), 1e-30)


def rejected(action, phrase: str) -> dict[str, str]:
    try:
        action()
    except VectorSolidViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise VectorSolidViolation("negative control was accepted")


def rigid_translation_error(mesh: dict[str, Any]) -> float:
    nodes = np.asarray(mesh["nodes"], dtype=float)
    translation = np.tile(np.array([0.3, -0.4, 0.7]), 4)
    return max(float(np.max(np.abs(element_kinematics(nodes[np.asarray(tet["nodes"], dtype=int) - 1])[1] @ translation))) for tet in mesh["tetrahedra"])


def disconnected_mesh() -> dict[str, Any]:
    spec = {"minimum": (0.0, 0.0, 0.0), "maximum": (0.04, 0.01, 0.01), "resolution": 0.01, "dimensions": (4, 1, 1)}
    mesh = build_mesh({(0, 0, 0): "a", (3, 0, 0): "a"}, spec, maximum_elements=500)
    return relabel_x_faces(mesh, 0.0, 0.04)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    config_path = (ROOT / args.config).resolve() if not args.config.is_absolute() else args.config
    output_root = (ROOT / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    output_root.mkdir(parents=True, exist_ok=True)

    raw = load_json(config_path)
    validation = validate_protocol(raw)
    require_dependency(raw)
    material = raw["material"]
    tolerances = raw["tolerances"]

    reference = raw["reference"]
    reference_load = {**raw["load"], "resultant_force_n": [-reference["force_n"], 0.0, 0.0], "body_acceleration_m_s2": [0.0, 0.0, 0.0]}
    reference_levels = []
    reference_mesh = None
    for resolution in (0.04, 0.02, 0.01):
        mesh = rectangular_mesh(reference["length_m"], reference["width_m"], reference["height_m"], resolution)
        record = run_and_store(mesh, material, reference_load, output_root / f"reference_{resolution:.3f}_fields.json")
        assert_gates(record, tolerances)
        analytic_compliance = reference["length_m"] / (material["youngs_modulus_pa"] * reference["width_m"] * reference["height_m"])
        analytic_displacement = reference["force_n"] * analytic_compliance
        error = abs(record["load_average_displacement_m"][0] + analytic_displacement) / analytic_displacement
        record.update({"resolution_m": resolution, "analytic_compliance_m_per_n": analytic_compliance, "analytic_loaded_face_displacement_m": -analytic_displacement, "analytic_displacement_relative_error": error})
        reference_levels.append(record)
        reference_mesh = mesh
    if reference_levels[-1]["analytic_displacement_relative_error"] > reference["analytic_displacement_relative_tolerance"]:
        raise VectorSolidViolation("analytic reference displacement tolerance exceeded")

    assert reference_mesh is not None
    affine_gradient = np.array([[1.1e-5, 2.0e-6, -1.0e-6], [3.0e-6, -4.0e-6, 5.0e-7], [2.0e-6, -7.0e-7, 6.0e-6]])
    patch_error = patch_strain(reference_mesh, affine_gradient)
    if patch_error > reference["patch_strain_absolute_tolerance"]:
        raise VectorSolidViolation("affine patch strain tolerance exceeded")
    rotation_error = patch_strain(reference_mesh, np.array([[0.0, -2e-5, 3e-5], [2e-5, 0.0, -4e-5], [-3e-5, 4e-5, 0.0]]))
    translation_error = rigid_translation_error(reference_mesh)
    if max(rotation_error, translation_error) > reference["patch_strain_absolute_tolerance"]:
        raise VectorSolidViolation("rigid-body strain control failed")

    source_path = ROOT / raw["unfamiliar"]["source_config"]
    source_raw = load_json(source_path)
    unfamiliar_levels = []
    finest_field = None
    finest_spec = None
    finest_mesh = None
    for resolution in raw["unfamiliar"]["resolutions_m"]:
        field, source_cost = generate_source(source_raw, resolution)
        spec = grid_spec(source_raw["representation"], resolution)
        mesh = build_mesh(field, spec, maximum_elements=500_000)
        record = run_and_store(mesh, material, raw["load"], output_root / f"unfamiliar_{resolution:.3f}_fields.json")
        assert_gates(record, tolerances)
        record.update({"resolution_m": resolution, "occupied_cell_count": len(field), "source_grid_visits": source_cost["grid_visits"]})
        unfamiliar_levels.append(record)
        finest_field, finest_spec, finest_mesh = field, spec, mesh

    convergence = {}
    for quantity in ("maximum_displacement_m", "compliance_m_per_n", "p90_von_mises_stress_pa"):
        value = relative_change(unfamiliar_levels[-2][quantity], unfamiliar_levels[-1][quantity])
        convergence[quantity + "_last_two_relative_change"] = value
        if value > raw["unfamiliar"]["last_two_relative_change_limit"]:
            raise VectorSolidViolation(f"{quantity} did not meet the registered last-two refinement gate")

    assert finest_field is not None and finest_spec is not None and finest_mesh is not None
    stiff_material = {**material, "youngs_modulus_pa": 2 * material["youngs_modulus_pa"]}
    stiff = solve(finest_mesh, stiff_material, raw["load"])
    stiffness_ratio = stiff["compliance_m_per_n"] / unfamiliar_levels[-1]["compliance_m_per_n"]
    if abs(stiffness_ratio - 0.5) > 1e-10:
        raise VectorSolidViolation("Youngs-modulus causal control failed")
    rotated_load = {**raw["load"], "resultant_force_n": [-raw["load"]["resultant_force_n"][1], raw["load"]["resultant_force_n"][0], raw["load"]["resultant_force_n"][2]]}
    rotated = solve(finest_mesh, material, rotated_load)
    if rotated["displacement_sha256"] == unfamiliar_levels[-1]["displacement_sha256"]:
        raise VectorSolidViolation("load-direction causal control did not change the vector field")
    mutated_field = dict(finest_field)
    mutated_field.pop(max(mutated_field))
    mutated_mesh = build_mesh(mutated_field, finest_spec, maximum_elements=500_000)
    mutated = solve(mutated_mesh, material, raw["load"])
    if mutated["displacement_sha256"] == unfamiliar_levels[-1]["displacement_sha256"]:
        raise VectorSolidViolation("geometry causal control did not change the vector field")

    no_support = copy.deepcopy(reference_mesh)
    for triangle in no_support["triangles"]:
        if triangle["set"] == "contact_surface":
            triangle["set"] = "external_surface"
    corrupt_material = {**material, "youngs_modulus_pa": 0.0}
    support_ids = sorted({node - 1 for triangle in finest_mesh["triangles"] if triangle["set"] == raw["load"]["support_surface"] for node in triangle["nodes"]})
    assigned_reaction_field = np.zeros((len(finest_mesh["nodes"]), 3))
    assigned_reaction_field[support_ids] = -np.asarray(unfamiliar_levels[-1]["applied_force_n"]) / len(support_ids)
    assigned_hash = canonical_sha256(assigned_reaction_field.tolist())
    if assigned_hash == unfamiliar_levels[-1]["reaction_field_sha256"]:
        raise VectorSolidViolation("reaction field matches prohibited assigned-input control")
    controls = {
        "rigid_translation": {"status": "passed", "maximum_strain_error": translation_error},
        "rigid_rotation": {"status": "passed", "maximum_strain_error": rotation_error},
        "affine_patch": {"status": "passed", "maximum_strain_error": patch_error},
        "unsupported_rigid_modes": rejected(lambda: solve(no_support, material, reference_load), "unsupported rigid modes"),
        "severed_load_path": rejected(lambda: solve(disconnected_mesh(), material, reference_load), "severed load path"),
        "corrupt_stiffness": rejected(lambda: solve(reference_mesh, corrupt_material, reference_load), "corrupted stiffness"),
        "recovered_not_assigned": {"status": "passed", "recovered_reaction_field_sha256": unfamiliar_levels[-1]["reaction_field_sha256"], "prohibited_uniform_assignment_sha256": assigned_hash},
        "stiffness_scaling": {"status": "passed", "double_modulus_compliance_ratio": stiffness_ratio},
        "load_direction_mutation": {"status": "passed", "baseline_displacement_sha256": unfamiliar_levels[-1]["displacement_sha256"], "mutated_displacement_sha256": rotated["displacement_sha256"]},
        "geometry_mutation": {"status": "passed", "baseline_displacement_sha256": unfamiliar_levels[-1]["displacement_sha256"], "mutated_displacement_sha256": mutated["displacement_sha256"]},
    }

    body = {
        "status": "passed",
        "claim_scope": "Level-0 small-strain isotropic linear-elastic tetrahedral field evidence with synthetic material fixtures; not physical validation",
        "validation": validation,
        "dependency": raw["dependency"],
        "reference_levels": reference_levels,
        "unfamiliar_levels": unfamiliar_levels,
        "convergence": convergence,
        "controls": controls,
        "review": {
            "supporting_evidence": ["analytic axial reference and affine patch gates passed", "force, moment, and energy residuals passed at every admitted level", "geometry, load-direction, and stiffness mutations produced registered causal responses"],
            "contradicting_evidence": ["p90 stress and displacement remain discretization-dependent on the unfamiliar voxel boundary"],
            "alternative_explanations": ["regular six-tetra voxel cells may make conditioning and patch behavior easier than arbitrary unstructured tetrahedra"],
            "missing_evidence": ["independent production solver cross-check", "curved-element convergence", "nonlinear material/contact", "measured loads and physical validation"],
            "confidence": "high for deterministic assembled-field and balance evidence inside the admitted Level-0 scope; low for real-vehicle prediction",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    write_json(output_root / "result.json", result)
    if args.replay_reference:
        reference_path = (ROOT / args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference
        prior = load_json(reference_path)
        exact = prior.get("result_sha256") == result["result_sha256"]
        write_json(output_root / "replay.json", {"reference_result_sha256": prior.get("result_sha256"), "current_result_sha256": result["result_sha256"], "exact": exact})
        if not exact:
            raise VectorSolidViolation("replay differs from reference")
    print(json.dumps({"status": "passed", "result_sha256": result["result_sha256"], "reference_levels": len(reference_levels), "unfamiliar_levels": len(unfamiliar_levels)}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
