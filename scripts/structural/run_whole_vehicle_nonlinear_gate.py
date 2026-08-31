"""Execute and replay Work 064 whole-vehicle geometric-nonlinearity evidence."""

from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import time
from typing import Any, Mapping, Sequence


ROOT = Path(__file__).resolve().parents[2]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.experiments.campaign_runner import (  # noqa: E402
    ChainedJsonlLedger,
    decode_evaluation_evidence,
)
from formula_ultimate.experiments.whole_vehicle_search import (  # noqa: E402
    canonical_sha256,
    mutate_candidate_assembly,
)
from formula_ultimate.structural import (  # noqa: E402
    NONLINEAR_GATE_IDENTITY,
    VehicleFrameError,
    adjudicate_nonlinear_case,
    aggregate_candidate_nonlinear_gate,
    build_calculix_b31_deck,
    build_vehicle_frame,
    loads_from_work048,
    nonlinear_gate_config_from_mapping,
    parse_calculix_b31_dat,
    parse_calculix_section_forces_frd,
    section_force_extreme_von_mises,
)
from formula_ultimate.topology.vehicle_assembly import (  # noqa: E402
    from_mapping,
    mass_properties,
    validate,
)


CAMPAIGN_ID = "FU-NLG-001"
EVIDENCE_CLASS = "post_campaign_sensitivity"
LEDGER_KIND = "nonlinear_case"


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, text=True, capture_output=True, check=True).stdout.strip()


def _require_clean_tree() -> str:
    if _git("status", "--porcelain"):
        raise VehicleFrameError("Work 064 execution requires a clean worktree")
    return _git("rev-parse", "HEAD")


def _unique_payloads(payloads: Sequence[Mapping[str, Any]], record_type: str, key_path: tuple[str, ...]) -> dict[str, Mapping[str, Any]]:
    selected: dict[str, Mapping[str, Any]] = {}
    for payload in payloads:
        if payload.get("record_type") != record_type:
            continue
        value: Any = payload
        for key in key_path:
            value = value[key]
        identity = str(value)
        if identity in selected:
            raise VehicleFrameError(f"Work 062 contains duplicate {record_type} identity")
        selected[identity] = payload
    return selected


def load_work062_source(
    *, config_raw: Mapping[str, Any], summary_path: Path, stage_path: Path
) -> dict[str, Any]:
    """Validate chained Work 062 evidence and freeze the exact inclusion set."""

    summary = read_json(summary_path)
    source = config_raw["source_evidence"]
    expected = {
        "campaign_id": source["campaign_id"],
        "protocol_fingerprint_sha256": source["protocol_fingerprint_sha256"],
        "training_fingerprint_sha256": source["training_fingerprint_sha256"],
        "stage_fingerprint_sha256": source["stage_fingerprint_sha256"],
        "analysis_fingerprint_sha256": source["analysis_fingerprint_sha256"],
    }
    actual = {
        "campaign_id": summary["campaign_id"],
        "protocol_fingerprint_sha256": summary["protocol_fingerprint_sha256"],
        "training_fingerprint_sha256": summary["replay"]["training_fingerprint_sha256"],
        "stage_fingerprint_sha256": summary["replay"]["stage_fingerprint_sha256"],
        "analysis_fingerprint_sha256": summary["analysis"]["analysis_sha256"],
    }
    if actual != expected:
        raise VehicleFrameError("Work 062 source identity mismatch")
    if summary.get("status") != "passed" or summary.get("decision") != "completed_with_supported_finishers":
        raise VehicleFrameError("Work 062 source is not terminal and passed")

    ledger = ChainedJsonlLedger(
        stage_path,
        protocol_id=summary["protocol_id"],
        campaign_id=summary["campaign_id"],
        evidence_class=summary["evidence_class"],
        ledger_kind="stage",
    )
    rows = ledger.read_rows()
    if ledger.fingerprint() != source["stage_fingerprint_sha256"]:
        raise VehicleFrameError("Work 062 stage ledger fingerprint mismatch")
    payloads = tuple(row.payload for row in rows)
    holdouts = _unique_payloads(payloads, "holdout_result", ("evaluation", "candidate", "candidate_id"))
    refinements = _unique_payloads(payloads, "refinement_result", ("result", "candidate_id"))
    witnesses = _unique_payloads(payloads, "cad_witness_result", ("result", "candidate_id"))
    refinement_passed = {identity for identity, row in refinements.items() if row["result"]["status"] == "passed"}
    witness_passed = {identity for identity, row in witnesses.items() if row["result"]["status"] == "passed"}
    if refinement_passed != witness_passed:
        raise VehicleFrameError("Work 062 refinement/CAD passed sets differ")
    if len(witness_passed) != int(source["expected_cad_witness_passed"]):
        raise VehicleFrameError("Work 062 nonlinear inclusion count mismatch")
    if not witness_passed <= set(holdouts):
        raise VehicleFrameError("Work 062 finalist holdout evidence is missing")

    required_cases = tuple(config_raw["execution"]["required_holdout_case_ids"])
    linear_references: dict[str, dict[str, dict[str, float]]] = {}
    for identity in sorted(witness_passed):
        result = refinements[identity]["result"]
        by_case = {str(row["case_id"]): row for row in result["holdout_cases"]}
        if set(by_case) != set(required_cases):
            raise VehicleFrameError("Work 062 finalist refinement case set mismatch")
        linear_references[identity] = {}
        for case_id in required_cases:
            fine = [row for row in by_case[case_id]["refinements"] if int(row["subdivisions"]) == int(config_raw["execution"]["mesh_subdivisions"])]
            if len(fine) != 1:
                raise VehicleFrameError("Work 062 fine linear reference is missing or duplicate")
            linear_references[identity][case_id] = {
                "maximum_displacement_m": float(fine[0]["calculix"]["maximum_displacement_m"]),
                "maximum_surface_von_mises_pa": float(fine[0]["calculix"]["maximum_surface_von_mises_pa"]),
            }
    return {
        "summary": summary,
        "candidate_ids": tuple(sorted(witness_passed)),
        "holdouts": {identity: holdouts[identity]["evaluation"] for identity in sorted(witness_passed)},
        "linear_references": linear_references,
    }


def _run_ccx_case(
    *,
    ccx: Path,
    case_root: Path,
    model: Any,
    loads: Mapping[int, Sequence[float]],
    young: float,
    poisson: float,
    required_confirmation: str,
) -> tuple[float, float, int, str, list[dict[str, Any]]]:
    displacements: list[float] = []
    stresses: list[float] = []
    processes: list[dict[str, Any]] = []
    exit_code = 0
    confirmations: list[bool] = []
    for section in model.sections:
        run_dir = case_root / section.section_id
        run_dir.mkdir(parents=True, exist_ok=True)
        deck = build_calculix_b31_deck(
            model, loads, young, poisson, section.section_id, geometric_nonlinear=True
        )
        input_path = run_dir / "frame.inp"
        input_path.write_text(deck, encoding="ascii")
        before = time.perf_counter()
        process = subprocess.run([str(ccx), "frame"], cwd=run_dir, text=True, capture_output=True)
        wall = time.perf_counter() - before
        confirmed = required_confirmation in process.stdout.lower()
        confirmations.append(confirmed)
        record = {
            "section_id": section.section_id,
            "command": [str(ccx), "frame"],
            "exit_code": process.returncode,
            "wall_time_s": wall,
            "input_sha256": file_sha256(input_path),
            "stdout_sha256": hashlib.sha256(process.stdout.encode()).hexdigest(),
            "stderr": process.stderr,
            "solver_confirmation_present": confirmed,
        }
        dat_path, frd_path = run_dir / "frame.dat", run_dir / "frame.frd"
        if process.returncode == 0 and dat_path.is_file() and frd_path.is_file():
            parsed = parse_calculix_b31_dat(dat_path.read_text(encoding="utf-8", errors="replace"))
            section_rows = parse_calculix_section_forces_frd(frd_path.read_text(encoding="utf-8", errors="replace"))
            displacements.append(float(parsed["maximum_displacement_m"]))
            stresses.append(float(section_force_extreme_von_mises(section_rows, section)))
            record["dat_sha256"] = file_sha256(dat_path)
            record["frd_sha256"] = file_sha256(frd_path)
        else:
            exit_code = process.returncode or -1
        processes.append(record)
    if len(displacements) != len(model.sections) or len(stresses) != len(model.sections):
        return float("nan"), float("nan"), exit_code or -1, "", processes
    if max(displacements) - min(displacements) > 1.0e-10:
        return float("nan"), float("nan"), -1, "", processes
    stdout_for_gate = required_confirmation if all(confirmations) else ""
    return max(displacements), max(stresses), exit_code, stdout_for_gate, processes


def execute_case(
    *,
    candidate_evaluation: Mapping[str, Any],
    case_id: str,
    linear_reference: Mapping[str, float],
    config_raw: Mapping[str, Any],
    base_assembly: Mapping[str, Any],
    work048: Mapping[str, Any],
    ccx: Path,
    artifact_root: Path,
) -> dict[str, Any]:
    config = nonlinear_gate_config_from_mapping(config_raw)
    candidate = decode_evaluation_evidence(candidate_evaluation).candidate
    candidate_raw = mutate_candidate_assembly(base_assembly, dict(candidate.variables))
    candidate_raw["candidate_id"] = candidate.candidate_id
    assembly = from_mapping(candidate_raw)
    validate(assembly)
    base_properties = mass_properties(from_mapping(base_assembly))
    properties = mass_properties(assembly)
    mass_ratio = properties["mass_kg"] / base_properties["mass_kg"]
    holdouts = {row["case_id"]: row for row in work048["results"] if row["partition"] == "holdout"}
    if set(holdouts) != set(config.required_case_ids):
        raise VehicleFrameError("frozen Work 048 holdout case set mismatch")
    model = build_vehicle_frame(candidate_raw, config.mesh_subdivisions)
    loads = loads_from_work048(model, holdouts[case_id], mass_ratio, base_properties["centre_of_mass_m"])
    nonlinear_displacement, nonlinear_stress, exit_code, stdout, processes = _run_ccx_case(
        ccx=ccx,
        case_root=artifact_root / "solver" / candidate.candidate_id / case_id,
        model=model,
        loads=loads,
        young=float(config_raw["material"]["young_modulus_pa"]),
        poisson=float(config_raw["material"]["poisson_ratio"]),
        required_confirmation=config.required_confirmation,
    )
    result = adjudicate_nonlinear_case(
        config,
        candidate_id=candidate.candidate_id,
        case_id=case_id,
        linear_displacement_m=float(linear_reference["maximum_displacement_m"]),
        linear_surface_stress_pa=float(linear_reference["maximum_surface_von_mises_pa"]),
        nonlinear_displacement_m=nonlinear_displacement,
        nonlinear_surface_stress_pa=nonlinear_stress,
        process_exit_code=exit_code,
        solver_stdout=stdout,
    )
    return {
        "record_type": "nonlinear_case_result",
        "result": result,
        "candidate_geometry_sha256": canonical_sha256(candidate_raw),
        "processes": processes,
    }


def summarize_terminal_records(
    *,
    config_raw: Mapping[str, Any],
    source: Mapping[str, Any],
    records: Sequence[Mapping[str, Any]],
    ledger_fingerprint: str,
    identities: Mapping[str, Any],
    execution_commit: str,
) -> dict[str, Any]:
    config = nonlinear_gate_config_from_mapping(config_raw)
    expected_keys = {(identity, case) for identity in source["candidate_ids"] for case in config.required_case_ids}
    by_key: dict[tuple[str, str], Mapping[str, Any]] = {}
    for payload in records:
        if payload.get("record_type") != "nonlinear_case_result":
            raise VehicleFrameError("Work 064 ledger record type mismatch")
        result = payload["result"]
        key = (str(result["candidate_id"]), str(result["case_id"]))
        if key in by_key:
            raise VehicleFrameError("Work 064 ledger contains a duplicate candidate/case")
        if key not in expected_keys:
            raise VehicleFrameError("Work 064 ledger contains an out-of-scope candidate/case")
        by_key[key] = result
    if set(by_key) != expected_keys:
        raise VehicleFrameError("Work 064 terminal candidate/case set is incomplete")
    candidates = []
    for identity in source["candidate_ids"]:
        case_results = tuple(by_key[(identity, case)] for case in config.required_case_ids)
        candidates.append(aggregate_candidate_nonlinear_gate(config, candidate_id=identity, case_results=case_results))
    case_status = Counter(row["status"] for row in by_key.values())
    candidate_status = Counter(row["status"] for row in candidates)
    failures = Counter(code for row in by_key.values() for code in row["failure_codes"])
    displacement = [float(row["displacement_amplification"]) for row in by_key.values() if row["displacement_amplification"] is not None]
    stress = [float(row["stress_amplification"]) for row in by_key.values() if row["stress_amplification"] is not None]
    margin = [float(row["yield_margin"]) for row in by_key.values() if row["yield_margin"] is not None]
    draft = {
        "protocol_id": NONLINEAR_GATE_IDENTITY,
        "campaign_id": CAMPAIGN_ID,
        "evidence_class": EVIDENCE_CLASS,
        "status": "passed",
        "decision": "completed_with_nonlinear_passes" if candidate_status["passed"] else "completed_without_nonlinear_pass",
        "claim_level": config_raw["claim_level"],
        "execution_commit": execution_commit,
        "source_identity": config_raw["source_evidence"],
        "implementation_identity": identities,
        "inclusion": {"candidate_count": len(source["candidate_ids"]), "candidate_ids_sha256": canonical_sha256(source["candidate_ids"])},
        "terminal": {
            "case_count": len(by_key),
            "candidate_count": len(candidates),
            "case_status_counts": dict(sorted(case_status.items())),
            "candidate_status_counts": dict(sorted(candidate_status.items())),
            "failure_counts": dict(sorted(failures.items())),
        },
        "ranges": {
            "displacement_amplification": [min(displacement), max(displacement)],
            "stress_amplification": [min(stress), max(stress)],
            "yield_margin": [min(margin), max(margin)],
        },
        "replay": {"status": "exact", "ledger_fingerprint_sha256": ledger_fingerprint},
        "candidate_results": candidates,
        "limitations": config_raw["limitations"],
    }
    return {**draft, "summary_sha256": canonical_sha256(draft)}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, default=Path("config/structural/whole_vehicle_nonlinear_gate_v1.json"))
    parser.add_argument("--work062-summary", type=Path, default=Path("artifacts/work062/campaign_summary.json"))
    parser.add_argument("--work062-stage", type=Path, default=Path("artifacts/work062/stage_ledger.jsonl"))
    parser.add_argument("--artifact-root", type=Path, default=Path("artifacts/work064"))
    parser.add_argument("--ccx", type=Path, default=Path(r"C:\Program Files\FreeCAD 1.1\bin\ccx.exe"))
    parser.add_argument("--verify-only", action="store_true")
    args = parser.parse_args()
    head = _require_clean_tree()
    config_path = ROOT / args.config
    summary_path = ROOT / args.work062_summary
    stage_path = ROOT / args.work062_stage
    artifact_root = ROOT / args.artifact_root
    ccx = args.ccx if args.ccx.is_absolute() else ROOT / args.ccx
    config_raw = read_json(config_path)
    config = nonlinear_gate_config_from_mapping(config_raw)
    source = load_work062_source(config_raw=config_raw, summary_path=summary_path, stage_path=stage_path)
    if not ccx.is_file():
        raise VehicleFrameError("CalculiX executable is missing")
    identities = {
        "config_sha256": file_sha256(config_path),
        "runner_sha256": file_sha256(Path(__file__)),
        "gate_module_sha256": file_sha256(ROOT / "src/formula_ultimate/structural/vehicle_nonlinear_gate.py"),
        "frame_module_sha256": file_sha256(ROOT / "src/formula_ultimate/structural/vehicle_frame_refinement.py"),
        "ccx_sha256": file_sha256(ccx),
    }
    ledger = ChainedJsonlLedger(
        artifact_root / "nonlinear_case_ledger.jsonl",
        protocol_id=NONLINEAR_GATE_IDENTITY,
        campaign_id=CAMPAIGN_ID,
        evidence_class=EVIDENCE_CLASS,
        ledger_kind=LEDGER_KIND,
    )
    if not args.verify_only:
        ledger.initialize()
    rows = ledger.read_rows()
    existing = {(row.payload["result"]["candidate_id"], row.payload["result"]["case_id"]) for row in rows}
    if len(existing) != len(rows):
        raise VehicleFrameError("Work 064 resume ledger contains duplicate cases")
    if args.verify_only and len(rows) != len(source["candidate_ids"]) * len(config.required_case_ids):
        raise VehicleFrameError("Work 064 verify-only requires complete evidence")
    if not args.verify_only:
        base_assembly = read_json(ROOT / "config/vehicle/topology_neutral_vehicle_v1.json")
        work048 = read_json(ROOT / "artifacts/work048/experiment_summary.json")
        for candidate_id in source["candidate_ids"]:
            for case_id in config.required_case_ids:
                if (candidate_id, case_id) in existing:
                    continue
                payload = execute_case(
                    candidate_evaluation=source["holdouts"][candidate_id],
                    case_id=case_id,
                    linear_reference=source["linear_references"][candidate_id][case_id],
                    config_raw=config_raw,
                    base_assembly=base_assembly,
                    work048=work048,
                    ccx=ccx,
                    artifact_root=artifact_root,
                )
                ledger.append(payload)
        rows = ledger.read_rows()

    output_path = artifact_root / "nonlinear_gate_summary.json"
    if args.verify_only:
        if not output_path.is_file():
            raise VehicleFrameError("Work 064 summary is missing")
        recorded = read_json(output_path)
        execution_commit = str(recorded["execution_commit"])
        subprocess.run(["git", "merge-base", "--is-ancestor", execution_commit, head], cwd=ROOT, check=True)
    else:
        execution_commit = head
    calculated = summarize_terminal_records(
        config_raw=config_raw,
        source=source,
        records=tuple(row.payload for row in rows),
        ledger_fingerprint=ledger.fingerprint(),
        identities=identities,
        execution_commit=execution_commit,
    )
    if args.verify_only:
        if recorded != calculated:
            raise VehicleFrameError("Work 064 deterministic summary replay mismatch")
    else:
        write_json(output_path, calculated)
    print(json.dumps({
        "status": calculated["status"],
        "decision": calculated["decision"],
        "candidate_count": calculated["terminal"]["candidate_count"],
        "case_count": calculated["terminal"]["case_count"],
        "candidate_passed": calculated["terminal"]["candidate_status_counts"].get("passed", 0),
        "candidate_failed": calculated["terminal"]["candidate_status_counts"].get("failed", 0),
        "replay": calculated["replay"]["status"],
        "verify_only": args.verify_only,
    }, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
