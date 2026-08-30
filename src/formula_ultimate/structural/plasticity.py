"""Fail-closed bilinear plasticity verification contracts for Work 042."""

from __future__ import annotations

from dataclasses import dataclass
import math
from pathlib import Path
import re
from typing import Any, Mapping

from .acceptance import StructuralEvidenceError


_FLOAT = r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?"


@dataclass(frozen=True, slots=True)
class BilinearPlasticitySpec:
    protocol_id: str
    claim_level: str
    length_m: float
    width_m: float
    height_m: float
    material_id: str
    youngs_modulus_pa: float
    poisson_ratio: float
    density_kg_per_m3: float
    yield_stress_pa: float
    tangent_modulus_pa: float
    provenance: str

    def __post_init__(self) -> None:
        if any(not value.strip() for value in (self.protocol_id, self.claim_level, self.material_id, self.provenance)):
            raise StructuralEvidenceError("plasticity identity and provenance must not be empty")
        for name, value in (
            ("length_m", self.length_m), ("width_m", self.width_m),
            ("height_m", self.height_m), ("youngs_modulus_pa", self.youngs_modulus_pa),
            ("density_kg_per_m3", self.density_kg_per_m3),
            ("yield_stress_pa", self.yield_stress_pa), ("tangent_modulus_pa", self.tangent_modulus_pa),
        ):
            if not math.isfinite(value) or value <= 0.0:
                raise StructuralEvidenceError(f"{name} must be finite and > 0")
        if self.tangent_modulus_pa >= self.youngs_modulus_pa:
            raise StructuralEvidenceError("tangent_modulus_pa must be below youngs_modulus_pa")
        if not math.isfinite(self.poisson_ratio) or not (-1.0 < self.poisson_ratio < 0.5):
            raise StructuralEvidenceError("poisson_ratio must be finite and in (-1, 0.5)")

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "BilinearPlasticitySpec":
        try:
            geometry, material = value["geometry"], value["material"]
            if material["law"] != "synthetic_rate_independent_isotropic_bilinear":
                raise StructuralEvidenceError("unsupported plasticity law")
            return cls(
                str(value["protocol_id"]), str(value["claim_level"]),
                float(geometry["length_m"]), float(geometry["width_m"]), float(geometry["height_m"]),
                str(material["material_id"]), float(material["youngs_modulus_pa"]),
                float(material["poisson_ratio"]), float(material["density_kg_per_m3"]),
                float(material["yield_stress_pa"]), float(material["tangent_modulus_pa"]),
                str(material["provenance"]),
            )
        except (KeyError, TypeError, ValueError) as exc:
            if isinstance(exc, StructuralEvidenceError):
                raise
            raise StructuralEvidenceError(f"malformed plasticity specification: {exc}") from exc

    @property
    def area_m2(self) -> float:
        return self.width_m * self.height_m

    @property
    def yield_force_n(self) -> float:
        return self.yield_stress_pa * self.area_m2

    @property
    def hardening_modulus_pa(self) -> float:
        return self.youngs_modulus_pa * self.tangent_modulus_pa / (
            self.youngs_modulus_pa - self.tangent_modulus_pa
        )

    def monotonic_strain(self, stress_pa: float) -> float:
        sign = 1.0 if stress_pa >= 0.0 else -1.0
        magnitude = abs(stress_pa)
        if magnitude <= self.yield_stress_pa:
            return stress_pa / self.youngs_modulus_pa
        return sign * (
            self.yield_stress_pa / self.youngs_modulus_pa
            + (magnitude - self.yield_stress_pa) / self.tangent_modulus_pa
        )

    def monotonic_plastic_strain(self, stress_pa: float) -> float:
        if abs(stress_pa) <= self.yield_stress_pa:
            return 0.0
        return (abs(stress_pa) - self.yield_stress_pa) / self.hardening_modulus_pa


@dataclass(frozen=True, slots=True)
class HexMesh:
    nodes: dict[int, tuple[float, float, float]]
    elements: dict[int, tuple[int, int, int, int, int, int, int, int]]
    fixed_x: tuple[int, ...]
    loaded: tuple[int, ...]
    anchors_y: tuple[int, ...]
    anchors_z: tuple[int, ...]
    tributary_area_m2: dict[int, float]


def structured_hex_mesh(spec: BilinearPlasticitySpec, *, nx: int, ny: int = 2, nz: int = 2) -> HexMesh:
    if nx <= 0 or ny <= 0 or nz <= 0 or ny % 2 or nz % 2:
        raise StructuralEvidenceError("structured mesh requires nx>0 and positive even ny/nz")
    nodes: dict[int, tuple[float, float, float]] = {}
    ids: dict[tuple[int, int, int], int] = {}
    node = 1
    for k in range(nz + 1):
        z = -spec.height_m / 2.0 + spec.height_m * k / nz
        for j in range(ny + 1):
            y = -spec.width_m / 2.0 + spec.width_m * j / ny
            for i in range(nx + 1):
                x = spec.length_m * i / nx
                ids[i, j, k] = node
                nodes[node] = (x, y, z)
                node += 1
    elements: dict[int, tuple[int, int, int, int, int, int, int, int]] = {}
    element = 1
    for k in range(nz):
        for j in range(ny):
            for i in range(nx):
                elements[element] = (
                    ids[i, j, k], ids[i + 1, j, k], ids[i + 1, j + 1, k], ids[i, j + 1, k],
                    ids[i, j, k + 1], ids[i + 1, j, k + 1], ids[i + 1, j + 1, k + 1], ids[i, j + 1, k + 1],
                )
                element += 1
    fixed_x = tuple(sorted(ids[0, j, k] for j in range(ny + 1) for k in range(nz + 1)))
    loaded = tuple(sorted(ids[nx, j, k] for j in range(ny + 1) for k in range(nz + 1)))
    centre = ids[0, ny // 2, nz // 2]
    rotation_anchor = ids[0, ny // 2, nz]
    tributary = {node_id: 0.0 for node_id in loaded}
    patch_area = spec.area_m2 / (ny * nz)
    for j in range(ny):
        for k in range(nz):
            for key in ((nx, j, k), (nx, j + 1, k), (nx, j + 1, k + 1), (nx, j, k + 1)):
                tributary[ids[key]] += patch_area / 4.0
    if not math.isclose(math.fsum(tributary.values()), spec.area_m2, rel_tol=1e-12):
        raise StructuralEvidenceError("loaded-face tributary area does not close")
    return HexMesh(nodes, elements, fixed_x, loaded, (centre, rotation_anchor), (centre,), tributary)


def _nset(name: str, nodes: tuple[int, ...]) -> list[str]:
    lines = [f"*NSET, NSET={name}"]
    for start in range(0, len(nodes), 16):
        lines.append(", ".join(str(value) for value in nodes[start:start + 16]))
    return lines


def build_plasticity_deck(
    spec: BilinearPlasticitySpec,
    mesh: HexMesh,
    *,
    load_factors: tuple[float, ...],
    maximum_plastic_strain: float,
) -> str:
    if len(load_factors) < 4 or not all(math.isfinite(value) for value in load_factors):
        raise StructuralEvidenceError("plasticity load history is incomplete or non-finite")
    if not math.isfinite(maximum_plastic_strain) or maximum_plastic_strain <= 0.0:
        raise StructuralEvidenceError("maximum_plastic_strain must be finite and > 0")
    lines = ["*HEADING", spec.protocol_id, "*NODE, NSET=NALL"]
    lines.extend(f"{node}, {x:.17g}, {y:.17g}, {z:.17g}" for node, (x, y, z) in sorted(mesh.nodes.items()))
    lines.append("*ELEMENT, TYPE=C3D8, ELSET=EALL")
    lines.extend(f"{element}, {', '.join(str(node) for node in connectivity)}" for element, connectivity in sorted(mesh.elements.items()))
    lines.extend(_nset("FIXEDX", mesh.fixed_x))
    lines.extend(_nset("LOADED", mesh.loaded))
    lines.extend(_nset("ANCHORY", mesh.anchors_y))
    lines.extend(_nset("ANCHORZ", mesh.anchors_z))
    hardening = spec.hardening_modulus_pa
    lines.extend((
        f"*MATERIAL, NAME={spec.material_id}", "*ELASTIC",
        f"{spec.youngs_modulus_pa:.17g}, {spec.poisson_ratio:.17g}", "*PLASTIC",
        f"{spec.yield_stress_pa:.17g}, 0.0",
        f"{spec.yield_stress_pa + hardening * maximum_plastic_strain:.17g}, {maximum_plastic_strain:.17g}",
        f"*SOLID SECTION, ELSET=EALL, MATERIAL={spec.material_id}", "*BOUNDARY",
        "FIXEDX, 1, 1, 0.0", "ANCHORY, 2, 2, 0.0", "ANCHORZ, 3, 3, 0.0",
    ))
    for index, factor in enumerate(load_factors, start=1):
        force = factor * spec.yield_force_n
        lines.extend((f"*STEP, INC=100", "*STATIC", "0.1, 1.0, 1e-08, 0.1", "*CLOAD, OP=NEW"))
        for node, area in sorted(mesh.tributary_area_m2.items()):
            lines.append(f"{node}, 1, {force * area / spec.area_m2:.17g}")
        lines.extend((
            "*NODE PRINT, NSET=LOADED, FREQUENCY=999", "U", "*NODE PRINT, NSET=FIXEDX, TOTALS=YES, FREQUENCY=999", "RF",
            "*EL PRINT, ELSET=EALL, FREQUENCY=999", "S, E, PEEQ, ENER, ELSE", "*NODE FILE, FREQUENCY=999", "U, RF",
            "*EL FILE", "S, E, PEEQ", "*END STEP",
        ))
    lines.append("")
    return "\n".join(lines)


def _blocks(text: str, marker: str, next_markers: tuple[str, ...]) -> list[str]:
    starts = [match.end() for match in re.finditer(re.escape(marker), text)]
    blocks: list[str] = []
    for start in starts:
        end = len(text)
        for next_marker in next_markers:
            match = re.search(re.escape(next_marker), text[start:])
            if match:
                end = min(end, start + match.start())
        blocks.append(text[start:end])
    return blocks


def parse_plasticity_dat(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="ascii", errors="replace")
    displacement_marker = "displacements (vx,vy,vz) for set LOADED"
    reaction_marker = "forces (fx,fy,fz) for set FIXEDX"
    stress_marker = "stresses (elem, integ.pnt.,sxx,syy,szz,sxy,sxz,syz) for set EALL"
    strain_marker = "strains (elem, integ.pnt.,exx,eyy,ezz,exy,exz,eyz) for set EALL"
    peeq_markers = ("equivalent plastic strain", "equivalent plastic strains")
    displacement_blocks = _blocks(text, displacement_marker, (reaction_marker,))
    reaction_blocks = _blocks(text, reaction_marker, ("total force (fx,fy,fz) for set FIXEDX",))
    stress_blocks = _blocks(text, stress_marker, (strain_marker,))
    strain_blocks = _blocks(text, strain_marker, peeq_markers + ("internal energy density", "internal energies"))
    peeq_marker = next((marker for marker in peeq_markers if marker in text), None)
    if peeq_marker is None:
        raise StructuralEvidenceError("CalculiX equivalent plastic strain table is missing")
    peeq_blocks = _blocks(text, peeq_marker, ("internal energy density", "internal energies", displacement_marker))
    energy_marker = "internal energy (element, energy) for set EALL"
    energy_blocks = _blocks(text, energy_marker, (displacement_marker,)) if energy_marker in text else []
    counts = {len(displacement_blocks), len(reaction_blocks), len(stress_blocks), len(strain_blocks), len(peeq_blocks), len(energy_blocks)}
    if len(counts) != 1 or not counts or next(iter(counts)) == 0:
        raise StructuralEvidenceError(f"CalculiX multi-step table count mismatch: {sorted(counts)}")
    vector_pattern = re.compile(rf"^\s*(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", re.MULTILINE)
    tensor_pattern = re.compile(rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s+({_FLOAT})\s*$", re.MULTILINE)
    scalar_ip_pattern = re.compile(rf"^\s*(\d+)\s+(\d+)\s+({_FLOAT})\s*$", re.MULTILINE)
    scalar_element_pattern = re.compile(rf"^\s*(\d+)\s+({_FLOAT})\s*$", re.MULTILINE)
    results: list[dict[str, Any]] = []
    for index in range(len(displacement_blocks)):
        displacements = {int(row[0]): tuple(float(v) for v in row[1:]) for row in vector_pattern.findall(displacement_blocks[index])}
        reactions = {int(row[0]): tuple(float(v) for v in row[1:]) for row in vector_pattern.findall(reaction_blocks[index])}
        stresses = [(int(row[0]), int(row[1]), tuple(float(v) for v in row[2:])) for row in tensor_pattern.findall(stress_blocks[index])]
        strains = [(int(row[0]), int(row[1]), tuple(float(v) for v in row[2:])) for row in tensor_pattern.findall(strain_blocks[index])]
        peeq = [(int(row[0]), int(row[1]), float(row[2])) for row in scalar_ip_pattern.findall(peeq_blocks[index])]
        energies = {int(row[0]): float(row[1]) for row in scalar_element_pattern.findall(energy_blocks[index])}
        if not displacements or not reactions or not stresses or not strains or not peeq or not energies:
            raise StructuralEvidenceError(f"CalculiX step {index + 1} contains incomplete plasticity evidence")
        values = [value for vector in (*displacements.values(), *reactions.values()) for value in vector]
        values.extend(value for _, _, tensor in (*stresses, *strains) for value in tensor)
        values.extend(value for _, _, value in peeq)
        values.extend(energies.values())
        if not all(math.isfinite(value) for value in values):
            raise StructuralEvidenceError("CalculiX plasticity evidence contains a non-finite value")
        results.append({"displacements": displacements, "reactions": reactions, "stresses": stresses, "strains": strains, "peeq": peeq, "element_internal_energy_j": energies})
    return results
