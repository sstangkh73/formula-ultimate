#!/usr/bin/env python3
"""Run and replay the matched Work 095 validity/manufacturing pilot."""
from __future__ import annotations

import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.constructive_validity import canonical_bytes, build_candidate, evaluate_candidate, validate_gate_config  # noqa: E402
from formula_ultimate.components.freeform_solid_grammar import declaration_sha256 as solid_sha256  # noqa: E402
from formula_ultimate.search.topology_mutation import protocol_sha256  # noqa: E402


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def verify_sources(config: dict, solid: dict, manifest: dict, primitive: dict) -> None:
    if solid_sha256(solid) != config["source_solid_declaration_sha256"] or manifest["declaration_sha256"] != config["source_solid_declaration_sha256"]:
        raise RuntimeError("Work 092 solid declaration identity mismatch")
    if primitive["source_manifest_sha256"] != config["source_primitive_manifest_sha256"]:
        raise RuntimeError("primitive witness manifest identity mismatch")
    work092 = {item["candidate_id"]: item["step_sha256"] for item in manifest["candidates"]}
    primitive_parts = {item["part_id"]: item["step_sha256"] for item in primitive["parts"]}
    for family in config["representation_families"]:
        actual = (primitive_parts if family["source_collection"] == "primitive_witness" else work092).get(family["source_candidate_id"])
        if actual != family["source_geometry_sha256"]:
            raise RuntimeError(f"source geometry identity mismatch for {family['family']}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--mutation-protocol", type=Path, required=True)
    parser.add_argument("--solid-config", type=Path, required=True)
    parser.add_argument("--work092-manifest", type=Path, required=True)
    parser.add_argument("--primitive-witness", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    config, mutation = load(args.config), load(args.mutation_protocol)
    solid, manifest, primitive = load(args.solid_config), load(args.work092_manifest), load(args.primitive_witness)
    mutation_identity = protocol_sha256(mutation)
    validation = validate_gate_config(config, mutation_protocol_sha256=mutation_identity)
    verify_sources(config, solid, manifest, primitive)
    ledger = []
    for family in config["representation_families"]:
        for scenario in config["scenarios"]:
            outcome = evaluate_candidate(build_candidate(config, family, scenario), config)
            ledger.append({"scenario_id": scenario["scenario_id"], **outcome})

    opportunities = Counter(item["representation_family"] for item in ledger)
    status_by_family: dict[str, Counter] = defaultdict(Counter)
    causes_by_family: dict[str, Counter] = defaultdict(Counter)
    for item in ledger:
        status_by_family[item["representation_family"]][item["status"]] += 1
        for violation in item["violations"]: causes_by_family[item["representation_family"]][violation] += 1
    if set(opportunities.values()) != {len(config["scenarios"])}:
        raise RuntimeError("representation families did not receive equal opportunity")
    required = {"self_intersection", "sliver_feature", "zero_thickness", "tool_access_blocked", "wall_below_minimum", "unsupported_overhang", "hidden_repair"}
    for family in opportunities:
        if not required.issubset(causes_by_family[family]) or status_by_family[family] != Counter({"rejected": 6, "accepted": 1, "repaired": 1}):
            raise RuntimeError(f"matched control outcome mismatch for {family}")
    repaired = [item for item in ledger if item["status"] == "repaired"]
    if any(item["original_genotype_sha256"] == item["evaluated_genotype_sha256"] or not item["repair_trace"] for item in repaired):
        raise RuntimeError("repair did not enter genotype/provenance identity")

    body = {
        "status": "passed", "gate_version": config["gate_version"], "gate_sha256": validation["gate_sha256"],
        "source_mutation_protocol_sha256": mutation_identity, "source_solid_declaration_sha256": config["source_solid_declaration_sha256"],
        "source_primitive_manifest_sha256": config["source_primitive_manifest_sha256"], "total_opportunities": len(ledger),
        "opportunities_by_family": dict(sorted(opportunities.items())),
        "status_by_family": {family: dict(sorted(counts.items())) for family, counts in sorted(status_by_family.items())},
        "rejection_causes_by_family": {family: dict(sorted(counts.items())) for family, counts in sorted(causes_by_family.items())},
        "validity_yield_by_family": {family: (counts["accepted"] + counts["repaired"]) / opportunities[family] for family, counts in sorted(status_by_family.items())},
        "measurement_evidence": config["measurement_evidence"], "post_observation_repair_allowed": False,
        "cad_measurement_executed": False, "claim_boundary": "matched synthetic gate behavior only; no source STEP manufacturability conclusion",
        "ledger": ledger,
    }
    result = {**body, "result_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest()}; write(args.output, result)
    if args.replay_reference and load(args.replay_reference) != result:
        raise RuntimeError("constructive validity pilot replay mismatch")
    print(json.dumps({"status": "passed", "total_opportunities": len(ledger), "yield_per_family": sorted(set(result["validity_yield_by_family"].values())), "result_sha256": result["result_sha256"]}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
