"""Tests for the goal v2 post-layout leaf through-bores (Work 157)."""

from __future__ import annotations

import json
import math
import random
import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import DEFAULT_MATERIAL_CATALOGUE, load_leaf_materials, plan_vehicle
from formula_ultimate.hierarchy.functional import V2_DECOMPOSITION_CONFIG, config_sha256_v2, with_leaf_grammar_versions
from formula_ultimate.hierarchy.leaf_geometry import (
    LEAF_GRAMMAR_VERSION,
    LeafProgramError,
    leaf_program,
    placement_transforms,
    with_placement,
)
from formula_ultimate.hierarchy.leaf_refinement import (
    REFINED_LEAF_GRAMMAR_VERSION,
    base_program,
    bore_exits,
    bore_program,
    refine_layout,
    refinement_config_record,
    refinement_problems,
    validate_refined_program,
)


ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"


def _program(seed: int = 3, length: float = 0.2) -> dict:
    return leaf_program(random.Random(seed), length, leaf_id="t")


def _fitting_bore(program: dict, tilt: float = math.radians(12.0)) -> dict:
    rho = program["contact"]["inscribed_radius_m"] - program["tessellation"]["linear_tolerance_m"]
    radius = 0.15 * rho
    assert 0.5 * program["contact"]["height_m"] * math.tan(tilt) + radius / math.cos(tilt) < 0.9 * rho
    return bore_program(program, radius, tilt, 0.7)


def _flat_program() -> dict:
    for seed in range(200):
        program = _program(seed)
        if program["contact"]["height_m"] < program["contact"]["inscribed_radius_m"]:
            return program
    raise AssertionError("no flat leaf program in 200 draws")


class BoreProgramTests(unittest.TestCase):
    def test_bore_round_trips_to_the_placed_program(self):
        placed = with_placement(_flat_program(), placement_transforms("y", True, 0.4, [0.1, -0.2, 0.3]))
        refined = _fitting_bore(placed)
        self.assertEqual(refined["leaf_grammar_version"], REFINED_LEAF_GRAMMAR_VERSION)
        self.assertEqual([f["operator"] for f in refined["candidate"]["features"][:3]],
                         ["section", "extrude", "bore"])
        validate_refined_program(refined)
        self.assertEqual(base_program(refined), placed)
        self.assertEqual(base_program(placed), placed)

    def test_exits_lie_on_the_caps_at_the_tilt_offset(self):
        program = _flat_program()
        tilt, azimuth = math.radians(12.0), 0.7
        refined = _fitting_bore(program, tilt)
        exits = bore_exits(refined)
        h = program["contact"]["height_m"]
        offset = 0.5 * h * math.tan(tilt) * np.array([math.cos(azimuth), math.sin(azimuth)])
        np.testing.assert_allclose(exits["cap0"][0], [-offset[0], -offset[1], 0.0], atol=1e-12)
        np.testing.assert_allclose(exits["cap1"][0], [offset[0], offset[1], h], atol=1e-12)
        rho = program["contact"]["inscribed_radius_m"] - program["tessellation"]["linear_tolerance_m"]
        self.assertAlmostEqual(exits["cap0"][1], 0.15 * rho / math.cos(tilt))

    def test_bore_reaching_the_side_wall_is_rejected(self):
        program = _flat_program()
        rho = program["contact"]["inscribed_radius_m"]
        with self.assertRaises(LeafProgramError):
            bore_program(program, rho, 0.0, 0.0)
        with self.assertRaises(LeafProgramError):
            bore_program(program, 0.1 * rho, 0.2, 0.0, (rho, 0.0))

    def test_tampered_bore_axis_is_rejected(self):
        refined = _fitting_bore(_flat_program())
        refined["candidate"]["features"][2]["parameters"]["length_m"] *= 0.01
        with self.assertRaises(LeafProgramError):
            validate_refined_program(refined)
        refined = _fitting_bore(_flat_program())
        refined["candidate"]["features"][2]["parameters"]["direction"] = [1.0, 0.0, 0.0]
        with self.assertRaises(LeafProgramError):
            validate_refined_program(refined)


class RefineLayoutTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
        cls.plan = plan_vehicle(5, catalogue, V2_DECOMPOSITION_CONFIG)
        cls.refined = refine_layout(cls.plan.layout)

    def test_refinement_is_deterministic_and_rule_clean(self):
        again = refine_layout(self.plan.layout)
        self.assertEqual([leaf.program for leaf in again.leaves], [leaf.program for leaf in self.refined.leaves])
        self.assertEqual(refinement_problems(self.plan.layout, self.refined), [])
        self.assertEqual(self.refined.interfaces, self.plan.layout.interfaces)

    def test_a_substantial_share_of_leaves_is_bored(self):
        versions = [leaf.program["leaf_grammar_version"] for leaf in self.refined.leaves]
        bored = versions.count(REFINED_LEAF_GRAMMAR_VERSION)
        self.assertEqual(bored + versions.count(LEAF_GRAMMAR_VERSION), len(versions))
        self.assertGreater(bored / len(versions), 0.25)

    def test_exit_on_a_contact_patch_is_reported(self):
        # Move one bored leaf's exit onto the centre of a cap it receives contact on.
        from formula_ultimate.hierarchy.leaf_refinement import contact_patches

        patches = contact_patches(self.plan.layout)
        for index, leaf in enumerate(self.refined.leaves):
            if leaf.program["leaf_grammar_version"] == REFINED_LEAF_GRAMMAR_VERSION and patches[leaf.id]:
                break
        else:
            self.skipTest("no bored leaf with a received patch")
        program = leaf.program
        p = program["candidate"]["features"][2]["parameters"]
        d = np.asarray(p["direction"])
        h = program["contact"]["height_m"]
        cap = next(iter(patches[leaf.id]))
        target_local = np.array([0.0, 0.0, 0.0 if cap == "cap0" else h])
        # Axis through the cap centre: shift the origin laterally.
        point = np.asarray(p["origin_m"]) + (target_local[2] - p["origin_m"][2]) / d[2] * d
        tampered = json.loads(json.dumps(program))
        origin = np.asarray(p["origin_m"]) - np.array([point[0], point[1], 0.0])
        tampered["candidate"]["features"][2]["parameters"]["origin_m"] = [float(v) for v in origin]
        leaves = list(self.refined.leaves)
        leaves[index] = replace(leaf, program=tampered)
        problems = refinement_problems(self.plan.layout, replace(self.refined, leaves=tuple(leaves)))
        self.assertTrue(any(leaf.id in item for item in problems), problems)

    def test_manifest_records_each_leaf_grammar(self):
        program = self.refined.leaves[0].program
        manifest = {"nodes": [{"id": "a", "kind": "assembly"},
                              {"id": "p", "kind": "part", "generator": {
                                  "grammar_version": LEAF_GRAMMAR_VERSION, "program": program,
                                  "program_sha256": "x"}}]}
        out = with_leaf_grammar_versions(manifest)
        self.assertEqual(out["nodes"][1]["generator"]["grammar_version"], program["leaf_grammar_version"])
        self.assertEqual(manifest["nodes"][1]["generator"]["grammar_version"], LEAF_GRAMMAR_VERSION)
        self.assertNotEqual(config_sha256_v2("0" * 64), config_sha256_v2("0" * 64, refinement_config_record()))


CAD_CHECK = r"""
import json, sys
from pathlib import Path
root = Path(sys.argv[1])
sys.path.insert(0, str(root / "scripts" / "hierarchy"))
from functional_realization import realize_program
from formula_ultimate.hierarchy.leaf_geometry import closure_problems, read_binary_stl
import numpy as np
programs = json.loads(Path(sys.argv[2]).read_text())
out = {}
for name, program in programs.items():
    path = Path(sys.argv[3]) / f"{name}.stl"
    measured = realize_program(program, path, 1000.0)
    tris = read_binary_stl(path)
    verts, index = np.unique(tris.reshape(-1, 3), axis=0, return_inverse=True)
    faces = index.reshape(-1, 3)
    edges = np.unique(np.sort(np.concatenate([faces[:, [0, 1]], faces[:, [1, 2]], faces[:, [2, 0]]]), axis=1), axis=0)
    out[name] = {"mass": measured["mass_kg"], "closure": closure_problems(tris),
                 "euler": int(len(verts) - len(edges) + len(faces))}
print(json.dumps(out))
"""


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class BoreRealizationTests(unittest.TestCase):
    def test_bored_leaf_is_closed_with_one_through_hole_and_less_mass(self):
        plain = with_placement(_flat_program(), placement_transforms("x", False, 0.3, [0.5, 0.0, 0.2]))
        programs = {"plain": plain, "bored": _fitting_bore(plain)}
        with tempfile.TemporaryDirectory() as tmp:
            spec = Path(tmp) / "programs.json"
            spec.write_text(json.dumps(programs), encoding="utf-8")
            done = subprocess.run([str(CAD_PYTHON), "-c", CAD_CHECK, str(ROOT), str(spec), tmp], cwd=ROOT,
                                  capture_output=True, text=True, timeout=600)
        self.assertEqual(done.returncode, 0, done.stderr)
        result = json.loads(done.stdout.strip().splitlines()[-1])
        self.assertEqual(result["plain"]["closure"], [])
        self.assertEqual(result["bored"]["closure"], [])
        self.assertEqual(result["plain"]["euler"], 2)
        self.assertEqual(result["bored"]["euler"], 0)  # genus 1
        self.assertLess(result["bored"]["mass"], result["plain"]["mass"])


if __name__ == "__main__":
    unittest.main()
