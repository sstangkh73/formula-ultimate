from __future__ import annotations

import copy
import json
from pathlib import Path
import unittest

from formula_ultimate.structural.geometry_mesh_bridge import GeometryMeshViolation, build_mesh, gmsh_text, validate_mesh, validate_protocol

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/development/geometry_mesh_bridge_v1.json"


class GeometryMeshBridgeTests(unittest.TestCase):
    def setUp(self):
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.spec = {"minimum": (0.0, 0.0, 0.0), "maximum": (0.01, 0.01, 0.01), "resolution": 0.01, "dimensions": (1, 1, 1)}

    def test_protocol_pins_both_dependencies_and_three_levels(self):
        result = validate_protocol(self.raw)
        self.assertEqual(result["route_count"], 2); self.assertEqual(result["level_count"], 3)

    def test_single_cell_has_six_positive_tetrahedra_and_exact_volume(self):
        mesh = build_mesh({(0, 0, 0): "material_alpha"}, self.spec, maximum_elements=100)
        report = validate_mesh(mesh, ["external_surface", "load_surface", "contact_surface"], self.raw["limits"])
        self.assertEqual(report["node_count"], 8); self.assertEqual(report["tetrahedron_count"], 6); self.assertEqual(report["triangle_count"], 12)
        self.assertAlmostEqual(report["volume_m3"], 1e-6, places=15)
        text = gmsh_text(mesh); self.assertIn("$MeshFormat", text); self.assertIn("material_alpha", text)

    def test_material_interface_is_persistent_semantic_set(self):
        mesh = build_mesh({(0, 0, 0): "a", (1, 0, 0): "b"}, {**self.spec, "maximum": (.02, .01, .01), "dimensions": (2, 1, 1)}, maximum_elements=200)
        report = validate_mesh(mesh, ["material_interface", "load_surface", "contact_surface"], self.raw["limits"])
        self.assertEqual(report["boundary_element_counts"]["material_interface"], 2)
        self.assertEqual(set(report["material_element_counts"]), {"a", "b"})

    def test_inverted_missing_set_wrong_units_and_budget_fail_closed(self):
        mesh = build_mesh({(0, 0, 0): "a"}, self.spec, maximum_elements=100)
        inverted = copy.deepcopy(mesh); inverted["tetrahedra"][0]["jacobian_m3"] = -1
        with self.assertRaisesRegex(GeometryMeshViolation, "inverted"):
            validate_mesh(inverted, ["load_surface"], self.raw["limits"])
        missing = copy.deepcopy(mesh); missing["triangles"] = [item for item in missing["triangles"] if item["set"] != "load_surface"]
        with self.assertRaisesRegex(GeometryMeshViolation, "missing"):
            validate_mesh(missing, ["load_surface"], self.raw["limits"])
        invalid = copy.deepcopy(self.raw); invalid["units"] = "mm"
        with self.assertRaisesRegex(GeometryMeshViolation, "units"):
            validate_protocol(invalid)
        with self.assertRaisesRegex(GeometryMeshViolation, "budget"):
            build_mesh({(0, 0, 0): "a"}, self.spec, maximum_elements=10)


if __name__ == "__main__": unittest.main()
