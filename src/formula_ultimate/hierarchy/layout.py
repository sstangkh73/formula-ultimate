"""Seed-driven placement of hierarchy leaves with measurable flat contact.

Every leaf is a Work 151 extruded program. Leaves are placed with their
extrusion axis on a vehicle axis (x, y or z), so each leaf has an axis-aligned
box: exact for polyline profiles (the transformed prism vertices) and
conservative for B-spline profiles (``outer_radius_m`` across the axis).

Contact faces of a placed leaf (``leaf_faces``):

- ``cap0`` / ``cap1``: the flat end caps (disks: the cap contains its
  ``inscribed_radius_m`` disk and lies inside its ``outer_radius_m`` disk);
- ``side<i>``: for a polyline profile, a convex-hull edge whose outward normal
  is a vehicle axis. Its extruded face is an exact planar rectangle that lies
  in the leaf's box face. The planner chooses the spin so one such face exists.

Procedure (declared, seed-driven, no part catalogue): the root's anchor leaf
is placed at the origin. ``grow(assembly)`` lays out the anchor child first,
then puts each satellite child's anchor leaf, cap first, on a free face of a
leaf already placed inside the same assembly (the anchor child or an earlier
satellite), and grows the satellite. The attachment target is chosen here and
replaces the Work 150 draw. Each satellite joins the already connected
children, so the children of every assembly stay connected. A fresh source
leaf keeps its random shape but its length may move from the planning target
so that its cap fits inside the target face ("inside") or its inscribed disk
holds the target face ("around").

Collision rule: leaf boxes are pairwise interior-disjoint (touching allowed).
Two touching leaves are separated by the shared box plane, so no solid
interpenetration is possible. Every rule is re-checked from the placed
programs alone by ``layout_problems``.

Lengths are metres and angles radians. This is a geometric representation,
not physical validation: nothing here says a joint carries load.
"""

from __future__ import annotations

import hashlib
import math
import random
from dataclasses import dataclass
from typing import Any, Mapping

import numpy as np

from .decomposition import AbstractTree
from .leaf_geometry import AXES, leaf_program, placement_transforms, transform_points, with_placement


LAYOUT_VERSION = "hier-layout-v1"
BOX_EPS_M = 1e-9
AXIS_ALIGNED = 1.0 - 1e-9


class LayoutFailure(RuntimeError):
    """Raised when a leaf cannot be placed under the declared rules."""


@dataclass(frozen=True)
class LayoutConfig:
    min_leaf_length_m: float = 0.004
    offset_fractions: tuple[float, ...] = (0.0, 0.5, 0.999)
    offset_directions: int = 8
    inside_fractions: tuple[float, ...] = (0.9, 0.5, 0.25)
    around_factors: tuple[float, ...] = (1.1, 2.0)
    max_growth: float = 4.0
    fit_margin: float = 0.999
    reserve_factor: float = 1.0
    max_attempts: int = 16


DEFAULT_LAYOUT_CONFIG = LayoutConfig()


@dataclass(frozen=True)
class PlacedLeaf:
    id: str
    program: dict[str, Any]
    characteristic_length_m: float
    planned_length_m: float
    axis: int
    box_min_m: tuple[float, float, float]
    box_max_m: tuple[float, float, float]


@dataclass(frozen=True)
class PlannedInterface:
    id: str
    assembly: str
    a: str
    a_face: str
    b: str
    b_face: str
    kind: str
    mode: str


@dataclass(frozen=True)
class LayoutResult:
    version: str
    seed: int
    attempt: int
    leaves: tuple[PlacedLeaf, ...]
    interfaces: tuple[PlannedInterface, ...]

    def leaf_map(self) -> dict[str, PlacedLeaf]:
        return {leaf.id: leaf for leaf in self.leaves}


def _derived_seed(*parts: object) -> int:
    text = "|".join(str(p) for p in parts)
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest()[:16], 16)


# --------------------------------------------------------------------------
# Faces and boxes of a placed program
# --------------------------------------------------------------------------

def _profile_points(program: Mapping[str, Any]) -> np.ndarray | None:
    """Polyline profile vertices (without the closing repeat), else None."""

    segment = program["profile"]["loops"][0]["segments"][0]
    if segment["operator"] != "polyline":
        return None
    return np.asarray(segment["parameters"]["points_m"][:-1], dtype=float)


def _hull_edges(points: np.ndarray) -> list[tuple[int, np.ndarray]]:
    """Edges (index, outward unit normal) with every vertex on their inner side."""

    edges = []
    scale = float(np.abs(points).max())
    count = len(points)
    for i in range(count):
        a, b = points[i], points[(i + 1) % count]
        d = b - a
        normal = np.array([d[1], -d[0]]) / math.hypot(d[0], d[1])  # counter-clockwise loop
        if np.all(points @ normal <= a @ normal + 1e-12 * scale):
            edges.append((i, normal))
    return edges


def leaf_faces(program: Mapping[str, Any]) -> dict[str, Any]:
    """Axis, box and flat contact faces of a placed program (pure geometry)."""

    contact = program["contact"]
    height, outer, inscribed = contact["height_m"], contact["outer_radius_m"], contact["inscribed_radius_m"]
    tol = program["tessellation"]["linear_tolerance_m"]
    ends = transform_points(program, np.array([[0.0, 0.0, 0.0], [0.0, 0.0, height]]))
    direction = ends[1] - ends[0]
    axis = int(np.argmax(np.abs(direction)))
    aligned = abs(direction[axis]) >= AXIS_ALIGNED * height
    points = _profile_points(program)
    if points is not None:
        prism = np.vstack([np.column_stack([points, np.zeros(len(points))]),
                           np.column_stack([points, np.full(len(points), height)])])
        world = transform_points(program, prism)
        lo, hi = world.min(axis=0), world.max(axis=0)
    else:
        lo = np.minimum(ends[0], ends[1]) - outer
        hi = np.maximum(ends[0], ends[1]) + outer
        lo[axis], hi[axis] = min(ends[0][axis], ends[1][axis]), max(ends[0][axis], ends[1][axis])
    sign0 = -1 if direction[axis] > 0 else 1  # outward normal sign of cap0
    faces: dict[str, dict[str, Any]] = {}
    for name, end, sign in (("cap0", ends[0], sign0), ("cap1", ends[1], -sign0)):
        faces[name] = {"kind": "disk", "axis": axis, "sign": sign, "plane": float(end[axis]),
                       "center": end, "outer": outer, "inscribed": inscribed - tol}
    if points is not None:
        count = len(points)
        for i, normal in _hull_edges(points):
            mid = transform_points(program, np.array([[*points[i], 0.0], [*(points[i] + normal), 0.0]]))
            world_normal = mid[1] - mid[0]
            k = int(np.argmax(np.abs(world_normal)))
            if abs(world_normal[k]) < AXIS_ALIGNED:
                continue
            j = (i + 1) % count
            corners = transform_points(program, np.array([
                [*points[i], 0.0], [*points[j], 0.0], [*points[j], height], [*points[i], height]]))
            sign = 1 if world_normal[k] > 0 else -1
            faces[f"side{i}"] = {"kind": "rect", "axis": k, "sign": sign,
                                 "plane": float(hi[k] if sign > 0 else lo[k]),
                                 "center": corners.mean(axis=0), "corners": corners}
    return {"axis": axis, "aligned": aligned, "lo": lo, "hi": hi, "faces": faces}


def _region_holds_disk(face: Mapping[str, Any], center: np.ndarray, radius: float) -> bool:
    k = face["axis"]
    if face["kind"] == "disk":
        offset = float(np.linalg.norm(np.delete(center - face["center"], k)))
        return offset + radius <= face["inscribed"]
    corners = face["corners"]
    lo, hi = corners.min(axis=0), corners.max(axis=0)
    return all(lo[m] + radius <= center[m] <= hi[m] - radius for m in range(3) if m != k)


def _disk_holds_region(center: np.ndarray, radius: float, face: Mapping[str, Any]) -> bool:
    k = face["axis"]
    if face["kind"] == "disk":
        offset = float(np.linalg.norm(np.delete(center - face["center"], k)))
        return offset + face["outer"] <= radius
    return all(float(np.linalg.norm(np.delete(c - center, k))) <= radius for c in face["corners"])


# --------------------------------------------------------------------------
# Planner
# --------------------------------------------------------------------------

class _Planner:
    def __init__(self, tree: AbstractTree, config: LayoutConfig, attempt: int) -> None:
        self.tree = tree
        self.config = config
        self.nodes = tree.node_map()
        self.rng = random.Random(_derived_seed(LAYOUT_VERSION, tree.seed, tree.attempt, "layout", attempt))
        self.placed: dict[str, PlacedLeaf] = {}
        self.geometry: dict[str, dict[str, Any]] = {}
        self.order: list[str] = []
        self.lo = np.zeros((0, 3))
        self.hi = np.zeros((0, 3))
        self.interfaces: list[PlannedInterface] = []
        self.kind_of = {(a.assembly, a.source): (a.id, a.kind) for a in tree.attachments}

    # -- tree helpers -----------------------------------------------------
    def anchor_leaf(self, node_id: str) -> str:
        while self.nodes[node_id].children:
            node_id = self.nodes[node_id].anchor_child
        return node_id

    def subtree_leaves(self, node_id: str) -> list[str]:
        out, stack = [], [node_id]
        while stack:
            current = stack.pop()
            kids = self.nodes[current].children
            if kids:
                stack.extend(reversed(kids))
            else:
                out.append(current)
        return out

    # -- programs ---------------------------------------------------------
    def local_program(self, leaf_id: str, length: float) -> dict[str, Any]:
        # The per-leaf draw is independent of length, so a resized leaf keeps
        # its shape and only scales.
        rng = random.Random(_derived_seed(LAYOUT_VERSION, self.tree.seed, self.tree.attempt, leaf_id))
        return leaf_program(rng, length, leaf_id=leaf_id)

    def orientation(self, local: dict[str, Any], axis: int) -> tuple[bool, float]:
        """Random flip and a spin that puts one hull edge normal on a vehicle axis."""

        flip = self.rng.random() < 0.5
        points = _profile_points(local)
        if points is None:
            return flip, self.rng.uniform(0.0, 2 * math.pi)
        _, normal = self.rng.choice(_hull_edges(points))
        base = with_placement(local, placement_transforms(AXES[axis], flip, 0.0, [0.0, 0.0, 0.0]))
        rotation = transform_points(base, np.eye(3)).T  # columns: images of local x, y, z
        targets = [m for m in range(3) if m != axis]
        target = np.zeros(3)
        target[self.rng.choice(targets)] = self.rng.choice((1.0, -1.0))
        q = rotation.T @ target
        spin = math.atan2(q[1], q[0]) - math.atan2(normal[1], normal[0])
        return flip, spin % (2 * math.pi)

    def placed_program(self, local, axis, flip, spin, translation) -> dict[str, Any]:
        return with_placement(local, placement_transforms(AXES[axis], flip, spin, list(translation)))

    def commit(self, leaf_id: str, program: dict[str, Any], planned: float) -> None:
        geometry = leaf_faces(program)
        self.placed[leaf_id] = PlacedLeaf(
            id=leaf_id, program=program, characteristic_length_m=program["characteristic_length_m"],
            planned_length_m=planned, axis=geometry["axis"],
            box_min_m=tuple(float(v) for v in geometry["lo"]),
            box_max_m=tuple(float(v) for v in geometry["hi"]))
        self.geometry[leaf_id] = geometry
        self.order.append(leaf_id)
        self.lo = np.vstack([self.lo, geometry["lo"]])
        self.hi = np.vstack([self.hi, geometry["hi"]])

    def free(self, lo: np.ndarray, hi: np.ndarray) -> np.ndarray:
        """For candidate boxes (k, 3), True where no placed box overlaps the interior."""

        if not len(self.lo):
            return np.ones(len(lo), dtype=bool)
        overlap = np.all((lo[:, None, :] < self.hi[None, :, :] - BOX_EPS_M)
                         & (self.lo[None, :, :] < hi[:, None, :] - BOX_EPS_M), axis=2)
        return ~overlap.any(axis=1)

    # -- placement --------------------------------------------------------
    def place_root(self, leaf_id: str) -> None:
        planned = self.nodes[leaf_id].characteristic_length_m
        local = self.local_program(leaf_id, planned)
        axis = self.rng.randrange(3)
        flip, spin = self.orientation(local, axis)
        self.commit(leaf_id, self.placed_program(local, axis, flip, spin, [0.0, 0.0, 0.0]), planned)

    def attach(self, assembly: str, source: str, targets: list[str], reserve_m: float) -> None:
        planned = self.nodes[source].characteristic_length_m
        unit = self.local_program(source, 1.0)
        sites = [(t, name) for t in targets for name in sorted(self.geometry[t]["faces"])]
        self.rng.shuffle(sites)
        phase = self.rng.uniform(0.0, 2 * math.pi)
        directions = [phase + 2 * math.pi * k / self.config.offset_directions
                      for k in range(self.config.offset_directions)]
        # First pass keeps room for the satellite's own subtree; second pass
        # only requires the leaf itself to be collision-free.
        for target, name, reserve in [(t, n, r) for r in (reserve_m, 0.0) for t, n in sites]:
            face = self.geometry[target]["faces"][name]
            for length in self._candidate_lengths(unit, planned, face):
                placed = self._try_face(self.local_program(source, length), face, directions, reserve)
                if placed is not None:
                    program, cap, mode = placed
                    self.commit(source, program, planned)
                    attachment_id, kind = self.kind_of[(assembly, source)]
                    self.interfaces.append(PlannedInterface(
                        id=attachment_id, assembly=assembly, a=source, a_face=cap, b=target, b_face=name,
                        kind=kind, mode=mode))
                    return
        raise LayoutFailure(f"seed {self.tree.seed}: no free face for {source} in {assembly}")

    def _candidate_lengths(self, unit: Mapping[str, Any], planned: float, face: Mapping[str, Any]) -> list[float]:
        """Source lengths whose cap fits inside, or around, the target face.

        The source is a fresh leaf with no contacts yet, so its length may
        move from the planning target. Candidates are ordered by closeness to
        the planned length.
        """

        outer_u = unit["contact"]["outer_radius_m"]
        inscribed_u = unit["contact"]["inscribed_radius_m"] - unit["tessellation"]["linear_tolerance_m"]
        margin = self.config.fit_margin
        k = face["axis"]
        if face["kind"] == "disk":
            hold, span = face["inscribed"], face["outer"]
        else:
            lo, hi = face["corners"].min(axis=0), face["corners"].max(axis=0)
            half = [(hi[m] - lo[m]) / 2 for m in range(3) if m != k]
            hold, span = min(half), math.hypot(*half)
        inside_max = margin * hold / outer_u
        around_min = span / (margin * inscribed_u)
        candidates = [planned] if (planned <= inside_max or planned >= around_min) else []
        candidates += [inside_max * f for f in self.config.inside_fractions]
        candidates += [around_min * f for f in self.config.around_factors]
        low, high = self.config.min_leaf_length_m, planned * self.config.max_growth
        return sorted({x for x in candidates if low <= x <= high}, key=lambda x: (abs(math.log(x / planned)), x))

    def _try_face(self, local: dict[str, Any], face: Mapping[str, Any], directions: list[float],
                  reserve_m: float = 0.0):
        k, sign, plane = face["axis"], face["sign"], face["plane"]
        flip, spin = self.orientation(local, k)
        frame = leaf_faces(self.placed_program(local, k, flip, spin, [0.0, 0.0, 0.0]))
        # The source cap that faces the target has the opposite outward sign.
        cap = next(n for n in ("cap0", "cap1") if frame["faces"][n]["sign"] == -sign)
        cap_face = frame["faces"][cap]
        outer_s, inscribed_s = cap_face["outer"], cap_face["inscribed"]
        u, v = [m for m in range(3) if m != k]
        base = np.array(face["center"], dtype=float)
        margin = self.config.fit_margin
        # Lateral slack from the face centre in which the fit rule holds.
        if face["kind"] == "disk":
            inside = margin * face["inscribed"] - outer_s
            around = margin * inscribed_s - face["outer"]
        else:
            lo, hi = face["corners"].min(axis=0), face["corners"].max(axis=0)
            inside = margin * min((hi[m] - lo[m]) / 2 for m in (u, v)) - outer_s
            around = margin * inscribed_s - math.hypot(*[(hi[m] - lo[m]) / 2 for m in (u, v)])
        if inside >= 0:
            mode, slack = "inside", inside
        elif around >= 0:
            mode, slack = "around", around
        else:
            return None
        centers = []
        for fraction in self.config.offset_fractions:
            for angle in (directions if fraction else directions[:1]):
                c = base.copy()
                c[u] += fraction * slack * math.cos(angle)
                c[v] += fraction * slack * math.sin(angle)
                centers.append(c)
        centers = np.array(centers)
        # Translate the zero-placed frame so the facing cap sits on the plane.
        shift = centers - cap_face["center"]
        shift[:, k] = plane - cap_face["center"][k]
        lo = frame["lo"] + shift
        hi = frame["hi"] + shift
        if reserve_m > 0:
            # Claim box: the leaf box grown to reserve_m beyond the plane and
            # to reserve_m across it, a soft room-keeping heuristic.
            lo, hi = lo.copy(), hi.copy()
            mid = (lo + hi) / 2
            for m in (u, v):
                lo[:, m] = np.minimum(lo[:, m], mid[:, m] - reserve_m / 2)
                hi[:, m] = np.maximum(hi[:, m], mid[:, m] + reserve_m / 2)
            if sign > 0:
                hi[:, k] = np.maximum(hi[:, k], plane + reserve_m)
            else:
                lo[:, k] = np.minimum(lo[:, k], plane - reserve_m)
        ok = np.nonzero(self.free(lo, hi))[0]
        for index in ok:
            program = self.placed_program(local, k, flip, spin, shift[index])
            placed = leaf_faces(program)
            if contact_problem(placed["faces"][cap], face) is None:
                return program, cap, mode
        return None

    def grow(self, node_id: str) -> None:
        """Lay out node_id's subtree; its anchor leaf is already placed."""

        node = self.nodes[node_id]
        if not node.children:
            return
        self.grow(node.anchor_child)
        for child in node.children:
            if child != node.anchor_child:
                targets = [leaf for leaf in self.subtree_leaves(node_id) if leaf in self.placed]
                reserve = (self.config.reserve_factor * self.nodes[child].characteristic_length_m
                           if self.nodes[child].children else 0.0)
                self.attach(node_id, self.anchor_leaf(child), targets, reserve)
                self.grow(child)


def contact_problem(cap: Mapping[str, Any], face: Mapping[str, Any]) -> str | None:
    """Why a source cap and a target face do not make flat measurable contact."""

    if cap["axis"] != face["axis"] or cap["sign"] != -face["sign"]:
        return "faces are not opposed on one vehicle axis"
    if abs(cap["plane"] - face["plane"]) > BOX_EPS_M:
        return "faces are not coplanar"
    if face["kind"] == "rect" and np.ptp(face["corners"][:, face["axis"]]) > BOX_EPS_M:
        return "side face is not in the axis plane"
    if _region_holds_disk(face, cap["center"], cap["outer"]):
        return None
    if _disk_holds_region(cap["center"], cap["inscribed"], face):
        return None
    return "neither face lies inside the other"


def layout(tree: AbstractTree, config: LayoutConfig = DEFAULT_LAYOUT_CONFIG) -> LayoutResult:
    """Place every leaf of tree and plan one interface per Work 150 attachment."""

    failures = []
    for attempt in range(config.max_attempts):
        planner = _Planner(tree, config, attempt)
        try:
            planner.place_root(planner.anchor_leaf(tree.root))
            planner.grow(tree.root)
        except LayoutFailure as exc:
            failures.append(str(exc))
            continue
        missing = [n.id for n in tree.nodes if not n.children and n.id not in planner.placed]
        if missing:
            raise LayoutFailure(f"seed {tree.seed}: unplaced leaves {missing[:5]}")
        return LayoutResult(version=LAYOUT_VERSION, seed=tree.seed, attempt=attempt,
                            leaves=tuple(planner.placed[i] for i in planner.order),
                            interfaces=tuple(planner.interfaces))
    raise LayoutFailure(f"seed {tree.seed}: {config.max_attempts} layout attempts failed; last: {failures[-1]}")


# --------------------------------------------------------------------------
# Independent re-check from the placed programs
# --------------------------------------------------------------------------

def layout_problems(result: LayoutResult, tree: AbstractTree) -> list[str]:
    """Every violated layout rule, recomputed from the placed programs."""

    problems: list[str] = []
    nodes = tree.node_map()
    leaf_ids = sorted(n.id for n in tree.nodes if not n.children)
    geometry = {leaf.id: leaf_faces(leaf.program) for leaf in result.leaves}
    if sorted(geometry) != leaf_ids or len(result.leaves) != len(leaf_ids):
        problems.append("placed leaves do not match the tree leaves")
    for leaf_id, frame in geometry.items():
        if not frame["aligned"]:
            problems.append(f"{leaf_id}: extrusion axis is not a vehicle axis")
    ids = sorted(geometry)
    lo = np.array([geometry[i]["lo"] for i in ids]).reshape(-1, 3)
    hi = np.array([geometry[i]["hi"] for i in ids]).reshape(-1, 3)
    overlap = np.all((lo[:, None, :] < hi[None, :, :] - BOX_EPS_M)
                     & (lo[None, :, :] < hi[:, None, :] - BOX_EPS_M), axis=2)
    for i, j in zip(*np.nonzero(np.triu(overlap, k=1))):
        problems.append(f"boxes of {ids[i]} and {ids[j]} overlap")
    for item in result.interfaces:
        faces_a = geometry.get(item.a, {}).get("faces", {})
        faces_b = geometry.get(item.b, {}).get("faces", {})
        if item.a_face not in faces_a or item.b_face not in faces_b:
            problems.append(f"{item.id}: unknown endpoint or face")
            continue
        if faces_a[item.a_face]["kind"] != "disk":
            problems.append(f"{item.id}: source contact must be a cap")
            continue
        reason = contact_problem(faces_a[item.a_face], faces_b[item.b_face])
        if reason:
            problems.append(f"{item.id}: {reason}")
    leaf_memo: dict[str, list[str]] = {}

    def leaves_of(node_id: str) -> list[str]:
        if node_id not in leaf_memo:
            stack, out = [node_id], []
            while stack:
                current = stack.pop()
                kids = nodes[current].children
                if kids:
                    stack.extend(kids)
                else:
                    out.append(current)
            leaf_memo[node_id] = out
        return leaf_memo[node_id]

    for node in tree.nodes:
        if len(node.children) < 2:
            continue
        owner = {leaf: child for child in node.children for leaf in leaves_of(child)}
        parent = {c: c for c in node.children}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for item in result.interfaces:
            a, b = owner.get(item.a), owner.get(item.b)
            if a is not None and b is not None and a != b:
                parent[find(a)] = find(b)
        if len({find(c) for c in node.children}) != 1:
            problems.append(f"children of {node.id} are not connected")
    return problems
