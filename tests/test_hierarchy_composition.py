"""Tests for the Work 153 seed-to-manifest composition and generator CLI."""

from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

import numpy as np

from formula_ultimate.hierarchy.composition import (
    DEFAULT_COMPOSITION_CONFIG,
    DEFAULT_MATERIAL_CATALOGUE,
    CompositionFailure,
    LeafMaterial,
    assign_materials,
    build_manifest,
    composition_config_sha256,
    load_leaf_materials,
    manifest_bytes,
    plan_vehicle,
)
from formula_ultimate.hierarchy.decomposition import DEFAULT_CONFIG, decompose
from formula_ultimate.hierarchy.layout import DEFAULT_LAYOUT_CONFIG
from formula_ultimate.hierarchy.leaf_geometry import read_binary_stl, volume_and_centroid
from formula_ultimate.hierarchy.part_tree import canonical_sha256

ROOT = Path(__file__).resolve().parents[1]
CAD_PYTHON = ROOT / ".tools" / "cadquery-mcp" / "Scripts" / "python.exe"
GENERATOR = ROOT / "scripts" / "hierarchy" / "generate_hierarchical_vehicle.py"
FAKE = (LeafMaterial("synthetic_test_material", 1000.0, "synthetic"),)
TOP_FIELDS = {"design_language_version", "seed", "config_sha256", "git_commit", "length_unit",
              "mass_unit", "contact_tolerance_m", "root", "nodes", "interfaces"}


def fake_measurements(plan):
    """Placeholder measurements for pure manifest tests (not mesh-derived)."""

    return {leaf.id: {"mass_kg": 1.0 + i, "center_of_mass_m": [float(i), 0.0, 1.0]}
            for i, leaf in enumerate(plan.layout.leaves)}


class DecomposeStartAttemptTests(unittest.TestCase):
    def test_default_is_unchanged_and_start_skips_earlier_attempts(self):
        first = decompose(11)
        self.assertEqual(decompose(11, start_attempt=0), first)
        later = decompose(11, start_attempt=first.attempt + 1)
        self.assertGreater(later.attempt, first.attempt)

    def test_rejects_negative_start(self):
        with self.assertRaises(ValueError):
            decompose(11, start_attempt=-1)


class MaterialTests(unittest.TestCase):
    def test_catalogue_records_are_read_at_run_time(self):
        catalogue = load_leaf_materials(ROOT / DEFAULT_MATERIAL_CATALOGUE)
        self.assertTrue(catalogue)
        for material in catalogue:
            self.assertGreater(material.density_kg_m3, 0)
            self.assertEqual(material.evidence_status, "synthetic")

    def test_assignment_is_deterministic(self):
        ids = ["b", "a", "c"]
        two = FAKE + (LeafMaterial("synthetic_other", 2000.0, "synthetic"),)
        self.assertEqual(assign_materials(5, ids, two), assign_materials(5, list(reversed(ids)), two))


class PlanTests(unittest.TestCase):
    def test_layout_failure_moves_to_next_decomposition_attempt(self):
        # Work 152: the first decomposition of seed 4 does not lay out.
        plan = plan_vehicle(4, FAKE)
        self.assertTrue(plan.rejected)
        self.assertGreater(plan.tree.attempt, decompose(4).attempt)

    def test_exhausted_plan_attempts_raise(self):
        with self.assertRaises(CompositionFailure):
            plan_vehicle(4, FAKE, composition=replace(DEFAULT_COMPOSITION_CONFIG, max_plan_attempts=1))

    def test_config_hash_tracks_every_input(self):
        base = composition_config_sha256(DEFAULT_CONFIG, DEFAULT_LAYOUT_CONFIG, DEFAULT_COMPOSITION_CONFIG, FAKE)
        variants = [
            composition_config_sha256(replace(DEFAULT_CONFIG, leaf_budget_max=231), DEFAULT_LAYOUT_CONFIG,
                                      DEFAULT_COMPOSITION_CONFIG, FAKE),
            composition_config_sha256(DEFAULT_CONFIG, replace(DEFAULT_LAYOUT_CONFIG, max_attempts=3),
                                      DEFAULT_COMPOSITION_CONFIG, FAKE),
            composition_config_sha256(DEFAULT_CONFIG, DEFAULT_LAYOUT_CONFIG,
                                      replace(DEFAULT_COMPOSITION_CONFIG, contact_tolerance_m=2e-4), FAKE),
            composition_config_sha256(DEFAULT_CONFIG, DEFAULT_LAYOUT_CONFIG, DEFAULT_COMPOSITION_CONFIG,
                                      (LeafMaterial("synthetic_test_material", 1001.0, "synthetic"),)),
        ]
        self.assertRegex(base, r"^[0-9a-f]{64}$")
        self.assertEqual(len({base, *variants}), 5)


class ManifestTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.plan = plan_vehicle(23, FAKE)
        cls.manifest = build_manifest(cls.plan, fake_measurements(cls.plan), "0" * 64, "abc")

    def test_exact_contract_fields(self):
        m = self.manifest
        self.assertEqual(set(m), TOP_FIELDS)
        self.assertEqual((m["seed"], m["length_unit"], m["mass_unit"]), (23, "m", "kg"))
        self.assertTrue(0 < m["contact_tolerance_m"] <= 5e-4)
        for node in m["nodes"]:
            if node["kind"] == "part":
                gen = node["generator"]
                self.assertEqual(gen["program_sha256"], canonical_sha256(gen["program"]))
                self.assertEqual(node["mesh"], f"meshes/{node['id']}.stl")
        for item in m["interfaces"]:
            self.assertEqual(set(item), {"id", "a", "b", "kind"})

    def test_root_mass_is_the_sum_of_leaf_measurements(self):
        root = next(n for n in self.manifest["nodes"] if n["id"] == self.manifest["root"])
        leaves = [n for n in self.manifest["nodes"] if n["kind"] == "part"]
        self.assertAlmostEqual(root["mass_kg"], sum(n["mass_kg"] for n in leaves), places=9)

    def test_missing_measurement_is_an_error(self):
        measurements = fake_measurements(self.plan)
        measurements.pop(next(iter(measurements)))
        with self.assertRaises(KeyError):
            build_manifest(self.plan, measurements, "0" * 64, "abc")

    def test_manifest_bytes_are_deterministic(self):
        again = build_manifest(plan_vehicle(23, FAKE), fake_measurements(self.plan), "0" * 64, "abc")
        self.assertEqual(manifest_bytes(self.manifest), manifest_bytes(again))
        self.assertEqual(json.loads(manifest_bytes(self.manifest)), self.manifest)


@unittest.skipUnless(CAD_PYTHON.is_file(), "pinned CadQuery runtime is absent")
class GeneratorCliTests(unittest.TestCase):
    def test_cli_writes_measured_package(self):
        with tempfile.TemporaryDirectory(prefix="fu_work153_") as tmp:
            out = Path(tmp) / "not_yet" / "pkg"
            done = subprocess.run([str(CAD_PYTHON), str(GENERATOR), "--seed", "37", "--out", str(out)],
                                  cwd=ROOT, capture_output=True, text=True, timeout=1200)
            self.assertEqual(done.returncode, 0, done.stdout + done.stderr)
            manifest = json.loads((out / "manifest.json").read_text(encoding="utf-8"))
            self.assertEqual(set(manifest), TOP_FIELDS)
            head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, capture_output=True,
                                  text=True, check=True).stdout.strip()
            self.assertEqual(manifest["git_commit"], head)
            parts = [n for n in manifest["nodes"] if n["kind"] == "part"]
            self.assertGreaterEqual(len(parts), 150)
            for node in parts[:: max(1, len(parts) // 20)]:
                volume, centroid = volume_and_centroid(read_binary_stl(out / node["mesh"]))
                self.assertAlmostEqual(node["mass_kg"] / (volume * node["density_kg_m3"]), 1.0, delta=1e-9)
                np.testing.assert_allclose(node["center_of_mass_m"], centroid, atol=1e-9, rtol=0)


if __name__ == "__main__":
    unittest.main()
