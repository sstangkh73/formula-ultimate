"""Geometry-general structural evaluation contracts for Work 138.

The bounded campaign evaluator reads five scale variables, so a shape outside
its template cannot be scored at all. This module scores any valid single
solid: it builds a C3D10 deck from a tetrahedral mesh of that solid, derives
mass properties from the mesh rather than from a declaration, and classifies
each outcome with a status that keeps a solver limitation distinct from a
physical verdict.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any, Iterable, Mapping, Sequence

from .acceptance import StructuralEvidenceError
from .element_verification import ElementMeshData

PROTOCOL_VERSION = "geometry_general_evaluator_v1"
FINAL_STATUS = "passed_geometry_general_structural_evaluation"

#: One status per candidate. ``unresolved_*`` is a statement about the tooling,
#: never a statement about the design.
STATUSES = (
    "passed",
    "failed_physics",
    "unresolved_mesh",
    "unresolved_solver",
    "unresolved_convergence",
    "unsupported_representation",
)
UNRESOLVED_STATUSES = ("unresolved_mesh", "unresolved_solver", "unresolved_convergence")

#: CalculiX reads free-field numbers into a 20-character buffer. A longer field
#: is either rejected (exit 201) or, worse, silently truncated: the probe in the
#: Work 138 plan read ``-1.00000000000000e+03`` as ``-1.0`` and returned exit 0
#: with a displacement 1000x too small.
CALCULIX_FIELD_LIMIT = 20

_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"


class GeometryEvaluationError(StructuralEvidenceError):
    """Raised when evaluation evidence or its declaration is invalid."""


def canonical_sha256(value: Any) -> str:
    try:
        payload = json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
    except (TypeError, ValueError) as exc:
        raise GeometryEvaluationError("evidence must be finite canonical JSON") from exc
    return hashlib.sha256(payload).hexdigest()


def calculix_number(value: float) -> str:
    """Format a number CalculiX reads back exactly as written."""

    if not isinstance(value, (int, float)) or isinstance(value, bool) or not math.isfinite(float(value)):
        raise GeometryEvaluationError("CalculiX fields must be finite numbers")
    for digits in range(12, 3, -1):
        text = f"{float(value):.{digits}g}"
        if len(text) <= CALCULIX_FIELD_LIMIT:
            return text
    raise GeometryEvaluationError(f"value cannot be written within {CALCULIX_FIELD_LIMIT} characters: {value}")


def _positive(value: Any, label: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)) or not math.isfinite(value) or value <= 0.0:
        raise GeometryEvaluationError(f"{label} must be a finite positive number")
    return float(value)


def _axis_index(axis: Any) -> int:
    if axis not in ("x", "y", "z"):
        raise GeometryEvaluationError("axis must be x, y, or z")
    return {"x": 0, "y": 1, "z": 2}[axis]


def validate_protocol(raw: Mapping[str, Any]) -> dict[str, Any]:
    """Fail closed on the frozen Work 138 declaration before anything runs."""

    required = {
        "protocol_version", "units", "runtimes", "materials", "mesh_levels",
        "convergence", "budget", "residuals", "candidates", "controls", "experiment",
    }
    if set(raw) != required or raw.get("protocol_version") != PROTOCOL_VERSION:
        raise GeometryEvaluationError("protocol schema or identity mismatch")
    if raw.get("units") != "SI_m_kg_s_N_Pa":
        raise GeometryEvaluationError("protocol units mismatch")
    for runtime in raw["runtimes"]:
        if set(runtime) != {"runtime_id", "path", "version"} or runtime["runtime_id"] not in {"gmsh", "ccx"}:
            raise GeometryEvaluationError("runtime identity is invalid")
    if {item["runtime_id"] for item in raw["runtimes"]} != {"gmsh", "ccx"}:
        raise GeometryEvaluationError("both gmsh and ccx runtimes are required")

    materials = raw["materials"]
    if not materials:
        raise GeometryEvaluationError("at least one material is required")
    for material_id, material in materials.items():
        if set(material) != {"youngs_modulus_pa", "poisson_ratio", "density_kg_m3", "allowable_von_mises_pa", "evidence_class"}:
            raise GeometryEvaluationError(f"material {material_id} schema is invalid")
        _positive(material["youngs_modulus_pa"], "youngs_modulus_pa")
        _positive(material["density_kg_m3"], "density_kg_m3")
        _positive(material["allowable_von_mises_pa"], "allowable_von_mises_pa")
        if not 0.0 < float(material["poisson_ratio"]) < 0.5:
            raise GeometryEvaluationError(f"material {material_id} poisson ratio is invalid")
        if material["evidence_class"] not in {"synthetic_geometry_only", "measured"}:
            raise GeometryEvaluationError(f"material {material_id} evidence class is invalid")

    levels = raw["mesh_levels"]
    if len(levels) < 3:
        raise GeometryEvaluationError("at least three mesh levels are required")
    sizes = [_positive(item["characteristic_size_scale"], "characteristic_size_scale") for item in levels]
    if sizes != sorted(sizes, reverse=True) or len(set(sizes)) != len(sizes):
        raise GeometryEvaluationError("mesh levels must be strictly coarse to fine")
    for item in levels:
        if set(item) != {"level_id", "characteristic_size_scale"}:
            raise GeometryEvaluationError("mesh level schema is invalid")

    convergence = raw["convergence"]
    if set(convergence) != {"displacement_relative", "stress_relative"}:
        raise GeometryEvaluationError("convergence schema is invalid")
    for key, value in convergence.items():
        if not 0.0 < float(value) < 1.0:
            raise GeometryEvaluationError(f"convergence {key} must lie in (0, 1)")

    budget = raw["budget"]
    if set(budget) != {"maximum_nodes", "maximum_solver_seconds", "mesh_retries"}:
        raise GeometryEvaluationError("budget schema is invalid")
    _positive(budget["maximum_nodes"], "maximum_nodes")
    _positive(budget["maximum_solver_seconds"], "maximum_solver_seconds")
    if not isinstance(budget["mesh_retries"], int) or isinstance(budget["mesh_retries"], bool) or budget["mesh_retries"] < 0:
        raise GeometryEvaluationError("mesh_retries must be a non-negative integer")

    residuals = raw["residuals"]
    if set(residuals) != {"reaction_relative", "declared_mass_relative"}:
        raise GeometryEvaluationError("residual schema is invalid")
    for key, value in residuals.items():
        if not 0.0 < float(value) < 1.0:
            raise GeometryEvaluationError(f"residual {key} must lie in (0, 1)")

    candidates = raw["candidates"]
    if not candidates:
        raise GeometryEvaluationError("at least one candidate is required")
    seen: set[str] = set()
    for candidate in candidates:
        if set(candidate) != {"candidate_id", "source", "geometry", "material_id", "length_unit_m", "boundary", "load_cases", "declared_mass_kg"}:
            raise GeometryEvaluationError("candidate schema is invalid")
        if candidate["candidate_id"] in seen:
            raise GeometryEvaluationError("candidate identities are duplicated")
        seen.add(candidate["candidate_id"])
        if candidate["material_id"] not in materials:
            raise GeometryEvaluationError("candidate material is not declared")
        _positive(candidate["length_unit_m"], "length_unit_m")
        geometry = candidate["geometry"]
        if geometry["kind"] == "step_file":
            if set(geometry) != {"kind", "path"}:
                raise GeometryEvaluationError("step_file geometry schema is invalid")
        elif geometry["kind"] == "benchmark_box":
            if set(geometry) != {"kind", "length_m", "width_m", "height_m", "analytical_tip_displacement_tolerance"}:
                raise GeometryEvaluationError("benchmark_box geometry schema is invalid")
            for key in ("length_m", "width_m", "height_m"):
                _positive(geometry[key], key)
            if not 0.0 < float(geometry["analytical_tip_displacement_tolerance"]) < 1.0:
                raise GeometryEvaluationError("benchmark tolerance must lie in (0, 1)")
        else:
            raise GeometryEvaluationError("geometry kind is not declared")
        _validate_selection(candidate["boundary"], "boundary")
        if not candidate["load_cases"]:
            raise GeometryEvaluationError("each candidate requires at least one load case")
        case_ids: set[str] = set()
        for case in candidate["load_cases"]:
            if set(case) != {"case_id", "selection", "force_n"}:
                raise GeometryEvaluationError("load case schema is invalid")
            if case["case_id"] in case_ids:
                raise GeometryEvaluationError("load case identities are duplicated")
            case_ids.add(case["case_id"])
            _validate_selection(case["selection"], "load selection")
            force = case["force_n"]
            if len(force) != 3 or not all(isinstance(v, (int, float)) and not isinstance(v, bool) and math.isfinite(v) for v in force):
                raise GeometryEvaluationError("load force must be a finite 3-vector")
            if math.fsum(abs(v) for v in force) <= 0.0:
                raise GeometryEvaluationError("load force must not be zero")
        declared = candidate["declared_mass_kg"]
        if declared is not None:
            _positive(declared, "declared_mass_kg")

    controls = raw["controls"]
    if len(controls) != 8 or len(set(controls)) != 8:
        raise GeometryEvaluationError("exactly eight registered controls are required")
    if any(not values for values in raw["experiment"].values()):
        raise GeometryEvaluationError("experiment registration is incomplete")
    return {
        "status": "passed",
        "protocol_sha256": canonical_sha256(raw),
        "candidate_count": len(candidates),
        "level_count": len(levels),
        "control_count": len(controls),
    }


def _validate_selection(selection: Mapping[str, Any], label: str) -> None:
    if set(selection) != {"axis", "side", "tolerance_m"}:
        raise GeometryEvaluationError(f"{label} schema is invalid")
    _axis_index(selection["axis"])
    if selection["side"] not in ("minimum", "maximum"):
        raise GeometryEvaluationError(f"{label} side must be minimum or maximum")
    _positive(selection["tolerance_m"], f"{label} tolerance_m")


def scaled_nodes(mesh: ElementMeshData, length_unit_m: float) -> dict[int, tuple[float, float, float]]:
    """Return mesh coordinates in metres; STEP files from CadQuery are in mm."""

    scale = _positive(length_unit_m, "length_unit_m")
    return {node: tuple(value * scale for value in xyz) for node, xyz in mesh.nodes.items()}


def select_nodes(nodes: Mapping[int, Sequence[float]], selection: Mapping[str, Any]) -> tuple[int, ...]:
    axis = _axis_index(selection["axis"])
    tolerance = float(selection["tolerance_m"])
    values = [xyz[axis] for xyz in nodes.values()]
    extreme = min(values) if selection["side"] == "minimum" else max(values)
    selected = tuple(sorted(node for node, xyz in nodes.items() if abs(xyz[axis] - extreme) <= tolerance))
    if not selected:
        raise GeometryEvaluationError("boundary selection is empty")
    return selected


def _triangle_area(a: Sequence[float], b: Sequence[float], c: Sequence[float]) -> float:
    ab = [second - first for first, second in zip(a, b)]
    ac = [second - first for first, second in zip(a, c)]
    cross = (
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    )
    return 0.5 * math.sqrt(math.fsum(value * value for value in cross))


def consistent_surface_loads(
    mesh: ElementMeshData,
    nodes: Mapping[int, Sequence[float]],
    loaded: Iterable[int],
    force_n: Sequence[float],
) -> dict[int, tuple[float, float, float]]:
    """Distribute a resultant over a TRI6 face with the exact consistent weights.

    For a constant traction on a six-node triangle the corner shape functions
    integrate to zero and each midside integrates to A/3, the same rule Work 041
    uses in ``element_verification``.
    """

    loaded_set = set(loaded)
    tributary = {node: 0.0 for node in loaded_set}
    area = 0.0
    for triangle in mesh.triangles.values():
        if not set(triangle) <= loaded_set:
            continue
        triangle_area = _triangle_area(*(nodes[node] for node in triangle[:3]))
        if not math.isfinite(triangle_area) or triangle_area <= 0.0:
            raise GeometryEvaluationError("loaded surface has an invalid triangle")
        area += triangle_area
        for node in (triangle[3:] if mesh.order == 2 else triangle):
            tributary[node] += triangle_area / 3.0
    if area <= 0.0 or not any(weight > 0.0 for weight in tributary.values()):
        raise GeometryEvaluationError("loaded surface has no complete face triangles")
    loads = {
        node: tuple(component * weight / area for component in force_n)
        for node, weight in sorted(tributary.items()) if weight > 0.0
    }
    for index, component in enumerate(force_n):
        total = math.fsum(load[index] for load in loads.values())
        if not math.isclose(total, component, rel_tol=1e-12, abs_tol=1e-12):
            raise GeometryEvaluationError("consistent surface loads do not close")
    return loads


def mesh_mass_properties(
    mesh: ElementMeshData, nodes: Mapping[int, Sequence[float]], density_kg_m3: float
) -> dict[str, Any]:
    """Volume, mass, centre and inertia from the mesh itself, not from a claim."""

    density = _positive(density_kg_m3, "density_kg_m3")
    volume = 0.0
    moment = [0.0, 0.0, 0.0]
    contributions: list[tuple[float, tuple[float, float, float]]] = []
    for connectivity in mesh.tetrahedra.values():
        corners = [nodes[node] for node in connectivity[:4]]
        a, b, c, d = corners
        matrix = [[b[i] - a[i] for i in range(3)], [c[i] - a[i] for i in range(3)], [d[i] - a[i] for i in range(3)]]
        determinant = (
            matrix[0][0] * (matrix[1][1] * matrix[2][2] - matrix[1][2] * matrix[2][1])
            - matrix[0][1] * (matrix[1][0] * matrix[2][2] - matrix[1][2] * matrix[2][0])
            + matrix[0][2] * (matrix[1][0] * matrix[2][1] - matrix[1][1] * matrix[2][0])
        )
        element_volume = abs(determinant) / 6.0
        if element_volume <= 0.0:
            raise GeometryEvaluationError("mesh contains a degenerate tetrahedron")
        centroid = tuple(math.fsum(corner[i] for corner in corners) / 4.0 for i in range(3))
        volume += element_volume
        contributions.append((element_volume, centroid))
        for i in range(3):
            moment[i] += element_volume * centroid[i]
    if volume <= 0.0:
        raise GeometryEvaluationError("mesh volume is not positive")
    center = tuple(value / volume for value in moment)
    inertia = [0.0, 0.0, 0.0]
    for element_volume, centroid in contributions:
        mass = element_volume * density
        dx, dy, dz = (centroid[i] - center[i] for i in range(3))
        inertia[0] += mass * (dy * dy + dz * dz)
        inertia[1] += mass * (dx * dx + dz * dz)
        inertia[2] += mass * (dx * dx + dy * dy)
    return {
        "volume_m3": volume,
        "mass_kg": volume * density,
        "center_m": list(center),
        "point_mass_inertia_kg_m2": inertia,
    }


def build_deck(
    *,
    mesh: ElementMeshData,
    nodes: Mapping[int, Sequence[float]],
    material_id: str,
    material: Mapping[str, Any],
    fixed: Sequence[int],
    loads: Mapping[int, Sequence[float]],
    heading: str,
) -> str:
    """Build a linear-static C3D10 deck whose every field survives the parser."""

    if set(fixed) & set(loads):
        raise GeometryEvaluationError("a node cannot be both fixed and loaded")
    if mesh.order != 2:
        raise GeometryEvaluationError("this evaluator registers second-order tetrahedra")
    lines = ["*HEADING", heading, "*NODE, NSET=NALL"]
    lines.extend(
        f"{node}, {calculix_number(nodes[node][0])}, {calculix_number(nodes[node][1])}, {calculix_number(nodes[node][2])}"
        for node in sorted(nodes)
    )
    lines.append(f"*ELEMENT, TYPE={mesh.calculix_element_type}, ELSET=EALL")
    lines.extend(
        f"{element}, " + ", ".join(str(node) for node in connectivity)
        for element, connectivity in sorted(mesh.tetrahedra.items())
    )
    lines.extend(_nset("FIXED", tuple(sorted(fixed))))
    lines.extend(_nset("LOADED", tuple(sorted(loads))))
    lines.extend((
        f"*MATERIAL, NAME={material_id}",
        "*ELASTIC",
        f"{calculix_number(material['youngs_modulus_pa'])}, {calculix_number(material['poisson_ratio'])}",
        "*DENSITY",
        calculix_number(material["density_kg_m3"]),
        f"*SOLID SECTION, ELSET=EALL, MATERIAL={material_id}",
        "*BOUNDARY",
        "FIXED, 1, 3, 0.0",
        "*STEP",
        "*STATIC",
        "*CLOAD",
    ))
    for node in sorted(loads):
        for direction, component in enumerate(loads[node], start=1):
            if component != 0.0:
                lines.append(f"{node}, {direction}, {calculix_number(component)}")
    lines.extend((
        "*NODE PRINT, NSET=NALL", "U",
        "*NODE PRINT, NSET=FIXED, TOTALS=YES", "RF",
        "*EL PRINT, ELSET=EALL", "S, E",
        "*END STEP", "",
    ))
    deck = "\n".join(lines)
    for index, line in enumerate(deck.splitlines()):
        if line.startswith("*") or index == 1:  # index 1 is the free-text heading
            continue
        for field in line.split(","):
            text = field.strip()
            if _is_number(text) and len(text) > CALCULIX_FIELD_LIMIT:
                raise GeometryEvaluationError("deck contains a field CalculiX would truncate")
    return deck


def _is_number(text: str) -> bool:
    try:
        float(text)
    except ValueError:
        return False
    return True


def _nset(name: str, nodes: Sequence[int]) -> list[str]:
    if not nodes:
        raise GeometryEvaluationError(f"node set {name} must not be empty")
    lines = [f"*NSET, NSET={name}"]
    lines.extend(
        ", ".join(str(node) for node in nodes[index:index + 16])
        for index in range(0, len(nodes), 16)
    )
    return lines


def von_mises(tensor: Sequence[float]) -> float:
    sxx, syy, szz, sxy, sxz, syz = tensor
    return math.sqrt(
        0.5 * ((sxx - syy) ** 2 + (syy - szz) ** 2 + (szz - sxx) ** 2)
        + 3.0 * (sxy * sxy + sxz * sxz + syz * syz)
    )


def parse_static_dat(text: str) -> dict[str, Any]:
    """Parse one static increment, keeping every integration point."""

    displacement_marker = "displacements (vx,vy,vz) for set NALL"
    reaction_marker = "forces (fx,fy,fz) for set FIXED"
    total_marker = "total force (fx,fy,fz) for set FIXED"
    stress_marker = "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL"
    strain_marker = "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL"
    for marker in (displacement_marker, reaction_marker, total_marker, stress_marker, strain_marker):
        if marker not in text:
            raise GeometryEvaluationError(f"CalculiX table is missing: {marker}")
    displacement_block = text.split(displacement_marker, 1)[1].split(reaction_marker, 1)[0]
    displacement_rows = re.findall(
        rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", displacement_block, re.MULTILINE
    )
    total_block = text.split(total_marker, 1)[1].split(stress_marker, 1)[0]
    total_rows = re.findall(rf"^\s*({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", total_block, re.MULTILINE)
    stress_block = text.split(stress_marker, 1)[1].split(strain_marker, 1)[0]
    stress_rows = re.findall(
        rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        stress_block, re.MULTILINE,
    )
    if not displacement_rows or len(total_rows) != 1 or not stress_rows:
        raise GeometryEvaluationError("CalculiX static evidence is missing or ambiguous")
    displacements = {int(row[0]): tuple(float(value) for value in row[1:4]) for row in displacement_rows}
    if len(displacements) != len(displacement_rows):
        raise GeometryEvaluationError("CalculiX displacement node IDs are duplicated")
    stresses = [tuple(float(value) for value in row[2:8]) for row in stress_rows]
    total_reaction = tuple(float(value) for value in total_rows[0])
    values = [value for vector in (*displacements.values(), total_reaction, *stresses) for value in vector]
    if not all(math.isfinite(value) for value in values):
        raise GeometryEvaluationError("CalculiX evidence contains a non-finite value")
    magnitudes = [math.sqrt(math.fsum(component * component for component in vector)) for vector in displacements.values()]
    stress_values = [von_mises(tensor) for tensor in stresses]
    stress_values.sort()
    index = min(len(stress_values) - 1, int(math.floor(0.9 * (len(stress_values) - 1))))
    return {
        "maximum_displacement_m": max(magnitudes),
        "maximum_von_mises_pa": max(stress_values),
        "p90_von_mises_pa": stress_values[index],
        "total_reaction_n": list(total_reaction),
        "node_count": len(displacements),
        "integration_point_count": len(stress_values),
    }


def relative_change(previous: float, current: float) -> float:
    denominator = max(abs(previous), abs(current))
    return 0.0 if denominator == 0.0 else abs(current - previous) / denominator


def classify_candidate(
    *,
    levels: Sequence[Mapping[str, Any]],
    convergence: Mapping[str, float],
    residuals: Mapping[str, float],
    allowable_von_mises_pa: float,
    applied_force_n: Sequence[float],
    declared_mass_kg: float | None,
) -> dict[str, Any]:
    """Return exactly one registered status, with the evidence behind it."""

    if not levels:
        raise GeometryEvaluationError("classification requires at least one level record")
    for level in levels:
        if level["status"] == "unresolved_mesh":
            return {"status": "unresolved_mesh", "cause": level.get("cause", "mesh generation failed"), "levels": list(levels)}
        if level["status"] == "unresolved_solver":
            return {"status": "unresolved_solver", "cause": level.get("cause", "solver did not complete"), "levels": list(levels)}
        if level["status"] == "unsupported_representation":
            return {"status": "unsupported_representation", "cause": level.get("cause", "input is not one valid solid"), "levels": list(levels)}
    solved = [level for level in levels if level["status"] == "solved"]
    if len(solved) < 3:
        return {"status": "unresolved_convergence", "cause": "fewer than three solved refinement levels", "levels": list(levels)}
    last, previous = solved[-1], solved[-2]
    displacement_change = relative_change(previous["maximum_displacement_m"], last["maximum_displacement_m"])
    stress_change = relative_change(previous["p90_von_mises_pa"], last["p90_von_mises_pa"])
    converged = (
        displacement_change <= float(convergence["displacement_relative"])
        and stress_change <= float(convergence["stress_relative"])
    )
    applied = math.sqrt(math.fsum(component * component for component in applied_force_n))
    reaction = math.sqrt(math.fsum(component * component for component in last["total_reaction_n"]))
    reaction_residual = relative_change(applied, reaction)
    mass_residual = None
    if declared_mass_kg is not None:
        mass_residual = relative_change(float(declared_mass_kg), float(last["mass_kg"]))
    evidence = {
        "displacement_relative_change": displacement_change,
        "stress_relative_change": stress_change,
        "reaction_residual_relative": reaction_residual,
        "declared_mass_residual_relative": mass_residual,
        "utilization": last["maximum_von_mises_pa"] / _positive(allowable_von_mises_pa, "allowable_von_mises_pa"),
        "levels": list(levels),
    }
    if not converged:
        return {"status": "unresolved_convergence", "cause": "last two levels exceed the registered change limits", **evidence}
    if reaction_residual > float(residuals["reaction_relative"]):
        return {"status": "unresolved_solver", "cause": "reaction does not balance the applied resultant", **evidence}
    if mass_residual is not None and mass_residual > float(residuals["declared_mass_relative"]):
        return {"status": "failed_physics", "cause": "mesh mass contradicts the declared mass", **evidence}
    if evidence["utilization"] > 1.0:
        return {"status": "failed_physics", "cause": "peak von Mises exceeds the declared allowable", **evidence}
    return {"status": "passed", "cause": None, **evidence}


def euler_bernoulli_tip_displacement(
    *, force_n: float, length_m: float, width_m: float, height_m: float, youngs_modulus_pa: float
) -> float:
    """Closed-form cantilever tip deflection for the registered benchmark."""

    second_moment = width_m * height_m ** 3 / 12.0
    return abs(force_n) * length_m ** 3 / (3.0 * _positive(youngs_modulus_pa, "youngs_modulus_pa") * second_moment)


def summarize(candidates: Sequence[Mapping[str, Any]], controls: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    """Aggregate the run; an unresolved candidate is counted, never dropped."""

    counts: dict[str, int] = {status: 0 for status in STATUSES}
    for candidate in candidates:
        status = candidate["status"]
        if status not in counts:
            raise GeometryEvaluationError(f"candidate carries an unregistered status: {status}")
        counts[status] += 1
    if sum(counts.values()) != len(candidates):
        raise GeometryEvaluationError("candidate status accounting does not close")
    rejected = [control for control in controls if control["rejected"]]
    unresolved = {status: counts[status] for status in UNRESOLVED_STATUSES if counts[status]}
    return {
        "status": FINAL_STATUS if len(rejected) == len(controls) else "failed_controls",
        "status_counts": counts,
        "unresolved_causes": sorted(
            (candidate["candidate_id"], candidate["status"], candidate.get("cause"))
            for candidate in candidates if candidate["status"] in UNRESOLVED_STATUSES
        ),
        "unresolved_count": sum(unresolved.values()),
        "controls_rejected": len(rejected),
        "control_count": len(controls),
        "promotion_allowed": False,
        "race_time_claim": False,
        "physical_validation": False,
    }
