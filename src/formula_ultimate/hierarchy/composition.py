"""Seed-to-manifest composition of the hierarchical vehicle (pure Python).

The procedure is declared and seed-driven: Work 150 ``decompose`` proposes an
abstract tree, Work 152 ``layout`` places its leaves; when the layout fails,
the same decomposition search continues from the next attempt (bounded by
``CompositionConfig.max_plan_attempts``). Rejected attempts are recorded, not
hidden. Leaf masses enter the manifest only from measurements of the exported
meshes (``leaf_geometry.measure_mesh``); assembly masses roll up exactly.

Materials are drawn per leaf from declared catalogue records. The v1 catalogue
is a synthetic fixture (``evidence_status=synthetic``,
``design_use_allowed=false``), so masses are representation values, not
design masses. Nothing here is physical validation.
"""

from __future__ import annotations

import json
import random
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .decomposition import (
    DECOMPOSITION_VERSION,
    DEFAULT_CONFIG,
    AbstractTree,
    DecompositionConfig,
    decompose,
)
from .layout import (
    DEFAULT_LAYOUT_CONFIG,
    LAYOUT_VERSION,
    LayoutConfig,
    LayoutFailure,
    LayoutResult,
    layout,
    layout_problems,
)
from .leaf_geometry import LEAF_GRAMMAR_VERSION
from .part_tree import (
    AssemblyNode,
    Interface,
    PartNode,
    PartTree,
    canonical_sha256,
    to_manifest_interfaces,
    to_manifest_nodes,
    validate_part_tree,
)


DESIGN_LANGUAGE_VERSION = "hier-composition-v1"
MESH_DIR = "meshes"
DEFAULT_MATERIAL_CATALOGUE = Path("config") / "materials" / "engineering_material_manufacturing_v1.json"


class CompositionFailure(RuntimeError):
    """Raised when no declared plan attempt produces a valid layout."""


@dataclass(frozen=True)
class CompositionConfig:
    contact_tolerance_m: float = 1e-4
    max_plan_attempts: int = 8


DEFAULT_COMPOSITION_CONFIG = CompositionConfig()


@dataclass(frozen=True)
class LeafMaterial:
    material_id: str
    density_kg_m3: float
    evidence_status: str


@dataclass(frozen=True)
class VehiclePlan:
    seed: int
    tree: AbstractTree
    layout: LayoutResult
    rejected: tuple[str, ...]
    materials: dict[str, LeafMaterial]


# --------------------------------------------------------------------------
# Materials
# --------------------------------------------------------------------------

def _material_records(value: Any):
    if isinstance(value, dict):
        if isinstance(value.get("material_id"), str) and isinstance(value.get("properties"), dict):
            yield value
        for child in value.values():
            yield from _material_records(child)
    elif isinstance(value, list):
        for child in value:
            yield from _material_records(child)


def load_leaf_materials(path: Path) -> tuple[LeafMaterial, ...]:
    """Material id, density and evidence status of every record in a catalogue file.

    Values are read at run time; they are never copied into tracked files.
    """

    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    materials = []
    for record in _material_records(payload):
        properties = record["properties"]
        density = properties.get("density_kg_m3", properties.get("density_kg_per_m3"))
        if isinstance(density, (int, float)) and not isinstance(density, bool) and density > 0:
            materials.append(LeafMaterial(record["material_id"], float(density),
                                          str(record.get("evidence_status", "unknown"))))
    if not materials:
        raise CompositionFailure(f"{path}: no material record with a positive density")
    return tuple(sorted(materials, key=lambda m: m.material_id))


def assign_materials(seed: int, leaf_ids: Sequence[str],
                     catalogue: Sequence[LeafMaterial]) -> dict[str, LeafMaterial]:
    """Seed-driven material draw per leaf from the declared catalogue."""

    rng = random.Random(canonical_sha256({"materials": DESIGN_LANGUAGE_VERSION, "seed": seed}))
    return {leaf_id: rng.choice(list(catalogue)) for leaf_id in sorted(leaf_ids)}


# --------------------------------------------------------------------------
# Planning
# --------------------------------------------------------------------------

def composition_config_sha256(decomposition: DecompositionConfig, layout_config: LayoutConfig,
                              composition: CompositionConfig,
                              catalogue: Sequence[LeafMaterial]) -> str:
    return canonical_sha256({
        "design_language_version": DESIGN_LANGUAGE_VERSION,
        "decomposition": {"version": DECOMPOSITION_VERSION, **asdict(decomposition)},
        "layout": {"version": LAYOUT_VERSION, **asdict(layout_config)},
        "leaf_grammar_version": LEAF_GRAMMAR_VERSION,
        "composition": asdict(composition),
        "materials": [asdict(m) for m in catalogue],
    })


def plan_vehicle(seed: int, catalogue: Sequence[LeafMaterial],
                 decomposition: DecompositionConfig = DEFAULT_CONFIG,
                 layout_config: LayoutConfig = DEFAULT_LAYOUT_CONFIG,
                 composition: CompositionConfig = DEFAULT_COMPOSITION_CONFIG) -> VehiclePlan:
    """Decompose and lay out seed; on layout failure continue the declared search."""

    rejected: list[str] = []
    start = 0
    for _ in range(composition.max_plan_attempts):
        tree = decompose(seed, decomposition, start_attempt=start)
        try:
            result = layout(tree, layout_config)
        except LayoutFailure as exc:
            rejected.append(f"decomposition attempt {tree.attempt}: {exc}")
            start = tree.attempt + 1
            continue
        problems = layout_problems(result, tree)
        if problems:
            raise CompositionFailure(f"seed {seed}: layout re-check failed: {problems[:5]}")
        leaf_ids = [leaf.id for leaf in result.leaves]
        return VehiclePlan(seed=seed, tree=tree, layout=result, rejected=tuple(rejected),
                           materials=assign_materials(seed, leaf_ids, catalogue))
    raise CompositionFailure(f"seed {seed}: {composition.max_plan_attempts} plan attempts failed; "
                             f"last: {rejected[-1] if rejected else 'none'}")


def mesh_path(leaf_id: str) -> str:
    return f"{MESH_DIR}/{leaf_id}.stl"


# --------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------

def build_part_tree(plan: VehiclePlan, measurements: Mapping[str, Mapping[str, Any]],
                    composition: CompositionConfig = DEFAULT_COMPOSITION_CONFIG) -> PartTree:
    """Part tree from the plan and per-leaf mesh measurements (mass, centre of mass)."""

    placed = plan.layout.leaf_map()
    nodes: list[PartNode | AssemblyNode] = []
    for node in plan.tree.nodes:
        if node.children:
            nodes.append(AssemblyNode(id=node.id, children=tuple(node.children),
                                      functions=tuple(node.functions)))
            continue
        measured = measurements[node.id]
        material = plan.materials[node.id]
        nodes.append(PartNode(
            id=node.id, mesh=mesh_path(node.id), material_id=material.material_id,
            density_kg_m3=material.density_kg_m3, mass_kg=float(measured["mass_kg"]),
            center_of_mass_m=tuple(float(v) for v in measured["center_of_mass_m"]),
            grammar_version=LEAF_GRAMMAR_VERSION, program=placed[node.id].program))
    interfaces = tuple(Interface(id=item.id, a=item.a, b=item.b, kind=item.kind)
                       for item in plan.layout.interfaces)
    tree = PartTree(root=plan.tree.root, nodes=tuple(nodes), interfaces=interfaces,
                    contact_tolerance_m=composition.contact_tolerance_m)
    validate_part_tree(tree)
    return tree


def build_manifest(plan: VehiclePlan, measurements: Mapping[str, Mapping[str, Any]], config_sha256: str,
                   git_commit: str, composition: CompositionConfig = DEFAULT_COMPOSITION_CONFIG) -> dict:
    """The manifest with exactly the contract's top-level fields."""

    tree = build_part_tree(plan, measurements, composition)
    return {
        "design_language_version": DESIGN_LANGUAGE_VERSION,
        "seed": plan.seed,
        "config_sha256": config_sha256,
        "git_commit": git_commit,
        "length_unit": "m",
        "mass_unit": "kg",
        "contact_tolerance_m": composition.contact_tolerance_m,
        "root": tree.root,
        "nodes": to_manifest_nodes(tree),
        "interfaces": to_manifest_interfaces(tree),
    }


def manifest_bytes(manifest: Mapping[str, Any]) -> bytes:
    """Deterministic UTF-8 JSON (sorted keys, no NaN, trailing newline)."""

    text = json.dumps(manifest, sort_keys=True, indent=1, ensure_ascii=True, allow_nan=False)
    return (text + "\n").encode("utf-8")
