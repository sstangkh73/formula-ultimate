"""Persistent loaded-interface geometry, mesh mapping, and solver evidence."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any, Mapping

from .acceptance import MeshData, StructuralEvidenceError


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"


@dataclass(frozen=True, slots=True)
class CylindricalInterface:
    interface_id: str
    role: str
    center_x_m: float
    center_y_m: float
    radius_m: float

    def __post_init__(self) -> None:
        if not self.interface_id.strip() or self.role not in {"loaded", "support"}:
            raise StructuralEvidenceError("interface identity/role is invalid")
        for name, value in (("center_x_m", self.center_x_m), ("center_y_m", self.center_y_m), ("radius_m", self.radius_m)):
            if not math.isfinite(value) or (name == "radius_m" and value <= 0.0):
                raise StructuralEvidenceError(f"{name} is invalid")


@dataclass(frozen=True, slots=True)
class LoadedInterfacePlateSpec:
    protocol_id: str
    length_m: float
    width_m: float
    thickness_m: float
    youngs_modulus_pa: float
    poisson_ratio: float
    density_kg_per_m3: float
    material_id: str
    provenance: str
    load_force_n: tuple[float, float, float]
    interfaces: tuple[CylindricalInterface, ...]
    minimum_ligament_m: float

    def __post_init__(self) -> None:
        if not self.protocol_id.strip() or not self.material_id.strip() or not self.provenance.strip():
            raise StructuralEvidenceError("loaded-interface identity/provenance is required")
        for name, value in (("length_m", self.length_m), ("width_m", self.width_m), ("thickness_m", self.thickness_m), ("youngs_modulus_pa", self.youngs_modulus_pa), ("density_kg_per_m3", self.density_kg_per_m3), ("minimum_ligament_m", self.minimum_ligament_m)):
            if not math.isfinite(value) or value <= 0.0:
                raise StructuralEvidenceError(f"{name} must be finite and > 0")
        if not math.isfinite(self.poisson_ratio) or not (-1 < self.poisson_ratio < 0.5):
            raise StructuralEvidenceError("poisson_ratio is invalid")
        if not all(math.isfinite(value) for value in self.load_force_n) or math.sqrt(math.fsum(value * value for value in self.load_force_n)) <= 0.0:
            raise StructuralEvidenceError("interface load must be finite and non-zero")
        ids = [item.interface_id for item in self.interfaces]
        if len(ids) != len(set(ids)):
            raise StructuralEvidenceError("interface IDs are duplicated")
        if sum(item.role == "loaded" for item in self.interfaces) != 1 or sum(item.role == "support" for item in self.interfaces) < 1:
            raise StructuralEvidenceError("exactly one loaded and at least one support interface are required")
        for item in self.interfaces:
            edge = min(item.center_x_m, self.length_m - item.center_x_m, item.center_y_m + self.width_m / 2, self.width_m / 2 - item.center_y_m) - item.radius_m
            if edge < self.minimum_ligament_m:
                raise StructuralEvidenceError("interface violates the minimum outer ligament")
        for index, left in enumerate(self.interfaces):
            for right in self.interfaces[index + 1:]:
                ligament = math.hypot(left.center_x_m - right.center_x_m, left.center_y_m - right.center_y_m) - left.radius_m - right.radius_m
                if ligament < self.minimum_ligament_m:
                    raise StructuralEvidenceError("interfaces violate the minimum internal ligament")

    @property
    def loaded_interface(self) -> CylindricalInterface:
        return next(item for item in self.interfaces if item.role == "loaded")

    @property
    def support_interfaces(self) -> tuple[CylindricalInterface, ...]:
        return tuple(item for item in self.interfaces if item.role == "support")


@dataclass(frozen=True, slots=True)
class MappedInterface:
    interface_id: str
    triangle_ids: tuple[int, ...]
    node_ids: tuple[int, ...]
    faceted_area_m2: float

    def __post_init__(self) -> None:
        if not self.interface_id.strip() or not self.triangle_ids or not self.node_ids:
            raise StructuralEvidenceError("mapped interface identity/coverage is incomplete")
        if not math.isfinite(self.faceted_area_m2) or self.faceted_area_m2 <= 0.0:
            raise StructuralEvidenceError("mapped interface has zero or invalid area")


def spec_from_mapping(value: Mapping[str, Any]) -> LoadedInterfacePlateSpec:
    try:
        geometry, material, load = value["geometry"], value["material"], value["load"]
        interfaces = tuple(CylindricalInterface(str(item["interface_id"]), str(item["role"]), float(item["center_x_m"]), float(item["center_y_m"]), float(item["radius_m"])) for item in value["interfaces"])
        return LoadedInterfacePlateSpec(str(value["protocol_id"]), float(geometry["length_m"]), float(geometry["width_m"]), float(geometry["thickness_m"]), float(material["youngs_modulus_pa"]), float(material["poisson_ratio"]), float(material["density_kg_per_m3"]), str(material["material_id"]), str(material["provenance"]), tuple(float(item) for item in load["force_n"]), interfaces, float(geometry["minimum_ligament_m"]))  # type: ignore[arg-type]
    except (KeyError, TypeError, ValueError) as exc:
        if isinstance(exc, StructuralEvidenceError):
            raise
        raise StructuralEvidenceError(f"malformed loaded-interface plate: {exc}") from exc


def triangle_area(a: tuple[float, float, float], b: tuple[float, float, float], c: tuple[float, float, float]) -> float:
    ab = tuple(b[i] - a[i] for i in range(3)); ac = tuple(c[i] - a[i] for i in range(3))
    cross = (ab[1] * ac[2] - ab[2] * ac[1], ab[2] * ac[0] - ab[0] * ac[2], ab[0] * ac[1] - ab[1] * ac[0])
    return 0.5 * math.sqrt(math.fsum(value * value for value in cross))


def map_cylindrical_interfaces(spec: LoadedInterfacePlateSpec, mesh: MeshData, *, radial_tolerance_m: float) -> dict[str, MappedInterface]:
    if not math.isfinite(radial_tolerance_m) or radial_tolerance_m <= 0.0:
        raise StructuralEvidenceError("radial_tolerance_m must be finite and > 0")
    result: dict[str, MappedInterface] = {}
    claimed: set[int] = set()
    for interface in spec.interfaces:
        triangles: list[int] = []
        nodes: set[int] = set()
        area = 0.0
        for triangle_id, connectivity in mesh.triangles.items():
            points = [mesh.nodes[node] for node in connectivity]
            if all(abs(math.hypot(point[0] - interface.center_x_m, point[1] - interface.center_y_m) - interface.radius_m) <= radial_tolerance_m and -radial_tolerance_m <= point[2] <= spec.thickness_m + radial_tolerance_m for point in points):
                if triangle_id in claimed:
                    raise StructuralEvidenceError("one mesh triangle maps to multiple interfaces")
                triangles.append(triangle_id); nodes.update(connectivity); area += triangle_area(*points)
        if not triangles or not nodes or area <= 0.0:
            raise StructuralEvidenceError(f"interface {interface.interface_id} has zero mapped area")
        claimed.update(triangles)
        result[interface.interface_id] = MappedInterface(interface.interface_id, tuple(sorted(triangles)), tuple(sorted(nodes)), area)
    return result


def consistent_interface_load(spec: LoadedInterfacePlateSpec, mesh: MeshData, mapped: MappedInterface) -> dict[int, tuple[float, float, float]]:
    raw = {node: [0.0, 0.0, 0.0] for node in mapped.node_ids}
    for triangle_id in mapped.triangle_ids:
        connectivity = mesh.triangles[triangle_id]
        area = triangle_area(*(mesh.nodes[node] for node in connectivity))
        for node in connectivity:
            for axis in range(3):
                raw[node][axis] += spec.load_force_n[axis] * area / (3.0 * mapped.faceted_area_m2)
    loads = {node: tuple(vector) for node, vector in raw.items()}
    totals = tuple(math.fsum(vector[axis] for vector in loads.values()) for axis in range(3))
    if any(abs(totals[axis] - spec.load_force_n[axis]) > 1e-10 * max(abs(spec.load_force_n[axis]), 1.0) for axis in range(3)):
        raise StructuralEvidenceError("consistent interface load does not close")
    return loads


def _nset(name: str, nodes: tuple[int, ...]) -> list[str]:
    lines = [f"*NSET, NSET={name}"]
    for start in range(0, len(nodes), 16):
        lines.append(", ".join(str(node) for node in nodes[start:start + 16]))
    return lines


def build_loaded_interface_deck(spec: LoadedInterfacePlateSpec, mesh: MeshData, mapped: Mapping[str, MappedInterface], *, support_interface_ids: tuple[str, ...]) -> tuple[str, dict[int, tuple[float, float, float]], tuple[int, ...]]:
    if not support_interface_ids or len(set(support_interface_ids)) != len(support_interface_ids):
        raise StructuralEvidenceError("support interface selection is missing or duplicated")
    declared_supports = {item.interface_id for item in spec.support_interfaces}
    if not set(support_interface_ids) <= declared_supports:
        raise StructuralEvidenceError("support selection contains an undeclared interface")
    loaded = mapped[spec.loaded_interface.interface_id]
    loads = consistent_interface_load(spec, mesh, loaded)
    support_nodes = tuple(sorted(set().union(*(set(mapped[item].node_ids) for item in support_interface_ids))))
    if not support_nodes or set(support_nodes) & set(loaded.node_ids):
        raise StructuralEvidenceError("support and loaded interface nodes are invalid")
    lines = ["*HEADING", spec.protocol_id, "*NODE, NSET=NALL"]
    # CalculiX free-field coordinates reject fields longer than their parser limit.
    lines.extend(f"{node}, {x:.12g}, {y:.12g}, {z:.12g}" for node, (x, y, z) in sorted(mesh.nodes.items()))
    lines.append("*ELEMENT, TYPE=C3D4, ELSET=EALL")
    lines.extend(f"{element}, {', '.join(str(node) for node in connectivity)}" for element, connectivity in sorted(mesh.tetrahedra.items()))
    lines.extend(_nset("LOADED_IFACE", loaded.node_ids))
    for interface in spec.support_interfaces:
        lines.extend(_nset(interface.interface_id.upper(), mapped[interface.interface_id].node_ids))
    lines.extend(_nset("ACTIVE_SUPPORT", support_nodes))
    lines.extend((f"*MATERIAL, NAME={spec.material_id}", "*ELASTIC", f"{spec.youngs_modulus_pa:.17g}, {spec.poisson_ratio:.17g}", "*DENSITY", f"{spec.density_kg_per_m3:.17g}", f"*SOLID SECTION, ELSET=EALL, MATERIAL={spec.material_id}", "*BOUNDARY", "ACTIVE_SUPPORT, 1, 3, 0.0", "*STEP", "*STATIC", "*CLOAD"))
    for node, vector in sorted(loads.items()):
        for dof, value in enumerate(vector, start=1):
            if value:
                lines.append(f"{node}, {dof}, {value:.17g}")
    lines.extend(("*NODE PRINT, NSET=LOADED_IFACE", "U", "*NODE PRINT, NSET=ACTIVE_SUPPORT, TOTALS=YES", "RF"))
    for interface in spec.support_interfaces:
        lines.extend((f"*NODE PRINT, NSET={interface.interface_id.upper()}, TOTALS=YES", "RF"))
    lines.extend(("*EL PRINT, ELSET=EALL", "S, E, ENER, ELSE", "*NODE FILE", "U, RF", "*EL FILE", "S, E", "*END STEP", ""))
    return "\n".join(lines), loads, support_nodes


def parse_loaded_interface_dat(path: Path, *, support_set_names: tuple[str, ...]) -> dict[str, Any]:
    text = path.read_text(encoding="ascii", errors="replace")
    vector_pattern = re.compile(rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", re.MULTILINE)
    displacement_marker = "displacements (vx,vy,vz) for set LOADED_IFACE"
    first_force = "forces (fx,fy,fz) for set ACTIVE_SUPPORT"
    if displacement_marker not in text or first_force not in text:
        raise StructuralEvidenceError("loaded-interface displacement/reaction tables are missing")
    displacement_block = text.split(displacement_marker, 1)[1].split(first_force, 1)[0]
    displacements = {int(row[0]): tuple(float(v) for v in row[1:]) for row in vector_pattern.findall(displacement_block)}
    reactions: dict[str, dict[int, tuple[float, float, float]]] = {}
    for name in ("ACTIVE_SUPPORT", *support_set_names):
        marker = f"forces (fx,fy,fz) for set {name}"
        total = f"total force (fx,fy,fz) for set {name}"
        if marker not in text or total not in text:
            raise StructuralEvidenceError(f"reaction table for {name} is missing")
        block = text.split(marker, 1)[1].split(total, 1)[0]
        reactions[name] = {int(row[0]): tuple(float(v) for v in row[1:]) for row in vector_pattern.findall(block)}
    stress_marker = "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL"
    strain_marker = "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL"
    energy_marker = "internal energy (element, energy) for set EALL"
    if any(marker not in text for marker in (stress_marker, strain_marker, energy_marker)):
        raise StructuralEvidenceError("loaded-interface field/energy table is missing")
    tensor_pattern = re.compile(rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", re.MULTILINE)
    stress_block = text.split(stress_marker, 1)[1].split(strain_marker, 1)[0]
    stresses = [(int(row[0]), int(row[1]), tuple(float(value) for value in row[2:])) for row in tensor_pattern.findall(stress_block)]
    energy_block = text.split(energy_marker, 1)[1]
    energy_pattern = re.compile(rf"^\s*(\d+)\s+({_FLOAT})\s*$", re.MULTILINE)
    energies = {int(row[0]): float(row[1]) for row in energy_pattern.findall(energy_block)}
    if not displacements or not all(reactions.values()) or not stresses or not energies:
        raise StructuralEvidenceError("loaded-interface solver evidence is incomplete")
    return {"displacements": displacements, "reactions": reactions, "stresses": stresses, "element_internal_energy_j": energies}
