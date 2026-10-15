"""Hex-socket fasteners for the functional (goal v2) vehicle (pure Python).

After the Work 157 bores, a seed-chosen subset of the still unbored leaves
gets one axial regular-hexagon socket, cut as a ``hole`` loop of the extruded
profile (grammar ``func-leaf-socketed-v2``: ``section(outer + hole) ->
extrude -> transforms``). A new pin leaf, a plain v1 hexagonal extrusion, sits
in the socket with a declared clearance; the holed leaf and the pin are joined
by a ``threaded`` interface whose axis is the socket axis.

Local frame of the holed leaf (metres, radians): extrusion along +z from
``z = 0`` to ``z = h``, ``rho`` is the declared inscribed radius minus the
tessellation tolerance. The socket has apothem ``a``, phase ``phi``, centre
``(ox, oy)`` and circumradius ``R = a / cos(pi/6)``; the rule
``|(ox, oy)| + R <= (1 - wall) rho`` keeps it inside the inscribed circle. The
pin has the same phase, apothem ``a - c`` and height ``h - 2c`` and is
translated by ``(ox, oy, c)`` before the holed leaf's placement, so each flat
pin face is parallel to a socket face at distance ``c`` (the clearance). Flat
faces tessellate exactly, so the measured contact gap is ``c`` and nothing
interpenetrates. Each socket opening keeps clear of the contact patches its
cap receives (Work 157 ``contact_patches``).

Threads are represented as a pin through a hole only: no helix, no preload,
no load-path claim. Nothing here is physical validation.
"""

from __future__ import annotations

import copy
import hashlib
import math
import random
from dataclasses import asdict, dataclass, replace
from typing import Any, Mapping, Sequence

import numpy as np

from .composition import LeafMaterial, VehiclePlan
from .decomposition import AbstractNode, Attachment
from .layout import LayoutResult, PlacedLeaf, PlannedInterface
from .leaf_geometry import (
    LEAF_GRAMMAR_VERSION,
    LINEAR_TOLERANCE_FRACTION,
    ANGULAR_TOLERANCE_RAD,
    SOLID_GRAMMAR_VERSION,
    WIRE_GRAMMAR_VERSION,
    LeafProgramError,
    transform_points,
    validate_leaf_program,
)
from .leaf_refinement import contact_patches, validate_refined_program


SOCKETED_LEAF_GRAMMAR_VERSION = "func-leaf-socketed-v2"
FASTENER_VERSION = "func-fastener-v1"
SOCKET_LOOP_ID = "socket"
PIN_SUFFIX = ".pin"
THREAD_SUFFIX = ".thread"
_COS30 = math.cos(math.pi / 6)


@dataclass(frozen=True)
class FastenerConfig:
    socket_probability: float = 1.0
    apothem_fraction: tuple[float, float] = (0.15, 0.35)
    min_apothem_m: float = 5e-4
    wall_fraction: float = 0.12
    clearance_m: float = 2.5e-5
    draws: int = 24


DEFAULT_FASTENER_CONFIG = FastenerConfig()


@dataclass(frozen=True)
class FastenerResult:
    plan: VehiclePlan
    #: interface id -> (world axis point, world unit axis direction)
    axes: dict[str, tuple[tuple[float, float, float], tuple[float, float, float]]]


def fastener_config_record(config: FastenerConfig = DEFAULT_FASTENER_CONFIG) -> dict[str, Any]:
    return {"version": FASTENER_VERSION, "grammar_version": SOCKETED_LEAF_GRAMMAR_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


def _derived_seed(*parts: object) -> int:
    text = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


def hexagon(center: Sequence[float], apothem_m: float, phase_rad: float) -> list[list[float]]:
    """Counter-clockwise regular hexagon vertices (no closing repeat)."""

    radius = apothem_m / _COS30
    return [[float(center[0]) + radius * math.cos(phase_rad + k * math.pi / 3),
             float(center[1]) + radius * math.sin(phase_rad + k * math.pi / 3)] for k in range(6)]


# --------------------------------------------------------------------------
# Programs
# --------------------------------------------------------------------------

def socket_program(program: Mapping[str, Any], apothem_m: float, phase_rad: float,
                   center_m: tuple[float, float]) -> dict[str, Any]:
    """A copy of a placed v1 program with one axial hexagon socket hole loop."""

    validate_leaf_program(program)
    result = copy.deepcopy(dict(program))
    points = hexagon(center_m, apothem_m, phase_rad)
    result["profile"]["loops"].append({"loop_id": SOCKET_LOOP_ID, "role": "hole", "segments": [{
        "segment_id": "s0", "operator": "polyline", "parameters": {"points_m": points + [list(points[0])]},
        "trim_fraction": [0.0, 1.0]}]})
    result["profile"]["constraints"] = [{"kind": "hole_count", "value": 1}]
    result["socket"] = {"apothem_m": float(apothem_m), "phase_rad": float(phase_rad),
                        "center_m": [float(center_m[0]), float(center_m[1])]}
    result["leaf_grammar_version"] = SOCKETED_LEAF_GRAMMAR_VERSION
    validate_v2_program(result)
    return result


def socket_base_program(program: Mapping[str, Any]) -> dict[str, Any]:
    """The v1 program a socketed program was derived from."""

    if program["leaf_grammar_version"] != SOCKETED_LEAF_GRAMMAR_VERSION:
        raise LeafProgramError("not a socketed program")
    result = copy.deepcopy(dict(program))
    loops = result["profile"]["loops"]
    if len(loops) != 2 or loops[1]["loop_id"] != SOCKET_LOOP_ID or loops[1]["role"] != "hole":
        raise LeafProgramError("socketed program must have the socket as its second loop")
    loops.pop(1)
    result["profile"]["constraints"] = [{"kind": "hole_count", "value": 0}]
    result.pop("socket", None)
    result["leaf_grammar_version"] = LEAF_GRAMMAR_VERSION
    return result


def validate_v2_program(program: Mapping[str, Any]) -> None:
    """Check a v1, bored (Work 157) or socketed leaf program."""

    if program.get("leaf_grammar_version") != SOCKETED_LEAF_GRAMMAR_VERSION:
        validate_refined_program(program)
        return
    validate_leaf_program(socket_base_program(program))
    socket = program["socket"]
    if set(socket) != {"apothem_m", "phase_rad", "center_m"} or len(socket["center_m"]) != 2:
        raise LeafProgramError("socket fields mismatch")
    apothem, phase = float(socket["apothem_m"]), float(socket["phase_rad"])
    center = [float(v) for v in socket["center_m"]]
    if not all(math.isfinite(v) for v in (apothem, phase, *center)) or apothem <= 0:
        raise LeafProgramError("socket parameters must be finite with a positive apothem")
    points = hexagon(center, apothem, phase)
    segment = program["profile"]["loops"][1]["segments"]
    if (len(segment) != 1 or segment[0]["operator"] != "polyline" or segment[0]["trim_fraction"] != [0.0, 1.0]
            or segment[0]["parameters"] != {"points_m": points + [list(points[0])]}):
        raise LeafProgramError("socket loop does not match its declared hexagon")
    rho = program["contact"]["inscribed_radius_m"] - program["tessellation"]["linear_tolerance_m"]
    if not math.hypot(*center) + apothem / _COS30 < rho:
        raise LeafProgramError("socket does not stay inside the inscribed circle")


def pin_program(holed: Mapping[str, Any], clearance_m: float, leaf_id: str) -> dict[str, Any]:
    """A v1 hexagonal extrusion seated in the socket of a socketed program."""

    socket = holed["socket"]
    apothem = float(socket["apothem_m"]) - clearance_m
    height = holed["contact"]["height_m"] - 2.0 * clearance_m
    if apothem <= 0 or height <= 0:
        raise LeafProgramError("clearance leaves no pin")
    points = hexagon((0.0, 0.0), apothem, float(socket["phase_rad"]))
    length = 2.0 * max(apothem / _COS30, 0.5 * height)
    profile = {
        "profile_id": f"{leaf_id}-profile".lower(),
        "family": "regular_hexagon",
        "loops": [{"loop_id": "outer", "role": "outer", "segments": [{
            "segment_id": "s0", "operator": "polyline", "parameters": {"points_m": points + [list(points[0])]},
            "trim_fraction": [0.0, 1.0]}]}],
        "transforms": [],
        "offset": {"distance_m": 0.0, "kind": "arc"},
        "constraints": [{"kind": "hole_count", "value": 0}],
    }
    shift = {"translation_m": [float(socket["center_m"][0]), float(socket["center_m"][1]), float(clearance_m)],
             "axis_start_m": [0.0, 0.0, 0.0], "axis_end_m": [0.0, 0.0, 1.0], "angle_rad": 0.0}
    steps = [shift] + [f["parameters"] for f in holed["candidate"]["features"] if f["operator"] == "transform"]
    features: list[dict[str, Any]] = [
        {"feature_id": "sec", "operator": "section", "inputs": [], "parameters": {
            "profile_id": profile["profile_id"], "scale": 1.0,
            "translation_m": [0.0, 0.0, 0.0], "rotation_rad": 0.0}},
        {"feature_id": "body", "operator": "extrude", "inputs": ["sec"], "parameters": {
            "vector_m": [0.0, 0.0, height], "taper_rad": 0.0}},
    ]
    previous = "body"
    for index, step in enumerate(steps):
        feature_id = f"place{index}"
        features.append({"feature_id": feature_id, "operator": "transform", "inputs": [previous],
                         "parameters": copy.deepcopy(dict(step))})
        previous = feature_id
    program = {
        "leaf_grammar_version": LEAF_GRAMMAR_VERSION,
        "wire_grammar_version": WIRE_GRAMMAR_VERSION,
        "solid_grammar_version": SOLID_GRAMMAR_VERSION,
        "units": "SI_m_rad",
        "characteristic_length_m": length,
        "contact": {"height_m": height, "inscribed_radius_m": apothem, "outer_radius_m": apothem / _COS30},
        "profile": profile,
        "candidate": {
            "candidate_id": f"{leaf_id}-solid".lower(), "family": "extruded_hexagon_pin",
            "expected_body_count": 1, "features": features, "final_feature_id": previous,
            "datums": [
                {"datum_id": "center", "kind": "bbox_center", "parameters": {}},
                {"datum_id": "long", "kind": "longest_bbox_axis", "parameters": {}},
                {"datum_id": "base", "kind": "extreme_plane", "parameters": {"axis": "z", "side": "min"}},
            ],
        },
        "tessellation": {"linear_tolerance_m": LINEAR_TOLERANCE_FRACTION * length,
                         "angular_tolerance_rad": ANGULAR_TOLERANCE_RAD},
    }
    validate_leaf_program(program)
    return program


def socket_axis(program: Mapping[str, Any]) -> tuple[np.ndarray, np.ndarray]:
    """World axis point (local mid plane) and unit axis direction of a socket."""

    cx, cy = program["socket"]["center_m"]
    height = program["contact"]["height_m"]
    world = transform_points(program, np.array([[cx, cy, 0.0], [cx, cy, 0.5 * height], [cx, cy, height]]))
    direction = world[2] - world[0]
    return world[1], direction / np.linalg.norm(direction)


def socket_exits(program: Mapping[str, Any]) -> dict[str, tuple[np.ndarray, float]]:
    """World opening centre and circumradius per cap of a socketed program."""

    cx, cy = program["socket"]["center_m"]
    height = program["contact"]["height_m"]
    world = transform_points(program, np.array([[cx, cy, 0.0], [cx, cy, height]]))
    radius = float(program["socket"]["apothem_m"]) / _COS30
    return {"cap0": (world[0], radius), "cap1": (world[1], radius)}


def _clear_of_patches(program: Mapping[str, Any], patches: Mapping[str, list[tuple[np.ndarray, float]]]) -> bool:
    tol = program["tessellation"]["linear_tolerance_m"]
    exits = socket_exits(program)
    return all(float(np.linalg.norm(exits[cap][0] - center)) >= r + exits[cap][1] + tol
               for cap, items in patches.items() if cap in exits for center, r in items)


def _try_socket(program: Mapping[str, Any], patches: Mapping[str, list[tuple[np.ndarray, float]]],
                rng: random.Random, config: FastenerConfig) -> dict[str, Any] | None:
    rho = program["contact"]["inscribed_radius_m"] - program["tessellation"]["linear_tolerance_m"]
    if rho <= 0:
        return None
    limit = (1.0 - config.wall_fraction) * rho
    for _ in range(config.draws):
        apothem = rng.uniform(*config.apothem_fraction) * rho
        phase = rng.uniform(0.0, math.pi / 3)
        room = limit - apothem / _COS30
        if apothem < config.min_apothem_m or apothem <= 4.0 * config.clearance_m or room < 0:
            continue
        spread, angle = room * math.sqrt(rng.random()), rng.uniform(0.0, 2 * math.pi)
        candidate = socket_program(program, apothem, phase, (spread * math.cos(angle), spread * math.sin(angle)))
        if _clear_of_patches(candidate, patches):
            return candidate
    return None


# --------------------------------------------------------------------------
# Plan transformation
# --------------------------------------------------------------------------

def _placed(leaf_id: str, program: Mapping[str, Any], axis: int) -> PlacedLeaf:
    contact = program["contact"]
    points = np.asarray(program["profile"]["loops"][0]["segments"][0]["parameters"]["points_m"][:-1], dtype=float)
    prism = np.vstack([np.column_stack([points, np.zeros(len(points))]),
                       np.column_stack([points, np.full(len(points), contact["height_m"])])])
    world = transform_points(program, prism)
    return PlacedLeaf(id=leaf_id, program=dict(program), characteristic_length_m=program["characteristic_length_m"],
                      planned_length_m=program["characteristic_length_m"], axis=axis,
                      box_min_m=tuple(float(v) for v in world.min(axis=0)),
                      box_max_m=tuple(float(v) for v in world.max(axis=0)))


def add_fasteners(plan: VehiclePlan, catalogue: Sequence[LeafMaterial],
                  config: FastenerConfig = DEFAULT_FASTENER_CONFIG) -> FastenerResult:
    """The plan with sockets, pin leaves and threaded interfaces; deterministic per leaf."""

    result: LayoutResult = plan.layout
    patches = contact_patches(result)
    nodes = {node.id: node for node in plan.tree.nodes}
    leaves: list[PlacedLeaf] = []
    pins: list[tuple[PlacedLeaf, str]] = []  # (pin, holed id)
    for leaf in result.leaves:
        rng = random.Random(_derived_seed(FASTENER_VERSION, result.seed, result.attempt, leaf.id))
        program = None
        if leaf.program["leaf_grammar_version"] == LEAF_GRAMMAR_VERSION and rng.random() < config.socket_probability:
            program = _try_socket(leaf.program, patches[leaf.id], rng, config)
        if program is None:
            leaves.append(leaf)
            continue
        pin_id = leaf.id + PIN_SUFFIX
        if pin_id in nodes:
            raise LeafProgramError(f"pin id {pin_id} collides with an existing node")
        leaves.append(replace(leaf, program=program))
        pins.append((_placed(pin_id, pin_program(program, config.clearance_m, pin_id), leaf.axis), leaf.id))

    interfaces = list(result.interfaces)
    attachments = list(plan.tree.attachments)
    axes: dict[str, tuple[tuple[float, float, float], tuple[float, float, float]]] = {}
    added_children: dict[str, list[str]] = {}
    new_nodes: list[AbstractNode] = []
    materials = dict(plan.materials)
    holed_programs = {leaf.id: leaf.program for leaf in leaves}
    for pin, holed_id in pins:
        holed = nodes[holed_id]
        interface_id = pin.id + THREAD_SUFFIX
        interfaces.append(PlannedInterface(id=interface_id, assembly=holed.parent, a=holed_id, a_face=SOCKET_LOOP_ID,
                                           b=pin.id, b_face="body", kind="threaded", mode="socket"))
        attachments.append(Attachment(id=interface_id, assembly=holed.parent, source=pin.id, target=holed_id,
                                      kind="threaded"))
        point, direction = socket_axis(holed_programs[holed_id])
        axes[interface_id] = (tuple(float(v) for v in point), tuple(float(v) for v in direction))
        added_children.setdefault(holed.parent, []).append(pin.id)
        new_nodes.append(AbstractNode(id=pin.id, parent=holed.parent, depth=holed.depth, children=(),
                                      functions=(), anchor_child=None,
                                      characteristic_length_m=pin.characteristic_length_m))
        rng = random.Random(_derived_seed(FASTENER_VERSION, "material", result.seed, pin.id))
        materials[pin.id] = rng.choice(list(catalogue))

    tree_nodes = []
    for node in plan.tree.nodes:
        if node.id in added_children:
            node = replace(node, children=tuple(node.children) + tuple(added_children[node.id]))
        tree_nodes.append(node)
    tree = replace(plan.tree, nodes=tuple(tree_nodes) + tuple(new_nodes), attachments=tuple(attachments))
    layout_result = replace(result, leaves=tuple(leaves) + tuple(pin for pin, _ in pins),
                            interfaces=tuple(interfaces))
    return FastenerResult(plan=replace(plan, tree=tree, layout=layout_result, materials=materials), axes=axes)


def fastener_problems(before: VehiclePlan, after: FastenerResult,
                      config: FastenerConfig = DEFAULT_FASTENER_CONFIG) -> list[str]:
    """Every violated fastener rule, recomputed from the programs."""

    problems: list[str] = []
    old = before.layout.leaf_map()
    new = after.plan.layout.leaf_map()
    patches = contact_patches(before.layout)
    if not set(old) <= set(new):
        return ["fastener step removed leaves"]
    if after.plan.layout.interfaces[:len(before.layout.interfaces)] != before.layout.interfaces:
        problems.append("fastener step changed the existing interfaces")
    threaded = [i for i in after.plan.layout.interfaces if i.kind == "threaded"]
    if set(after.axes) != {i.id for i in threaded}:
        problems.append("threaded interfaces and declared axes differ")
    for leaf_id, leaf in new.items():
        try:
            validate_v2_program(leaf.program)
        except LeafProgramError as exc:
            problems.append(f"{leaf_id}: {exc}")
            continue
        if leaf_id in old and leaf.program != old[leaf_id].program:
            if leaf.program["leaf_grammar_version"] != SOCKETED_LEAF_GRAMMAR_VERSION \
                    or socket_base_program(leaf.program) != old[leaf_id].program:
                problems.append(f"{leaf_id}: socketed program is not derived from the placed program")
            elif not _clear_of_patches(leaf.program, patches[leaf_id]):
                problems.append(f"{leaf_id}: socket opening overlaps a contact patch")
    for item in threaded:
        holed, pin = new.get(item.a), new.get(item.b)
        if holed is None or pin is None or holed.program["leaf_grammar_version"] != SOCKETED_LEAF_GRAMMAR_VERSION:
            problems.append(f"{item.id}: threaded joint is not socket-to-pin")
            continue
        if pin.program != pin_program(holed.program, config.clearance_m, pin.id):
            problems.append(f"{item.id}: pin does not match its socket")
        point, direction = socket_axis(holed.program)
        declared = after.axes.get(item.id)
        if declared is None or not (np.allclose(declared[0], point, rtol=0, atol=1e-12)
                                    and np.allclose(declared[1], direction, rtol=0, atol=1e-12)):
            problems.append(f"{item.id}: declared axis differs from the socket axis")
    return problems
