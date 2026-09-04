#!/usr/bin/env python3
"""Validate and fingerprint the Work 093 typed topology corpus."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.freeform_solid_grammar import declaration_sha256 as solid_declaration_sha256  # noqa: E402
from formula_ultimate.search.topology_genome import canonical_bytes, validate_topology_corpus  # noqa: E402


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--solid-config", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    raw = json.loads(args.config.read_text(encoding="utf-8")); solid = json.loads(args.solid_config.read_text(encoding="utf-8"))
    source_identity = solid_declaration_sha256(solid)
    if raw["source_solid_declaration_sha256"] != source_identity:
        raise RuntimeError("source solid declaration identity mismatch")
    candidates = {item["candidate_id"]: item["family"] for item in solid["candidates"]}
    validation = validate_topology_corpus(raw, candidates)
    body = {
        "status": "passed", "genome_version": raw["genome_version"], "source_solid_declaration_sha256": source_identity,
        "genome_count": validation["genome_count"], "distinct_part_counts": validation["distinct_part_counts"],
        "unique_topology_signature_count": validation["unique_topology_signature_count"],
        "declaration_sha256": validation["declaration_sha256"], "descriptors": validation["descriptors"],
        "legacy_five_scalar_dependency": False, "cad_executed": False,
        "claim_boundary": "typed topology representation and pre-CAD traceability only",
    }
    result = {**body, "result_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest()}; write(args.output, result)
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        if reference != result: raise RuntimeError("topology corpus replay mismatch")
    print(json.dumps({"status": "passed", "genome_count": result["genome_count"], "unique_topology_signature_count": result["unique_topology_signature_count"], "result_sha256": result["result_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
