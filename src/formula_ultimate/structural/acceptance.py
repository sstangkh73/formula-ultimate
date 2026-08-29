"""Fail-closed contracts for the first axial-tension solver acceptance run."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any, Mapping


class StructuralEvidenceError(ValueError):
    """Raised when structural evidence cannot be admitted."""


def _finite_positive(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise StructuralEvidenceError(f"{name} must be finite and > 0")


@dataclass(frozen=True, slots=True)
class TensionSpec:
    protocol_id: str
    experiment_id: str
    specimen_id: str
    claim_level: str
    length_m: float
    width_m: float
    height_m: float
    material_id: str
    youngs_modulus_pa: float
    poisson_ratio: float
    density_kg_per_m3: float
    material_provenance: str
    resultant_force_n: float

    def __post_init__(self) -> None:
        text_values = (
            self.protocol_id,
            self.experiment_id,
            self.specimen_id,
            self.claim_level,
            self.material_id,
            self.material_provenance,
        )
        if any(not item.strip() for item in text_values):
            raise StructuralEvidenceError("identity and provenance must not be empty")
        for name, value in (
            ("length_m", self.length_m),
            ("width_m", self.width_m),
            ("height_m", self.height_m),
            ("youngs_modulus_pa", self.youngs_modulus_pa),
            ("density_kg_per_m3", self.density_kg_per_m3),
        ):
            _finite_positive(name, value)
        if not math.isfinite(self.poisson_ratio) or not (-1.0 < self.poisson_ratio < 0.5):
            raise StructuralEvidenceError("poisson_ratio must be finite and in (-1, 0.5)")
        if not math.isfinite(self.resultant_force_n) or self.resultant_force_n == 0.0:
            raise StructuralEvidenceError("resultant_force_n must be finite and non-zero")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "TensionSpec":
        try:
            geometry = value["geometry"]
            material = value["material"]
            load = value["load"]
            if load["axis"] != "positive_x":
                raise StructuralEvidenceError("only the declared positive_x load axis is admitted")
            if load["distribution"] != "surface_triangle_tributary_area_weighted_nodal_loads":
                raise StructuralEvidenceError("unexpected load distribution policy")
            return cls(
                protocol_id=str(value["protocol_id"]),
                experiment_id=str(value["experiment_id"]),
                specimen_id=str(value["specimen_id"]),
                claim_level=str(value["claim_level"]),
                length_m=float(geometry["length_m"]),
                width_m=float(geometry["width_m"]),
                height_m=float(geometry["height_m"]),
                material_id=str(material["material_id"]),
                youngs_modulus_pa=float(material["youngs_modulus_pa"]),
                poisson_ratio=float(material["poisson_ratio"]),
                density_kg_per_m3=float(material["density_kg_per_m3"]),
                material_provenance=str(material["provenance"]),
                resultant_force_n=float(load["resultant_force_n"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, StructuralEvidenceError):
                raise
            raise StructuralEvidenceError(f"malformed tension specification: {exc}") from exc

    @property
    def area_m2(self) -> float:
        return self.width_m * self.height_m

    @property
    def volume_m3(self) -> float:
        return self.length_m * self.area_m2

    @property
    def analytical_stress_pa(self) -> float:
        return self.resultant_force_n / self.area_m2

    @property
    def analytical_strain(self) -> float:
        return self.analytical_stress_pa / self.youngs_modulus_pa

    @property
    def analytical_displacement_m(self) -> float:
        return self.analytical_strain * self.length_m

    @property
    def analytical_energy_j(self) -> float:
        return 0.5 * self.resultant_force_n * self.analytical_displacement_m


@dataclass(frozen=True, slots=True)
class MeshData:
    nodes: dict[int, tuple[float, float, float]]
    tetrahedra: dict[int, tuple[int, int, int, int]]
    triangles: dict[int, tuple[int, int, int]]

    def __post_init__(self) -> None:
        if not self.nodes or not self.tetrahedra or not self.triangles:
            raise StructuralEvidenceError("mesh requires nodes, tetrahedra, and boundary triangles")
        node_ids = set(self.nodes)
        used = {node for item in self.tetrahedra.values() for node in item}
        if not used <= node_ids:
            raise StructuralEvidenceError("tetrahedron references an unknown node")
        if any(not all(math.isfinite(v) for v in xyz) for xyz in self.nodes.values()):
            raise StructuralEvidenceError("mesh contains a non-finite coordinate")
        remaining = set(self.tetrahedra)
        start = remaining.pop()
        visited = {start}
        node_to_elements: dict[int, set[int]] = {}
        for element_id, connectivity in self.tetrahedra.items():
            for node in connectivity:
                node_to_elements.setdefault(node, set()).add(element_id)
        frontier = [start]
        while frontier:
            current = frontier.pop()
            neighbours = set().union(
                *(node_to_elements[node] for node in self.tetrahedra[current])
            )
            for neighbour in neighbours - visited:
                visited.add(neighbour)
                frontier.append(neighbour)
        if len(visited) != len(self.tetrahedra):
            raise StructuralEvidenceError("tetrahedral mesh is disconnected")


def parse_msh2(path: Path) -> MeshData:
    """Parse the ASCII MSH 2.2 subset emitted by the Work 034 Gmsh route."""

    lines = path.read_text(encoding="ascii", errors="strict").splitlines()
    try:
        mesh_index = lines.index("$MeshFormat")
        if lines[mesh_index + 1].split()[:2] != ["2.2", "0"]:
            raise StructuralEvidenceError("mesh is not ASCII MSH 2.2")
        node_index = lines.index("$Nodes")
        node_count = int(lines[node_index + 1])
        nodes: dict[int, tuple[float, float, float]] = {}
        for line in lines[node_index + 2 : node_index + 2 + node_count]:
            fields = line.split()
            nodes[int(fields[0])] = tuple(float(v) for v in fields[1:4])  # type: ignore[assignment]
        element_index = lines.index("$Elements")
        element_count = int(lines[element_index + 1])
        tetrahedra: dict[int, tuple[int, int, int, int]] = {}
        triangles: dict[int, tuple[int, int, int]] = {}
        element_ids: set[int] = set()
        for line in lines[element_index + 2 : element_index + 2 + element_count]:
            fields = line.split()
            element_id = int(fields[0])
            if element_id in element_ids:
                raise StructuralEvidenceError("mesh element IDs are duplicated")
            element_ids.add(element_id)
            element_type = int(fields[1])
            tag_count = int(fields[2])
            connectivity = tuple(int(v) for v in fields[3 + tag_count :])
            if element_type == 2:
                if len(connectivity) != 3:
                    raise StructuralEvidenceError("triangle connectivity is malformed")
                triangles[element_id] = connectivity  # type: ignore[assignment]
            elif element_type == 4:
                if len(connectivity) != 4:
                    raise StructuralEvidenceError("tetrahedron connectivity is malformed")
                tetrahedra[element_id] = connectivity  # type: ignore[assignment]
    except (ValueError, IndexError) as exc:
        raise StructuralEvidenceError(f"malformed MSH 2.2 evidence: {exc}") from exc
    if len(nodes) != node_count:
        raise StructuralEvidenceError("mesh node IDs are duplicated")
    return MeshData(nodes=nodes, tetrahedra=tetrahedra, triangles=triangles)


def _triangle_area(
    a: tuple[float, float, float],
    b: tuple[float, float, float],
    c: tuple[float, float, float],
) -> float:
    ab = tuple(b_i - a_i for a_i, b_i in zip(a, b, strict=True))
    ac = tuple(c_i - a_i for a_i, c_i in zip(a, c, strict=True))
    cross = (
        ab[1] * ac[2] - ab[2] * ac[1],
        ab[2] * ac[0] - ab[0] * ac[2],
        ab[0] * ac[1] - ab[1] * ac[0],
    )
    return 0.5 * math.sqrt(sum(value * value for value in cross))


def build_calculix_input(
    *, spec: TensionSpec, mesh: MeshData, boundary_tolerance_m: float
) -> tuple[str, dict[int, float], tuple[int, ...], tuple[int, ...]]:
    """Build a C3D4 deck and tributary-area weighted finite-surface load."""

    fixed = tuple(sorted(
        node_id for node_id, xyz in mesh.nodes.items()
        if abs(xyz[0]) <= boundary_tolerance_m
    ))
    loaded = tuple(sorted(
        node_id for node_id, xyz in mesh.nodes.items()
        if abs(xyz[0] - spec.length_m) <= boundary_tolerance_m
    ))
    if not fixed or not loaded or set(fixed) & set(loaded):
        raise StructuralEvidenceError("fixed/loaded boundary node identity is invalid")
    loaded_set = set(loaded)
    tributary: dict[int, float] = {node_id: 0.0 for node_id in loaded}
    face_area = 0.0
    face_count = 0
    for connectivity in mesh.triangles.values():
        if set(connectivity) <= loaded_set:
            area = _triangle_area(*(mesh.nodes[node] for node in connectivity))
            if not math.isfinite(area) or area <= 0.0:
                raise StructuralEvidenceError("loaded surface has an invalid triangle")
            face_area += area
            face_count += 1
            for node in connectivity:
                tributary[node] += area / 3.0
    if face_count == 0 or not math.isclose(face_area, spec.area_m2, rel_tol=1e-8, abs_tol=1e-14):
        raise StructuralEvidenceError(
            f"loaded face area {face_area} differs from declared {spec.area_m2}"
        )
    nodal_loads = {
        node: spec.resultant_force_n * area / face_area
        for node, area in tributary.items()
        if area > 0.0
    }
    if set(nodal_loads) != loaded_set:
        raise StructuralEvidenceError("some loaded-face nodes have zero tributary area")
    if not math.isclose(
        math.fsum(nodal_loads.values()),
        spec.resultant_force_n,
        rel_tol=1e-12,
        abs_tol=1e-12,
    ):
        raise StructuralEvidenceError("distributed nodal loads do not close")

    lines = [
        "*HEADING",
        f"{spec.experiment_id} {spec.specimen_id}",
        "*NODE, NSET=NALL",
    ]
    lines.extend(
        f"{node_id}, {xyz[0]:.17g}, {xyz[1]:.17g}, {xyz[2]:.17g}"
        for node_id, xyz in sorted(mesh.nodes.items())
    )
    lines.append("*ELEMENT, TYPE=C3D4, ELSET=EALL")
    lines.extend(
        f"{element_id}, {', '.join(str(node) for node in connectivity)}"
        for element_id, connectivity in sorted(mesh.tetrahedra.items())
    )
    lines.extend(("*NSET, NSET=FIXED", ", ".join(str(node) for node in fixed)))
    lines.extend(("*NSET, NSET=LOADED", ", ".join(str(node) for node in loaded)))
    lines.extend((
        f"*MATERIAL, NAME={spec.material_id}",
        "*ELASTIC",
        f"{spec.youngs_modulus_pa:.17g}, {spec.poisson_ratio:.17g}",
        "*DENSITY",
        f"{spec.density_kg_per_m3:.17g}",
        f"*SOLID SECTION, ELSET=EALL, MATERIAL={spec.material_id}",
        "*BOUNDARY",
        "FIXED, 1, 3, 0.0",
        "*STEP",
        "*STATIC",
        "*CLOAD",
    ))
    lines.extend(f"{node}, 1, {load:.17g}" for node, load in sorted(nodal_loads.items()))
    lines.extend((
        "*NODE PRINT, NSET=LOADED",
        "U",
        "*NODE PRINT, NSET=FIXED, TOTALS=YES",
        "RF",
        "*EL PRINT, ELSET=EALL",
        "S, E",
        "*NODE FILE",
        "U, RF",
        "*EL FILE",
        "S, E",
        "*END STEP",
        "",
    ))
    return "\n".join(lines), nodal_loads, fixed, loaded


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"


def parse_calculix_dat(path: Path) -> dict[str, Any]:
    """Parse the narrow Work 034 CalculiX .dat tables; fail on unknown evidence."""

    text = path.read_text(encoding="ascii", errors="replace")
    if "displacements (vx,vy,vz) for set LOADED" not in text:
        raise StructuralEvidenceError("CalculiX displacement table is missing")
    if "forces (fx,fy,fz) for set FIXED" not in text:
        raise StructuralEvidenceError("CalculiX reaction table is missing")
    displacement_block = text.split(
        "displacements (vx,vy,vz) for set LOADED", 1
    )[1].split("forces (fx,fy,fz) for set FIXED", 1)[0]
    displacement_rows = re.findall(
        rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        displacement_block,
        flags=re.MULTILINE,
    )
    if not displacement_rows:
        raise StructuralEvidenceError("CalculiX loaded displacement rows are missing")
    reaction_start = "forces (fx,fy,fz) for set FIXED"
    reaction_end = "total force (fx,fy,fz) for set FIXED"
    if reaction_end not in text:
        raise StructuralEvidenceError("CalculiX total reaction table is missing")
    reaction_block = text.split(reaction_start, 1)[1].split(reaction_end, 1)[0]
    reaction_rows = re.findall(
        rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        reaction_block,
        flags=re.MULTILINE,
    )
    if not reaction_rows:
        raise StructuralEvidenceError("CalculiX fixed reaction rows are missing")
    stress_marker = "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL"
    strain_marker = "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL"
    if stress_marker not in text:
        raise StructuralEvidenceError("CalculiX stress table is missing")
    if strain_marker not in text:
        raise StructuralEvidenceError("CalculiX strain table is missing")
    stress_block = text.split(stress_marker, 1)[1].split(strain_marker, 1)[0]
    stress_rows = re.findall(
        rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$",
        stress_block,
        flags=re.MULTILINE,
    )
    if not stress_rows:
        raise StructuralEvidenceError("CalculiX stress rows are missing")
    displacements = {
        int(row[0]): tuple(float(v) for v in row[1:4])
        for row in displacement_rows
    }
    reactions = {int(row[0]): tuple(float(v) for v in row[1:4]) for row in reaction_rows}
    stresses = {int(row[0]): float(row[2]) for row in stress_rows}
    if len(displacements) != len(displacement_rows):
        raise StructuralEvidenceError("CalculiX displacement node IDs are duplicated")
    if len(reactions) != len(reaction_rows):
        raise StructuralEvidenceError("CalculiX reaction node IDs are duplicated")
    if len(stresses) != len(stress_rows):
        raise StructuralEvidenceError("CalculiX stress element IDs are duplicated")
    values = [value for vector in (*displacements.values(), *reactions.values()) for value in vector]
    values.extend(stresses.values())
    if not all(math.isfinite(value) for value in values):
        raise StructuralEvidenceError("CalculiX parsed evidence contains a non-finite value")
    return {
        "displacements": displacements,
        "reactions": reactions,
        "axial_stress_by_element_pa": stresses,
    }
