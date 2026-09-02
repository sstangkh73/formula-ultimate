from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.geometry_witness import (
    GeometryWitnessViolation,
    WITNESS_VERSION,
    canonical_sha256,
    compare_geometry_witness,
    symmetric_eigen_3x3,
    validate_witness_config,
)


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/cad/step_freecad_geometry_witness_v2.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def reverse_mappings(value):
    if isinstance(value, dict):
        return {key: reverse_mappings(item) for key, item in reversed(tuple(value.items()))}
    if isinstance(value, list):
        return [reverse_mappings(item) for item in value]
    return value


def make_report(config: dict) -> dict:
    parts = []
    for part in config["parts"]:
        density = part["material_density_kg_per_m3"]
        geometric = [[1.0e-6, 0.0, 0.0], [0.0, 2.0e-6, 0.0], [0.0, 0.0, 3.0e-6]]
        mass_tensor = [[value * density for value in row] for row in geometric]
        surfaces = []
        for interface in part["interfaces"]:
            body = {
                "geometry_type": "cylindrical_surface",
                "surface_class": "Cylinder",
                "radius_m": interface["radius_m"],
                "axis": deepcopy(interface["axis"]),
                "axis_offset_point_m": deepcopy(interface["axis_offset_point_m"]),
                "axial_bounds_m": deepcopy(interface["axial_bounds_m"]),
                "area_m2": 1.0e-3,
            }
            surfaces.append({**body, "surface_signature_sha256": canonical_sha256(body)})
        parts.append({
            "part_id": part["part_id"],
            "step_file": part["step_file"],
            "step_sha256": part["step_sha256"],
            "step_bytes": 1000,
            "shape_type": "Compound",
            "solid_count": 1,
            "shell_count": 1,
            "is_valid": True,
            "volume_m3": part["expected"]["volume_m3"],
            "bounding_box_m": deepcopy(part["expected"]["bounding_box_m"]),
            "centre_of_mass_m": [0.0, 0.0, 0.0],
            "geometric_inertia_tensor_m5": geometric,
            "material_density_kg_per_m3": density,
            "mass_kg": part["expected"]["volume_m3"] * density,
            "mass_inertia_tensor_kg_m2": mass_tensor,
            "principal_moments_kg_m2": [density * 1.0e-6, density * 2.0e-6, density * 3.0e-6],
            "principal_axes": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]],
            "cylindrical_surfaces": surfaces,
            "unsupported_measurements": deepcopy(part["unsupported_measurements"]),
            "hidden_geometry_repair": False,
        })
    body = {
        "witness_version": WITNESS_VERSION,
        "source_manifest_sha256": config["source_manifest_sha256"],
        "freecad_version": "1.1.3",
        "occt_version": "7.9.2",
        "import_mode": "Part.Shape.read_step_no_repair",
        "hidden_geometry_repair": False,
        "parts": parts,
    }
    return {**body, "report_sha256": canonical_sha256(body)}


def rehash_report(report: dict) -> None:
    body = {key: value for key, value in report.items() if key != "report_sha256"}
    report["report_sha256"] = canonical_sha256(body)


class GeometryWitnessV2Tests(unittest.TestCase):
    def assert_code(self, expected: str, config: dict, report: dict) -> None:
        with self.assertRaises(GeometryWitnessViolation) as caught:
            compare_geometry_witness(config, report)
        self.assertEqual(expected, caught.exception.code)

    def test_config_freezes_all_five_exact_step_identities(self) -> None:
        result = validate_witness_config(load_config())
        self.assertEqual("passed", result["status"])
        self.assertEqual(5, len(result["parts"]))
        self.assertEqual(5, len({part["step_sha256"] for part in result["parts"]}))

    def test_reference_comparison_recovers_interfaces_but_forbids_design_use(self) -> None:
        config = load_config()
        result = compare_geometry_witness(config, make_report(config))
        self.assertEqual("passed", result["status"])
        self.assertEqual(5, result["part_count"])
        self.assertEqual("toolchain_cross_check", result["evidence_class"])
        self.assertFalse(result["design_use_allowed"])
        self.assertTrue(all(len(part["interfaces"]) == 1 for part in result["comparisons"]))

    def test_mapping_key_order_preserves_config_and_comparison_identity(self) -> None:
        config = load_config()
        report = make_report(config)
        reordered_config = reverse_mappings(config)
        reordered_report = reverse_mappings(report)
        self.assertEqual(validate_witness_config(config)["config_sha256"], validate_witness_config(reordered_config)["config_sha256"])
        self.assertEqual(compare_geometry_witness(config, report)["comparison_sha256"], compare_geometry_witness(reordered_config, reordered_report)["comparison_sha256"])

    def test_report_content_and_source_manifest_identity_fail_closed(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["volume_m3"] *= 2.0
        self.assert_code("report_identity_mismatch", config, report)

        report = make_report(config)
        report["source_manifest_sha256"] = "0" * 64
        rehash_report(report)
        self.assert_code("source_manifest_mismatch", config, report)

    def test_changed_step_hash_and_topology_fail_closed(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["step_sha256"] = "0" * 64
        rehash_report(report)
        self.assert_code("step_hash_mismatch", config, report)

        report = make_report(config)
        report["parts"][0]["solid_count"] = 2
        rehash_report(report)
        self.assert_code("invalid_imported_topology", config, report)

    def test_hidden_repair_and_nonfinite_measurement_fail_closed(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["hidden_geometry_repair"] = True
        rehash_report(report)
        self.assert_code("hidden_geometry_repair", config, report)

        report = make_report(config)
        report["parts"][0]["centre_of_mass_m"][0] = math.nan
        report["report_sha256"] = "0" * 64
        self.assert_code("canonicalization_error", config, report)

    def test_volume_bounds_mass_and_inertia_are_measured_constraints(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["volume_m3"] *= 1.01
        report["parts"][0]["mass_kg"] *= 1.01
        rehash_report(report)
        self.assert_code("volume_mismatch", config, report)

        report = make_report(config)
        report["parts"][0]["bounding_box_m"]["maximum"][0] += 0.001
        rehash_report(report)
        self.assert_code("bounding_box_mismatch", config, report)

        report = make_report(config)
        report["parts"][0]["mass_inertia_tensor_kg_m2"][0][0] *= 1.01
        rehash_report(report)
        self.assert_code("inertia_density_mismatch", config, report)

    def test_missing_and_ambiguous_geometric_signatures_fail_closed(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["cylindrical_surfaces"] = []
        rehash_report(report)
        self.assert_code("missing_interface_signature", config, report)

        report = make_report(config)
        report["parts"][0]["cylindrical_surfaces"].append(deepcopy(report["parts"][0]["cylindrical_surfaces"][0]))
        rehash_report(report)
        self.assert_code("ambiguous_interface_signature", config, report)

    def test_surface_identity_and_explicit_limitations_cannot_drift(self) -> None:
        config = load_config()
        report = make_report(config)
        report["parts"][0]["cylindrical_surfaces"][0]["area_m2"] *= 2.0
        rehash_report(report)
        self.assert_code("surface_identity_mismatch", config, report)

        report = make_report(config)
        report["parts"][0]["unsupported_measurements"] = []
        rehash_report(report)
        self.assert_code("limitation_mismatch", config, report)

    def test_symmetric_eigensolver_preserves_known_principal_values(self) -> None:
        values, axes = symmetric_eigen_3x3([[3.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 2.0]])
        self.assertEqual([1.0, 2.0, 3.0], values)
        for axis in axes:
            self.assertAlmostEqual(1.0, math.sqrt(sum(value * value for value in axis)))


if __name__ == "__main__":
    unittest.main()
