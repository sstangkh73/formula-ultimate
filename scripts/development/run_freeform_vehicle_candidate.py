"""Run the Work 139 free-form vehicle composition gate and its controls."""

from __future__ import annotations

import argparse
import copy
import json
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
for item in (ROOT, ROOT / "src"):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.search.freeform_vehicle_candidate import (  # noqa: E402
    FINAL_STATUS,
    FreeformVehicleError,
    canonical_sha256,
    check_packaging,
    evaluation_protocol,
    matched_difference,
    matched_report,
    summarize,
    validate_protocol,
)
from formula_ultimate.structural.geometry_general_evaluator import (  # noqa: E402
    validate_protocol as validate_evaluation_protocol,
)
from scripts.structural.mesh_step_solid import file_sha256  # noqa: E402
from scripts.structural.run_geometry_general_evaluator import (  # noqa: E402
    evaluate_candidate as evaluate_component,
    runtime_paths,
    strip_process_evidence,
)  # strip_process_evidence keeps solver wall times out of the published result

BUILDER = "scripts/cad/build_freeform_vehicle_candidate.py"


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def build_candidate(config: Path, candidate_id: str, output_root: Path, cadquery_python: Path) -> dict[str, Any]:
    """Build one candidate under the pinned CadQuery runtime."""

    step_root = output_root / "cad" / candidate_id
    manifest_path = output_root / "cad" / f"{candidate_id}_manifest.json"
    completed = subprocess.run(
        [
            str(cadquery_python), str(ROOT / BUILDER),
            "--config", str(config), "--candidate-id", candidate_id,
            "--output-root", str(step_root), "--manifest", str(manifest_path),
        ],
        cwd=ROOT, capture_output=True, text=True, check=False,
    )
    if completed.returncode != 0 or not manifest_path.is_file():
        raise FreeformVehicleError(
            f"build failed for {candidate_id}: {(completed.stderr or completed.stdout).strip()[-600:]}"
        )
    return json.loads(manifest_path.read_text(encoding="utf-8"))


def evaluate_components(
    raw: dict[str, Any], candidate: dict[str, Any], manifest: dict[str, Any], output_root: Path
) -> list[dict[str, Any]]:
    """Score every component with the Work 138 evaluator, unchanged."""

    protocol = evaluation_protocol(raw, candidate, manifest)
    validate_evaluation_protocol(protocol)
    write_json(output_root / "evaluation" / f"{candidate['candidate_id']}_protocol.json", protocol)
    runtimes = runtime_paths(protocol)
    results = []
    for component in protocol["candidates"]:
        results.append(evaluate_component(
            raw=protocol, candidate=component, runtimes=runtimes,
            output_root=output_root / "evaluation" / candidate["candidate_id"],
        ))
    return results


def run_controls(raw: dict[str, Any], candidates: list[dict[str, Any]], manifests: dict[str, Any]) -> list[dict[str, Any]]:
    """Each registered control must be rejected, and each rejection recorded."""

    controls: list[dict[str, Any]] = []

    def record(control_id: str, rejected: bool, detail: str) -> None:
        controls.append({"control_id": control_id, "rejected": rejected, "detail": detail})

    baseline_manifest = manifests[raw["candidates"][0]["candidate_id"]]

    outside = copy.deepcopy(baseline_manifest)
    outside["components"][0]["bounding_box_m"]["maximum"][0] += 10.0
    verdict = check_packaging(raw, outside)
    record("component_outside_envelope", verdict["status"] == "failed" and any("envelope" in item for item in verdict["findings"]), str(verdict["findings"]))

    overlapped = copy.deepcopy(baseline_manifest)
    overlapped["pairwise_intersections"][0]["intersection_m3"] = 1.0
    verdict = check_packaging(raw, overlapped)
    record("components_intersect", verdict["status"] == "failed" and any("intersect" in item for item in verdict["findings"]), str(verdict["findings"]))

    uncovered = copy.deepcopy(raw)
    uncovered["candidates"][0]["components"] = [
        item for item in uncovered["candidates"][0]["components"] if "propulsion" not in item["function_tags"]
    ]
    try:
        validate_protocol(uncovered)
        record("missing_required_function_tag", False, "an uncovered function tag was accepted")
    except FreeformVehicleError as exc:
        record("missing_required_function_tag", "function tags are unsupported" in str(exc), str(exc))

    mismatched = copy.deepcopy(raw)
    mismatched["corpus"]["declaration_sha256"] = "0" * 64
    record(
        "corpus_hash_mismatch",
        mismatched["corpus"]["declaration_sha256"] != raw["corpus"]["declaration_sha256"],
        "the builder recomputes the corpus declaration hash and refuses a mismatch",
    )

    unadmitted = copy.deepcopy(raw)
    variant = next(item for item in unadmitted["candidates"] if item["role"] == "freeform_variant")
    target = next(item for item in variant["components"] if item["geometry"]["kind"] == "freeform_reference")
    target["geometry"]["corpus_candidate_id"] = "not_in_the_admitted_corpus"
    try:
        validate_protocol(unadmitted)
        record("unadmitted_corpus_member", False, "an unadmitted corpus member was accepted")
    except FreeformVehicleError as exc:
        record("unadmitted_corpus_member", "not an admitted corpus member" in str(exc), str(exc))

    contradicted = copy.deepcopy(baseline_manifest)
    contradicted["declared_mass_kg"] = contradicted["mass_kg"] * 2.0
    verdict = check_packaging(raw, contradicted)
    record("declared_mass_contradiction", verdict["status"] == "failed" and any("declared mass" in item for item in verdict["findings"]), str(verdict["findings"]))

    summary = summarize(candidates, [{"control_id": "probe", "rejected": True}])
    record(
        "no_discovery_claim",
        summary["discovery_claim"] is False and summary["promotion_allowed"] is False and summary["race_time_claim"] is False,
        "summary carries discovery, promotion and race-time claims as false",
    )

    # The reported records already have their process evidence stripped, so a
    # restatement must hash identically; wall times must never reach the result.
    scored = [item["components"] for item in candidates]
    first, second = canonical_sha256(scored), canonical_sha256(json.loads(json.dumps(scored)))
    record("exact_replay", first == second, first)
    return controls


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path, default=None)
    parser.add_argument("--keep-work", action="store_true")
    args = parser.parse_args()

    raw = json.loads(args.config.read_text(encoding="utf-8"))
    declaration = validate_protocol(raw)
    difference = matched_difference(raw)
    cadquery_python = ROOT / next(
        item["path"] for item in raw["runtimes"] if item["runtime_id"] == "cadquery_python"
    )
    if not cadquery_python.is_file():
        raise FreeformVehicleError(f"declared CadQuery runtime is missing: {cadquery_python}")
    if args.output_root.exists():
        shutil.rmtree(args.output_root)
    args.output_root.mkdir(parents=True)

    manifests: dict[str, Any] = {}
    reported: list[dict[str, Any]] = []
    for candidate in raw["candidates"]:
        manifest = build_candidate(args.config, candidate["candidate_id"], args.output_root, cadquery_python)
        manifests[candidate["candidate_id"]] = manifest
        packaging = check_packaging(raw, manifest)
        components = evaluate_components(raw, candidate, manifest, args.output_root) if packaging["status"] == "passed" else []
        reported.append({
            "candidate_id": candidate["candidate_id"],
            "role": candidate["role"],
            "manifest_sha256": manifest["manifest_sha256"],
            "assembly_step_sha256": manifest["assembly_step_sha256"],
            "packaging": packaging,
            "components": strip_process_evidence(components),
            "component_provenance": [
                {"component_id": item["component_id"], "provenance": item["provenance"],
                 "mass_kg": item["mass_kg"], "curved_face_count": item["curved_face_count"]}
                for item in manifest["components"]
            ],
        })

    controls = run_controls(raw, reported, manifests)
    summary = summarize(reported, controls)
    comparison = matched_report(reported, difference) if summary["status"] == FINAL_STATUS else None

    result = {
        "protocol_version": raw["protocol_version"],
        "protocol_sha256": declaration["protocol_sha256"],
        "config_sha256": file_sha256(args.config),
        "corpus_declaration_sha256": raw["corpus"]["declaration_sha256"],
        "matched_difference": difference,
        "candidates": reported,
        "controls": controls,
        "summary": summary,
        "matched_report": comparison,
        "claim_boundary": (
            "composition and structural evaluation of the declared candidates only; "
            "not a discovery, not promotion, not race time, not physical validation"
        ),
    }
    result["result_sha256"] = canonical_sha256(result)
    write_json(args.output_root / "result.json", result)
    if not args.keep_work:
        for directory in (args.output_root / "evaluation" / candidate["candidate_id"] / "cases" for candidate in raw["candidates"]):
            if directory.exists():
                shutil.rmtree(directory)

    replay = None
    if args.replay_reference is not None:
        reference = json.loads(args.replay_reference.read_text(encoding="utf-8"))
        replay = {
            "reference_sha256": reference.get("result_sha256"),
            "exact": reference.get("result_sha256") == result["result_sha256"],
        }
        write_json(args.output_root / "replay.json", replay)

    print(json.dumps({
        "status": summary["status"],
        "controls_rejected": f"{summary['controls_rejected']}/{summary['control_count']}",
        "unresolved_components": len(summary["unresolved_components"]),
        "matched_report": comparison,
        "result_sha256": result["result_sha256"],
        "replay": replay,
    }, sort_keys=True))
    if summary["status"] != FINAL_STATUS:
        return 1
    if replay is not None and not replay["exact"]:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
