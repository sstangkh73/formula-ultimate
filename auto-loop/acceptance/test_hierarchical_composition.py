"""Acceptance suite for the hierarchical free-form composition goal (Work 148).

This file is the loop's specification. It is protected: the loop stops if it
changes. It runs the generator entry point as a black box and checks what the
generator wrote against independent recomputation from the meshes. Nothing the
generator says about itself is trusted when it can be measured instead.

Passing this suite is a geometry and assembly representation gate. It is not
physical validation of any part or of the vehicle.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES

ROOT = Path(__file__).resolve().parents[2]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
GENERATOR = ROOT / "scripts" / "hierarchy" / "generate_hierarchical_vehicle.py"
#: Self-check hook only. verify.ps1 removes it so the loop cannot use it.
OVERRIDE_ENV = "FU_ACCEPTANCE_GENERATOR"

SEEDS = (11, 23, 37)
RUN_TIMEOUT_S = 1200

MIN_LEVELS = 4
MIN_LEAVES = 150
MIN_SIZE_RATIO = 100.0
CAPABILITY_MIN_HEIGHT = 2
CAPABILITY_MIN_LEAVES = 5
MAX_BOX_FRACTION = 0.25
BOX_FILL = 0.999
MAX_CONTACT_TOLERANCE_M = 5e-4
MAX_INTERFERENCE_M = 1e-4
JOINT_KINDS = ("threaded", "welded", "bonded", "interference", "integral")
MASS_REL_TOL = 1e-5
COM_ABS_TOL_M = 1e-5
GEOM_EPS_M = 1e-9
RAY_DIRECTION = np.array([1.0, 0.7071067811865476, 0.3183098861837907])
RAY_DIRECTION = RAY_DIRECTION / np.linalg.norm(RAY_DIRECTION)

ASSEMBLY_FIELDS = {"id", "kind", "children", "functions", "mass_kg", "center_of_mass_m"}
PART_FIELDS = {"id", "kind", "mesh", "material_id", "density_kg_m3", "mass_kg",
               "center_of_mass_m", "generator"}
TOP_FIELDS = {"design_language_version", "seed", "config_sha256", "git_commit", "length_unit",
              "mass_unit", "contact_tolerance_m", "root", "nodes", "interfaces"}


# --------------------------------------------------------------------------
# Running the generator
# --------------------------------------------------------------------------

def _generator_command() -> list[str]:
    override = os.environ.get(OVERRIDE_ENV)
    if override:
        command = json.loads(override)
        if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
            raise RuntimeError(f"{OVERRIDE_ENV} must be a JSON list of strings")
        return command
    return [str(CAD_PYTHON), str(GENERATOR)]


def _run(seed: int, out: Path) -> tuple[Path | None, str]:
    command = _generator_command() + ["--seed", str(seed), "--out", str(out)]
    try:
        done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True,
                              timeout=RUN_TIMEOUT_S)
    except FileNotFoundError as exc:
        return None, f"generator could not start: {exc}"
    except subprocess.TimeoutExpired:
        return None, f"generator exceeded {RUN_TIMEOUT_S} s for seed {seed}"
    if done.returncode != 0:
        tail = (done.stdout + done.stderr)[-3000:]
        return None, f"generator exit {done.returncode} for seed {seed}:\n{tail}"
    if not (out / "manifest.json").is_file():
        return None, f"generator wrote no manifest.json for seed {seed}"
    return out, ""


_TMP: tempfile.TemporaryDirectory | None = None
RUNS: dict[str, tuple[Path | None, str]] = {}
_PACKAGES: dict[str, "Package"] = {}


def setUpModule() -> None:  # noqa: N802 - unittest hook
    global _TMP
    _TMP = tempfile.TemporaryDirectory(prefix="fu_acceptance_")
    base = Path(_TMP.name)
    if not os.environ.get(OVERRIDE_ENV):
        missing = [str(p) for p in (CAD_PYTHON, GENERATOR) if not p.is_file()]
        if missing:
            for key in [f"seed{s}" for s in SEEDS] + ["replay"]:
                RUNS[key] = (None, "missing: " + ", ".join(missing))
            return
    for seed in SEEDS:
        RUNS[f"seed{seed}"] = _run(seed, base / f"seed{seed}")
    RUNS["replay"] = _run(SEEDS[0], base / f"seed{SEEDS[0]}_replay")


def tearDownModule() -> None:  # noqa: N802 - unittest hook
    if _TMP is not None:
        _TMP.cleanup()


# --------------------------------------------------------------------------
# Mesh utilities (independent of the generator)
# --------------------------------------------------------------------------

def read_stl(path: Path) -> np.ndarray:
    """Return triangles as an (n, 3, 3) float64 array."""

    data = path.read_bytes()
    if len(data) >= 84:
        count = struct.unpack_from("<I", data, 80)[0]
        if len(data) == 84 + 50 * count:
            record = np.dtype([("normal", "<f4", 3), ("v", "<f4", (3, 3)), ("attr", "<u2")])
            return np.frombuffer(data, dtype=record, count=count, offset=84)["v"].astype(np.float64)
    text = data.decode("ascii", errors="strict")
    values = re.findall(r"vertex\s+(\S+)\s+(\S+)\s+(\S+)", text)
    if not values or len(values) % 3:
        raise ValueError(f"{path.name}: not a readable STL")
    return np.array(values, dtype=np.float64).reshape(-1, 3, 3)


def closure_problems(tris: np.ndarray) -> list[str]:
    """Closed, consistently oriented 2-manifold check on exact shared vertices."""

    if len(tris) < 4:
        return ["fewer than 4 triangles"]
    if not np.all(np.isfinite(tris)):
        return ["non-finite coordinate"]
    flat = tris.reshape(-1, 3)
    _, index = np.unique(flat, axis=0, return_inverse=True)
    faces = index.reshape(-1, 3)
    if np.any((faces[:, 0] == faces[:, 1]) | (faces[:, 1] == faces[:, 2]) | (faces[:, 0] == faces[:, 2])):
        return ["degenerate triangle with a repeated vertex"]
    directed = np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]])
    pairs, counts = np.unique(directed, axis=0, return_counts=True)
    problems = []
    if np.any(counts != 1):
        problems.append("a directed edge is used more than once (inconsistent orientation or non-manifold)")
    forward = {tuple(p) for p in pairs.tolist()}
    if any((b, a) not in forward for a, b in forward):
        problems.append("an edge has no opposite half-edge (open mesh)")
    return problems


def volume_and_centroid(tris: np.ndarray) -> tuple[float, np.ndarray]:
    a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
    signed = np.einsum("ij,ij->i", a, np.cross(b, c)) / 6.0
    volume = float(signed.sum())
    if volume == 0.0:
        return 0.0, np.zeros(3)
    centroid = (signed[:, None] * (a + b + c) / 4.0).sum(axis=0) / volume
    return volume, centroid


def _dot(u: np.ndarray, v: np.ndarray) -> np.ndarray:
    return np.einsum("...k,...k->...", u, v)


def _safe_div(n: np.ndarray, d: np.ndarray) -> np.ndarray:
    return np.divide(n, d, out=np.zeros(np.broadcast(n, d).shape), where=d != 0)


def point_triangle_distance(points: np.ndarray, tris: np.ndarray, chunk: int = 2_000_000) -> np.ndarray:
    """Minimum distance from each point to a set of triangles (Ericson, region test)."""

    if len(points) == 0:
        return np.zeros(0)
    if len(tris) == 0:
        return np.full(len(points), np.inf)
    result = np.empty(len(points))
    step = max(1, chunk // len(tris))
    a0, b0, c0 = tris[None, :, 0], tris[None, :, 1], tris[None, :, 2]
    for start in range(0, len(points), step):
        p = points[start:start + step, None, :]
        a, b, c = a0, b0, c0
        ab, ac = b - a, c - a
        ap, bp, cp = p - a, p - b, p - c
        d1, d2 = _dot(ab, ap), _dot(ac, ap)
        d3, d4 = _dot(ab, bp), _dot(ac, bp)
        d5, d6 = _dot(ab, cp), _dot(ac, cp)
        va = d3 * d6 - d5 * d4
        vb = d5 * d2 - d1 * d6
        vc = d1 * d4 - d3 * d2
        denom = va + vb + vc
        v = _safe_div(vb, denom)
        w = _safe_div(vc, denom)
        q = a + ab * v[..., None] + ac * w[..., None]
        w_bc = _safe_div(d4 - d3, (d4 - d3) + (d5 - d6))
        q = np.where(((va <= 0) & (d4 - d3 >= 0) & (d5 - d6 >= 0))[..., None], b + (c - b) * w_bc[..., None], q)
        w_ac = _safe_div(d2, d2 - d6)
        q = np.where(((vb <= 0) & (d2 >= 0) & (d6 <= 0))[..., None], a + ac * w_ac[..., None], q)
        q = np.where(((d6 >= 0) & (d5 <= d6))[..., None], np.broadcast_to(c, q.shape), q)
        v_ab = _safe_div(d1, d1 - d3)
        q = np.where(((vc <= 0) & (d1 >= 0) & (d3 <= 0))[..., None], a + ab * v_ab[..., None], q)
        q = np.where(((d3 >= 0) & (d4 <= d3))[..., None], np.broadcast_to(b, q.shape), q)
        q = np.where(((d1 <= 0) & (d2 <= 0))[..., None], np.broadcast_to(a, q.shape), q)
        result[start:start + step] = np.sqrt(((p - q) ** 2).sum(axis=-1)).min(axis=1)
    return result


def points_inside(points: np.ndarray, tris: np.ndarray, chunk: int = 2_000_000) -> np.ndarray:
    """Ray-parity containment test against a closed mesh."""

    if len(points) == 0:
        return np.zeros(0, dtype=bool)
    inside = np.zeros(len(points), dtype=bool)
    step = max(1, chunk // len(tris))
    a, b, c = tris[None, :, 0], tris[None, :, 1], tris[None, :, 2]
    e1, e2 = b - a, c - a
    h = np.cross(RAY_DIRECTION, e2)
    det = _dot(e1, h)
    ok = np.abs(det) > 1e-18
    inv = _safe_div(np.ones_like(det), det)
    for start in range(0, len(points), step):
        p = points[start:start + step, None, :]
        s = p - a
        u = _dot(s, h) * inv
        qv = np.cross(s, e1)
        v = _dot(np.broadcast_to(RAY_DIRECTION, qv.shape), qv) * inv
        t = _dot(e2, qv) * inv
        hit = ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)
        inside[start:start + step] = (hit.sum(axis=1) % 2) == 1
    return inside


def _within_box(points: np.ndarray, lo: np.ndarray, hi: np.ndarray, pad: float) -> np.ndarray:
    return np.all((points >= lo - pad) & (points <= hi + pad), axis=1)


def _tris_near_box(tris: np.ndarray, lo: np.ndarray, hi: np.ndarray, pad: float) -> np.ndarray:
    return np.all((tris.max(axis=1) >= lo - pad) & (tris.min(axis=1) <= hi + pad), axis=1)


def mesh_distance(ta: np.ndarray, tb: np.ndarray, pad: float) -> float:
    """Approximate minimum surface distance using vertices and centroids of each side."""

    best = np.inf
    for src, dst in ((ta, tb), (tb, ta)):
        lo, hi = dst.reshape(-1, 3).min(axis=0), dst.reshape(-1, 3).max(axis=0)
        pts = np.unique(np.concatenate([src.reshape(-1, 3), src.mean(axis=1)]), axis=0)
        pts = pts[_within_box(pts, lo, hi, pad)]
        slo, shi = src.reshape(-1, 3).min(axis=0), src.reshape(-1, 3).max(axis=0)
        near = dst[_tris_near_box(dst, slo, shi, pad)]
        if len(pts) and len(near):
            best = min(best, float(point_triangle_distance(pts, near).min()))
    return best


def penetration_depth(ta: np.ndarray, tb: np.ndarray) -> float:
    """Deepest sampled point of either mesh lying inside the other."""

    worst = 0.0
    for src, dst in ((ta, tb), (tb, ta)):
        lo, hi = dst.reshape(-1, 3).min(axis=0), dst.reshape(-1, 3).max(axis=0)
        pts = np.unique(np.concatenate([src.reshape(-1, 3), src.mean(axis=1)]), axis=0)
        pts = pts[_within_box(pts, lo, hi, 0.0)]
        if not len(pts):
            continue
        inner = pts[points_inside(pts, dst)]
        if len(inner):
            worst = max(worst, float(point_triangle_distance(inner, dst).max()))
    return worst


def canonical_sha256(value) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


# --------------------------------------------------------------------------
# Package loading
# --------------------------------------------------------------------------

class Package:
    def __init__(self, directory: Path) -> None:
        self.dir = directory
        self.manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
        self.nodes = {n["id"]: n for n in self.manifest.get("nodes", []) if isinstance(n, dict) and "id" in n}
        self._meshes: dict[str, np.ndarray] = {}

    def leaves(self) -> list[dict]:
        return [n for n in self.nodes.values() if n.get("kind") == "part"]

    def mesh(self, node_id: str) -> np.ndarray:
        if node_id not in self._meshes:
            rel = self.nodes[node_id]["mesh"]
            path = (self.dir / rel).resolve()
            if self.dir.resolve() not in path.parents:
                raise ValueError(f"{node_id}: mesh path escapes the package")
            self._meshes[node_id] = read_stl(path)
        return self._meshes[node_id]

    def children(self, node_id: str) -> list[str]:
        return list(self.nodes[node_id].get("children", []))

    def depth_map(self) -> dict[str, int]:
        depth = {self.manifest["root"]: 0}
        stack = [self.manifest["root"]]
        while stack:
            current = stack.pop()
            for child in self.children(current):
                depth[child] = depth[current] + 1
                stack.append(child)
        return depth

    def height(self, node_id: str, memo: dict[str, int]) -> int:
        if node_id not in memo:
            kids = self.children(node_id)
            memo[node_id] = 0 if not kids else 1 + max(self.height(k, memo) for k in kids)
        return memo[node_id]

    def leaf_set(self, node_id: str, memo: dict[str, frozenset]) -> frozenset:
        if node_id not in memo:
            node = self.nodes[node_id]
            if node.get("kind") == "part":
                memo[node_id] = frozenset([node_id])
            else:
                memo[node_id] = frozenset().union(*(self.leaf_set(k, memo) for k in self.children(node_id)))
        return memo[node_id]

    def signature(self, node_id: str, memo: dict[str, str]) -> str:
        if node_id not in memo:
            node = self.nodes[node_id]
            if node.get("kind") == "part":
                memo[node_id] = "L"
            else:
                kids = sorted(self.signature(k, memo) for k in self.children(node_id))
                memo[node_id] = "(" + ",".join(sorted(node.get("functions", []))) + ":" + "".join(kids) + ")"
        return memo[node_id]


def _git_head() -> str:
    return subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                          text=True, check=True).stdout.strip()


class _Base(unittest.TestCase):
    def package(self, key: str) -> Package:
        directory, error = RUNS.get(key, (None, "generator was not run"))
        if directory is None:
            self.fail(error)
        if key not in _PACKAGES:
            try:
                _PACKAGES[key] = Package(directory)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.fail(f"{key}: unreadable manifest: {exc}")
        return _PACKAGES[key]

    def packages(self) -> list[tuple[int, Package]]:
        return [(seed, self.package(f"seed{seed}")) for seed in SEEDS]


# --------------------------------------------------------------------------
# 1. Replay and metadata
# --------------------------------------------------------------------------

class T1ReplayAndMetadata(_Base):
    def test_same_seed_is_byte_identical(self):
        first, replay = self.package(f"seed{SEEDS[0]}"), self.package("replay")
        files_a = sorted(p.relative_to(first.dir).as_posix() for p in first.dir.rglob("*") if p.is_file())
        files_b = sorted(p.relative_to(replay.dir).as_posix() for p in replay.dir.rglob("*") if p.is_file())
        self.assertEqual(files_a, files_b, "replay wrote a different file set")
        for rel in files_a:
            self.assertEqual((first.dir / rel).read_bytes(), (replay.dir / rel).read_bytes(),
                             f"replay differs in {rel}")

    def test_manifest_metadata(self):
        head = _git_head()
        for seed, pkg in self.packages():
            m = pkg.manifest
            self.assertEqual(set(m), TOP_FIELDS, f"seed {seed}: top-level fields")
            self.assertEqual(m["seed"], seed)
            self.assertIsInstance(m["design_language_version"], str)
            self.assertTrue(m["design_language_version"].strip())
            self.assertRegex(m["config_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(m["git_commit"], head, f"seed {seed}: git_commit must be the HEAD it ran at")
            self.assertEqual((m["length_unit"], m["mass_unit"]), ("m", "kg"))
            tol = m["contact_tolerance_m"]
            self.assertIsInstance(tol, (int, float))
            self.assertTrue(0 < tol <= MAX_CONTACT_TOLERANCE_M, f"seed {seed}: contact tolerance {tol}")


# --------------------------------------------------------------------------
# 2. Hierarchy
# --------------------------------------------------------------------------

class T2Hierarchy(_Base):
    def test_tree_is_well_formed(self):
        for seed, pkg in self.packages():
            nodes, root = pkg.nodes, pkg.manifest["root"]
            self.assertEqual(len(nodes), len(pkg.manifest["nodes"]), f"seed {seed}: duplicate or invalid node ids")
            self.assertIn(root, nodes)
            self.assertEqual(nodes[root]["kind"], "assembly")
            parents: dict[str, str] = {}
            for node in nodes.values():
                kind = node.get("kind")
                if kind == "assembly":
                    self.assertEqual(set(node), ASSEMBLY_FIELDS, f"seed {seed}: {node['id']} fields")
                    self.assertTrue(node["children"], f"seed {seed}: empty assembly {node['id']}")
                    self.assertIsInstance(node["functions"], list)
                    for child in node["children"]:
                        self.assertIn(child, nodes, f"seed {seed}: unknown child {child}")
                        self.assertNotIn(child, parents, f"seed {seed}: {child} has two parents")
                        parents[child] = node["id"]
                elif kind == "part":
                    self.assertEqual(set(node), PART_FIELDS, f"seed {seed}: {node['id']} fields")
                else:
                    self.fail(f"seed {seed}: {node.get('id')} has kind {kind!r}")
            self.assertNotIn(root, parents)
            depth = pkg.depth_map()
            self.assertEqual(set(depth), set(nodes), f"seed {seed}: nodes unreachable from root or cyclic")

    def test_depth_count_and_scale(self):
        for seed, pkg in self.packages():
            levels = max(pkg.depth_map().values()) + 1
            self.assertGreaterEqual(levels, MIN_LEVELS, f"seed {seed}: levels")
            leaves = pkg.leaves()
            self.assertGreaterEqual(len(leaves), MIN_LEAVES, f"seed {seed}: leaf parts")
            sizes = []
            for leaf in leaves:
                pts = pkg.mesh(leaf["id"]).reshape(-1, 3)
                sizes.append(float(np.linalg.norm(pts.max(axis=0) - pts.min(axis=0))))
            self.assertGreater(min(sizes), 0.0)
            self.assertGreaterEqual(max(sizes) / min(sizes), MIN_SIZE_RATIO, f"seed {seed}: size span")


# --------------------------------------------------------------------------
# 3. Every function is realized in depth
# --------------------------------------------------------------------------

class T3EveryCapability(_Base):
    def test_each_capability_has_a_deep_subtree(self):
        for seed, pkg in self.packages():
            heights: dict[str, int] = {}
            leaf_memo: dict[str, frozenset] = {}
            for capability in sorted(REQUIRED_CAPABILITIES):
                ok = [n for n in pkg.nodes.values()
                      if n.get("kind") == "assembly" and capability in n.get("functions", [])
                      and pkg.height(n["id"], heights) >= CAPABILITY_MIN_HEIGHT
                      and len(pkg.leaf_set(n["id"], leaf_memo)) >= CAPABILITY_MIN_LEAVES]
                self.assertTrue(ok, f"seed {seed}: no subtree of height >= {CAPABILITY_MIN_HEIGHT} "
                                    f"with >= {CAPABILITY_MIN_LEAVES} leaves realizes {capability}")


# --------------------------------------------------------------------------
# 4. Geometry and mass accounting
# --------------------------------------------------------------------------

class T4GeometryAndMass(_Base):
    def test_leaf_meshes_closed_and_masses_measured(self):
        for seed, pkg in self.packages():
            for leaf in pkg.leaves():
                tris = pkg.mesh(leaf["id"])
                problems = closure_problems(tris)
                self.assertFalse(problems, f"seed {seed}: {leaf['id']}: {problems}")
                volume, centroid = volume_and_centroid(tris)
                self.assertGreater(volume, 0.0, f"seed {seed}: {leaf['id']} volume (inverted?)")
                density = leaf["density_kg_m3"]
                self.assertTrue(isinstance(density, (int, float)) and density > 0)
                self.assertIsInstance(leaf["material_id"], str)
                self.assertAlmostEqual(leaf["mass_kg"] / (volume * density), 1.0, delta=MASS_REL_TOL,
                                       msg=f"seed {seed}: {leaf['id']} mass is not mesh volume x density")
                np.testing.assert_allclose(leaf["center_of_mass_m"], centroid, atol=COM_ABS_TOL_M, rtol=0,
                                           err_msg=f"seed {seed}: {leaf['id']} centre of mass")

    def test_assembly_mass_and_centre_of_mass_roll_up(self):
        for seed, pkg in self.packages():
            for node in pkg.nodes.values():
                if node.get("kind") != "assembly":
                    continue
                kids = [pkg.nodes[k] for k in node["children"]]
                total = sum(k["mass_kg"] for k in kids)
                self.assertAlmostEqual(node["mass_kg"], total, delta=1e-9 * max(1.0, total),
                                       msg=f"seed {seed}: {node['id']} mass is not the sum of its children")
                com = sum(np.asarray(k["center_of_mass_m"]) * k["mass_kg"] for k in kids) / total
                np.testing.assert_allclose(node["center_of_mass_m"], com, atol=COM_ABS_TOL_M, rtol=0,
                                           err_msg=f"seed {seed}: {node['id']} centre of mass")


# --------------------------------------------------------------------------
# 5. Free form and recorded programs
# --------------------------------------------------------------------------

class T5FreeForm(_Base):
    def test_not_mostly_boxes(self):
        for seed, pkg in self.packages():
            boxes = 0
            for leaf in pkg.leaves():
                tris = pkg.mesh(leaf["id"])
                pts = tris.reshape(-1, 3)
                extent = pts.max(axis=0) - pts.min(axis=0)
                volume, _ = volume_and_centroid(tris)
                if float(np.prod(extent)) > 0 and volume / float(np.prod(extent)) >= BOX_FILL:
                    boxes += 1
            fraction = boxes / len(pkg.leaves())
            self.assertLessEqual(fraction, MAX_BOX_FRACTION, f"seed {seed}: {boxes} leaves are boxes")

    def test_programs_are_recorded_and_hashed(self):
        for seed, pkg in self.packages():
            for leaf in pkg.leaves():
                gen = leaf["generator"]
                self.assertEqual(set(gen), {"grammar_version", "program", "program_sha256"},
                                 f"seed {seed}: {leaf['id']} generator fields")
                self.assertTrue(isinstance(gen["grammar_version"], str) and gen["grammar_version"].strip())
                self.assertIsInstance(gen["program"], dict)
                self.assertTrue(gen["program"], f"seed {seed}: {leaf['id']} empty program")
                self.assertEqual(gen["program_sha256"], canonical_sha256(gen["program"]),
                                 f"seed {seed}: {leaf['id']} program hash")


# --------------------------------------------------------------------------
# 6. Interfaces backed by measured contact, no interpenetration
# --------------------------------------------------------------------------

class T6Interfaces(_Base):
    def _interfaces(self, seed: int, pkg: Package) -> list[dict]:
        leaves = {n["id"] for n in pkg.leaves()}
        interfaces = pkg.manifest["interfaces"]
        self.assertIsInstance(interfaces, list)
        for item in interfaces:
            self.assertTrue({"id", "a", "b", "kind"} <= set(item) <= {"id", "a", "b", "kind", "interference_m"},
                            f"seed {seed}: interface fields {sorted(item)}")
            self.assertIn(item["kind"], JOINT_KINDS, f"seed {seed}: {item['id']} kind")
            self.assertIn(item["a"], leaves, f"seed {seed}: {item['id']} endpoint a is not a leaf part")
            self.assertIn(item["b"], leaves, f"seed {seed}: {item['id']} endpoint b is not a leaf part")
            self.assertNotEqual(item["a"], item["b"])
            if "interference_m" in item:
                self.assertEqual(item["kind"], "interference", f"seed {seed}: {item['id']}")
                self.assertTrue(0 < item["interference_m"] <= MAX_INTERFERENCE_M, f"seed {seed}: {item['id']}")
        return interfaces

    def test_children_of_every_assembly_are_connected(self):
        for seed, pkg in self.packages():
            interfaces = self._interfaces(seed, pkg)
            memo: dict[str, frozenset] = {}
            owner_of: dict[str, dict[str, str]] = {}
            for node in pkg.nodes.values():
                if node.get("kind") != "assembly" or len(node["children"]) < 2:
                    continue
                owner = {leaf: child for child in node["children"] for leaf in pkg.leaf_set(child, memo)}
                owner_of[node["id"]] = owner
                parent = {c: c for c in node["children"]}

                def find(x: str) -> str:
                    while parent[x] != x:
                        parent[x] = parent[parent[x]]
                        x = parent[x]
                    return x

                for item in interfaces:
                    a, b = owner.get(item["a"]), owner.get(item["b"])
                    if a is not None and b is not None and a != b:
                        parent[find(a)] = find(b)
                groups = {find(c) for c in node["children"]}
                self.assertEqual(len(groups), 1,
                                 f"seed {seed}: children of {node['id']} form {len(groups)} disconnected groups")

    def test_interfaces_touch_and_nothing_interpenetrates(self):
        for seed, pkg in self.packages():
            interfaces = self._interfaces(seed, pkg)
            tol = pkg.manifest["contact_tolerance_m"]
            allowed: dict[frozenset, float] = {}
            for item in interfaces:
                gap = mesh_distance(pkg.mesh(item["a"]), pkg.mesh(item["b"]), tol)
                self.assertLessEqual(gap, tol + GEOM_EPS_M,
                                     f"seed {seed}: interface {item['id']} has no measured contact "
                                     f"within {tol:.1e} m (inf = no sample within tolerance)")
                key = frozenset((item["a"], item["b"]))
                allowed[key] = max(allowed.get(key, 0.0), item.get("interference_m", 0.0))
            leaves = [n["id"] for n in pkg.leaves()]
            lo = np.array([pkg.mesh(i).reshape(-1, 3).min(axis=0) for i in leaves])
            hi = np.array([pkg.mesh(i).reshape(-1, 3).max(axis=0) for i in leaves])
            overlap = np.all((lo[:, None, :] < hi[None, :, :] - tol) & (lo[None, :, :] < hi[:, None, :] - tol), axis=2)
            for i, j in zip(*np.nonzero(np.triu(overlap, k=1))):
                a, b = leaves[i], leaves[j]
                limit = max(tol, allowed.get(frozenset((a, b)), 0.0)) + GEOM_EPS_M
                depth = penetration_depth(pkg.mesh(a), pkg.mesh(b))
                self.assertLessEqual(depth, limit, f"seed {seed}: {a} and {b} interpenetrate by {depth:.3e} m")


# --------------------------------------------------------------------------
# 7. No fixed template
# --------------------------------------------------------------------------

class T7NoFixedTemplate(_Base):
    def test_whole_trees_differ_across_seeds(self):
        signatures = {}
        for seed, pkg in self.packages():
            signatures[seed] = pkg.signature(pkg.manifest["root"], {})
        self.assertEqual(len(set(signatures.values())), len(SEEDS),
                         "different seeds produced the same tree topology")

    def test_each_capability_varies_across_seeds(self):
        per_seed = []
        for _seed, pkg in self.packages():
            memo: dict[str, str] = {}
            per_seed.append({cap: frozenset(pkg.signature(n["id"], memo) for n in pkg.nodes.values()
                                            if n.get("kind") == "assembly" and cap in n.get("functions", []))
                             for cap in REQUIRED_CAPABILITIES})
        for cap in sorted(REQUIRED_CAPABILITIES):
            variants = {seed_caps[cap] for seed_caps in per_seed}
            self.assertGreaterEqual(len(variants), 2, f"{cap} has the same subtree topology for every seed")


if __name__ == "__main__":
    sys.exit(unittest.main())
