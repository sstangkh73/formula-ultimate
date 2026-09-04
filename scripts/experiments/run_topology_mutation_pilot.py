#!/usr/bin/env python3
"""Run and exactly replay the balanced Work 094 mutation pilot."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.freeform_solid_grammar import declaration_sha256 as solid_sha256  # noqa: E402
from formula_ultimate.search.topology_genome import canonical_bytes, declaration_sha256, validate_topology_corpus  # noqa: E402
from formula_ultimate.search.topology_mutation import (  # noqa: E402
    TOPOLOGY_OPERATORS,
    propose,
    validate_mutation_protocol,
)


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--genome-config", type=Path, required=True)
    parser.add_argument("--solid-config", type=Path, required=True)
    parser.add_argument("--protocol", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    corpus = json.loads(args.genome_config.read_text(encoding="utf-8"))
    solids = json.loads(args.solid_config.read_text(encoding="utf-8"))
    protocol = json.loads(args.protocol.read_text(encoding="utf-8"))
    candidates = {item["candidate_id"]: item["family"] for item in solids["candidates"]}
    solid_identity = solid_sha256(solids)
    if corpus["source_solid_declaration_sha256"] != solid_identity:
        raise RuntimeError("source solid declaration identity mismatch")
    genome_validation = validate_topology_corpus(corpus, candidates)
    genome_identity = declaration_sha256(corpus)
    protocol_validation = validate_mutation_protocol(protocol, genome_identity)

    ledger = []
    for stratum in protocol["initializer_strata"]:
        for slot_index, operator in enumerate(protocol["operator_schedule"]):
            proposal = propose(
                corpus, protocol, candidates,
                parent_genome_id=stratum["parent_genome_id"], operator=operator,
                seed=stratum["seed"], slot_index=slot_index,
            )
            ledger.append({"stratum": stratum["stratum"], **proposal})

    opportunities = Counter(item["stratum"] for item in ledger)
    accepted = Counter(item["stratum"] for item in ledger if item["status"] == "accepted")
    rejected = Counter(item["stratum"] for item in ledger if item["status"] == "rejected")
    operator_accepts = Counter(item["operator"] for item in ledger if item["status"] == "accepted")
    accepted_topology_families = sorted(operator for operator in TOPOLOGY_OPERATORS if operator_accepts[operator])
    expected = len(protocol["operator_schedule"])
    if set(opportunities.values()) != {expected}:
        raise RuntimeError("initializer strata did not receive equal proposal opportunity")
    if len(accepted_topology_families) < 4:
        raise RuntimeError("fewer than four topology-changing operator families were accepted")
    if any(item["declared_topology_change"] and item["child_topology_signature"] == item["parent_topology_signature"] for item in ledger if item["status"] == "accepted"):
        raise RuntimeError("accepted topology proposal preserved its parent signature")

    body = {
        "status": "passed",
        "protocol_version": protocol["protocol_version"],
        "protocol_sha256": protocol_validation["protocol_sha256"],
        "source_genome_declaration_sha256": genome_identity,
        "source_solid_declaration_sha256": solid_identity,
        "source_genome_validation_sha256": genome_validation["declaration_sha256"],
        "total_slots": len(ledger),
        "opportunities_by_stratum": dict(sorted(opportunities.items())),
        "accepted_by_stratum": dict(sorted(accepted.items())),
        "rejected_by_stratum": dict(sorted(rejected.items())),
        "accepted_by_operator": {name: operator_accepts[name] for name in protocol["operator_schedule"]},
        "accepted_topology_operator_families": accepted_topology_families,
        "crossover": protocol["crossover"],
        "mutation_after_observation_allowed": False,
        "cad_executed": False,
        "claim_boundary": "deterministic pre-evaluation topology proposal and typed-genome validity only",
        "ledger": ledger,
    }
    result = {**body, "result_sha256": hashlib.sha256(canonical_bytes(body)).hexdigest()}
    write(args.output, result)
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        if reference != result:
            raise RuntimeError("topology mutation replay mismatch")
    print(json.dumps({
        "status": "passed", "total_slots": result["total_slots"],
        "accepted_topology_operator_families": accepted_topology_families,
        "result_sha256": result["result_sha256"],
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
