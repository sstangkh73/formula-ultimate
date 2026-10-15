"""Acceptance suite for goal v2: functional composition (Work 154).

Protected: the loop stops if this file changes. The v2 generator is run as a
black box and every claim is re-measured from the meshes. Every v1 check is
re-applied to the v2 package by subclassing, and the v2 checks are grouped in
tiers so that partial progress is visible:

- TierA*: geometry language, declared motions, inertia
- TierB*: per-capability function evidence, threaded joints, ground stability
- TierC*: Level-0 race evaluation on the existing kernel

Passing is a representation, kinematic-clearance and Level-0 coupling gate.
It is not physical validation of any part or of the vehicle.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import numpy as np

import test_hierarchical_composition as v1
from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES

ROOT = v1.ROOT
GENERATOR = ROOT / "scripts" / "hierarchy" / "generate_functional_vehicle.py"
EVALUATOR = ROOT / "scripts" / "hierarchy" / "evaluate_level0.py"
#: Self-check hooks only. verify.ps1 removes them so the loop cannot use them.
GENERATOR_ENV = "FU_ACCEPTANCE_GENERATOR_V2"
EVALUATOR_ENV = "FU_ACCEPTANCE_EVALUATOR"

SEEDS = v1.SEEDS
RUN_TIMEOUT_S = 1800
EVAL_TIMEOUT_S = 600

V2_TOP_FIELDS = v1.TOP_FIELDS | {"up_axis", "motions", "function_evidence", "vehicle_inertia_kg_m2"}
V2_JOINT_KINDS = v1.JOINT_KINDS + ("bearing", "guide", "rolling")
MOTION_KINDS = ("bearing", "guide")
MOTION_TOLERANCE_M = 1e-3
SWEEP_STEPS = 8
MIN_NON_PRISMATIC_FRACTION = 0.25
MIN_THROUGH_HOLE_FRACTION = 0.05
PRISMATIC_AREA_FRACTION = 0.99
MIN_STORED_VOLUME_M3 = 0.01
MIN_HEAT_AREA_RATIO = 3.0
MAX_BRAKE_GAP_M = 2e-3
MIN_STEER_RANGE_RAD = 0.2
MIN_STEER_AXIS_ANGLE_DEG = 30.0
MIN_THREADED_JOINTS = 8
GROUND_BAND_M = 1e-3
MIN_STABILITY_MARGIN_M = 0.05
INERTIA_REL_TOL = 1e-5
RACE_KERNEL_ID = "race-level0-v1"
EVAL_FIELDS = {"manifest_sha256", "mass_kg", "drag_area_m2", "outcome", "race_time_s",
               "consumed_energy_j", "terminal_energy_boundary_residual_j", "circuit_id", "race_kernel"}
MOTION_FIELDS_REVOLUTE = {"id", "parts", "type", "axis_point_m", "axis_dir", "range_rad"}
MOTION_FIELDS_PRISMATIC = {"id", "parts", "type", "axis_point_m", "axis_dir", "stroke_m"}
EVIDENCE_FIELDS = {
    "energy_storage": {"vessel", "stored_volume_m3"},
    "energy_converter": {"chamber", "motion"},
    "power_transmission": {"chain"},
    "ground_propulsion": {"motions"},
    "direction_control": {"motion"},
    "braking": {"rotor_motion", "stator"},
    "load_structure": {"members"},
    "heat_rejection": {"surfaces"},
    "controller": {"housing", "contents"},
}


# --------------------------------------------------------------------------
# Running the v2 generator and the evaluator
# --------------------------------------------------------------------------

def _command(env: str, default: list[str]) -> list[str]:
    override = os.environ.get(env)
    if override:
        command = json.loads(override)
        if not isinstance(command, list) or not all(isinstance(x, str) for x in command):
            raise RuntimeError(f"{env} must be a JSON list of strings")
        return command
    return default


def _run_generator(seed: int, out: Path) -> tuple[Path | None, str]:
    command = _command(GENERATOR_ENV, [str(v1.CAD_PYTHON), str(GENERATOR)]) + ["--seed", str(seed), "--out", str(out)]
    try:
        done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=RUN_TIMEOUT_S)
    except FileNotFoundError as exc:
        return None, f"v2 generator could not start: {exc}"
    except subprocess.TimeoutExpired:
        return None, f"v2 generator exceeded {RUN_TIMEOUT_S} s for seed {seed}"
    if done.returncode != 0:
        return None, f"v2 generator exit {done.returncode} for seed {seed}:\n{(done.stdout + done.stderr)[-3000:]}"
    if not (out / "manifest.json").is_file():
        return None, f"v2 generator wrote no manifest.json for seed {seed}"
    return out, ""


def run_evaluator(manifest: Path, out: Path) -> tuple[dict | None, bytes, str]:
    command = _command(EVALUATOR_ENV, [sys.executable, str(EVALUATOR)]) + ["--manifest", str(manifest), "--out", str(out)]
    try:
        done = subprocess.run(command, cwd=ROOT, capture_output=True, text=True, timeout=EVAL_TIMEOUT_S)
    except FileNotFoundError as exc:
        return None, b"", f"evaluator could not start: {exc}"
    except subprocess.TimeoutExpired:
        return None, b"", f"evaluator exceeded {EVAL_TIMEOUT_S} s"
    if done.returncode != 0:
        return None, b"", f"evaluator exit {done.returncode}:\n{(done.stdout + done.stderr)[-3000:]}"
    if not out.is_file():
        return None, b"", "evaluator wrote no output file"
    data = out.read_bytes()
    try:
        return json.loads(data.decode("utf-8")), data, ""
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return None, data, f"evaluator output is not JSON: {exc}"


_TMP: tempfile.TemporaryDirectory | None = None
RUNS: dict[str, tuple[Path | None, str]] = {}
_PACKAGES: dict[str, v1.Package] = {}


def setUpModule() -> None:  # noqa: N802 - unittest hook
    global _TMP
    _TMP = tempfile.TemporaryDirectory(prefix="fu_acceptance_v2_")
    base = Path(_TMP.name)
    if not os.environ.get(GENERATOR_ENV):
        missing = [str(p) for p in (v1.CAD_PYTHON, GENERATOR) if not p.is_file()]
        if missing:
            for key in [f"seed{s}" for s in SEEDS] + ["replay"]:
                RUNS[key] = (None, "missing: " + ", ".join(missing))
            return
    for seed in SEEDS:
        RUNS[f"seed{seed}"] = _run_generator(seed, base / f"seed{seed}")
    RUNS["replay"] = _run_generator(SEEDS[0], base / f"seed{SEEDS[0]}_replay")


def tearDownModule() -> None:  # noqa: N802 - unittest hook
    if _TMP is not None:
        _TMP.cleanup()


# --------------------------------------------------------------------------
# Mesh measurements (independent of the generator)
# --------------------------------------------------------------------------

def _faces(tris: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    verts, index = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
    return verts, index.reshape(-1, 3)


def components(tris: np.ndarray) -> list[np.ndarray]:
    """Split a mesh into vertex-connected components."""

    verts, faces = _faces(tris)
    label = np.arange(len(verts))
    while True:
        face_min = label[faces].min(axis=1)
        new = label.copy()
        np.minimum.at(new, faces.ravel(), np.repeat(face_min, 3))
        new = new[new]
        if np.array_equal(new, label):
            break
        label = new
    face_label = label[faces[:, 0]]
    return [tris[face_label == value] for value in np.unique(face_label)]


def genus(tris: np.ndarray) -> int:
    total = 0
    for comp in components(tris):
        verts, faces = _faces(comp)
        edges = np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1)
        chi = len(verts) - len(np.unique(edges, axis=0)) + len(faces)
        total += max(0, (2 - chi) // 2)
    return total


def void_volume(tris: np.ndarray) -> float:
    return float(-sum(min(0.0, v1.volume_and_centroid(c)[0]) for c in components(tris)))


def outer_shell(tris: np.ndarray) -> np.ndarray:
    comps = components(tris)
    return comps[int(np.argmax([v1.volume_and_centroid(c)[0] for c in comps]))]


def in_cavity(points: np.ndarray, tris: np.ndarray) -> np.ndarray:
    """Inside the outer shell but not inside the solid material."""

    return v1.points_inside(points, outer_shell(tris)) & ~v1.points_inside(points, tris)


def surface_area(tris: np.ndarray) -> float:
    return float(np.linalg.norm(np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]), axis=1).sum() / 2.0)


def is_prismatic(tris: np.ndarray) -> bool:
    """True when some direction leaves at least 99 % of the area parallel or perpendicular to it."""

    cross = np.cross(tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0])
    area = np.linalg.norm(cross, axis=1)
    keep = area > 0
    normals, area = cross[keep] / area[keep, None], area[keep]
    total = area.sum()
    for direction in normals[np.argsort(area)[::-1][:20]]:
        dots = np.abs(normals @ direction)
        aligned = (dots > 0.9998) | (dots < 0.0175)
        if area[aligned].sum() >= PRISMATIC_AREA_FRACTION * total:
            return True
    return False


def inertia_about_com(meshes_and_density: list[tuple[np.ndarray, float]]) -> tuple[float, np.ndarray, np.ndarray]:
    """Mass, centre of mass and inertia tensor about the centre of mass."""

    canonical = np.array([[2.0, 1.0, 1.0], [1.0, 2.0, 1.0], [1.0, 1.0, 2.0]]) / 120.0
    mass, first, second = 0.0, np.zeros(3), np.zeros((3, 3))
    for tris, density in meshes_and_density:
        a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
        det = np.einsum("ij,ij->i", a, np.cross(b, c))
        mass += density * det.sum() / 6.0
        first += density * (det[:, None] * (a + b + c)).sum(axis=0) / 24.0
        frames = np.stack([a, b, c], axis=2)
        second += density * np.einsum("n,nij,jk,nlk->il", det, frames, canonical, frames)
    com = first / mass
    covariance = second - mass * np.outer(com, com)
    return mass, com, np.trace(covariance) * np.eye(3) - covariance


def rotation(axis: np.ndarray, angle: float) -> np.ndarray:
    x, y, z = axis
    k = np.array([[0.0, -z, y], [z, 0.0, -x], [-y, x, 0.0]])
    return np.eye(3) + math.sin(angle) * k + (1.0 - math.cos(angle)) * (k @ k)


def line_hits(origin: np.ndarray, direction: np.ndarray, tris: np.ndarray) -> int:
    """Number of triangles crossed by the infinite line origin + t * direction."""

    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    h = np.cross(direction, e2)
    det = np.einsum("ij,ij->i", e1, h)
    ok = np.abs(det) > 1e-18
    inv = np.divide(1.0, det, out=np.zeros_like(det), where=ok)
    s = origin - tris[:, 0]
    u = np.einsum("ij,ij->i", s, h) * inv
    q = np.cross(s, e1)
    v = (q @ direction) * inv
    return int((ok & (u >= 0) & (v >= 0) & (u + v <= 1)).sum())


def ray_hits(origin: np.ndarray, direction: np.ndarray, tris: np.ndarray) -> int:
    """Number of triangles crossed by the ray origin + t * direction, t > 0."""

    e1, e2 = tris[:, 1] - tris[:, 0], tris[:, 2] - tris[:, 0]
    h = np.cross(direction, e2)
    det = np.einsum("ij,ij->i", e1, h)
    ok = np.abs(det) > 1e-18
    inv = np.divide(1.0, det, out=np.zeros_like(det), where=ok)
    s = origin - tris[:, 0]
    u = np.einsum("ij,ij->i", s, h) * inv
    q = np.cross(s, e1)
    v = (q @ direction) * inv
    t = np.einsum("ij,ij->i", q, e2) * inv
    return int((ok & (u >= 0) & (v >= 0) & (u + v <= 1) & (t > 0)).sum())


def surrounds_axis(tris: np.ndarray, origin: np.ndarray, direction: np.ndarray) -> bool:
    """Every one of eight radial rays from the axis point meets the part's material."""

    helper = np.array([1.0, 0.0, 0.0]) if abs(direction[0]) < 0.9 else np.array([0.0, 1.0, 0.0])
    e1 = np.cross(direction, helper)
    e1 /= np.linalg.norm(e1)
    e2 = np.cross(direction, e1)
    for k in range(8):
        angle = k * math.pi / 4 + 0.4027
        if ray_hits(origin, math.cos(angle) * e1 + math.sin(angle) * e2, tris) == 0:
            return False
    return True


def convex_hull_2d(points: np.ndarray) -> np.ndarray:
    pts = sorted(set(map(tuple, np.round(points, 12).tolist())))
    if len(pts) < 3:
        return np.array(pts)

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in pts:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(pts):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return np.array(lower[:-1] + upper[:-1])


def hull_margin(hull: np.ndarray, point: np.ndarray) -> float:
    """Signed distance from a point to the boundary of a CCW convex polygon (positive inside)."""

    if len(hull) < 3:
        return -math.inf
    margins = []
    for i in range(len(hull)):
        a, b = hull[i], hull[(i + 1) % len(hull)]
        edge = b - a
        normal = np.array([-edge[1], edge[0]]) / np.linalg.norm(edge)
        margins.append(float((point - a) @ normal))
    return min(margins)


def samples(tris: np.ndarray) -> np.ndarray:
    return np.unique(np.concatenate([tris.reshape(-1, 3), tris.mean(axis=1)]), axis=0)


# --------------------------------------------------------------------------
# Shared base
# --------------------------------------------------------------------------

class _V2Base(unittest.TestCase):
    def package(self, key: str) -> v1.Package:
        directory, error = RUNS.get(key, (None, "v2 generator was not run"))
        if directory is None:
            self.fail(error)
        if key not in _PACKAGES:
            try:
                _PACKAGES[key] = v1.Package(directory)
            except (OSError, ValueError, json.JSONDecodeError) as exc:
                self.fail(f"{key}: unreadable manifest: {exc}")
        return _PACKAGES[key]

    def packages(self) -> list[tuple[int, v1.Package]]:
        return [(seed, self.package(f"seed{seed}")) for seed in SEEDS]

    # -- helpers on a package ------------------------------------------------
    def leaf_ids(self, pkg: v1.Package) -> set[str]:
        return {n["id"] for n in pkg.leaves()}

    def capability_leaves(self, pkg: v1.Package, capability: str) -> set[str]:
        memo: dict[str, frozenset] = {}
        result: set[str] = set()
        for node in pkg.nodes.values():
            if node.get("kind") == "assembly" and capability in node.get("functions", []):
                result |= pkg.leaf_set(node["id"], memo)
        return result

    def motions(self, seed: int, pkg: v1.Package) -> dict[str, dict]:
        motions = pkg.manifest.get("motions")
        self.assertIsInstance(motions, list, f"seed {seed}: motions must be a list")
        leaves, seen, result = self.leaf_ids(pkg), set(), {}
        for m in motions:
            kind = m.get("type")
            self.assertIn(kind, ("revolute", "prismatic"), f"seed {seed}: motion type {kind!r}")
            expected = MOTION_FIELDS_REVOLUTE if kind == "revolute" else MOTION_FIELDS_PRISMATIC
            self.assertEqual(set(m), expected, f"seed {seed}: motion {m.get('id')} fields")
            self.assertNotIn(m["id"], result, f"seed {seed}: duplicate motion id {m['id']}")
            self.assertTrue(m["parts"], f"seed {seed}: motion {m['id']} has no parts")
            for part in m["parts"]:
                self.assertIn(part, leaves, f"seed {seed}: motion {m['id']} part {part} is not a leaf")
                self.assertNotIn(part, seen, f"seed {seed}: {part} belongs to two motions")
                seen.add(part)
            axis = np.asarray(m["axis_dir"], dtype=float)
            self.assertEqual(axis.shape, (3,))
            self.assertAlmostEqual(float(np.linalg.norm(axis)), 1.0, delta=1e-9, msg=f"seed {seed}: {m['id']} axis_dir")
            self.assertEqual(np.asarray(m["axis_point_m"], dtype=float).shape, (3,))
            if kind == "revolute":
                self.assertTrue(0 < m["range_rad"] <= 2 * math.pi + 1e-12, f"seed {seed}: {m['id']} range_rad")
            else:
                self.assertTrue(m["stroke_m"] > 0, f"seed {seed}: {m['id']} stroke_m")
            result[m["id"]] = m
        return result

    def evidence(self, seed: int, pkg: v1.Package, capability: str) -> dict:
        evidence = pkg.manifest.get("function_evidence")
        self.assertIsInstance(evidence, dict, f"seed {seed}: function_evidence must be an object")
        self.assertEqual(set(evidence), set(REQUIRED_CAPABILITIES), f"seed {seed}: function_evidence keys")
        item = evidence[capability]
        self.assertEqual(set(item), EVIDENCE_FIELDS[capability], f"seed {seed}: {capability} evidence fields")
        return item

    def motion_points(self, pkg: v1.Package, motion: dict) -> np.ndarray:
        return np.concatenate([samples(pkg.mesh(p)) for p in motion["parts"]])

    def motion_by_id(self, seed: int, pkg: v1.Package, motion_id: str, capability: str) -> dict:
        motions = self.motions(seed, pkg)
        self.assertIn(motion_id, motions, f"seed {seed}: {capability} names unknown motion {motion_id}")
        motion = motions[motion_id]
        inside = self.capability_leaves(pkg, capability)
        for part in motion["parts"]:
            self.assertIn(part, inside, f"seed {seed}: motion {motion_id} part {part} is outside {capability}")
        return motion

    def assert_full_turn(self, seed: int, motion: dict, capability: str) -> None:
        self.assertEqual(motion["type"], "revolute", f"seed {seed}: {capability} motion {motion['id']} must be revolute")
        self.assertGreaterEqual(motion["range_rad"], 2 * math.pi - 1e-9,
                                f"seed {seed}: {capability} motion {motion['id']} must turn fully")


# --------------------------------------------------------------------------
# Tier A: v1 contract re-applied to the v2 package
# --------------------------------------------------------------------------

class TierA0Replay(_V2Base, v1.T1ReplayAndMetadata):
    def test_manifest_metadata(self):
        head = v1._git_head()
        for seed, pkg in self.packages():
            m = pkg.manifest
            self.assertEqual(set(m), V2_TOP_FIELDS, f"seed {seed}: top-level fields")
            self.assertEqual(m["seed"], seed)
            self.assertTrue(isinstance(m["design_language_version"], str) and m["design_language_version"].strip())
            self.assertRegex(m["config_sha256"], r"^[0-9a-f]{64}$")
            self.assertEqual(m["git_commit"], head)
            self.assertEqual((m["length_unit"], m["mass_unit"], m["up_axis"]), ("m", "kg", "z"))
            self.assertTrue(0 < m["contact_tolerance_m"] <= v1.MAX_CONTACT_TOLERANCE_M)


class TierA0Hierarchy(_V2Base, v1.T2Hierarchy):
    pass


class TierA0Capabilities(_V2Base, v1.T3EveryCapability):
    pass


class TierA0GeometryAndMass(_V2Base, v1.T4GeometryAndMass):
    pass


class TierA0FreeForm(_V2Base, v1.T5FreeForm):
    pass


class TierA0Interfaces(_V2Base, v1.T6Interfaces):
    def _interfaces(self, seed, pkg):
        leaves = self.leaf_ids(pkg)
        interfaces = pkg.manifest["interfaces"]
        self.assertIsInstance(interfaces, list)
        for item in interfaces:
            kind = item.get("kind")
            self.assertIn(kind, V2_JOINT_KINDS, f"seed {seed}: {item.get('id')} kind")
            allowed = {"id", "a", "b", "kind"}
            if kind == "interference":
                allowed |= {"interference_m"}
            if kind == "threaded":
                allowed |= {"axis_point_m", "axis_dir"}
                self.assertTrue({"axis_point_m", "axis_dir"} <= set(item), f"seed {seed}: {item['id']} needs an axis")
            self.assertTrue({"id", "a", "b", "kind"} <= set(item) <= allowed, f"seed {seed}: interface fields {sorted(item)}")
            self.assertIn(item["a"], leaves)
            self.assertIn(item["b"], leaves)
            self.assertNotEqual(item["a"], item["b"])
            if "interference_m" in item:
                self.assertTrue(0 < item["interference_m"] <= v1.MAX_INTERFERENCE_M)
        return interfaces


class TierA0NoFixedTemplate(_V2Base, v1.T7NoFixedTemplate):
    pass


# --------------------------------------------------------------------------
# Tier A: geometry language, motions, inertia
# --------------------------------------------------------------------------

class TierA1GeometryLanguage(_V2Base):
    def test_non_prismatic_and_through_hole_shares(self):
        for seed, pkg in self.packages():
            leaves = pkg.leaves()
            non_prismatic = sum(1 for leaf in leaves if not is_prismatic(pkg.mesh(leaf["id"])))
            holed = sum(1 for leaf in leaves if genus(pkg.mesh(leaf["id"])) >= 1)
            self.assertGreaterEqual(non_prismatic / len(leaves), MIN_NON_PRISMATIC_FRACTION,
                                    f"seed {seed}: only {non_prismatic}/{len(leaves)} leaves are non-prismatic")
            self.assertGreaterEqual(holed / len(leaves), MIN_THROUGH_HOLE_FRACTION,
                                    f"seed {seed}: only {holed}/{len(leaves)} leaves have a through-hole")


class TierA2Motions(_V2Base):
    def test_every_motion_has_a_bearing_or_guide(self):
        for seed, pkg in self.packages():
            for motion in self.motions(seed, pkg).values():
                parts = set(motion["parts"])
                wanted = "bearing" if motion["type"] == "revolute" else "guide"
                ok = [i for i in pkg.manifest["interfaces"] if i["kind"] == wanted
                      and ((i["a"] in parts) != (i["b"] in parts))]
                self.assertTrue(ok, f"seed {seed}: motion {motion['id']} has no {wanted} interface to a fixed part")

    def test_motions_sweep_without_collision(self):
        for seed, pkg in self.packages():
            leaves = [n["id"] for n in pkg.leaves()]
            boxes = {i: (pkg.mesh(i).reshape(-1, 3).min(axis=0), pkg.mesh(i).reshape(-1, 3).max(axis=0)) for i in leaves}
            for motion in self.motions(seed, pkg).values():
                parts = set(motion["parts"])
                points = self.motion_points(pkg, motion)
                origin = np.asarray(motion["axis_point_m"], dtype=float)
                axis = np.asarray(motion["axis_dir"], dtype=float)
                if motion["type"] == "revolute":
                    half = motion["range_rad"] / 2
                    poses = [rotation(axis, a) for a in np.linspace(-half, half, 2 * SWEEP_STEPS + 1)]
                    moved = [(points - origin) @ r.T + origin for r in poses]
                else:
                    moved = [points + axis * s for s in np.linspace(0, motion["stroke_m"], SWEEP_STEPS + 1)[1:]]
                for pts in moved:
                    lo, hi = pts.min(axis=0), pts.max(axis=0)
                    for other in leaves:
                        if other in parts:
                            continue
                        olo, ohi = boxes[other]
                        if np.any(hi < olo) or np.any(lo > ohi):
                            continue
                        near = pts[v1._within_box(pts, olo, ohi, 0.0)]
                        if not len(near):
                            continue
                        inner = near[v1.points_inside(near, pkg.mesh(other))]
                        if len(inner):
                            depth = float(v1.point_triangle_distance(inner, pkg.mesh(other)).max())
                            self.assertLessEqual(depth, MOTION_TOLERANCE_M,
                                                 f"seed {seed}: motion {motion['id']} collides with {other} by {depth:.3e} m")


class TierA3Inertia(_V2Base):
    def test_vehicle_inertia_matches_meshes(self):
        for seed, pkg in self.packages():
            mass, com, inertia = inertia_about_com([(pkg.mesh(n["id"]), n["density_kg_m3"]) for n in pkg.leaves()])
            declared = np.asarray(pkg.manifest["vehicle_inertia_kg_m2"], dtype=float)
            self.assertEqual(declared.shape, (3, 3), f"seed {seed}: inertia must be 3x3")
            scale = float(np.abs(inertia).max())
            np.testing.assert_allclose(declared, inertia, rtol=0, atol=INERTIA_REL_TOL * scale,
                                       err_msg=f"seed {seed}: vehicle inertia about the centre of mass")


# --------------------------------------------------------------------------
# Tier B: function evidence
# --------------------------------------------------------------------------

class TierB1EnergyStorage(_V2Base):
    def test_vessel_holds_declared_volume(self):
        for seed, pkg in self.packages():
            item = self.evidence(seed, pkg, "energy_storage")
            self.assertIn(item["vessel"], self.capability_leaves(pkg, "energy_storage"))
            declared = item["stored_volume_m3"]
            self.assertGreaterEqual(declared, MIN_STORED_VOLUME_M3, f"seed {seed}: stored volume")
            measured = void_volume(pkg.mesh(item["vessel"]))
            self.assertGreaterEqual(measured, declared * (1 - 1e-6),
                                    f"seed {seed}: vessel void {measured:.4e} m3 < declared {declared:.4e} m3")


class TierB2EnergyConverter(_V2Base):
    def test_moving_member_works_inside_a_chamber(self):
        for seed, pkg in self.packages():
            item = self.evidence(seed, pkg, "energy_converter")
            chamber = item["chamber"]
            self.assertIn(chamber, self.capability_leaves(pkg, "energy_converter"))
            motion = self.motion_by_id(seed, pkg, item["motion"], "energy_converter")
            self.assertNotIn(chamber, motion["parts"])
            mesh = pkg.mesh(chamber)
            self.assertTrue(genus(mesh) >= 1 or void_volume(mesh) > 0, f"seed {seed}: chamber has no bore or cavity")
            pts = self.motion_points(pkg, motion)
            lo, hi = mesh.reshape(-1, 3).min(axis=0), mesh.reshape(-1, 3).max(axis=0)
            inside_box = v1._within_box(pts, lo, hi, 0.0)
            in_material = np.zeros(len(pts), dtype=bool)
            in_material[inside_box] = v1.points_inside(pts[inside_box], mesh)
            share = float((inside_box & ~in_material).mean())
            self.assertGreaterEqual(share, 0.5, f"seed {seed}: only {share:.0%} of the moving member is in the chamber")


class TierB3PowerTransmission(_V2Base):
    def test_chain_of_rotating_members_in_contact(self):
        for seed, pkg in self.packages():
            chain = self.evidence(seed, pkg, "power_transmission")["chain"]
            self.assertGreaterEqual(len(chain), 2, f"seed {seed}: transmission chain too short")
            members = [self.motion_by_id(seed, pkg, m, "power_transmission") for m in chain]
            for member in members:
                self.assert_full_turn(seed, member, "power_transmission")
            for first, second in zip(members, members[1:]):
                a, b = set(first["parts"]), set(second["parts"])
                linked = [i for i in pkg.manifest["interfaces"]
                          if (i["a"] in a and i["b"] in b) or (i["a"] in b and i["b"] in a)]
                self.assertTrue(linked, f"seed {seed}: {first['id']} and {second['id']} are not in contact")


class TierB4GroundPropulsion(_V2Base):
    def test_rotating_ground_contacts_carry_the_vehicle_stably(self):
        for seed, pkg in self.packages():
            ids = self.evidence(seed, pkg, "ground_propulsion")["motions"]
            self.assertGreaterEqual(len(ids), 2, f"seed {seed}: fewer than two ground motions")
            motions = [self.motion_by_id(seed, pkg, m, "ground_propulsion") for m in ids]
            contact_parts = set()
            for motion in motions:
                self.assert_full_turn(seed, motion, "ground_propulsion")
                contact_parts |= set(motion["parts"])
            leaves = pkg.leaves()
            z_min = min(float(pkg.mesh(n["id"])[:, :, 2].min()) for n in leaves)
            band, owners = [], set()
            for n in leaves:
                pts = pkg.mesh(n["id"]).reshape(-1, 3)
                low = pts[pts[:, 2] <= z_min + GROUND_BAND_M]
                if len(low):
                    band.append(low)
                    owners.add(n["id"])
            self.assertTrue(owners <= contact_parts,
                            f"seed {seed}: ground is touched by non-propulsive parts {sorted(owners - contact_parts)}")
            hull = convex_hull_2d(np.concatenate(band)[:, :2])
            com = np.asarray(pkg.nodes[pkg.manifest["root"]]["center_of_mass_m"], dtype=float)[:2]
            margin = hull_margin(hull, com)
            self.assertGreaterEqual(margin, MIN_STABILITY_MARGIN_M,
                                    f"seed {seed}: centre of mass is {margin:.3f} m inside the support polygon")


class TierB5DirectionControl(_V2Base):
    def test_steering_axis_is_independent_of_drive_axes(self):
        for seed, pkg in self.packages():
            motion = self.motion_by_id(seed, pkg, self.evidence(seed, pkg, "direction_control")["motion"], "direction_control")
            self.assertEqual(motion["type"], "revolute", f"seed {seed}: steering must be revolute")
            self.assertGreaterEqual(motion["range_rad"], MIN_STEER_RANGE_RAD, f"seed {seed}: steering range")
            steer = np.asarray(motion["axis_dir"], dtype=float)
            limit = math.cos(math.radians(MIN_STEER_AXIS_ANGLE_DEG))
            all_motions = self.motions(seed, pkg)
            for mid in self.evidence(seed, pkg, "ground_propulsion")["motions"]:
                drive = np.asarray(all_motions[mid]["axis_dir"], dtype=float)
                self.assertLessEqual(abs(float(steer @ drive)), limit,
                                     f"seed {seed}: steering axis is within {MIN_STEER_AXIS_ANGLE_DEG} deg of drive {mid}")


class TierB6Braking(_V2Base):
    def test_stator_faces_a_rotor_closely(self):
        for seed, pkg in self.packages():
            item = self.evidence(seed, pkg, "braking")
            rotor = self.motion_by_id(seed, pkg, item["rotor_motion"], "braking")
            self.assert_full_turn(seed, rotor, "braking")
            stator = item["stator"]
            self.assertIn(stator, self.capability_leaves(pkg, "braking"))
            moving = {p for m in self.motions(seed, pkg).values() for p in m["parts"]}
            self.assertNotIn(stator, moving, f"seed {seed}: the stator must not move")
            gap = min(v1.mesh_distance(pkg.mesh(p), pkg.mesh(stator), MAX_BRAKE_GAP_M) for p in rotor["parts"])
            self.assertLessEqual(gap, MAX_BRAKE_GAP_M, f"seed {seed}: stator is not within {MAX_BRAKE_GAP_M} m of the rotor")


class TierB7LoadStructure(_V2Base):
    def test_backbone_is_connected_and_reaches_every_function(self):
        for seed, pkg in self.packages():
            members = set(self.evidence(seed, pkg, "load_structure")["members"])
            self.assertTrue(members, f"seed {seed}: no structural members")
            self.assertTrue(members <= self.capability_leaves(pkg, "load_structure"),
                            f"seed {seed}: structural members outside load_structure")
            interfaces = pkg.manifest["interfaces"]
            parent = {m: m for m in members}

            def find(x):
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            for i in interfaces:
                if i["a"] in members and i["b"] in members:
                    parent[find(i["a"])] = find(i["b"])
            self.assertEqual(len({find(m) for m in members}), 1, f"seed {seed}: structural members are disconnected")
            for capability in sorted(REQUIRED_CAPABILITIES - {"load_structure"}):
                leaves = self.capability_leaves(pkg, capability) - members
                reached = [i for i in interfaces if (i["a"] in members and i["b"] in leaves)
                           or (i["b"] in members and i["a"] in leaves)]
                self.assertTrue(reached, f"seed {seed}: {capability} is not attached to the structural backbone")


class TierB8HeatRejection(_V2Base):
    def test_surfaces_are_extended(self):
        for seed, pkg in self.packages():
            surfaces = self.evidence(seed, pkg, "heat_rejection")["surfaces"]
            self.assertTrue(surfaces)
            self.assertTrue(set(surfaces) <= self.capability_leaves(pkg, "heat_rejection"))
            area = sum(surface_area(pkg.mesh(s)) for s in surfaces)
            volume = sum(v1.volume_and_centroid(pkg.mesh(s))[0] for s in surfaces)
            sphere = 4 * math.pi * (3 * volume / (4 * math.pi)) ** (2 / 3)
            self.assertGreaterEqual(area / sphere, MIN_HEAT_AREA_RATIO,
                                    f"seed {seed}: heat surface area is only {area / sphere:.2f}x a sphere's")


class TierB9Controller(_V2Base):
    def test_housing_encloses_its_contents(self):
        for seed, pkg in self.packages():
            item = self.evidence(seed, pkg, "controller")
            inside = self.capability_leaves(pkg, "controller")
            housing = item["housing"]
            self.assertIn(housing, inside)
            self.assertGreaterEqual(len(item["contents"]), 2, f"seed {seed}: fewer than two enclosed parts")
            self.assertGreater(void_volume(pkg.mesh(housing)), 0.0, f"seed {seed}: housing has no cavity")
            for content in item["contents"]:
                self.assertIn(content, inside)
                pts = pkg.mesh(content).reshape(-1, 3)
                share = float(in_cavity(pts, pkg.mesh(housing)).mean())
                self.assertEqual(share, 1.0, f"seed {seed}: {content} is only {share:.0%} inside the housing cavity")


class TierB10ThreadedJoints(_V2Base):
    def test_threaded_joints_pass_through_a_hole(self):
        for seed, pkg in self.packages():
            threaded = [i for i in pkg.manifest["interfaces"] if i["kind"] == "threaded"]
            self.assertGreaterEqual(len(threaded), MIN_THREADED_JOINTS, f"seed {seed}: threaded joints")
            for item in threaded:
                origin = np.asarray(item["axis_point_m"], dtype=float)
                axis = np.asarray(item["axis_dir"], dtype=float)
                self.assertAlmostEqual(float(np.linalg.norm(axis)), 1.0, delta=1e-9)
                ok = False
                for holed, pin in ((item["a"], item["b"]), (item["b"], item["a"])):
                    h, p = pkg.mesh(holed), pkg.mesh(pin)
                    if (genus(h) >= 1 and line_hits(origin, axis, h) == 0
                            and surrounds_axis(h, origin, axis) and line_hits(origin, axis, p) >= 2):
                        ok = True
                        break
                self.assertTrue(ok, f"seed {seed}: threaded joint {item['id']} has no pin through a hole on its axis")


# --------------------------------------------------------------------------
# Tier C: Level-0 race coupling
# --------------------------------------------------------------------------

class TierC1Level0(_V2Base):
    def test_level0_race_uses_the_generated_vehicle(self):
        pkg = self.package(f"seed{SEEDS[0]}")
        with tempfile.TemporaryDirectory(prefix="fu_level0_") as tmp:
            tmp = Path(tmp)
            manifest = pkg.dir / "manifest.json"
            first, raw_first, error = run_evaluator(manifest, tmp / "a.json")
            self.assertIsNotNone(first, error)
            _, raw_second, error = run_evaluator(manifest, tmp / "b.json")
            self.assertEqual(raw_first, raw_second, f"evaluator is not deterministic {error}")
            self.assertEqual(set(first), EVAL_FIELDS, "evaluator output fields")
            self.assertEqual(first["manifest_sha256"], hashlib.sha256(manifest.read_bytes()).hexdigest())
            self.assertEqual(first["race_kernel"], RACE_KERNEL_ID)
            self.assertEqual(first["outcome"], "finished", "the generated vehicle must finish the Level-0 race")
            root_mass = pkg.nodes[pkg.manifest["root"]]["mass_kg"]
            self.assertAlmostEqual(first["mass_kg"] / root_mass, 1.0, delta=1e-9, msg="race mass is not the vehicle mass")
            pts = np.concatenate([pkg.mesh(n["id"]).reshape(-1, 3) for n in pkg.leaves()])
            extent = pts.max(axis=0) - pts.min(axis=0)
            self.assertTrue(0 < first["drag_area_m2"] <= 1.5 * extent[1] * extent[2], "drag area vs frontal extent")
            self.assertTrue(math.isfinite(first["race_time_s"]) and first["race_time_s"] > 0)
            self.assertLessEqual(abs(first["terminal_energy_boundary_residual_j"]), 1.0, "energy residual")

            heavy_dir = tmp / "heavy"
            shutil.copytree(pkg.dir, heavy_dir)
            heavy = json.loads((heavy_dir / "manifest.json").read_text(encoding="utf-8"))
            for node in heavy["nodes"]:
                if node["id"] == heavy["root"]:
                    node["mass_kg"] *= 1.5
            (heavy_dir / "manifest.json").write_text(json.dumps(heavy, sort_keys=True), encoding="utf-8")
            result, _, error = run_evaluator(heavy_dir / "manifest.json", tmp / "heavy.json")
            self.assertIsNotNone(result, error)
            self.assertAlmostEqual(result["mass_kg"] / (1.5 * root_mass), 1.0, delta=1e-9)
            slower = result["outcome"] != "finished" or result["race_time_s"] > first["race_time_s"]
            self.assertTrue(slower, "a 50 % heavier vehicle did not get slower: the race ignores the vehicle")


if __name__ == "__main__":
    sys.exit(unittest.main())
