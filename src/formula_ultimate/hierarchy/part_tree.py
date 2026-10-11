"""Representation model for hierarchical vehicle parts, not physical validation."""

from __future__ import annotations

import hashlib
import json
import math
import os
from dataclasses import dataclass
from pathlib import PurePosixPath, PureWindowsPath
from numbers import Real


JOINT_KINDS = (
    "threaded",
    "welded",
    "bonded",
    "interference",
    "integral",
)
MAX_CONTACT_TOLERANCE_M = 5e-4
MAX_INTERFERENCE_M = 1e-4


class PartTreeViolation(ValueError):
    """Raised when a part tree violates its structural data contract."""


def canonical_sha256(value) -> str:
    """Return the SHA-256 digest of the canonical JSON representation of value."""

    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
        allow_nan=False,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


@dataclass(frozen=True)
class PartNode:
    id: str
    mesh: str
    material_id: str
    density_kg_m3: float
    mass_kg: float
    center_of_mass_m: tuple[float, float, float]
    grammar_version: str
    program: dict

    @property
    def program_sha256(self) -> str:
        return canonical_sha256(self.program)

    @property
    def kind(self) -> str:
        return "part"


@dataclass(frozen=True)
class AssemblyNode:
    id: str
    children: tuple[str, ...]
    functions: tuple[str, ...]

    @property
    def kind(self) -> str:
        return "assembly"


@dataclass(frozen=True)
class Interface:
    id: str
    a: str
    b: str
    kind: str
    interference_m: float | None = None


@dataclass(frozen=True)
class PartTree:
    root: str
    nodes: tuple[PartNode | AssemblyNode, ...]
    interfaces: tuple[Interface, ...]
    contact_tolerance_m: float

    def node_map(self) -> dict[str, PartNode | AssemblyNode]:
        return {node.id: node for node in self.nodes}


def _is_finite_real(value) -> bool:
    if isinstance(value, bool) or not isinstance(value, Real):
        return False
    try:
        return math.isfinite(float(value))
    except (OverflowError, TypeError, ValueError):
        return False


def _require_nonempty_string(value, description: str) -> None:
    if not isinstance(value, str) or not value:
        raise PartTreeViolation(f"{description} must be a non-empty string")


def _mesh_is_absolute(mesh: str) -> bool:
    return (
        os.path.isabs(mesh)
        or PurePosixPath(mesh).is_absolute()
        or PureWindowsPath(mesh).is_absolute()
    )


def _mesh_has_parent_segment(mesh: str) -> bool:
    return any(segment == ".." for segment in mesh.replace("\\", "/").split("/"))


def validate_part_tree(tree) -> None:
    """Validate all structural, numeric, path, program, and interface constraints."""

    if not isinstance(tree, PartTree):
        raise PartTreeViolation("tree must be a PartTree")

    _require_nonempty_string(tree.root, "tree root")
    try:
        nodes = tuple(tree.nodes)
    except TypeError as exc:
        raise PartTreeViolation("tree nodes must be iterable") from exc

    node_by_id: dict[str, PartNode | AssemblyNode] = {}
    for index, node in enumerate(nodes):
        if not isinstance(node, (PartNode, AssemblyNode)):
            raise PartTreeViolation(f"node {index} is not a PartNode or AssemblyNode")
        _require_nonempty_string(node.id, f"node {index} id")
        if node.id in node_by_id:
            raise PartTreeViolation(f"duplicate node id: {node.id!r}")
        node_by_id[node.id] = node

    root = node_by_id.get(tree.root)
    if root is None:
        raise PartTreeViolation(f"root id is missing: {tree.root!r}")
    if not isinstance(root, AssemblyNode):
        raise PartTreeViolation("root must refer to an AssemblyNode")

    parent_of: dict[str, str] = {}
    for node in nodes:
        if isinstance(node, PartNode):
            if not _is_finite_real(node.density_kg_m3) or node.density_kg_m3 <= 0:
                raise PartTreeViolation(
                    f"part {node.id!r} density_kg_m3 must be finite and > 0"
                )
            if not _is_finite_real(node.mass_kg) or node.mass_kg <= 0:
                raise PartTreeViolation(
                    f"part {node.id!r} mass_kg must be finite and > 0"
                )
            com = node.center_of_mass_m
            if (
                not isinstance(com, (tuple, list))
                or len(com) != 3
                or any(not _is_finite_real(component) for component in com)
            ):
                raise PartTreeViolation(
                    f"part {node.id!r} center_of_mass_m must contain 3 finite floats"
                )
            if not isinstance(node.mesh, str) or not node.mesh:
                raise PartTreeViolation(f"part {node.id!r} mesh must be non-empty")
            if _mesh_is_absolute(node.mesh):
                raise PartTreeViolation(f"part {node.id!r} mesh must be relative")
            if _mesh_has_parent_segment(node.mesh):
                raise PartTreeViolation(
                    f"part {node.id!r} mesh must not contain a '..' segment"
                )
            _require_nonempty_string(node.material_id, f"part {node.id!r} material_id")
            _require_nonempty_string(
                node.grammar_version, f"part {node.id!r} grammar_version"
            )
            if not isinstance(node.program, dict) or not node.program:
                raise PartTreeViolation(
                    f"part {node.id!r} program must be a non-empty dict"
                )
            try:
                canonical_sha256(node.program)
            except (TypeError, ValueError, OverflowError) as exc:
                raise PartTreeViolation(
                    f"part {node.id!r} program must be JSON-serializable with allow_nan=False"
                ) from exc
        else:
            try:
                children = tuple(node.children)
            except TypeError as exc:
                raise PartTreeViolation(
                    f"assembly {node.id!r} children must be iterable"
                ) from exc
            if not children:
                raise PartTreeViolation(f"assembly {node.id!r} must have children")
            seen_children: set[str] = set()
            for child_id in children:
                if not isinstance(child_id, str) or not child_id:
                    raise PartTreeViolation(
                        f"assembly {node.id!r} child id must be a non-empty string"
                    )
                if child_id in seen_children:
                    raise PartTreeViolation(
                        f"assembly {node.id!r} lists child {child_id!r} more than once"
                    )
                seen_children.add(child_id)
                if child_id not in node_by_id:
                    raise PartTreeViolation(
                        f"assembly {node.id!r} references unknown child {child_id!r}"
                    )
                previous_parent = parent_of.get(child_id)
                if previous_parent is not None:
                    raise PartTreeViolation(
                        f"node {child_id!r} has two parents: "
                        f"{previous_parent!r} and {node.id!r}"
                    )
                parent_of[child_id] = node.id

            try:
                functions = tuple(node.functions)
            except TypeError as exc:
                raise PartTreeViolation(
                    f"assembly {node.id!r} functions must be iterable"
                ) from exc
            seen_functions: set[str] = set()
            for function in functions:
                if not isinstance(function, str) or not function:
                    raise PartTreeViolation(
                        f"assembly {node.id!r} functions must be non-empty strings"
                    )
                if function in seen_functions:
                    raise PartTreeViolation(
                        f"assembly {node.id!r} has duplicate function {function!r}"
                    )
                seen_functions.add(function)

    if tree.root in parent_of:
        raise PartTreeViolation("root must not have a parent")

    reachable: set[str] = set()
    reach_stack = [tree.root]
    while reach_stack:
        node_id = reach_stack.pop()
        if node_id in reachable:
            continue
        reachable.add(node_id)
        node = node_by_id[node_id]
        if isinstance(node, AssemblyNode):
            reach_stack.extend(node.children)

    colours: dict[str, int] = {}
    for start_id in node_by_id:
        if colours.get(start_id, 0) == 2:
            continue
        stack: list[tuple[str, bool]] = [(start_id, False)]
        while stack:
            node_id, exiting = stack.pop()
            if exiting:
                colours[node_id] = 2
                continue
            state = colours.get(node_id, 0)
            if state == 1:
                raise PartTreeViolation(f"cycle detected at node {node_id!r}")
            if state == 2:
                continue
            colours[node_id] = 1
            stack.append((node_id, True))
            node = node_by_id[node_id]
            if isinstance(node, AssemblyNode):
                for child_id in reversed(tuple(node.children)):
                    child_state = colours.get(child_id, 0)
                    if child_state == 1:
                        raise PartTreeViolation(
                            f"cycle detected through child {child_id!r}"
                        )
                    if child_state == 0:
                        stack.append((child_id, False))

    unreachable = [node_id for node_id in node_by_id if node_id not in reachable]
    if unreachable:
        raise PartTreeViolation(
            "nodes unreachable from root: " + ", ".join(repr(node_id) for node_id in unreachable)
        )

    if not _is_finite_real(tree.contact_tolerance_m) or not (
        0 < tree.contact_tolerance_m <= MAX_CONTACT_TOLERANCE_M
    ):
        raise PartTreeViolation(
            "contact_tolerance_m must be finite and in (0, 5e-4] m"
        )

    try:
        interfaces = tuple(tree.interfaces)
    except TypeError as exc:
        raise PartTreeViolation("interfaces must be iterable") from exc
    interface_ids: set[str] = set()
    for interface in interfaces:
        if not isinstance(interface, Interface):
            raise PartTreeViolation("interfaces must contain Interface values")
        _require_nonempty_string(interface.id, "interface id")
        if interface.id in interface_ids:
            raise PartTreeViolation(f"duplicate interface id: {interface.id!r}")
        interface_ids.add(interface.id)
        if not isinstance(interface.a, str) or not isinstance(interface.b, str):
            raise PartTreeViolation(
                f"interface {interface.id!r} endpoints must be PartNode ids"
            )
        a_node = node_by_id.get(interface.a)
        b_node = node_by_id.get(interface.b)
        if not isinstance(a_node, PartNode) or not isinstance(b_node, PartNode):
            raise PartTreeViolation(
                f"interface {interface.id!r} endpoints must be PartNode ids"
            )
        if interface.a == interface.b:
            raise PartTreeViolation(
                f"interface {interface.id!r} endpoints must be different"
            )
        if interface.kind not in JOINT_KINDS:
            raise PartTreeViolation(
                f"interface {interface.id!r} has invalid joint kind {interface.kind!r}"
            )
        if interface.kind != "interference" and interface.interference_m is not None:
            raise PartTreeViolation(
                f"interface {interface.id!r} may set interference_m only for interference joints"
            )
        if interface.interference_m is not None and (
            not _is_finite_real(interface.interference_m)
            or not (0 < interface.interference_m <= MAX_INTERFERENCE_M)
        ):
            raise PartTreeViolation(
                f"interface {interface.id!r} interference_m must be finite and in (0, 1e-4] m"
            )


def roll_up(
    tree: PartTree,
) -> dict[str, tuple[float, tuple[float, float, float]]]:
    """Return mass and mass-weighted centre of mass for every tree node."""

    validate_part_tree(tree)
    node_by_id = tree.node_map()
    rolled: dict[str, tuple[float, tuple[float, float, float]]] = {}
    stack: list[tuple[str, bool]] = [(tree.root, False)]
    while stack:
        node_id, expanded = stack.pop()
        node = node_by_id[node_id]
        if isinstance(node, PartNode):
            rolled[node_id] = (
                float(node.mass_kg),
                tuple(float(value) for value in node.center_of_mass_m),
            )
            continue
        if not expanded:
            stack.append((node_id, True))
            for child_id in reversed(node.children):
                stack.append((child_id, False))
            continue
        mass_kg = 0.0
        moment = [0.0, 0.0, 0.0]
        for child_id in node.children:
            child_mass, child_com = rolled[child_id]
            mass_kg += child_mass
            for axis in range(3):
                moment[axis] += child_com[axis] * child_mass
        rolled[node_id] = (
            mass_kg,
            (
                moment[0] / mass_kg,
                moment[1] / mass_kg,
                moment[2] / mass_kg,
            ),
        )
    return rolled


def _validated_node_map(tree: PartTree) -> dict[str, PartNode | AssemblyNode]:
    validate_part_tree(tree)
    return tree.node_map()


def levels(tree: PartTree) -> int:
    """Return the maximum root depth plus one."""

    node_by_id = _validated_node_map(tree)
    maximum_depth = 0
    stack: list[tuple[str, int]] = [(tree.root, 0)]
    while stack:
        node_id, depth = stack.pop()
        maximum_depth = max(maximum_depth, depth)
        node = node_by_id[node_id]
        if isinstance(node, AssemblyNode):
            stack.extend((child_id, depth + 1) for child_id in node.children)
    return maximum_depth + 1


def leaf_ids(tree: PartTree) -> tuple[str, ...]:
    """Return part ids in deterministic depth-first pre-order."""

    node_by_id = _validated_node_map(tree)
    leaves: list[str] = []
    stack = [tree.root]
    while stack:
        node_id = stack.pop()
        node = node_by_id[node_id]
        if isinstance(node, PartNode):
            leaves.append(node_id)
        else:
            stack.extend(reversed(node.children))
    return tuple(leaves)


def _require_node(tree: PartTree, node_id: str) -> tuple[dict[str, PartNode | AssemblyNode], PartNode | AssemblyNode]:
    node_by_id = _validated_node_map(tree)
    if node_id not in node_by_id:
        raise PartTreeViolation(f"unknown node id: {node_id!r}")
    return node_by_id, node_by_id[node_id]


def subtree_height(tree: PartTree, node_id: str) -> int:
    """Return the number of edges in the longest path below node_id."""

    node_by_id, node = _require_node(tree, node_id)
    if isinstance(node, PartNode):
        return 0
    heights: dict[str, int] = {}
    stack: list[tuple[str, bool]] = [(node_id, False)]
    while stack:
        current_id, expanded = stack.pop()
        current = node_by_id[current_id]
        if isinstance(current, PartNode):
            heights[current_id] = 0
        elif not expanded:
            stack.append((current_id, True))
            stack.extend((child_id, False) for child_id in reversed(current.children))
        else:
            heights[current_id] = 1 + max(heights[child_id] for child_id in current.children)
    return heights[node_id]


def subtree_leaves(tree: PartTree, node_id: str) -> frozenset[str]:
    """Return the set of part ids below node_id."""

    node_by_id, _ = _require_node(tree, node_id)
    leaves: set[str] = set()
    stack = [node_id]
    while stack:
        current_id = stack.pop()
        current = node_by_id[current_id]
        if isinstance(current, PartNode):
            leaves.add(current_id)
        else:
            stack.extend(current.children)
    return frozenset(leaves)


def topology_signature(tree: PartTree, node_id: str) -> str:
    """Return the order-independent canonical topology/function signature."""

    node_by_id, _ = _require_node(tree, node_id)
    signatures: dict[str, str] = {}
    stack: list[tuple[str, bool]] = [(node_id, False)]
    while stack:
        current_id, expanded = stack.pop()
        node = node_by_id[current_id]
        if isinstance(node, PartNode):
            signatures[current_id] = "L"
        elif not expanded:
            stack.append((current_id, True))
            stack.extend((child_id, False) for child_id in reversed(node.children))
        else:
            child_signature = "".join(
                sorted(signatures[child_id] for child_id in node.children)
            )
            signatures[current_id] = (
                "(" + ",".join(sorted(node.functions)) + ":" + child_signature + ")"
            )
    return signatures[node_id]


def _preorder_ids(tree: PartTree) -> list[str]:
    node_by_id = tree.node_map()
    ordered: list[str] = []
    stack = [tree.root]
    while stack:
        node_id = stack.pop()
        ordered.append(node_id)
        node = node_by_id[node_id]
        if isinstance(node, AssemblyNode):
            stack.extend(reversed(node.children))
    return ordered


def to_manifest_nodes(tree: PartTree) -> list[dict]:
    """Serialize nodes in root-first depth-first order with rolled-up values."""

    validate_part_tree(tree)
    node_by_id = tree.node_map()
    rolled = roll_up(tree)
    manifest: list[dict] = []
    for node_id in _preorder_ids(tree):
        node = node_by_id[node_id]
        mass_kg, center_of_mass_m = rolled[node_id]
        center = [float(value) for value in center_of_mass_m]
        if isinstance(node, AssemblyNode):
            manifest.append(
                {
                    "id": node.id,
                    "kind": "assembly",
                    "children": list(node.children),
                    "functions": list(node.functions),
                    "mass_kg": float(mass_kg),
                    "center_of_mass_m": center,
                }
            )
        else:
            manifest.append(
                {
                    "id": node.id,
                    "kind": "part",
                    "mesh": node.mesh,
                    "material_id": node.material_id,
                    "density_kg_m3": float(node.density_kg_m3),
                    "mass_kg": float(mass_kg),
                    "center_of_mass_m": center,
                    "generator": {
                        "grammar_version": node.grammar_version,
                        "program": node.program,
                        "program_sha256": node.program_sha256,
                    },
                }
            )
    return manifest


def to_manifest_interfaces(tree: PartTree) -> list[dict]:
    """Serialize interfaces in their declared order."""

    validate_part_tree(tree)
    manifest: list[dict] = []
    for interface in tree.interfaces:
        item = {
            "id": interface.id,
            "a": interface.a,
            "b": interface.b,
            "kind": interface.kind,
        }
        if interface.interference_m is not None:
            item["interference_m"] = interface.interference_m
        manifest.append(item)
    return manifest
