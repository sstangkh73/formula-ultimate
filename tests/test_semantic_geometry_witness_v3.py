from __future__ import annotations

from copy import deepcopy
import json
import math
from pathlib import Path
import unittest

from formula_ultimate.components.semantic_geometry_witness import SemanticWitnessViolation, canonical_sha256, compare_report, derive_datums, select_face_signatures, validate_config


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config/cad/semantic_geometry_witness_v3.json"


def load_config() -> dict:
    return json.loads(CONFIG.read_text(encoding="utf-8"))


def manifest(config: dict) -> dict:
    return {"manifest_sha256": config["source_manifest_sha256"], "hidden_geometry_repair": False, "candidates": [{"candidate_id": item["candidate_id"], "family": item["family"], "step_sha256": item["step_sha256"], "solid_count": item["expected_solid_count"], "datum_declarations": deepcopy(item["datums"])} for item in config["candidate_bindings"]]}


def face(surface: str, center: list[float], area: float, curvature: float = 0.0) -> dict:
    sample = {"u_fraction": 0.5, "v_fraction": 0.5, "k1_per_m": curvature, "k2_per_m": 0.0, "radii_m": [] if curvature == 0 else [1 / abs(curvature)]}
    body = {"surface_class": surface, "area_m2": area, "center_m": center, "bounds_m": {"minimum": [center[0] - 0.1, center[1] - 0.1, center[2]], "maximum": [center[0] + 0.1, center[1] + 0.1, center[2]]}, "normal": [0.0, 0.0, 1.0], "curvature_samples": [sample]}
    return {**body, "face_signature_sha256": canonical_sha256(body)}


def make_report(config: dict) -> dict:
    density = config["material_density_kg_per_m3"]; candidates = []
    for index, binding in enumerate(config["candidate_bindings"]):
        bounds = {"minimum": [0.0, 0.0, 0.0], "maximum": [1.0, 2.0, 3.0]}
        faces = [face("Plane", [0.0, 0.0, 0.0], 1.0), face("Cylinder", [0.0, 0.0, 1.5], 2.0, 10.0 + index), face("Plane", [0.0, 0.0, 3.0], 1.5)]
        path_axis = 2; regions = []
        for declaration in config["semantic_regions"]:
            selected = select_face_signatures(faces, declaration["selector"], path_axis, config["tolerances"]["region_tie_relative"])
            area = math.fsum(item["area_m2"] for item in faces if item["face_signature_sha256"] in selected)
            body = {"region_id": declaration["region_id"], "intent": declaration["intent"], "selector": declaration["selector"], "face_signatures": selected, "area_m2": area}
            regions.append({**body, "region_signature_sha256": canonical_sha256(body)})
        geometric = [[1e-6, 0.0, 0.0], [0.0, 2e-6, 0.0], [0.0, 0.0, 3e-6]]
        sections = [{"path_fraction": fraction, "area_m2": 0.01, "equivalent_radius_m": math.sqrt(0.01 / math.pi), "second_moment_proxy_m4": 1e-5} for fraction in config["sampling_protocol"]["section_path_fractions"]]
        candidates.append({
            "candidate_id": binding["candidate_id"], "family": binding["family"], "step_sha256": binding["step_sha256"], "shape_type": "Compound", "is_valid": True,
            "body_count": binding["expected_solid_count"], "solid_count": binding["expected_solid_count"], "shell_count": binding["expected_solid_count"],
            "volume_m3": 0.01, "surface_area_m2": 4.5, "material_density_kg_per_m3": density, "mass_kg": 0.01 * density, "centre_of_mass_m": [0.0, 0.0, 1.5],
            "geometric_inertia_tensor_m5": geometric, "mass_inertia_tensor_kg_m2": [[item * density for item in row] for row in geometric],
            "principal_moments_kg_m2": [density * 1e-6, density * 2e-6, density * 3e-6], "principal_axes": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "principal_axis_degeneracy_ratio": 0.1,
            "axis_aligned_bounds_m": bounds, "principal_oriented_bounds_m": {"method": "vertex_and_tessellation_projection", "axes": [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0], [0.0, 0.0, 1.0]], "minimum": [0.0, 0.0, 0.0], "maximum": [1.0, 2.0, 3.0]},
            "faces": faces, "curvature_spectrum": {"surface_class_counts": {"Cylinder": 1, "Plane": 2}, "surface_class_area_m2": {"Cylinder": 2.0, "Plane": 2.5}, "curvature_sample_count": 3, "finite_radius_count": 1, "minimum_sampled_radius_m": 1 / (10.0 + index), "maximum_sampled_radius_m": 1 / (10.0 + index)},
            "thickness_field": {"method": "axis_aligned_brep_line_material_spans", "probe_count": 27, "material_span_count": 2, "samples_m": [0.1, 0.2], "minimum_sampled_span_m": 0.1},
            "section_evolution": {"method": "thin_brep_slab_volume", "path_axis_index": path_axis, "path_length_m": 3.0, "samples": sections},
            "datums": derive_datums(bounds, binding["datums"]), "regions": regions,
            "path_witness": {"path_datum_id": binding["path_datum_id"], "path_axis_index": path_axis, "path_length_m": 3.0, "minimum_sampled_bend_radius_m": 1 / (10.0 + index), "cross_section_sample_count": 3},
            "clearance_interference": {"scope": "within_imported_candidate_solids", "solid_pair_count": binding["expected_solid_count"] * (binding["expected_solid_count"] - 1) // 2, "minimum_clearance_m": 0.01 if binding["expected_solid_count"] > 1 else None, "interference_volume_m3": 0.0},
            "swept_envelope": {"motion_model": "static_identity_only", "bounds_m": bounds, "envelope_volume_m3": 6.0},
            "limitations": ["sampled_not_global_thickness", "no_structural_validity"], "hidden_geometry_repair": False,
        })
    body = {"witness_version": config["witness_version"], "source_manifest_sha256": config["source_manifest_sha256"], "freecad_version": "1.1.3", "occt_version": "7.8.1", "import_mode": "Part.Shape.read_step_no_repair", "hidden_geometry_repair": False, "candidates": candidates}
    return {**body, "report_sha256": canonical_sha256(body)}


def rehash(report: dict) -> None:
    report["report_sha256"] = canonical_sha256({key: value for key, value in report.items() if key != "report_sha256"})


class SemanticGeometryWitnessV3Tests(unittest.TestCase):
    def assert_code(self, code: str, config: dict, report: dict) -> None:
        with self.assertRaises(SemanticWitnessViolation) as caught: compare_report(config, report)
        self.assertEqual(code, caught.exception.code)

    def test_config_covers_exact_ten_candidate_manifest(self) -> None:
        config = load_config(); result = validate_config(config, manifest(config))
        self.assertEqual("passed", result["status"]); self.assertEqual(10, result["candidate_count"])
        self.assertEqual(4, config["candidate_bindings"][-1]["expected_solid_count"])

    def test_complete_report_passes_without_structural_claim(self) -> None:
        result = compare_report(load_config(), make_report(load_config()))
        self.assertEqual("passed", result["status"]); self.assertEqual(10, result["candidate_count"]); self.assertFalse(result["structural_validity"])

    def test_face_candidate_datum_and_region_record_permutation_preserves_semantic_identity(self) -> None:
        config = load_config(); report = make_report(config); baseline = compare_report(config, report)["comparison_sha256"]
        report["candidates"].reverse()
        for candidate in report["candidates"]:
            candidate["faces"].reverse(); candidate["datums"].reverse(); candidate["regions"].reverse()
        rehash(report)
        self.assertEqual(baseline, compare_report(config, report)["comparison_sha256"])

    def test_changed_step_and_hidden_repair_fail_closed(self) -> None:
        config = load_config(); report = make_report(config); report["candidates"][0]["step_sha256"] = "0" * 64; rehash(report)
        self.assert_code("step_hash_mismatch", config, report)
        report = make_report(config); report["candidates"][0]["hidden_geometry_repair"] = True; rehash(report)
        self.assert_code("hidden_geometry_repair", config, report)

    def test_missing_datum_region_and_altered_region_fail_closed(self) -> None:
        config = load_config(); report = make_report(config); report["candidates"][0]["datums"].pop(); rehash(report)
        self.assert_code("datum_correspondence_mismatch", config, report)
        report = make_report(config); report["candidates"][0]["regions"].pop(); rehash(report)
        self.assert_code("missing_region", config, report)
        report = make_report(config); report["candidates"][0]["regions"][0]["face_signatures"] = []; body = {key: value for key, value in report["candidates"][0]["regions"][0].items() if key != "region_signature_sha256"}; report["candidates"][0]["regions"][0]["region_signature_sha256"] = canonical_sha256(body); rehash(report)
        self.assert_code("region_correspondence_mismatch", config, report)

    def test_face_signature_report_hash_and_nonfinite_value_fail_closed(self) -> None:
        config = load_config(); report = make_report(config); report["candidates"][0]["faces"][0]["area_m2"] *= 2; rehash(report)
        self.assert_code("face_signature_mismatch", config, report)
        report = make_report(config); report["report_sha256"] = "0" * 64
        self.assert_code("report_identity_mismatch", config, report)
        report = make_report(config); report["candidates"][0]["mass_kg"] = math.nan; report["report_sha256"] = "0" * 64
        self.assert_code("canonicalization_error", config, report)

    def test_ambiguous_face_signature_and_invalid_thickness_fail_closed(self) -> None:
        config = load_config(); report = make_report(config); report["candidates"][0]["faces"].append(deepcopy(report["candidates"][0]["faces"][0])); rehash(report)
        self.assert_code("ambiguous_face_signature", config, report)
        report = make_report(config); report["candidates"][0]["thickness_field"]["minimum_sampled_span_m"] = 0.2; rehash(report)
        self.assert_code("invalid_thickness_field", config, report)

    def test_sampling_protocol_and_manifest_mutation_fail_or_change_identity(self) -> None:
        config = load_config(); bad_manifest = manifest(config); bad_manifest["candidates"][0]["step_sha256"] = "0" * 64
        with self.assertRaises(SemanticWitnessViolation) as caught: validate_config(config, bad_manifest)
        self.assertEqual("source_manifest_mismatch", caught.exception.code)
        changed = deepcopy(config); changed["sampling_protocol"]["section_slab_fraction"] *= 2
        self.assertNotEqual(validate_config(config)["config_sha256"], validate_config(changed)["config_sha256"])


if __name__ == "__main__":
    unittest.main()
