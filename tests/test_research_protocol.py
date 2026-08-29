from __future__ import annotations

import copy
import json
from pathlib import Path
import tempfile
import unittest

from formula_ultimate.experiments import (
    CandidateDeclaration,
    EvidenceViolation,
    ResearchProtocol,
    admit_candidate_evidence,
)


ROOT = Path(__file__).resolve().parents[1]


class ResearchProtocolTests(unittest.TestCase):
    def setUp(self) -> None:
        self.protocol_payload = json.loads((
            ROOT / "config/experiments/research_experiment_protocol_v1.json"
        ).read_text(encoding="utf-8"))
        self.candidate_payload = json.loads((
            ROOT / "config/experiments/candidate_fu-c0001.json"
        ).read_text(encoding="utf-8"))

    def test_declared_protocol_and_candidate_are_admitted(self) -> None:
        protocol = ResearchProtocol.from_mapping(self.protocol_payload)
        candidate = CandidateDeclaration.from_mapping(self.candidate_payload)
        self.assertEqual("FU-C0001", candidate.candidate_id)
        self.assertEqual(protocol.protocol_id, candidate.protocol_id)
        self.assertEqual(31001, candidate.seed)

    def test_protocol_rejects_silent_geometry_repair(self) -> None:
        payload = copy.deepcopy(self.protocol_payload)
        payload["failure_policy"]["silent_geometry_repair"] = True
        with self.assertRaisesRegex(EvidenceViolation, "silent correction"):
            ResearchProtocol.from_mapping(payload)

    def test_candidate_rejects_internal_identity_mismatch(self) -> None:
        payload = copy.deepcopy(self.candidate_payload)
        payload["candidate"]["candidate_id"] = "FU-C9999"
        with self.assertRaisesRegex(EvidenceViolation, "differs inside"):
            CandidateDeclaration.from_mapping(payload)

    def test_candidate_requires_pre_registered_variables_and_finite_tolerances(self) -> None:
        payload = copy.deepcopy(self.candidate_payload)
        payload["dependent_variables"] = []
        with self.assertRaisesRegex(EvidenceViolation, "variables"):
            CandidateDeclaration.from_mapping(payload)
        payload = copy.deepcopy(self.candidate_payload)
        payload["tolerances"]["volume_relative"] = float("nan")
        with self.assertRaisesRegex(EvidenceViolation, "finite"):
            CandidateDeclaration.from_mapping(payload)

    def test_exact_step_hash_and_freecad_volume_feed_level0(self) -> None:
        protocol = ResearchProtocol.from_mapping(self.protocol_payload)
        declaration = CandidateDeclaration.from_mapping(self.candidate_payload)
        volume = declaration.spec.analytical_volume_m3
        measurement = {
            "source": "test",
            "volume_m3": volume,
            "solid_count": 1,
            "is_valid": True,
            "bounds_m": [0.2, 0.12, 0.008],
            "centre_of_mass_m": [0.0, 0.0, 0.004],
        }
        with tempfile.TemporaryDirectory() as temporary:
            step_path = Path(temporary) / "candidate.step"
            step_path.write_text("ISO-10303-21;\nEND-ISO-10303-21;\n", encoding="ascii")
            from formula_ultimate.experiments.research_protocol import sha256_file
            step_hash = sha256_file(step_path)
            manifest = {
                "candidate_id": declaration.candidate_id,
                "seed": declaration.seed,
                "spec": {"grammar_version": declaration.grammar_version},
                "step": {"header": "ISO-10303-21;", "sha256": step_hash},
                "cadquery_measurement": measurement,
            }
            freecad = {**measurement, "source": "FreeCAD STEP import", "step_sha256": step_hash}
            result = admit_candidate_evidence(
                protocol=protocol,
                declaration=declaration,
                manifest=manifest,
                freecad_report=freecad,
                step_path=step_path,
            )
        self.assertEqual("passed", result["status"])
        self.assertAlmostEqual(
            volume * declaration.spec.material.density_kg_per_m3,
            result["level0_from_freecad"]["component_mass_kg"],
        )

    def test_hash_mismatch_is_observable(self) -> None:
        protocol = ResearchProtocol.from_mapping(self.protocol_payload)
        declaration = CandidateDeclaration.from_mapping(self.candidate_payload)
        with tempfile.TemporaryDirectory() as temporary:
            step_path = Path(temporary) / "candidate.step"
            step_path.write_text("ISO-10303-21;\n", encoding="ascii")
            manifest = {
                "candidate_id": declaration.candidate_id,
                "seed": declaration.seed,
                "spec": {"grammar_version": declaration.grammar_version},
                "step": {"header": "ISO-10303-21;", "sha256": "WRONG"},
            }
            with self.assertRaisesRegex(EvidenceViolation, "STEP hash"):
                admit_candidate_evidence(
                    protocol=protocol,
                    declaration=declaration,
                    manifest=manifest,
                    freecad_report={},
                    step_path=step_path,
                )


if __name__ == "__main__":
    unittest.main()
