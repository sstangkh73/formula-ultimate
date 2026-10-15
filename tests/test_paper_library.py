from __future__ import annotations

import json
import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
LIBRARY = ROOT / "docs" / "research" / "paper_library"
SOURCES = LIBRARY / "sources"
MANIFEST = LIBRARY / "manifest_v1.json"
STATUSES = {"downloaded", "no_open_access_copy", "identity_unconfirmed", "download_failed"}
RELATIONS = {"direct", "indirect", "data"}


def load_sources() -> tuple[list[dict], list[dict]]:
    categories, papers = [], []
    for path in sorted(SOURCES.glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        categories.append(payload["category"])
        for paper in payload["papers"]:
            papers.append({**paper, "category": payload["category"]["key"]})
    return categories, papers


class PaperLibraryCatalogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.categories, self.papers = load_sources()

    def test_categories_are_unique_and_described_in_both_languages(self) -> None:
        keys = [c["key"] for c in self.categories]
        folders = [c["folder"] for c in self.categories]
        self.assertEqual(len(keys), len(set(keys)))
        self.assertEqual(len(folders), len(set(folders)))
        for category in self.categories:
            for field in ("title_en", "title_th", "scope_en", "scope_th"):
                self.assertTrue(category[field].strip(), f"{category['key']} lacks {field}")

    def test_papers_have_unique_prefixed_ids_and_required_fields(self) -> None:
        ids = [p["id"] for p in self.papers]
        self.assertEqual(len(ids), len(set(ids)), "duplicate paper ids")
        for paper in self.papers:
            with self.subTest(paper=paper["id"]):
                self.assertRegex(paper["id"], rf"^{paper['category']}-\d{{3}}$")
                self.assertIn(paper["relation"], RELATIONS)
                self.assertTrue(paper["title"].strip())
                self.assertTrue(paper["why_en"].strip())
                self.assertRegex(paper["why_th"], r"[฀-๿]", "Thai note must be Thai")
                if "arxiv" in paper:
                    self.assertRegex(paper["arxiv"], r"^\d{4}\.\d{4,5}$")
                if "doi" in paper:
                    self.assertTrue(paper["doi"].startswith("10."))

    def test_titles_are_not_duplicated(self) -> None:
        normalized = [re.sub(r"[^a-z0-9]+", " ", p["title"].lower()).strip() for p in self.papers]
        duplicates = {t for t in normalized if normalized.count(t) > 1}
        self.assertFalse(duplicates, f"duplicate titles: {sorted(duplicates)}")

    def test_work_102_catalog_papers_are_all_carried_over(self) -> None:
        carried = {p["prior_catalog_id"] for p in self.papers if p.get("prior_catalog_id")}
        self.assertEqual(carried, {f"P{n:02d}" for n in range(1, 63)})

    def test_manifest_covers_every_paper_with_a_recorded_status(self) -> None:
        manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))["papers"]
        self.assertEqual(set(manifest), {p["id"] for p in self.papers})
        for pid, entry in manifest.items():
            with self.subTest(paper=pid):
                self.assertIn(entry["status"], STATUSES)
                if entry["status"] == "downloaded":
                    self.assertRegex(entry["sha256"], r"^[0-9a-f]{64}$")
                    self.assertGreater(entry["bytes"], 0)
                    self.assertTrue(entry["local_path"].startswith("papers/"))
                    self.assertTrue(entry["local_path"].endswith(".pdf"))

    def test_downloaded_papers_stay_out_of_version_control(self) -> None:
        ignore = (ROOT / "papers" / ".gitignore").read_text(encoding="utf-8").split()
        self.assertIn("*", ignore)
        self.assertIn("!.gitignore", ignore)


if __name__ == "__main__":
    unittest.main()
