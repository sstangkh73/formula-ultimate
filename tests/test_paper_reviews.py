from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "docs" / "research" / "paper_reviews" / "reading_manifest.json"
sys.path.insert(0, str(ROOT / "scripts" / "research"))

from extract_paper_corpus import normalize_authors  # noqa: E402

# papers/ is git-ignored (most PDFs are not redistributable), so a clean
# checkout, including CI, has no PDFs to compare against the manifest.
HAS_LOCAL_PDFS = any((ROOT / "papers").rglob("*.pdf"))


class PaperReviewTests(unittest.TestCase):
    def setUp(self) -> None:
        self.payload = json.loads(MANIFEST.read_text(encoding="utf-8"))
        self.records = self.payload["papers"]

    @unittest.skipUnless(HAS_LOCAL_PDFS, "downloaded papers are not in the repository (papers/ is git-ignored)")
    def test_manifest_matches_local_pdf_inventory(self) -> None:
        actual = {path.relative_to(ROOT).as_posix() for path in (ROOT / "papers").rglob("*.pdf")}
        recorded = {item["source_pdf"] for item in self.records}
        self.assertEqual(recorded, actual)
        self.assertEqual(self.payload["paper_count"], len(actual))

    def test_extraction_has_page_level_coverage(self) -> None:
        for item in self.records:
            with self.subTest(paper=item["id"]):
                self.assertEqual(item["page_count"], len(item["page_character_counts"]))
                self.assertGreater(item["page_count"], 0)
                self.assertGreaterEqual(item["text_coverage"], 0)
                self.assertLessEqual(item["text_coverage"], 1)
                self.assertRegex(item["sha256"], r"^[0-9a-f]{64}$")

    def test_public_manifest_contains_no_extracted_source_passages(self) -> None:
        raw = MANIFEST.read_text(encoding="utf-8")
        self.assertNotIn('"sections"', raw)
        self.assertNotIn('"evidence_sentences"', raw)
        for item in self.records:
            self.assertIn("section_headings", item)
            self.assertIn("evidence_pages", item)
            self.assertIn("bibliography", item)

    def test_bilingual_reports_exist_and_name_their_source(self) -> None:
        root = MANIFEST.parent / "by_paper"
        for item in self.records:
            en = root / f"{item['id']}_review.md"
            th = root / f"{item['id']}_review.th.md"
            with self.subTest(paper=item["id"]):
                self.assertTrue(en.is_file())
                self.assertTrue(th.is_file())
                self.assertIn(f"English source: `{en.name}`", th.read_text(encoding="utf-8"))

    def test_synthesis_links_every_report_in_both_languages(self) -> None:
        en = (MANIFEST.parent / "FULL_LIBRARY_SYNTHESIS_2026-09-28.md").read_text(encoding="utf-8")
        th = (MANIFEST.parent / "FULL_LIBRARY_SYNTHESIS_2026-09-28.th.md").read_text(encoding="utf-8")
        for item in self.records:
            with self.subTest(paper=item["id"]):
                self.assertIn(f"by_paper/{item['id']}_review.md", en)
                self.assertIn(f"by_paper/{item['id']}_review.th.md", th)

    def test_every_report_has_a_transfer_experiment_and_deep_reviews_are_labeled(self) -> None:
        root = MANIFEST.parent / "by_paper"
        deep_en = 0
        deep_th = 0
        for item in self.records:
            en = (root / f"{item['id']}_review.md").read_text(encoding="utf-8")
            th = (root / f"{item['id']}_review.th.md").read_text(encoding="utf-8")
            with self.subTest(paper=item["id"]):
                self.assertIn("| Target artifact/module |", en)
                self.assertIn("| Experiment and control |", en)
                self.assertIn("| Acceptance and failure evidence |", en)
                self.assertIn("| artifact/module เป้าหมาย |", th)
                self.assertIn("| experiment และ control |", th)
                self.assertIn("| หลักฐานผ่านและล้มเหลว |", th)
                self.assertIn("[local PDF](../../../../papers/", en)
                self.assertIn("[PDF ในเครื่อง](../../../../papers/", th)
                deep_en += "Decision-critical deep review" in en
                deep_th += "deep review สำหรับการตัดสินใจ" in th
        self.assertEqual(deep_en, 15)
        self.assertEqual(deep_th, 15)

    def test_author_normalization_accepts_manifest_and_source_shapes(self) -> None:
        self.assertEqual(normalize_authors(["Ada Lovelace", "Grace Hopper"]), ["Ada Lovelace", "Grace Hopper"])
        self.assertEqual(normalize_authors("Ada Lovelace"), ["Ada Lovelace"])
        self.assertEqual(normalize_authors(None), [])


if __name__ == "__main__":
    unittest.main()
