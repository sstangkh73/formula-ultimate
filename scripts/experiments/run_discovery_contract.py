"""Execute only the synthetic Work 098 acceptance ledger; no CAD/physics claim."""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.discovery_evidence import gate_for
from formula_ultimate.experiments.discovery_ledger import DiscoveryLedger, scientific_summary
from formula_ultimate.experiments.discovery_registration import (
    DiscoveryViolation, clone, digest, require, strict_json, validate_registration, zero_cost,
)


def fixture_candidate(registration: dict, cid: str, *, parents: list[str] | None = None,
                      representation: str = "solid", treatment: str = "OPEN_ARCHITECTURE",
                      seed: int = 7, unsealed: bool = False) -> dict:
    require(registration["body"]["evidence_class"] == "software_fixture", "fixture builder cannot produce scientific candidates")
    genotype = {"operator": "synthetic_geometry_declaration", "parameter": len(cid), "id": cid}
    context = {"candidate_id": cid, "genotype_sha256": digest(genotype),
               "geometry_sha256": None if unsealed else digest(["geometry", cid]),
               "material_sha256": digest(["fixture_material", cid]),
               "boundary_sha256": None if unsealed else digest(["boundary", cid]),
               "controller_sha256": digest(["controller", cid]),
               "environment_sha256": registration["body"]["profiles"]["environment_sha256"],
               "task_sha256": registration["body"]["profiles"]["task_sha256"],
               "registration_sha256": registration["registration_sha256"]}
    return {"id": cid, "parents": parents or [], "genotype": genotype, "context": context,
            "representation": representation, "treatment": treatment, "seed": seed,
            "partition": "training", "dataset_id": "training_fixture",
            "mutation_trace": [{"operator": "synthetic_descendant", "parameters": {"parameter": len(cid)}}] if parents else []}


def fixture_cost(**overrides) -> dict:
    return {**zero_cost(), "attempts": 1, "cpu_s": 0.25, "wall_s": 0.5, "peak_memory_bytes": 1024, **overrides}


def fixture_outcome(ledger: DiscoveryLedger, cid: str, scope: str, *, value: float = 0.5,
                    status: str | None = None, reason: str = "synthetic_observation") -> dict:
    reg = ledger.registration["body"]
    require(reg["evidence_class"] == "software_fixture", "fixture builder cannot produce scientific evidence")
    state = ledger.replay()["state"]
    candidate = state["candidates"][cid]
    context = clone(state["states"][cid]["context"])
    if scope in {"representation", "boundary"}:
        dim = scope
        status = status or ("geometry_measured" if dim == "representation" else "boundary_resolved")
        if status == "geometry_measured" and context["geometry_sha256"] is None:
            context["geometry_sha256"] = digest(["geometry", cid])
        if status == "boundary_resolved" and context["boundary_sha256"] is None:
            context["boundary_sha256"] = digest(["boundary", cid])
        body = {"context_sha256": digest(context), "evidence_class": "software_fixture",
                "details": {"synthetic_only": True, "measured_geometry": False, "status": status}}
    else:
        gate = gate_for(reg, scope)
        dim = gate["kind"] if gate["kind"] in {"physics", "manufacturing"} else "gate"
        passed = value <= gate["threshold"] if gate["comparison"] == "le" else value >= gate["threshold"]
        status = status or ({"physics": ("physically_feasible" if passed else "physically_failed"),
                             "manufacturing": ("manufacturing_compatible" if passed else "manufacturing_incompatible"),
                             "gate": ("passed" if passed else "failed")}[dim])
        ev = next(e for e in reg["evaluators"] if e["id"] == gate["evaluator_id"])
        body = {"evidence_class": "software_fixture", "evaluator_id": ev["id"],
                "implementation_sha256": ev["implementation_sha256"], "validation_sha256": ev["validation_sha256"],
                "context_sha256": digest(context), "gate_id": scope,
                "dataset_id": reg["partitions"]["holdout"][0] if gate["kind"] == "holdout" else candidate["dataset_id"],
                "metric": gate["metric"], "unit": gate["unit"], "value": value, "converged": True,
                "error": 0.0, "refinements": [4 * 2 ** i for i in range(gate["minimum_refinements"])],
                "evidence_type": gate["evidence_type"], "details": {"synthetic_only": True, "no_field_solver_executed": True}}
    unresolved = status in {"not_evaluated", "numerically_unresolved", "manufacturing_unresolved"}
    return {"dimension": dim, "scope": scope, "status": status, "reason": reason, "context": context,
            "artifact": None if unresolved else {"body": body, "sha256": digest(body)}}


def reserve(ledger: DiscoveryLedger, cid: str, scope: str, *, aid: str | None = None, pool: str = "exploration",
            cost: dict | None = None, retry_of: str | None = None, cache_of: str | None = None,
            selection_sha256: str | None = None) -> str:
    state = ledger.replay()["state"]
    if aid is None:
        aid = f"attempt_{len(state['attempts']):04d}"
    gate = None if scope in {"representation", "boundary"} else gate_for(ledger.registration["body"], scope)
    dimension = scope if gate is None else (gate["kind"] if gate["kind"] in {"physics", "manufacturing"} else "gate")
    ledger.append({"type": "reserve", "id": aid, "candidate_id": cid, "pool": pool, "dimension": dimension,
                   "scope": scope, "cost": fixture_cost() if cost is None else cost, "retry_of": retry_of,
                   "cache_of": cache_of, "selection_sha256": selection_sha256})
    return aid


def evaluate(ledger: DiscoveryLedger, cid: str, scope: str, *, cost: dict | None = None,
             pool: str = "exploration", retry_of: str | None = None, selection_sha256: str | None = None, **kwargs) -> str:
    result = fixture_outcome(ledger, cid, scope, **kwargs)
    aid = reserve(ledger, cid, scope, pool=pool, retry_of=retry_of, cost=cost, selection_sha256=selection_sha256)
    ledger.append({"type": "start", "id": aid})
    ledger.append({"type": "settle", "id": aid, "observed_cost": fixture_cost() if cost is None else cost,
                   "result": result, "diagnostics": {"software_fixture": True}})
    return aid


def measured(ledger: DiscoveryLedger, cid: str, **kwargs) -> None:
    ledger.append({"type": "candidate", "candidate": fixture_candidate(ledger.registration, cid, **kwargs)})
    evaluate(ledger, cid, "representation")
    evaluate(ledger, cid, "boundary")


def run_fixture(registration: dict, output: Path) -> dict:
    validate_registration(registration)
    require(registration["body"]["evidence_class"] == "software_fixture", "runner is fixture-only")
    require(not output.exists() or (output.is_dir() and not any(output.iterdir())), "output directory must be new or empty")
    output.mkdir(parents=True, exist_ok=True)
    ledger = DiscoveryLedger(output / "ledger.jsonl", registration)
    measured(ledger, "mixed", representation="multi_body", unsealed=True)
    evaluate(ledger, "mixed", "structural_coarse")
    evaluate(ledger, "mixed", "additive", value=2.0)
    ledger.append({"type": "explore", "candidate_id": "mixed", "declaration": {
        "missing_domains": ["flow"], "approximations": ["synthetic_fixture"],
        "interfaces_sha256": digest("synthetic_interfaces"), "scope": "coupling_contract_test"}})
    measured(ledger, "failed", representation="shell")
    evaluate(ledger, "failed", "structural_coarse", value=2.0)
    ledger.append({"type": "select", "pool": "audit", "gate_id": "structural_coarse"})
    audit = ledger.replay()["state"]["selections"][-1]["selection_sha256"]
    evaluate(ledger, "failed", "structural_fine", pool="audit", selection_sha256=audit)
    evaluate(ledger, "mixed", "structural_fine", status="numerically_unresolved", reason="timeout",
             pool="audit", selection_sha256=audit)
    ledger.append({"type": "select", "pool": "stepping_stone", "gate_id": "structural_coarse"})
    ledger.append({"type": "select", "pool": "quality", "gate_id": "structural_coarse"})
    measured(ledger, "descendant", parents=["failed"], representation="lattice")
    for gate_id in registration["body"]["promotion_gates"]:
        evaluate(ledger, "descendant", gate_id, pool="finalist")
    for target in ("candidate_survivor", "promotion_ready"):
        ledger.append({"type": "promote", "candidate_id": "descendant", "target": target,
                       "use": registration["body"]["promotion_scope"]})
    for cid, status in (("invalid", "representation_invalid"), ("unbound", "geometry_measured")):
        ledger.append({"type": "candidate", "candidate": fixture_candidate(registration, cid)})
        evaluate(ledger, cid, "representation", status=status)
    evaluate(ledger, "unbound", "boundary", status="boundary_unresolved", reason="ambiguous_terminal")
    ledger.append({"type": "candidate", "candidate": fixture_candidate(registration, "generated_only")})
    measured(ledger, "recovery", treatment="CONVENTIONAL_CONTROL", seed=19)
    aid = reserve(ledger, "recovery", "structural_coarse")
    ledger.append({"type": "start", "id": aid})
    checkpoint = ledger.replay()["head_sha256"]
    ledger = DiscoveryLedger(output / "ledger.jsonl", registration, expected_head=checkpoint)
    ledger.append({"type": "recover", "id": aid})
    evaluate(ledger, "recovery", "structural_coarse", retry_of=aid)
    aid = reserve(ledger, "recovery", "structural_fine")
    ledger.append({"type": "recover", "id": aid})
    ledger.append({"type": "quarantine", "source_sha256": digest("injected_bad_provenance"), "reason": "synthetic_corrupt_source"})
    replay = ledger.replay()
    restored = DiscoveryLedger(output / "ledger.jsonl", registration, expected_head=replay["head_sha256"]).replay()
    require(replay == restored, "decision replay mismatch")
    state = replay["state"]
    counts = {"scientific_survivors": scientific_summary(state)["scientific_survivors"],
              "candidates": len(state["candidates"]), "attempts": len(state["attempts"])}
    report = {"schema": "work098_fixture_result_v1", "evidence_class": "software_fixture",
              "registration_sha256": registration["registration_sha256"],
              "head_sha256": replay["head_sha256"], "state_sha256": replay["state_sha256"],
              "decision_replay": "exact", "counts": counts,
              "audit": ledger.audit_report(audit, "structural_fine"),
              "accounting_complete": state["accounting_complete"],
              "scientific_admission": scientific_summary(state),
              "limitations": ["software_fixture_only", "no_CAD_or_physics_executed", "recovered_started_cost_is_unknown",
                              "no_physical_validation", "no_scientific_survivors"],
              "implementation_sha256": {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                                          for p in sorted((ROOT / "src/formula_ultimate/experiments").glob("discovery_*.py"))}}
    report["report_sha256"] = digest(report)
    (output / "result.json").write_text(json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/discovery_contract_fixture_v1.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    try:
        registration = strict_json(args.config.read_text(encoding="utf-8"))
        report = run_fixture(registration, args.output_dir)
        if args.replay_reference:
            expected = strict_json(args.replay_reference.read_text(encoding="utf-8"))
            require(report == expected, "fixture report replay mismatch")
        print(json.dumps({k: report[k] for k in ("counts", "decision_replay", "head_sha256", "report_sha256")}, sort_keys=True))
        return 0
    except (DiscoveryViolation, OSError) as error:
        print(f"Work 098 failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
