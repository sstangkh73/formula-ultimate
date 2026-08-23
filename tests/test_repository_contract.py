from __future__ import annotations

import re
import tomllib
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class RepositoryContractTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
