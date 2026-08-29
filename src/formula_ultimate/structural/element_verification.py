"""Element-aware mesh, deck, and result contracts for Work 041."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any

from .acceptance import StructuralEvidenceError, TensionSpec


@dataclass(frozen=True, slots=True)
class ElementMeshData:
    nodes: dict[int, tuple[float, float, float]]
    tetrahedra: dict[int, tuple[int, ...]]
    triangles: dict[int, tuple[int, ...]]
    order: int

    def __post_init__(self) -> None:
        expected_tet = 4 if self.order == 1 else 10 if self.order == 2 else 0
        expected_tri = 3 if self.order == 1 else 6 if self.order == 2 else 0
        if not expected_tet or not self.nodes or not self.tetrahedra or not self.triangles:
            raise StructuralEvidenceError("element mesh identity/order is invalid")
        if any(len(item) != expected_tet for item in self.tetrahedra.values()):
            raise StructuralEvidenceError("tetrahedral connectivity does not match order")
        if any(len(item) != expected_tri for item in self.triangles.values()):
            raise StructuralEvidenceError("triangle connectivity does not match order")
        used = {node for item in self.tetrahedra.values() for node in item}
        triangle_used = {node for item in self.triangles.values() for node in item}
        if not used <= set(self.nodes) or not triangle_used <= set(self.nodes):
            raise StructuralEvidenceError("element references an unknown node")
        if any(not all(math.isfinite(value) for value in xyz) for xyz in self.nodes.values()):
            raise StructuralEvidenceError("mesh contains a non-finite coordinate")

    @property
    def calculix_element_type(self) -> str:
        return "C3D4" if self.order == 1 else "C3D10"


def parse_element_msh2(path: Path, *, expected_order: int) -> ElementMeshData:
    """Parse the exact ASCII MSH 2.2 linear/quadratic tetrahedral subset."""

    lines = path.read_text(encoding="ascii", errors="strict").splitlines()
    tetra_type, triangle_type = (4, 2) if expected_order == 1 else (11, 9)
    tet_nodes, tri_nodes = (4, 3) if expected_order == 1 else (10, 6)
    try:
        mesh_index = lines.index("$MeshFormat")
        if lines[mesh_index + 1].split()[:2] != ["2.2", "0"]:
            raise StructuralEvidenceError("mesh is not ASCII MSH 2.2")
        node_index = lines.index("$Nodes")
        node_count = int(lines[node_index + 1])
        nodes = {
            int(fields[0]): tuple(float(value) for value in fields[1:4])
            for fields in (
                line.split() for line in lines[node_index + 2 : node_index + 2 + node_count]
            )
        }
        element_index = lines.index("$Elements")
        element_count = int(lines[element_index + 1])
        tetrahedra: dict[int, tuple[int, ...]] = {}
        triangles: dict[int, tuple[int, ...]] = {}
        seen: set[int] = set()
        for line in lines[element_index + 2 : element_index + 2 + element_count]:
            fields = line.split()
            element_id, element_type, tag_count = int(fields[0]), int(fields[1]), int(fields[2])
            if element_id in seen:
                raise StructuralEvidenceError("mesh element IDs are duplicated")
            seen.add(element_id)
            connectivity = tuple(int(value) for value in fields[3 + tag_count :])
            if element_type == tetra_type:
                if len(connectivity) != tet_nodes:
                    raise StructuralEvidenceError("tetrahedron connectivity is malformed")
                if expected_order == 2:
                    # Gmsh and Abaqus/CalculiX exchange the final two edge nodes.
                    connectivity = connectivity[:8] + (connectivity[9], connectivity[8])
                tetrahedra[element_id] = connectivity
            elif element_type == triangle_type:
                if len(connectivity) != tri_nodes:
                    raise StructuralEvidenceError("triangle connectivity is malformed")
                triangles[element_id] = connectivity
    except (ValueError, IndexError) as exc:
        if isinstance(exc, StructuralEvidenceError):
            raise
        raise StructuralEvidenceError(f"malformed element MSH 2.2 evidence: {exc}") from exc
    if len(nodes) != node_count:
        raise StructuralEvidenceError("mesh node IDs are duplicated")
    return ElementMeshData(nodes, tetrahedra, triangles, expected_order)


def imperfect_element_mesh(
    mesh: ElementMeshData, *, length_m: float, tip_amplitude_m: float
) -> ElementMeshData:
    if not math.isfinite(tip_amplitude_m) or tip_amplitude_m < 0.0:
        raise StructuralEvidenceError("tip imperfection must be finite and non-negative")
    nodes = {}
    for node, xyz in mesh.nodes.items():
        if xyz[0] < 0.0 or xyz[0] > length_m:
            raise StructuralEvidenceError("mesh node lies outside declared column length")
        shape = 1.0 - math.cos(math.pi * xyz[0] / (2.0 * length_m))
        nodes[node] = (xyz[0], xyz[1], xyz[2] + tip_amplitude_m * shape)
    return ElementMeshData(nodes, mesh.tetrahedra, mesh.triangles, mesh.order)


def _triangle_area(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    c: tuple[float, float, float],
) -> float:
    ab = tuple(second - first for first, second in zip(a, b, strict=True))
    ac = tuple(second - first for first, second in zip(a, c, strict=True))
    cross = (
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    )
    return 0.5 * math.sqrt(math.fsum(value * value for value in cross))


def _nset(name: str, nodes: tuple[int, ...]) -> list[str]:
    if not nodes:
        raise StructuralEvidenceError(f"node set {name} must not be empty")
    return [f"*NSET, NSET={name}"] + [
        ", ".join(str(node) for node in nodes[index : index + 16])
        for index in range(0, len(nodes), 16)
    ]


def build_element_column_input(
    *, spec: TensionSpec, mesh: ElementMeshData, boundary_tolerance_m: float
) -> tuple[str, dict[int, float], tuple[int, ...], tuple[int, ...]]:
    """Build C3D4/C3D10 column decks with consistent end-face nodal loads."""

    fixed = tuple(sorted(node for node, xyz in mesh.nodes.items() if abs(xyz[0]) <= boundary_tolerance_m))
    loaded = tuple(sorted(node for node, xyz in mesh.nodes.items() if abs(xyz[0] - spec.length_m) <= boundary_tolerance_m))
    if not fixed or not loaded or set(fixed) & set(loaded):
        raise StructuralEvidenceError("fixed/loaded boundary node identity is invalid")
    loaded_set = set(loaded)
    tributary = {node: 0.0 for node in loaded}
    face_area = 0.0
    for triangle in mesh.triangles.values():
        if not set(triangle) <= loaded_set:
            continue
        area = _triangle_area(*(mesh.nodes[node] for node in triangle[:3]))
        if not math.isfinite(area) or area <= 0.0:
            raise StructuralEvidenceError("loaded surface has an invalid triangle")
        face_area += area
        if mesh.order == 1:
            for node in triangle:
                tributary[node] += area / 3.0
        else:
            # Exact consistent integral for a constant traction on TRI6:
            # corner shape functions integrate to zero; midsides integrate to A/3.
            for node in triangle[3:]:
                tributary[node] += area / 3.0
    if not math.isclose(face_area, spec.area_m2, rel_tol=1e-8, abs_tol=1e-14):
        raise StructuralEvidenceError(f"loaded face area {face_area} differs from declared {spec.area_m2}")
    loads = {
        node: spec.resultant_force_n * weight / face_area
        for node, weight in tributary.items() if weight > 0.0
    }
    if not loads or not math.isclose(math.fsum(loads.values()), spec.resultant_force_n, rel_tol=1e-12, abs_tol=1e-12):
        raise StructuralEvidenceError("consistent end-face loads do not close")

    lines = ["*HEADING", f"{spec.experiment_id} {spec.specimen_id}", "*NODE, NSET=NALL"]
    lines.extend(
        f"{node}, {xyz[0]:.12g}, {xyz[1]:.12g}, {xyz[2]:.12g}"
        for node, xyz in sorted(mesh.nodes.items())
    )
    lines.append(f"*ELEMENT, TYPE={mesh.calculix_element_type}, ELSET=EALL")
    lines.extend(
        f"{element}, {', '.join(str(node) for node in connectivity)}"
        for element, connectivity in sorted(mesh.tetrahedra.items())
    )
    lines.extend(_nset("FIXED", fixed))
    lines.extend(_nset("LOADED", loaded))
    lines.extend((
        f"*MATERIAL, NAME={spec.material_id}", "*ELASTIC",
        f"{spec.youngs_modulus_pa:.17g}, {spec.poisson_ratio:.17g}", "*DENSITY",
        f"{spec.density_kg_per_m3:.17g}", f"*SOLID SECTION, ELSET=EALL, MATERIAL={spec.material_id}",
        "*BOUNDARY", "FIXED, 1, 3, 0.0", "*STEP", "*STATIC", "*CLOAD",
    ))
    lines.extend(f"{node}, 1, {load:.17g}" for node, load in sorted(loads.items()))
    lines.extend((
        "*NODE PRINT, NSET=LOADED", "U", "*NODE PRINT, NSET=FIXED, TOTALS=YES", "RF",
        "*EL PRINT, ELSET=EALL", "S, E", "*NODE FILE", "U, RF", "*EL FILE", "S, E",
        "*END STEP", "",
    ))
    return "\n".join(lines).replace("e-", "E-").replace("e+", "E+"), loads, fixed, loaded


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"


def parse_element_column_dat(path: Path) -> dict[str, Any]:
    """Parse one final Work 041 static increment, retaining all integration points."""

    text = path.read_text(encoding="ascii", errors="replace")
    displacement_marker = "displacements (vx,vy,vz) for set LOADED"
    reaction_marker = "forces (fx,fy,fz) for set FIXED"
    total_marker = "total force (fx,fy,fz) for set FIXED"
    stress_marker = "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL"
    strain_marker = "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL"
    for marker in (displacement_marker, reaction_marker, total_marker, stress_marker, strain_marker):
        if marker not in text:
            raise StructuralEvidenceError(f"CalculiX table is missing: {marker}")
    displacement_block = text.split(displacement_marker, 1)[1].split(reaction_marker, 1)[0]
    displacement_rows = re.findall(
        rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", displacement_block, re.MULTILINE
    )
    reaction_block = text.split(reaction_marker, 1)[1].split(total_marker, 1)[0]
    reaction_rows = re.findall(
        rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", reaction_block, re.MULTILINE
    )
    total_block = text.split(total_marker, 1)[1].split(stress_marker, 1)[0]
    total_rows = re.findall(rf"^\s*({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", total_block, re.MULTILINE)
    stress_block = text.split(stress_marker, 1)[1].split(strain_marker, 1)[0]
    stress_rows = re.findall(
        rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        stress_block, re.MULTILINE,
    )
    if not displacement_rows or not reaction_rows or len(total_rows) != 1 or not stress_rows:
        raise StructuralEvidenceError("CalculiX static evidence is missing or ambiguous")
    displacements = {int(row[0]): tuple(float(value) for value in row[1:4]) for row in displacement_rows}
    stresses = {
        (int(row[0]), int(row[1])): tuple(float(value) for value in row[2:8])
        for row in stress_rows
    }
    if len(displacements) != len(displacement_rows) or len(stresses) != len(stress_rows):
        raise StructuralEvidenceError("CalculiX evidence identities are duplicated")
    total_reaction = tuple(float(value) for value in total_rows[0])
    values = [value for vector in (*displacements.values(), total_reaction, *stresses.values()) for value in vector]
    if not all(math.isfinite(value) for value in values):
        raise StructuralEvidenceError("CalculiX evidence contains a non-finite value")
    return {"displacements": displacements, "total_reaction": total_reaction, "stress_tensors_pa": stresses}
