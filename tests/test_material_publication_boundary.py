from __future__ import annotations

import sys
import unittest
from pathlib import Path, PurePosixPath


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts" / "validation"))

from check_material_publication_boundary import (  # noqa: E402
    run,
    validate_json_payload,
    validate_paths,
)


def material_record(evidence_status: str, **extra: object) -> dict[str, object]:
    return {
        "material_id": "fixture",
        "evidence_status": evidence_status,
        "properties": {"density_kg_per_m3": 1.0},
        "claim_boundary": {"design_use_allowed": evidence_status == "sourced"},
        **extra,
    }


def open_rights() -> dict[str, object]:
    return {
        "status": "open_licensed",
        "redistribution_allowed": True,
        "evidence_uri": "https://example.invalid/licence",
        "evidence_sha256": "a" * 64,
        "verified_on": "2026-09-28",
        "license_id": "CC-BY-4.0",
        "required_notice": "Example source under CC BY 4.0",
    }


class MaterialPublicationBoundaryTests(unittest.TestCase):
    def test_repository_passes_publication_boundary(self) -> None:
        self.assertEqual([], run(ROOT))

    def test_policy_documents_are_bilingual_and_cross_linked(self) -> None:
        pairs = (
            (ROOT / "LICENSE-DATA.md", ROOT / "LICENSE-DATA.th.md"),
            (
                ROOT / "docs" / "MATERIAL_DATA_POLICY.md",
                ROOT / "docs" / "MATERIAL_DATA_POLICY.th.md",
            ),
            (
                ROOT / "docs" / "MATERIAL_SOURCE_RIGHTS_REGISTER.md",
                ROOT / "docs" / "MATERIAL_SOURCE_RIGHTS_REGISTER.th.md",
            ),
        )
        for english, thai in pairs:
            with self.subTest(english=english.name):
                self.assertTrue(english.is_file())
                self.assertTrue(thai.is_file())
                self.assertIn(thai.name, english.read_text(encoding="utf-8"))
                self.assertIn(english.name, thai.read_text(encoding="utf-8"))

        policy = (ROOT / "docs" / "MATERIAL_DATA_POLICY.md").read_text(encoding="utf-8")
        licence = (ROOT / "LICENSE-DATA.md").read_text(encoding="utf-8")
        self.assertIn("MATERIAL_SOURCE_RIGHTS_REGISTER.md", policy)
        self.assertIn("MATERIAL_DATA_POLICY.md", licence)
        self.assertIn("MATERIAL_SOURCE_RIGHTS_REGISTER.md", licence)
        self.assertIn("/private/", (ROOT / ".gitignore").read_text(encoding="utf-8"))

    def test_synthetic_fixture_must_remain_ineligible_for_design(self) -> None:
        allowed = material_record("synthetic")
        rejected = material_record(
            "synthetic", claim_boundary={"design_use_allowed": True}
        )
        self.assertEqual([], validate_json_payload(PurePosixPath("allowed.json"), allowed))
        findings = validate_json_payload(PurePosixPath("rejected.json"), rejected)
        self.assertTrue(any("design_use_allowed=false" in item.message for item in findings))

    def test_sourced_record_requires_admitted_redistribution_evidence(self) -> None:
        findings = validate_json_payload(
            PurePosixPath("missing.json"), material_record("sourced")
        )
        self.assertTrue(any("publication_rights object" in item.message for item in findings))

        admitted = material_record("sourced", publication_rights=open_rights())
        self.assertEqual([], validate_json_payload(PurePosixPath("open.json"), admitted))

    def test_restricted_and_unknown_rights_fail_closed(self) -> None:
        restricted = material_record(
            "sourced",
            publication_rights={
                **open_rights(),
                "status": "restricted_private",
            },
        )
        findings = validate_json_payload(PurePosixPath("restricted.json"), restricted)
        self.assertTrue(any("cannot be committed" in item.message for item in findings))
        self.assertTrue(any("must be public_domain" in item.message for item in findings))

    def test_permission_must_cover_public_git_redistribution(self) -> None:
        rights = {
            **open_rights(),
            "status": "permission_granted",
            "permission_reference": "permission-001",
            "permission_scope": ["internal_research"],
        }
        findings = validate_json_payload(
            PurePosixPath("permission.json"),
            material_record("sourced", publication_rights=rights),
        )
        self.assertTrue(any("public_git_redistribution" in item.message for item in findings))

    def test_private_paths_papers_and_material_source_documents_are_rejected(self) -> None:
        paths = (
            PurePosixPath("private/record.json"),
            PurePosixPath("papers/source.pdf"),
            PurePosixPath("data/materials/vendor_datasheet.pdf"),
        )
        findings = validate_paths(ROOT, paths)
        self.assertEqual(3, len(findings))
        self.assertTrue(any("/private/" in item.message for item in findings))
        self.assertTrue(any("paper files" in item.message for item in findings))
        self.assertTrue(any("source documents" in item.message for item in findings))


if __name__ == "__main__":
    unittest.main()
