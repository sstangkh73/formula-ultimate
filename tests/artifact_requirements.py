"""Skip helpers for tests whose inputs live outside the repository.

Some tests replay recorded experiment evidence from ``artifacts/``. That
directory holds large generated run outputs and is deliberately excluded from
the repository by ``.gitignore``, so on a clean checkout — including every CI
run — the inputs are absent.

Without a guard those tests raise during setup, which reports as an error and
makes a green run impossible for anyone who did not produce the artifacts
locally. Skipping is the honest outcome: the test did not run, and the report
says so, rather than the suite claiming a failure that says nothing about the
code under test.

Use ``requires_artifacts`` on the class or method that needs them.
"""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ARTIFACTS = ROOT / "artifacts"


def artifacts_present(*relative_paths: str) -> bool:
    """Return True when every named path under ``artifacts/`` exists."""
    if not relative_paths:
        return ARTIFACTS.is_dir()
    return all((ROOT / path).exists() for path in relative_paths)


def requires_artifacts(*relative_paths: str):
    """Skip the decorated test unless the named recorded artifacts exist."""
    missing = [path for path in relative_paths if not (ROOT / path).exists()]
    if relative_paths:
        reason = (
            "recorded artifacts are not in the repository: "
            + ", ".join(missing or relative_paths)
        )
    else:
        reason = "the artifacts/ directory is not present in this checkout"
    return unittest.skipUnless(artifacts_present(*relative_paths), reason)
