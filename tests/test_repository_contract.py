from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
    def test_every_english_markdown_has_a_thai_companion(self) -> None:
        excluded_parts = {
            ".agents",
            ".git",
            ".venv",
            "artifacts",
            "runs",
        }
        english_documents = sorted(
            path
            for path in ROOT.rglob("*.md")
            if not path.name.endswith(".th.md")
            and not any(part in excluded_parts for part in path.parts)
            and not any(part.endswith(".egg-info") for part in path.parts)
        )
        self.assertTrue(english_documents, "No maintained Markdown files found")

        for english in english_documents:
            thai = english.with_name(f"{english.stem}.th.md")
            relative_english = english.relative_to(ROOT)
            with self.subTest(english=str(relative_english)):
                self.assertTrue(
                    thai.is_file(),
                    f"Missing Thai companion for {relative_english}",
                )
                thai_text = thai.read_text(encoding="utf-8")
                self.assertGreater(
                    len(thai_text.strip()),
                    100,
                    f"Thai companion is unexpectedly empty: {thai.relative_to(ROOT)}",
                )
                self.assertIn(
                    f"`{english.name}`",
                    thai_text,
                    f"Thai companion must identify source {english.name}",
                )

    def test_required_governance_and_physics_documents_exist(self) -> None:
        required = {
            "AGENTS.md",
            "README.md",
            "CONTRIBUTING.md",
            "docs/RESEARCH_CHARTER.md",
            "docs/PHYSICS_SYSTEM_PLAN.md",
            "docs/DESIGN_LANGUAGE_BOUNDARY.md",
            "docs/VALIDATION_STRATEGY.md",
            "docs/WORK_PROTOCOL.md",
        }
        missing = sorted(path for path in required if not (ROOT / path).is_file())
        self.assertEqual([], missing, f"Missing required files: {missing}")

    def test_declared_package_boundaries_exist(self) -> None:
        package_root = ROOT / "src" / "formula_ultimate"
        packages = {
            "components",
            "topology",
            "physics",
            "simulation",
            "telemetry",
            "experiments",
        }
        missing = sorted(
            name for name in packages if not (package_root / name / "__init__.py").is_file()
        )
        self.assertEqual([], missing, f"Missing package boundaries: {missing}")

    def test_pyproject_is_valid_toml(self) -> None:
        with (ROOT / "pyproject.toml").open("rb") as handle:
            parsed = tomllib.load(handle)
        self.assertEqual("formula-ultimate", parsed["project"]["name"])

    def test_every_result_has_a_matching_plan(self) -> None:
        log_dir = ROOT / "docs" / "work_logs"
        result_pattern = re.compile(r"^(?P<prefix>.+)-result\.md$")
        for result in log_dir.glob("*-result.md"):
            match = result_pattern.match(result.name)
            self.assertIsNotNone(match)
            plan = log_dir / f"{match.group('prefix')}-plan.md"
            self.assertTrue(plan.is_file(), f"Missing plan for {result.name}")

    def test_every_completed_plan_has_a_matching_result(self) -> None:
        log_dir = ROOT / "docs" / "work_logs"
        plan_pattern = re.compile(r"^(?P<prefix>.+)-plan\.md$")
        for plan in log_dir.glob("*-plan.md"):
            if "Status: Completed" not in plan.read_text(encoding="utf-8"):
                continue
            match = plan_pattern.match(plan.name)
            self.assertIsNotNone(match)
            result = log_dir / f"{match.group('prefix')}-result.md"
            self.assertTrue(result.is_file(), f"Missing result for {plan.name}")


if __name__ == "__main__":
    unittest.main()
