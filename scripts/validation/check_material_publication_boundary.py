"""Fail closed when public material records lack redistribution evidence.

This validator is a repository publication control, not a legal opinion.  It
checks machine-readable declarations and obvious path leaks.  Human provenance
and source-licence review remain mandatory.
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath
from typing import Iterable, Iterator, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]

ADMITTED_RIGHTS = {"public_domain", "open_licensed", "permission_granted"}
MATERIAL_PROPERTY_KEYS = {
    "density_kg_m3",
    "density_kg_per_m3",
    "young_modulus_pa",
    "youngs_modulus_pa",
    "poisson_ratio",
    "shear_modulus_pa",
    "yield_strength_pa",
    "yield_stress_pa",
    "ultimate_strength_pa",
    "fracture_toughness_pa_sqrt_m",
    "thermal_conductivity_w_per_m_k",
    "specific_heat_capacity_j_per_kg_k",
    "thermal_expansion_per_k",
}
SOURCE_DOCUMENT_SUFFIXES = {".csv", ".doc", ".docx", ".pdf", ".tsv", ".xls", ".xlsx"}
MATERIAL_PATH_HINTS = {"asm", "cmh17", "cmh-17", "datasheet", "material", "materials", "matweb", "mmpds"}
HEX64 = re.compile(r"^[0-9a-f]{64}$")


@dataclass(frozen=True, order=True)
class Finding:
    path: str
    location: str
    message: str

    def render(self) -> str:
        return f"{self.path}:{self.location}: {self.message}"


def repository_paths(root: Path) -> tuple[PurePosixPath, ...]:
    """Return tracked and non-ignored untracked paths, including force-added files."""

    process = subprocess.run(
        ["git", "ls-files", "--cached", "--others", "--exclude-standard", "-z"],
        cwd=root,
        check=True,
        capture_output=True,
    )
    return tuple(
        PurePosixPath(raw.decode("utf-8"))
        for raw in process.stdout.split(b"\0")
        if raw
    )


def iter_mappings(value: object, location: str = "$") -> Iterator[tuple[str, Mapping[str, object]]]:
    if isinstance(value, dict):
        yield location, value
        for key, child in value.items():
            yield from iter_mappings(child, f"{location}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            yield from iter_mappings(child, f"{location}[{index}]")


def is_material_record(value: Mapping[str, object]) -> bool:
    properties = value.get("properties")
    return (
        isinstance(value.get("material_id"), str)
        and isinstance(value.get("evidence_status"), str)
        and isinstance(properties, dict)
        and bool(MATERIAL_PROPERTY_KEYS.intersection(properties))
    )


def _required_text(
    rights: Mapping[str, object], key: str, path: str, location: str, findings: list[Finding]
) -> str | None:
    value = rights.get(key)
    if not isinstance(value, str) or not value.strip():
        findings.append(Finding(path, location, f"publication_rights.{key} must be non-empty text"))
        return None
    return value.strip()


def validate_publication_rights(
    rights: object, *, path: str, location: str
) -> list[Finding]:
    findings: list[Finding] = []
    if not isinstance(rights, dict):
        return [Finding(path, location, "sourced material requires a publication_rights object")]

    status = rights.get("status")
    if status not in ADMITTED_RIGHTS:
        findings.append(
            Finding(
                path,
                location,
                "publication_rights.status must be public_domain, open_licensed, or permission_granted",
            )
        )
    if rights.get("redistribution_allowed") is not True:
        findings.append(Finding(path, location, "publication_rights.redistribution_allowed must be true"))

    evidence_uri = _required_text(rights, "evidence_uri", path, location, findings)
    if evidence_uri is not None and not evidence_uri.startswith(("https://", "http://")):
        findings.append(Finding(path, location, "publication_rights.evidence_uri must be an HTTP(S) URI"))

    evidence_sha256 = _required_text(rights, "evidence_sha256", path, location, findings)
    if evidence_sha256 is not None and HEX64.fullmatch(evidence_sha256) is None:
        findings.append(Finding(path, location, "publication_rights.evidence_sha256 must be lowercase SHA-256"))

    verified_on = _required_text(rights, "verified_on", path, location, findings)
    if verified_on is not None:
        try:
            parsed = date.fromisoformat(verified_on)
        except ValueError:
            findings.append(Finding(path, location, "publication_rights.verified_on must be ISO YYYY-MM-DD"))
        else:
            if parsed > date.today():
                findings.append(Finding(path, location, "publication_rights.verified_on cannot be in the future"))

    if status == "public_domain":
        _required_text(rights, "jurisdiction", path, location, findings)
        _required_text(rights, "legal_basis", path, location, findings)
    elif status == "open_licensed":
        _required_text(rights, "license_id", path, location, findings)
        _required_text(rights, "required_notice", path, location, findings)
    elif status == "permission_granted":
        _required_text(rights, "permission_reference", path, location, findings)
        scope = rights.get("permission_scope")
        if not isinstance(scope, list) or "public_git_redistribution" not in scope:
            findings.append(
                Finding(
                    path,
                    location,
                    "permission_scope must include public_git_redistribution",
                )
            )
    return findings


def validate_json_payload(path: PurePosixPath, payload: object) -> list[Finding]:
    findings: list[Finding] = []
    path_text = path.as_posix()
    for location, record in iter_mappings(payload):
        rights = record.get("publication_rights")
        if isinstance(rights, dict) and rights.get("status") == "restricted_private":
            findings.append(
                Finding(path_text, location, "restricted_private content cannot be committed publicly")
            )

        if not is_material_record(record):
            continue

        evidence_status = record["evidence_status"]
        claim_boundary = record.get("claim_boundary")
        design_use_allowed = (
            claim_boundary.get("design_use_allowed")
            if isinstance(claim_boundary, dict)
            else None
        )
        if evidence_status == "synthetic":
            if design_use_allowed is not False:
                findings.append(
                    Finding(
                        path_text,
                        location,
                        "synthetic material record must set claim_boundary.design_use_allowed=false",
                    )
                )
        elif evidence_status == "sourced":
            findings.extend(
                validate_publication_rights(rights, path=path_text, location=location)
            )
        else:
            findings.append(
                Finding(path_text, location, "material evidence_status must be synthetic or sourced")
            )
    return findings


def _is_material_source_document(path: PurePosixPath) -> bool:
    if path.suffix.lower() not in SOURCE_DOCUMENT_SUFFIXES:
        return False
    tokens = {part.lower() for part in path.parts}
    stem = path.stem.lower()
    return bool(MATERIAL_PATH_HINTS.intersection(tokens)) or any(
        hint in stem for hint in MATERIAL_PATH_HINTS
    )


def validate_paths(root: Path, paths: Iterable[PurePosixPath]) -> list[Finding]:
    findings: list[Finding] = []
    for path in sorted(set(paths), key=lambda item: item.as_posix()):
        path_text = path.as_posix()
        if path.parts and path.parts[0].lower() == "private":
            findings.append(Finding(path_text, "$", "files below /private/ cannot be committed"))
            continue
        if path.parts and path.parts[0].lower() == "papers" and path.name != ".gitignore":
            findings.append(Finding(path_text, "$", "third-party paper files cannot be committed"))
            continue
        if _is_material_source_document(path):
            findings.append(
                Finding(
                    path_text,
                    "$",
                    "material source documents/data files must remain private; publish an admitted JSON record instead",
                )
            )
            continue
        if path.suffix.lower() != ".json":
            continue
        absolute = root / Path(*path.parts)
        if not absolute.is_file():
            continue
        try:
            payload = json.loads(absolute.read_text(encoding="utf-8"))
        except (OSError, UnicodeError, json.JSONDecodeError) as exc:
            findings.append(Finding(path_text, "$", f"cannot validate JSON: {exc}"))
            continue
        findings.extend(validate_json_payload(path, payload))
    return sorted(findings)


def run(root: Path = ROOT, paths: Sequence[PurePosixPath] | None = None) -> list[Finding]:
    selected = repository_paths(root) if paths is None else tuple(paths)
    return validate_paths(root, selected)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT, help="repository root")
    args = parser.parse_args(argv)
    root = args.root.resolve()
    findings = run(root)
    if findings:
        print("material publication boundary: FAILED", file=sys.stderr)
        for finding in findings:
            print(f"- {finding.render()}", file=sys.stderr)
        return 1
    print("material publication boundary: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
