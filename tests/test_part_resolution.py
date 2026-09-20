from __future__ import annotations

import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.assembly.part_resolution import (  # noqa: E402
    FINAL_STATUS,
    JOINT_EVIDENCE,
    JOINT_STATUSES,
    PART_STATUSES,
    PartResolutionError,
    distinct_feature_scales,
    evaluate_joint,
    evaluate_part,
    summarize,
    validate_protocol,
)


CONFIG = ROOT / "config/development/part_resolution_gate_v1.json"
CADQUERY_PYTHON = ROOT / ".tools/cadquery-mcp/Scripts/python.exe"
HAS_CADQUERY_RUNTIME = CADQUERY_PYTHON.is_file()

REQUIREMENT = {"minimum_faces": 12, "minimum_curved_faces": 4, "minimum_distinct_feature_scales": 3, "minimum_edges": 20}
RESOLUTION = {"minimum_feature_m": 5e-05, "minimum_elements_across_feature": 1, "mesh_size_factor": 0.15}
PART = {"part_id": "subject", "part_class": "fastener", "source": "test", "geometry": {"kind": "step_file", "path": "x.step"}}


def measurement(**overrides):
    base = {
        "status": "measured", "valid": True, "solid_count": 1, "single_solid": True,
        "face_count": 34, "edge_count": 85, "curved_face_count": 17, "engagement_face_count": 2,
        "surface_types": {"BSPLINE": 2, "CYLINDER": 15, "PLANE": 17},
        "smallest_feature_m": 8.4e-05, "feature_scale_m": 0.00076,
        "edge_lengths_m": [8.4e-05, 0.0007, 0.004, 0.02],
        "volume_m3": 1.8e-06,
        "mesh": {"status": "meshed", "node_count": 90000, "tetrahedron_count": 60000,
                 "characteristic_length_m": 0.00066, "mesh_sha256": "0" * 64},
    }
    base.update(overrides)
    return base


def joint_measurement(**overrides):
    base = {
        "status": "measured", "clearance_m": 0.00015, "interference_volume_m3": 0.0,
        "penetration_depth_m": 0.0, "mating_face_pairs": 6, "overlap_area_m2": 0.0016,
        "engagement_face_count": 4, "single_solid": True,
    }
    base.update(overrides)
    return base


def joint(technology: str, fit=(0.0001, 0.0002), overlap=0.0001):
    return {
        "joint_id": f"{technology}_joint", "technology": technology, "parts": ["a", "b"],
        "placement": {}, "fit_range_m": list(fit), "minimum_overlap_area_m2": overlap,
    }


class DeclarationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_frozen_declaration_is_valid(self) -> None:
        declaration = validate_protocol(self.raw)
        self.assertEqual(declaration["status"], "passed")
        self.assertGreaterEqual(declaration["part_count"], 2)
        self.assertIn("threaded", declaration["technologies"])

    def test_declaration_fails_closed(self) -> None:
        invented = copy.deepcopy(self.raw)
        invented["joints"][0]["technology"] = "wishful_adhesion"
        with self.assertRaisesRegex(PartResolutionError, "not in the registry"):
            validate_protocol(invented)

        self_joined = copy.deepcopy(self.raw)
        self_joined["joints"][0]["parts"] = ["work135_bolt", "work135_bolt"]
        with self.assertRaisesRegex(PartResolutionError, "two distinct parts"):
            validate_protocol(self_joined)

        unknown_part = copy.deepcopy(self.raw)
        unknown_part["joints"][0]["parts"] = ["work135_bolt", "a_part_that_does_not_exist"]
        with self.assertRaisesRegex(PartResolutionError, "undeclared part"):
            validate_protocol(unknown_part)

        no_floor = copy.deepcopy(self.raw)
        no_floor["resolution"]["minimum_feature_m"] = 0.0
        with self.assertRaisesRegex(PartResolutionError, "minimum_feature_m"):
            validate_protocol(no_floor)

        seven = copy.deepcopy(self.raw)
        seven["controls"] = seven["controls"][:7]
        with self.assertRaisesRegex(PartResolutionError, "eight registered controls"):
            validate_protocol(seven)


class PartGateTests(unittest.TestCase):
    def test_detailed_part_passes(self) -> None:
        verdict = evaluate_part(PART, REQUIREMENT, RESOLUTION, measurement())
        self.assertEqual(verdict["status"], "passed_resolution")
        self.assertIsNone(verdict["cause"])
        self.assertGreater(verdict["elements_across_feature_scale"], 1.0)

    def test_primitive_part_is_insufficient(self) -> None:
        verdict = evaluate_part(PART, REQUIREMENT, RESOLUTION, measurement(
            face_count=5, curved_face_count=2, edge_count=6, engagement_face_count=0,
            surface_types={"CYLINDER": 2, "PLANE": 3}, edge_lengths_m=[0.006, 0.02, 0.28],
            smallest_feature_m=0.006, feature_scale_m=0.006,
        ))
        self.assertEqual(verdict["status"], "insufficient_resolution")
        self.assertIn("faces 5 < 12", verdict["cause"])

    def test_sliver_is_unmanufacturable(self) -> None:
        verdict = evaluate_part(PART, REQUIREMENT, RESOLUTION, measurement(smallest_feature_m=1e-06))
        self.assertEqual(verdict["status"], "unmanufacturable_feature")

    def test_geometry_verdict_precedes_the_mesh_verdict(self) -> None:
        verdict = evaluate_part(PART, REQUIREMENT, RESOLUTION, measurement(
            face_count=5, curved_face_count=1, edge_count=6,
            mesh={"status": "unresolved_mesh", "cause": "gmsh refused"},
        ))
        self.assertEqual(verdict["status"], "insufficient_resolution")
        self.assertEqual(verdict["mesh_failure"], "gmsh refused")

    def test_coarse_mesh_blocks_a_strength_claim(self) -> None:
        verdict = evaluate_part(PART, REQUIREMENT, RESOLUTION, measurement(
            mesh={"status": "meshed", "node_count": 10, "tetrahedron_count": 4,
                  "characteristic_length_m": 0.01, "mesh_sha256": "0" * 64},
        ))
        self.assertEqual(verdict["status"], "unresolved_measurement")
        self.assertIn("elements across", verdict["cause"])

    def test_missing_measurement_is_unresolved(self) -> None:
        self.assertEqual(evaluate_part(PART, REQUIREMENT, RESOLUTION, None)["status"], "unresolved_measurement")

    def test_feature_scales_count_decades(self) -> None:
        self.assertEqual(distinct_feature_scales({"edge_lengths_m": [0.0001, 0.001, 0.01]}), 3)
        self.assertEqual(distinct_feature_scales({"edge_lengths_m": [0.011, 0.012]}), 1)
        self.assertEqual(distinct_feature_scales({}), 0)


class JointGateTests(unittest.TestCase):
    def test_registry_covers_every_declared_technology(self) -> None:
        self.assertEqual(
            set(JOINT_EVIDENCE), {"threaded", "welded", "bonded", "interference", "integral"}
        )

    def test_bonded_joint_with_evidence_passes(self) -> None:
        verdict = evaluate_joint(joint("bonded"), joint_measurement())
        self.assertEqual(verdict["status"], "passed_joint_evidence")
        self.assertEqual(verdict["evidence_missing"], [])

    def test_threaded_joint_without_engagement_faces_is_unsupported(self) -> None:
        verdict = evaluate_joint(joint("threaded", fit=(0.0, 0.0005)), joint_measurement(
            clearance_m=0.0, engagement_face_count=0,
        ))
        self.assertEqual(verdict["status"], "unsupported_joint_evidence")
        self.assertIn("engagement_faces", verdict["evidence_missing"])

    def test_out_of_range_fit_is_its_own_status(self) -> None:
        verdict = evaluate_joint(joint("bonded"), joint_measurement(clearance_m=0.002))
        self.assertEqual(verdict["status"], "out_of_range_fit")

    def test_interference_needs_a_negative_fit(self) -> None:
        inside = evaluate_joint(joint("interference", fit=(-3e-05, -1e-05)),
                                joint_measurement(clearance_m=-2e-05, interference_volume_m3=6e-09))
        self.assertEqual(inside["status"], "passed_joint_evidence")
        outside = evaluate_joint(joint("interference", fit=(-3e-05, -1e-05)),
                                 joint_measurement(clearance_m=0.0001))
        self.assertEqual(outside["status"], "out_of_range_fit")

    def test_integral_joint_needs_one_continuous_solid(self) -> None:
        self.assertEqual(
            evaluate_joint(joint("integral"), joint_measurement(single_solid=False))["status"],
            "unsupported_joint_evidence",
        )

    def test_missing_measurement_is_unresolved(self) -> None:
        verdict = evaluate_joint(joint("welded"), None)
        self.assertEqual(verdict["status"], "unresolved_joint_measurement")
        self.assertEqual(verdict["required_evidence"], list(JOINT_EVIDENCE["welded"]))


class SummaryTests(unittest.TestCase):
    def parts(self, status: str = "passed_resolution"):
        return [{"part_id": "a", "status": "passed_resolution"}, {"part_id": "b", "status": status}]

    def joints(self, status: str = "passed_joint_evidence"):
        return [{"joint_id": "j1", "status": status}]

    def controls(self, rejected: bool = True):
        return [{"control_id": f"c{index}", "rejected": rejected or index > 0} for index in range(8)]

    def test_a_failing_subject_does_not_fail_the_run(self) -> None:
        summary = summarize(self.parts("insufficient_resolution"), self.joints("unsupported_joint_evidence"), self.controls())
        self.assertEqual(summary["status"], FINAL_STATUS)
        self.assertEqual(summary["parts_below_bar"], ["b"])
        self.assertEqual(summary["joints_without_evidence"], ["j1"])
        self.assertFalse(summary["discovery_claim"])
        self.assertFalse(summary["physical_validation"])

    def test_a_surviving_control_fails_the_run(self) -> None:
        self.assertEqual(summarize(self.parts(), self.joints(), self.controls(rejected=False))["status"], "failed_controls")

    def test_status_accounting_closes(self) -> None:
        summary = summarize(self.parts("unresolved_measurement"), self.joints(), self.controls())
        self.assertEqual(sum(summary["part_status_counts"].values()), 2)
        self.assertEqual(set(summary["part_status_counts"]), set(PART_STATUSES))
        self.assertEqual(set(summary["joint_status_counts"]), set(JOINT_STATUSES))

    def test_unregistered_status_is_refused(self) -> None:
        with self.assertRaisesRegex(PartResolutionError, "unregistered status"):
            summarize([{"part_id": "a", "status": "looks_detailed"}], [], [])


@unittest.skipUnless(HAS_CADQUERY_RUNTIME, "measurement runs under the pinned CadQuery runtime")
class MeasurementTests(unittest.TestCase):
    def test_reference_fastener_is_measurably_finer_than_the_vehicle_fastener(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            measurement_path = work / "measurement.json"
            completed = subprocess.run(
                [
                    str(CADQUERY_PYTHON), str(ROOT / "scripts/cad/measure_part_resolution.py"),
                    "--config", str(CONFIG), "--output-root", str(work / "cad"),
                    "--measurement", str(measurement_path),
                ],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr[-800:])
            measured = json.loads(measurement_path.read_text(encoding="utf-8"))
        reference = measured["parts"]["reference_m8_bolt"]
        vehicle = measured["parts"]["work135_bolt"]
        self.assertEqual(reference["status"], "measured")
        self.assertEqual(vehicle["status"], "measured")
        self.assertGreaterEqual(reference["face_count"], 12)
        self.assertGreaterEqual(reference["engagement_face_count"], 2)
        self.assertLess(vehicle["face_count"], 12)
        self.assertEqual(vehicle["engagement_face_count"], 0)
        self.assertLess(reference["smallest_feature_m"], vehicle["smallest_feature_m"])
        bonded = measured["joints"]["reference_bonded_lap"]
        self.assertEqual(bonded["status"], "measured")
        self.assertAlmostEqual(bonded["clearance_m"], 0.00015, places=6)


if __name__ == "__main__":
    unittest.main()
