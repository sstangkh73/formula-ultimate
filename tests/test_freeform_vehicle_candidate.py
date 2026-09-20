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

from formula_ultimate.search.freeform_vehicle_candidate import (  # noqa: E402
    FINAL_STATUS,
    INCOMPLETE_STATUS,
    FreeformVehicleError,
    canonical_sha256,
    check_packaging,
    evaluation_protocol,
    matched_difference,
    matched_report,
    summarize,
    validate_protocol,
)
from formula_ultimate.structural.geometry_general_evaluator import (  # noqa: E402
    validate_protocol as validate_evaluation_protocol,
)


CONFIG = ROOT / "config/development/freeform_vehicle_candidate_v1.json"
CADQUERY_PYTHON = ROOT / ".tools/cadquery-mcp/Scripts/python.exe"
HAS_CADQUERY_RUNTIME = CADQUERY_PYTHON.is_file()


def manifest_for(raw: dict, candidate: dict) -> dict:
    """A synthetic built manifest that satisfies every packaging gate."""

    components = []
    for index, component in enumerate(candidate["components"]):
        components.append({
            "component_id": component["component_id"],
            "function_tags": sorted(component["function_tags"]),
            "material_id": component["material_id"],
            "provenance": {"kind": component["geometry"]["kind"]},
            "valid": True,
            "solid_count": 1,
            "face_count": 6,
            "curved_face_count": 0,
            "volume_m3": 0.001,
            "mass_kg": 2.7,
            "center_m": [0.0, 0.0, 0.1],
            "bounding_box_m": {"minimum": [-0.01, -0.01, 0.09], "maximum": [0.01, 0.01, 0.11]},
            "step_path": f"artifacts/work139/test/{candidate['candidate_id']}/{component['component_id']}.step",
            "step_sha256": f"{index:064d}",
        })
    return {
        "candidate_id": candidate["candidate_id"],
        "role": candidate["role"],
        "components": components,
        "pairwise_intersections": [{"components": ["a", "b"], "intersection_m3": 0.0}],
        "keep_out_intersections": [{"keep_out_id": "protected", "component_id": "core", "intersection_m3": 0.0}],
        "mass_kg": sum(item["mass_kg"] for item in components),
        "volume_m3": sum(item["volume_m3"] for item in components),
        "assembly_step_sha256": "a" * 64,
        "declared_mass_kg": None,
        "manifest_sha256": "b" * 64,
    }


class DeclarationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))

    def test_frozen_declaration_is_valid(self) -> None:
        declaration = validate_protocol(self.raw)
        self.assertEqual(declaration["status"], "passed")
        self.assertEqual(declaration["candidate_count"], 2)
        self.assertGreaterEqual(declaration["freeform_component_count"], 1)

    def test_embedded_evaluation_template_is_a_valid_work138_protocol(self) -> None:
        candidate = next(item for item in self.raw["candidates"] if item["role"] == "freeform_variant")
        protocol = evaluation_protocol(self.raw, candidate, manifest_for(self.raw, candidate))
        declaration = validate_evaluation_protocol(protocol)
        self.assertEqual(declaration["candidate_count"], len(candidate["components"]))
        self.assertTrue(all(item["geometry"]["kind"] == "step_file" for item in protocol["candidates"]))
        self.assertTrue(all(item["declared_mass_kg"] is not None for item in protocol["candidates"]))

    def test_declaration_fails_closed(self) -> None:
        unadmitted = copy.deepcopy(self.raw)
        variant = next(item for item in unadmitted["candidates"] if item["role"] == "freeform_variant")
        target = next(item for item in variant["components"] if item["geometry"]["kind"] == "freeform_reference")
        target["geometry"]["corpus_candidate_id"] = "invented_shape_001"
        with self.assertRaisesRegex(FreeformVehicleError, "not an admitted corpus member"):
            validate_protocol(unadmitted)

        uncovered = copy.deepcopy(self.raw)
        uncovered["candidates"][0]["components"] = [
            item for item in uncovered["candidates"][0]["components"] if "propulsion" not in item["function_tags"]
        ]
        with self.assertRaisesRegex(FreeformVehicleError, "function tags are unsupported"):
            validate_protocol(uncovered)

        baseline_only = copy.deepcopy(self.raw)
        for candidate in baseline_only["candidates"]:
            candidate["role"] = "primitive_baseline"
        baseline_only["candidates"][1]["candidate_id"] = "second_baseline"
        with self.assertRaisesRegex(FreeformVehicleError, "primitive baseline and a free-form variant"):
            validate_protocol(baseline_only)

        zero_force = copy.deepcopy(self.raw)
        zero_force["candidates"][0]["components"][0]["load_case"]["force_n"] = [0.0, 0.0, 0.0]
        with self.assertRaisesRegex(FreeformVehicleError, "force must not be zero"):
            validate_protocol(zero_force)

    def test_matched_pair_must_differ_in_exactly_one_component(self) -> None:
        difference = matched_difference(self.raw)
        self.assertEqual(difference["changed_component_id"], "propulsor")
        self.assertEqual(difference["corpus_candidate_id"], "curved_branch_001")

        two_changes = copy.deepcopy(self.raw)
        variant = next(item for item in two_changes["candidates"] if item["role"] == "freeform_variant")
        variant["components"][0]["placement"]["translation_m"] = [0.05, 0.0, 0.15]
        with self.assertRaisesRegex(FreeformVehicleError, "exactly one component"):
            matched_difference(two_changes)

        no_change = copy.deepcopy(self.raw)
        by_role = {item["role"]: item for item in no_change["candidates"]}
        by_role["freeform_variant"]["components"] = copy.deepcopy(by_role["primitive_baseline"]["components"])
        with self.assertRaisesRegex(FreeformVehicleError, "exactly one component"):
            matched_difference(no_change)


class PackagingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        self.candidate = self.raw["candidates"][0]
        self.manifest = manifest_for(self.raw, self.candidate)

    def test_clean_packaging_passes(self) -> None:
        verdict = check_packaging(self.raw, self.manifest)
        self.assertEqual(verdict["status"], "passed")
        self.assertEqual(verdict["findings"], [])
        self.assertEqual(verdict["component_count"], len(self.candidate["components"]))

    def test_envelope_intersection_keepout_and_mass_are_gated(self) -> None:
        outside = copy.deepcopy(self.manifest)
        outside["components"][0]["bounding_box_m"]["maximum"][2] = 99.0
        self.assertIn("leaves the declared envelope", " ".join(check_packaging(self.raw, outside)["findings"]))

        overlapped = copy.deepcopy(self.manifest)
        overlapped["pairwise_intersections"][0]["intersection_m3"] = 1e-3
        self.assertIn("intersect", " ".join(check_packaging(self.raw, overlapped)["findings"]))

        invaded = copy.deepcopy(self.manifest)
        invaded["keep_out_intersections"][0]["intersection_m3"] = 1e-6
        self.assertIn("keep-out invaded", " ".join(check_packaging(self.raw, invaded)["findings"]))

        contradicted = copy.deepcopy(self.manifest)
        contradicted["declared_mass_kg"] = contradicted["mass_kg"] * 3.0
        self.assertIn("declared mass", " ".join(check_packaging(self.raw, contradicted)["findings"]))

        broken = copy.deepcopy(self.manifest)
        broken["components"][1]["solid_count"] = 2
        self.assertIn("not one valid solid", " ".join(check_packaging(self.raw, broken)["findings"]))


class SummaryTests(unittest.TestCase):
    def candidates(self, status: str = "passed", packaging: str = "passed") -> list[dict]:
        return [
            {
                "candidate_id": "primitive_baseline_139", "role": "primitive_baseline",
                "packaging": {"status": packaging, "mass_kg": 30.0, "findings": []},
                "components": [{"candidate_id": "primitive_baseline_139__propulsor", "status": "passed", "utilization": 0.01}],
            },
            {
                "candidate_id": "freeform_variant_139", "role": "freeform_variant",
                "packaging": {"status": "passed", "mass_kg": 28.0, "findings": []},
                "components": [{"candidate_id": "freeform_variant_139__propulsor", "status": status, "utilization": 0.3, "cause": "declared"}],
            },
        ]

    def controls(self, rejected: bool = True) -> list[dict]:
        return [{"control_id": f"c{index}", "rejected": rejected or index > 0} for index in range(8)]

    def test_clean_run_passes_and_claims_nothing(self) -> None:
        summary = summarize(self.candidates(), self.controls())
        self.assertEqual(summary["status"], FINAL_STATUS)
        self.assertFalse(summary["discovery_claim"])
        self.assertFalse(summary["promotion_allowed"])
        self.assertFalse(summary["race_time_claim"])
        self.assertFalse(summary["physical_validation"])

    def test_unresolved_components_are_counted_not_dropped(self) -> None:
        summary = summarize(self.candidates(status="unresolved_convergence"), self.controls())
        self.assertEqual(summary["status"], FINAL_STATUS)
        self.assertEqual(len(summary["unresolved_components"]), 1)
        self.assertEqual(summary["unresolved_components"][0][2], "unresolved_convergence")

    def test_unsupported_or_failed_packaging_is_incomplete(self) -> None:
        self.assertEqual(summarize(self.candidates(status="unsupported_representation"), self.controls())["status"], INCOMPLETE_STATUS)
        self.assertEqual(summarize(self.candidates(packaging="failed"), self.controls())["status"], INCOMPLETE_STATUS)

    def test_surviving_control_fails_the_run(self) -> None:
        self.assertEqual(summarize(self.candidates(), self.controls(rejected=False))["status"], "failed_controls")

    def test_matched_report_states_what_it_cannot_establish(self) -> None:
        report = matched_report(self.candidates(), {"changed_component_id": "propulsor", "corpus_candidate_id": "curved_branch_001"})
        self.assertAlmostEqual(report["mass_difference_kg"], -2.0, places=9)
        self.assertEqual(report["variant_component_utilization"], 0.3)
        self.assertIn("no superiority, discovery or promotion", report["interpretation"])

    def test_canonical_hash_is_stable(self) -> None:
        self.assertEqual(canonical_sha256(self.candidates()), canonical_sha256(json.loads(json.dumps(self.candidates()))))


@unittest.skipUnless(HAS_CADQUERY_RUNTIME, "the builder runs under the pinned CadQuery runtime")
class BuilderTests(unittest.TestCase):
    def test_free_form_variant_builds_with_curved_faces_and_no_overlap(self) -> None:
        raw = json.loads(CONFIG.read_text(encoding="utf-8"))
        candidate = next(item for item in raw["candidates"] if item["role"] == "freeform_variant")
        with tempfile.TemporaryDirectory() as directory:
            work = Path(directory)
            manifest_path = work / "manifest.json"
            completed = subprocess.run(
                [
                    str(CADQUERY_PYTHON), str(ROOT / "scripts/cad/build_freeform_vehicle_candidate.py"),
                    "--config", str(CONFIG), "--candidate-id", candidate["candidate_id"],
                    "--output-root", str(ROOT / "artifacts/work139/test_build"),
                    "--manifest", str(manifest_path),
                ],
                cwd=ROOT, capture_output=True, text=True, check=False,
            )
            self.assertEqual(completed.returncode, 0, completed.stderr[-800:])
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        self.assertEqual(len(manifest["components"]), len(candidate["components"]))
        self.assertTrue(all(item["valid"] and item["solid_count"] == 1 for item in manifest["components"]))
        freeform = next(item for item in manifest["components"] if item["provenance"]["kind"] == "freeform_reference")
        self.assertEqual(freeform["provenance"]["corpus_candidate_id"], "curved_branch_001")
        self.assertGreater(freeform["curved_face_count"], 0)
        self.assertEqual(max(item["intersection_m3"] for item in manifest["pairwise_intersections"]), 0.0)
        self.assertEqual(check_packaging(raw, manifest)["status"], "passed")


if __name__ == "__main__":
    unittest.main()
