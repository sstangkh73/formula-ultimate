"""Tests for the v2 rolling roller chain (Work 163)."""

from __future__ import annotations

import dataclasses
import json
import math
import subprocess
import tempfile
import unittest
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import LeafMaterial
from formula_ultimate.hierarchy.direction_control import add_direction_control, direction_control_problems
from formula_ultimate.hierarchy.ground_contacts import add_ground_contacts, ground_contact_problems
from formula_ultimate.hierarchy.leaf_geometry import closure_problems, read_binary_stl, volume_and_centroid
from formula_ultimate.hierarchy.mechanisms import (
    DECK_ID,
    ClusterBounds,
    mechanism_problems,
    plan_mechanisms,
    prism_vertices,
)
from formula_ultimate.hierarchy.power_transmission import (
    DEFAULT_POWER_TRANSMISSION_CONFIG,
    TRANSMISSION_FUNCTIONS,
    _z_prism,
    add_power_transmission,
    bay_occupants,
    power_transmission_problems,
    transmission_ids,
)


ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
CATALOGUE = (LeafMaterial("test-material-a", 1000.0, "synthetic"),
             LeafMaterial("test-material-b", 2000.0, "synthetic"))
BOUNDS = ClusterBounds(lo=(-0.2, -1.3, -1.4), hi=(2.2, 0.6, 1.2), lowest_leaf="g1.p0",
                       lowest_point=(0.3, -0.2, -1.4))
NARROW = ClusterBounds(lo=(0.0, -0.1, 0.0), hi=(0.3, 0.1, 0.4), lowest_leaf="g1.p0",
                       lowest_point=(0.1, 0.0, 0.0))
INDEX = 6


def _layer(seed: int, bounds: ClusterBounds = BOUNDS):
    layer = add_ground_contacts(plan_mechanisms(seed, bounds, CATALOGUE), seed, CATALOGUE)
    return add_power_transmission(add_direction_control(layer, seed, CATALOGUE), seed, CATALOGUE)


def _ids(layer):
    assembly = {a.id: a for a in layer.assemblies}[f"m{INDEX}-power_transmission"]
    return transmission_ids(INDEX, len(assembly.children) // 3)


class TransmissionPlanningTests(unittest.TestCase):
    def test_layers_pass_every_recheck_for_many_seeds(self):
        counts = set()
        for bounds in (BOUNDS, NARROW):
            for seed in range(30):
                layer = _layer(seed, bounds)
                self.assertEqual(mechanism_problems(layer, bounds, ["g1.p0"]), [], f"seed {seed}")
                self.assertEqual(ground_contact_problems(layer), [], f"seed {seed}")
                self.assertEqual(direction_control_problems(layer), [], f"seed {seed}")
                self.assertEqual(power_transmission_problems(layer), [], f"seed {seed}")
                counts.add(len(layer.evidence["power_transmission"]["chain"]))
        self.assertEqual(counts, {2, 3})

    def test_deterministic_and_seed_driven(self):
        self.assertEqual(_layer(11), _layer(11))
        roller = transmission_ids(INDEX, 2)["stations"][0]["roller"]
        programs = [{p.id: p.program for p in _layer(s).parts}[roller] for s in (11, 23)]
        self.assertNotEqual(programs[0], programs[1])

    def test_structure_motions_and_evidence(self):
        layer = _layer(11)
        ids = _ids(layer)
        assembly = {a.id: a for a in layer.assemblies}[ids["assembly"]]
        self.assertEqual(assembly.functions, TRANSMISSION_FUNCTIONS)
        self.assertEqual(layer.root_children[-1], ids["assembly"])
        motions = {m["id"]: m for m in layer.motions}
        chain = layer.evidence["power_transmission"]["chain"]
        self.assertEqual(chain, [s["motion"] for s in ids["stations"]])
        self.assertGreaterEqual(len(chain), 2)
        kinds = {(i["a"], i["b"]): i["kind"] for i in layer.interfaces}
        for sid in ids["stations"]:
            motion = motions[sid["motion"]]
            self.assertEqual((motion["type"], motion["parts"], motion["axis_dir"]),
                             ("revolute", [sid["roller"]], [0.0, 0.0, 1.0]))
            self.assertGreaterEqual(motion["range_rad"], 2 * math.pi - 1e-9)
            self.assertEqual(kinds[(sid["boss"], DECK_ID)], "bonded")
            self.assertEqual(kinds[(sid["roller"], sid["post"])], "bearing")
        for a, b in zip(ids["stations"], ids["stations"][1:]):
            self.assertEqual(kinds[(a["roller"], b["roller"])], "rolling")

    def test_rollers_touch_and_full_turns_clear_everything(self):
        c = DEFAULT_POWER_TRANSMISSION_CONFIG.bearing_clearance_m
        for seed in (11, 23, 37):
            layer = _layer(seed)
            ids = _ids(layer)
            verts = {p.id: prism_vertices(p.program) for p in layer.parts}
            motions = {m["id"]: m for m in layer.motions}
            rollers = [sid["roller"] for sid in ids["stations"]]
            for a, b in zip(rollers, rollers[1:]):
                gap = float(np.linalg.norm(verts[a][:, None, :2] - verts[b][None, :, :2], axis=2).min())
                self.assertAlmostEqual(gap, c, delta=1e-9)
            for sid in ids["stations"]:
                centre = np.asarray(motions[sid["motion"]]["axis_point_m"][:2])
                roller_z = verts[sid["roller"]][:, 2]
                reach = float(np.linalg.norm(verts[sid["roller"]][:, :2] - centre, axis=1).max())
                own = {sid["roller"], sid["post"]}
                for pid, v in verts.items():
                    if pid in own or pid == DECK_ID:
                        continue
                    level = v[(v[:, 2] >= roller_z.min()) & (v[:, 2] <= roller_z.max())]
                    if len(level):
                        self.assertGreaterEqual(float(np.linalg.norm(level[:, :2] - centre, axis=1).min()),
                                                reach - 1e-12, (seed, sid["roller"], pid))
                self.assertGreater(float(roller_z.min()), float(verts[DECK_ID][:, 2].max()))

    def test_bay_occupants_cover_the_steering_sweep(self):
        layer = add_direction_control(add_ground_contacts(plan_mechanisms(11, BOUNDS, CATALOGUE), 11, CATALOGUE),
                                      11, CATALOGUE)
        discs = bay_occupants(layer)
        self.assertEqual(len(discs), 3)
        arm = max(r for _, r in discs)
        steer = next(m for m in layer.motions if m["id"].endswith(".steer"))
        self.assertTrue(any(np.allclose(c, steer["axis_point_m"][:2]) and r == arm for c, r in discs))

    def test_problems_detect_broken_transmission(self):
        layer = _layer(11)
        ids = _ids(layer)
        roller = ids["stations"][1]["roller"]
        moved = [dataclasses.replace(p, program=_z_prism(roller, "transmission_roller",
                                                          [[0.0, 0.0], [0.01, 0.0], [0.0, 0.01]],
                                                          0.01, 0.0, 0.0, 9.0))
                 if p.id == roller else p for p in layer.parts]
        problems = power_transmission_problems(dataclasses.replace(layer, parts=tuple(moved)))
        self.assertTrue(any(roller in p for p in problems), problems)
        partial = [dict(m, range_rad=1.0) if m["id"] == ids["stations"][0]["motion"] else m for m in layer.motions]
        problems = power_transmission_problems(dataclasses.replace(layer, motions=tuple(partial)))
        self.assertTrue(any("full-turn" in p for p in problems), problems)
        unlinked = tuple(i for i in layer.interfaces if i["kind"] != "rolling")
        problems = power_transmission_problems(dataclasses.replace(layer, interfaces=unlinked))
        self.assertTrue(any("rolling" in p for p in problems), problems)


CAD_CHECK = r"""
import json, sys
from pathlib import Path
root, spec, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
sys.path[:0] = [str(root / "src"), str(root), str(root / "scripts" / "hierarchy")]
from functional_realization import realize_program
programs = json.loads(spec.read_text(encoding="utf-8"))
print(json.dumps({k: realize_program(v, out / (k + ".stl"), 1000.0) for k, v in programs.items()}))
"""


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class TransmissionRealizationTests(unittest.TestCase):
    def test_roller_meshes_are_closed_and_keep_the_rolling_gap(self):
        layer = _layer(11)
        rollers = [sid["roller"] for sid in _ids(layer)["stations"]][:2]
        programs = {f"r{i}": {p.id: p.program for p in layer.parts}[r] for i, r in enumerate(rollers)}
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "rollers.json"
            spec.write_text(json.dumps(programs), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
            self.assertEqual(done.returncode, 0, done.stderr)
            meshes = {k: read_binary_stl(Path(tmp) / f"{k}.stl") for k in programs}
        for key, tris in meshes.items():
            self.assertEqual(closure_problems(tris), [], key)
            self.assertGreater(volume_and_centroid(tris)[0], 0.0)
        a, b = (meshes[k].reshape(-1, 3)[:, :2] for k in ("r0", "r1"))
        gap = float(np.linalg.norm(a[:, None, :] - b[None, :, :], axis=2).min())
        self.assertLess(gap, 1e-4)
        self.assertGreater(gap, 0.0)


if __name__ == "__main__":
    unittest.main()
