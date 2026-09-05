#!/usr/bin/env python3
"""Execute and exactly replay the Work 097 reduced-order benchmark suite."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.components.semantic_geometry_witness import compare_report, validate_config as validate_semantic_config  # noqa: E402
from formula_ultimate.structural.generalized_geometry_benchmarks import canonical_sha256, evaluate_case, severed_edge_control, validate_config, validate_severed_edge_control, validate_source_evidence  # noqa: E402


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True); path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser(); parser.add_argument("--config", type=Path, required=True); parser.add_argument("--output", type=Path, required=True); parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args(); config = load(args.config); validation = validate_config(config); source = config["source"]
    semantic_config = load(ROOT / source["semantic_config_path"]); report = load(ROOT / source["freecad_report_path"]); frozen_comparison = load(ROOT / source["semantic_comparison_path"])
    semantic_validation = validate_semantic_config(semantic_config); comparison = compare_report(semantic_config, report)
    validate_source_evidence(source, semantic_validation, report, comparison, frozen_comparison)
    witnesses = {item["candidate_id"]: item for item in report["candidates"]}; case_results = []
    for case in config["cases"]:
        witness = witnesses.get(case["source_candidate_id"])
        if witness is None: raise RuntimeError(f"missing Work 096 witness for {case['source_candidate_id']}")
        case_results.append(evaluate_case(config, case, witness))
    models = sorted({item["model_selection"]["selected_model"] for item in case_results}); laws = sorted({item["contact_law"] for item in case_results})
    if models != validation["model_coverage"] or laws != validation["contact_law_coverage"]: raise RuntimeError("runtime model/contact-law coverage mismatch")
    severed = [severed_edge_control(case) for case in config["cases"]]
    for item in severed:
        validate_severed_edge_control(item)
    divergence = evaluate_case(config, config["cases"][0], witnesses[config["cases"][0]["source_candidate_id"]], force_divergence=True)
    if divergence["status"] != "invalid" or divergence["reason"] != "solver_divergence" or divergence["fallback_used"] is not False:
        raise RuntimeError("divergence control did not remain invalid")
    body = {"status": "passed", "schema_version": config["schema_version"], "config_sha256": validation["config_sha256"], "semantic_config_sha256": semantic_validation["config_sha256"], "freecad_report_sha256": report["report_sha256"], "semantic_comparison_sha256": comparison["comparison_sha256"], "case_count": len(case_results), "model_coverage": models, "contact_law_coverage": laws, "case_results": case_results, "controls": {"severed_edges": severed, "divergent_solver": divergence, "post_observation_failure_repair_allowed": False}, "evidence_class": config["evidence_policy"]["evidence_class"], "design_use_allowed": False, "claim_boundary": "seven reduced-order cross-method benchmarks only; no arbitrary-topology or real-material validation"}
    result = {**body, "result_sha256": canonical_sha256(body)}; write(args.output, result)
    if args.replay_reference and load(args.replay_reference) != result: raise RuntimeError("generalized benchmark replay mismatch")
    print(json.dumps({"status": "passed", "case_count": len(case_results), "models": models, "result_sha256": result["result_sha256"]}, sort_keys=True)); return 0


if __name__ == "__main__":
    raise SystemExit(main())
