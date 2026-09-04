#!/usr/bin/env python3
"""Run the Work 090 diversity census over the exact Work 050 proposal ledger."""
from __future__ import annotations

from dataclasses import asdict
import argparse
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.design_diversity import (  # noqa: E402
    canonical_sha256, describe_candidate, load_sources, summarize_census, validate_config,
)
from formula_ultimate.experiments.whole_vehicle_search import (  # noqa: E402
    mutate_candidate_assembly, run_search_pilot, validate_search_protocol,
)
from formula_ultimate.simulation.vehicle_load_cases import (  # noqa: E402
    canonical_sha256 as load_sha256, evaluate_all_load_cases, validate_protocol as validate_load_protocol,
)


def write(path: Path, value: object) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    if args.output_root.exists() and any(args.output_root.iterdir()):
        raise SystemExit("output-root must be absent or empty")
    args.output_root.mkdir(parents=True, exist_ok=True)

    config = json.loads(args.config.read_text(encoding="utf-8"))
    validation = validate_config(config)
    sources = load_sources(ROOT, config)
    base = sources["base_assembly"]
    search = sources["search_protocol"]
    load = sources["load_protocol"]
    failure = sources["failure_contract"]
    baseline_protocol = sources["baseline_protocol"]
    source_hashes = {key: config["sources"][key]["file_sha256"] for key in config["sources"]}

    assembly = validate_load_protocol(
        load, base,
        assembly_config_sha256=source_hashes["base_assembly"],
        assembly_step_sha256=load["assembly_identity"]["assembly_step_sha256"],
        failure_config_sha256=source_hashes["failure_contract"],
    )
    load_results = [asdict(item) for item in evaluate_all_load_cases(load, assembly, failure)]
    work048 = {"results": load_results, "partitions": load["partitions"]}
    baseline = {
        "replay": {
            "result_sha256": search["upstream_identity"]["reference_result_sha256"],
            "matrix_sha256": search["upstream_identity"]["reference_matrix_sha256"],
        },
        "upstream": {
            "load_case_result_sha256": load_sha256(load_results),
            "training_partition_sha256": load["partitions"]["training"],
            "holdout_partition_sha256": load["partitions"]["holdout"],
        },
    }
    evaluator = validate_search_protocol(search, baseline, baseline_protocol_sha256=source_hashes["baseline_protocol"])
    evaluations = run_search_pilot(search, base, work048, baseline_protocol, evaluator)
    rows = []
    for item in evaluations:
        candidate = mutate_candidate_assembly(base, dict(item.candidate.variables))
        rows.append({
            "candidate_id": item.candidate.candidate_id,
            "treatment": item.candidate.treatment,
            "seed": item.candidate.seed,
            "attempt_index": item.candidate.attempt_index,
            "variables": dict(item.candidate.variables),
            "evaluation_status": item.status,
            "failure_code": item.failure_code,
            "descriptor": describe_candidate(candidate),
        })
    summary = summarize_census(rows, config["census"]["expected_attempts"])
    census = {"census_id": config["census_id"], "rows": rows}
    census["census_sha256"] = canonical_sha256(census)
    write(args.output_root / "census.json", census)
    result_body = {
        "status": "passed",
        "census_id": config["census_id"],
        "claim_level": config["claim_level"],
        "config_sha256": validation["config_sha256"],
        "source_file_sha256": source_hashes,
        "evaluator_sha256": evaluator,
        "census_sha256": census["census_sha256"],
        "summary": summary,
    }
    result = {**result_body, "result_sha256": canonical_sha256(result_body)}
    write(args.output_root / "result.json", result)
    if args.replay_reference:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        exact = reference == result
        replay = {"status": "passed" if exact else "failed", "exact": exact, "reference_result_sha256": reference.get("result_sha256"), "replay_result_sha256": result["result_sha256"]}
        write(args.output_root / "replay.json", replay)
        if not exact:
            raise SystemExit("replay mismatch")
    print(json.dumps({"status": "passed", "result_sha256": result["result_sha256"], **summary}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
