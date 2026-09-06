#!/usr/bin/env python3
"""Execute the bounded Work 099 CAD morphology and archive software fixture."""

from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
import math
from pathlib import Path
import re
import sys
import time
from typing import Any, Mapping

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))

import cadquery as cq  # noqa: E402

from formula_ultimate.experiments.discovery_ledger import DiscoveryLedger, scientific_summary  # noqa: E402
from formula_ultimate.experiments.discovery_registration import (  # noqa: E402
    DiscoveryViolation,
    clone,
    digest as contract_digest,
    strict_json,
    validate_registration,
    zero_cost,
)
from formula_ultimate.search.executable_morphology import (  # noqa: E402
    GEOMETRY_OPERATORS,
    MorphologyViolation,
    OPERATORS,
    canonical_bytes,
    digest,
    functional_signature,
    mutate,
    root_genome,
    topology_descriptors,
    validate_config,
    validate_genome,
)
from formula_ultimate.search.morphology_archive import EVIDENCE_SCOPE, MorphologyArchive  # noqa: E402


MM = 1000.0


class CadExecutionViolation(RuntimeError):
    """Raised when the bounded genotype cannot produce valid CAD evidence."""


def _write_json(path: Path, value: Any) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8", newline="\n")


def _sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _canonicalize_step(path: Path) -> None:
    text = path.read_text(encoding="ascii", errors="strict")
    updated, count = re.subn(r"(FILE_NAME\('[^']*',)'[^']*'", r"\1'1970-01-01T00:00:00'", text, count=1)
    if count != 1:
        raise CadExecutionViolation("STEP timestamp is missing or ambiguous")
    path.write_text(updated, encoding="ascii", newline="\n")


def _vector(point_m: list[float] | tuple[float, float, float]) -> cq.Vector:
    return cq.Vector(*(float(value) * MM for value in point_m))


def _execute_part(part: Mapping[str, Any]) -> cq.Shape:
    nodes = {node["node_id"]: node for node in part["nodes"]}
    shape: cq.Shape | None = None
    for node in part["nodes"]:
        primitive = cq.Solid.makeSphere(float(node["radius_m"]) * MM, _vector(node["point_m"]))
        shape = primitive if shape is None else shape.fuse(primitive)
    for edge in part["edges"]:
        a, b = nodes[edge["a"]], nodes[edge["b"]]
        start, end = _vector(a["point_m"]), _vector(b["point_m"])
        delta = end.sub(start)
        length = delta.Length
        if not math.isfinite(length) or length <= 0.0:
            raise CadExecutionViolation("CAD edge is zero or non-finite")
        radius = min(float(a["radius_m"]), float(b["radius_m"])) * MM
        primitive = cq.Solid.makeCylinder(radius, length, start, delta.normalized())
        shape = primitive if shape is None else shape.fuse(primitive)
    if shape is None or shape.isNull() or not shape.isValid() or shape.Volume() <= 0.0:
        raise CadExecutionViolation(f"part {part['part_id']} produced invalid or empty geometry")
    solids = shape.Solids()
    if len(solids) != 1:
        raise CadExecutionViolation(f"part {part['part_id']} did not produce one connected solid: {len(solids)}")
    return shape


def execute_genome(genome: Mapping[str, Any], limits: Mapping[str, Any], output_path: Path) -> dict[str, Any]:
    """Execute actual CadQuery solids and return geometry-derived SI measurements."""
    validation = validate_genome(genome, limits)
    parts = [(part, _execute_part(part)) for part in genome["parts"]]
    compound = cq.Compound.makeCompound([shape for _, shape in parts])
    if compound.isNull() or not compound.isValid():
        raise CadExecutionViolation("assembly compound is invalid")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    cq.exporters.export(compound, str(output_path), exportType="STEP")
    _canonicalize_step(output_path)
    bounds = compound.BoundingBox()
    center = compound.Center()
    terminal_positions = {}
    parts_by_id = {part["part_id"]: part for part in genome["parts"]}
    for terminal in genome["terminals"]:
        node = next(node for node in parts_by_id[terminal["part_id"]]["nodes"] if node["node_id"] == terminal["node_id"])
        terminal_positions[terminal["terminal_id"]] = {
            "point_m": [float(value) for value in node["point_m"]],
            "role": terminal["role"],
            "domains": sorted(terminal["domains"]),
            "ancestry": list(terminal["ancestry"]),
        }
    volume_mm3 = sum(shape.Volume() for _, shape in parts)
    area_mm2 = sum(shape.Area() for _, shape in parts)
    measurement = {
        "volume_m3": volume_mm3 * 1e-9,
        "surface_area_m2": area_mm2 * 1e-6,
        "bounds_m": {
            "minimum": [bounds.xmin / MM, bounds.ymin / MM, bounds.zmin / MM],
            "maximum": [bounds.xmax / MM, bounds.ymax / MM, bounds.zmax / MM],
        },
        "center_m": [center.x / MM, center.y / MM, center.z / MM],
        "solid_count": sum(len(shape.Solids()) for _, shape in parts),
        "face_count": sum(len(shape.Faces()) for _, shape in parts),
        "edge_count": sum(len(shape.Edges()) for _, shape in parts),
        "terminal_positions_m": terminal_positions,
        "part_measurements": {
            part["part_id"]: {"volume_m3": shape.Volume() * 1e-9, "surface_area_m2": shape.Area() * 1e-6}
            for part, shape in parts
        },
    }
    if not all(math.isfinite(value) for value in (measurement["volume_m3"], measurement["surface_area_m2"], *measurement["center_m"])):
        raise CadExecutionViolation("CAD measurement is non-finite")
    return {
        "geometry_sha256": _sha256_file(output_path),
        "step_file": output_path.name,
        "measurement": measurement,
        "measurement_sha256": digest(measurement),
        "functional_signature": validation["functional_signature"],
        "descriptors": validation["descriptors"],
    }


def boundary_identity(genome: Mapping[str, Any], evidence: Mapping[str, Any]) -> str:
    body = {
        "terminals": evidence["measurement"]["terminal_positions_m"],
        "interfaces": [
            {key: interface[key] for key in ("part_a", "node_a", "part_b", "node_b", "kind", "domains", "ancestry")}
            for interface in genome["interfaces"]
        ],
    }
    return digest(body)


def _candidate(registration: Mapping[str, Any], genome: Mapping[str, Any], cid: str, *, parents: list[str], trace: Mapping[str, Any] | None) -> dict[str, Any]:
    genotype = deepcopy(dict(genome))
    material = {part["part_id"]: part["material_id"] for part in genotype["parts"]}
    context = {
        "candidate_id": cid,
        "genotype_sha256": contract_digest(genotype),
        "geometry_sha256": None,
        "material_sha256": contract_digest(material),
        "boundary_sha256": None,
        "controller_sha256": contract_digest(genotype["controller"]),
        "environment_sha256": registration["body"]["profiles"]["environment_sha256"],
        "task_sha256": registration["body"]["profiles"]["task_sha256"],
        "registration_sha256": registration["registration_sha256"],
    }
    mutation_trace = [] if trace is None else [{"operator": trace["operator"], "parameters": {key: clone(value) for key, value in trace.items() if key != "operator"}}]
    return {
        "id": cid,
        "parents": parents,
        "genotype": genotype,
        "context": context,
        "representation": "solid" if len(genotype["parts"]) == 1 else "multi_body",
        "treatment": "OPEN_ARCHITECTURE",
        "seed": genotype["seed"],
        "partition": "training",
        "dataset_id": "training_fixture",
        "mutation_trace": mutation_trace,
    }


def _cost(*, wall_s: float, cpu_s: float, cad: bool) -> dict[str, Any]:
    cost = zero_cost()
    cost.update({
        "attempts": 1,
        "geometry_executions": 1 if cad else 0,
        "cad_calls": 1 if cad else 0,
        "cpu_s": max(0.0, float(cpu_s)),
        "wall_s": max(0.0, float(wall_s)),
        "peak_memory_bytes": 0,
    })
    return cost


def _reserve(ledger: DiscoveryLedger, cid: str, dimension: str, aid: str, *, cad: bool) -> None:
    reservation = _cost(wall_s=10.0, cpu_s=10.0, cad=cad)
    ledger.append({"type": "reserve", "id": aid, "candidate_id": cid, "pool": "exploration", "dimension": dimension, "scope": dimension, "cost": reservation, "retry_of": None, "cache_of": None, "selection_sha256": None})
    ledger.append({"type": "start", "id": aid})


def _diagnostic(context: Mapping[str, Any], details: Mapping[str, Any]) -> dict[str, Any]:
    body = {"context_sha256": contract_digest(context), "evidence_class": "software_fixture", "details": clone(dict(details))}
    return {"body": body, "sha256": contract_digest(body)}


def _settle_representation(ledger: DiscoveryLedger, cid: str, aid: str, status: str, details: Mapping[str, Any], cost: Mapping[str, Any], *, geometry_sha256: str | None) -> None:
    context = clone(ledger.replay()["state"]["states"][cid]["context"])
    if status == "geometry_measured":
        context["geometry_sha256"] = geometry_sha256
    result = {"dimension": "representation", "scope": "representation", "status": status, "reason": "cad_geometry_measured" if status == "geometry_measured" else "representation_validation_failed", "context": context, "artifact": _diagnostic(context, details)}
    ledger.append({"type": "settle", "id": aid, "observed_cost": clone(dict(cost)), "result": result, "diagnostics": {"work": "099", "cad_executed": status == "geometry_measured"}})


def _settle_boundary(ledger: DiscoveryLedger, cid: str, aid: str, status: str, details: Mapping[str, Any], *, boundary_sha256: str | None, cost: Mapping[str, Any]) -> None:
    context = clone(ledger.replay()["state"]["states"][cid]["context"])
    if status == "boundary_resolved":
        context["boundary_sha256"] = boundary_sha256
    result = {"dimension": "boundary", "scope": "boundary", "status": status, "reason": "terminal_ancestry_resolved" if status == "boundary_resolved" else "ambiguous_terminal", "context": context, "artifact": _diagnostic(context, details)}
    ledger.append({"type": "settle", "id": aid, "observed_cost": clone(dict(cost)), "result": result, "diagnostics": {"work": "099", "terminal_ancestry_checked": True}})


def _different_measurement(a: Mapping[str, Any], b: Mapping[str, Any], relative: float, absolute: float) -> bool:
    for key in ("volume_m3", "surface_area_m2"):
        if not math.isclose(float(a[key]), float(b[key]), rel_tol=relative, abs_tol=absolute):
            return True
    if a["solid_count"] != b["solid_count"] or a["face_count"] != b["face_count"] or a["edge_count"] != b["edge_count"]:
        return True
    return any(abs(float(x) - float(y)) > absolute for side in ("minimum", "maximum") for x, y in zip(a["bounds_m"][side], b["bounds_m"][side]))


def _compare_reference(current: Mapping[str, Any], reference: Mapping[str, Any], relative: float, absolute: float) -> dict[str, Any]:
    current_candidates = current["deterministic_evidence"]["candidates"]
    reference_candidates = reference["deterministic_evidence"]["candidates"]
    if set(current_candidates) != set(reference_candidates):
        raise CadExecutionViolation("replay candidate identities differ")
    maximum_relative = 0.0
    maximum_absolute = 0.0
    for cid in sorted(current_candidates):
        a, b = current_candidates[cid], reference_candidates[cid]
        for key in ("genotype_sha256", "functional_signature", "status", "geometry_sha256", "measurement_sha256"):
            if a.get(key) != b.get(key):
                raise CadExecutionViolation(f"replay identity differs for {cid}: {key}")
        if a.get("measurement") is None:
            continue
        for key in ("volume_m3", "surface_area_m2"):
            x, y = float(a["measurement"][key]), float(b["measurement"][key])
            maximum_absolute = max(maximum_absolute, abs(x - y))
            maximum_relative = max(maximum_relative, abs(x - y) / max(abs(x), abs(y), 1e-18))
            if not math.isclose(x, y, rel_tol=relative, abs_tol=absolute):
                raise CadExecutionViolation(f"replay measurement differs for {cid}: {key}")
        for key in ("solid_count", "face_count", "edge_count", "terminal_positions_m"):
            if a["measurement"][key] != b["measurement"][key]:
                raise CadExecutionViolation(f"replay measurement differs for {cid}: {key}")
    if current["deterministic_evidence"]["archive"] != reference["deterministic_evidence"]["archive"]:
        raise CadExecutionViolation("replay archive differs")
    return {"status": "passed", "identity_exact": True, "maximum_relative_difference": maximum_relative, "maximum_absolute_difference": maximum_absolute, "timing_compared": False}


def run(config: Mapping[str, Any], registration: Mapping[str, Any], output_dir: Path, replay_reference: Mapping[str, Any] | None = None) -> dict[str, Any]:
    validation = validate_config(config)
    validate_registration(dict(registration))
    if registration["body"]["evidence_class"] != "software_fixture":
        raise CadExecutionViolation("Work 099 runner is restricted to the software-fixture evidence class")
    if output_dir.exists() and any(output_dir.iterdir()):
        raise CadExecutionViolation("output directory must be new or empty")
    output_dir.mkdir(parents=True, exist_ok=True)
    ledger = DiscoveryLedger(output_dir / "ledger.jsonl", dict(registration))
    archive = MorphologyArchive(config["archive"]["capacity_per_niche"], config["archive"]["reproduction_caps"])
    deterministic: dict[str, Any] = {}
    timings: dict[str, Any] = {}
    archive_events = []
    seen_signatures: set[str] = set()
    geometry_change_proofs = []
    attempt_index = 0

    def evaluate_program(genome: dict[str, Any], cid: str, parents: list[str], trace: Mapping[str, Any] | None, *, unresolved_boundary: bool = False) -> dict[str, Any]:
        nonlocal attempt_index
        candidate = _candidate(registration, genome, cid, parents=parents, trace=trace)
        ledger.append({"type": "candidate", "candidate": candidate})
        aid = f"work099_attempt_{attempt_index:04d}"
        attempt_index += 1
        _reserve(ledger, cid, "representation", aid, cad=True)
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        evidence = execute_genome(genome, config["limits"], output_dir / "cad" / f"{cid}.step")
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        observed = _cost(wall_s=wall_s, cpu_s=cpu_s, cad=True)
        details = {"executed_cad": True, "physical_evaluator_executed": False, "measurement_sha256": evidence["measurement_sha256"], "measurements": evidence["measurement"], "step_sha256": evidence["geometry_sha256"]}
        _settle_representation(ledger, cid, aid, "geometry_measured", details, observed, geometry_sha256=evidence["geometry_sha256"])
        boundary = boundary_identity(genome, evidence)
        aid = f"work099_attempt_{attempt_index:04d}"
        attempt_index += 1
        _reserve(ledger, cid, "boundary", aid, cad=False)
        boundary_cost = _cost(wall_s=0.0, cpu_s=0.0, cad=False)
        status = "boundary_unresolved" if unresolved_boundary else "boundary_resolved"
        _settle_boundary(ledger, cid, aid, status, {"terminal_positions_m": evidence["measurement"]["terminal_positions_m"], "interfaces": genome["interfaces"], "injected_software_fixture_ambiguity": unresolved_boundary}, boundary_sha256=None if unresolved_boundary else boundary, cost=boundary_cost)
        context = ledger.replay()["state"]["states"][cid]["context"]
        novelty = 0.0 if evidence["functional_signature"] in seen_signatures else 1.0
        seen_signatures.add(evidence["functional_signature"])
        disposition = "unresolved" if unresolved_boundary else "feasible"
        archive_cost = observed["attempts"] + observed["geometry_executions"] + observed["cad_calls"]
        record = {"candidate_id": cid, "context_sha256": contract_digest(context), "functional_signature": evidence["functional_signature"], "descriptors": evidence["descriptors"], "disposition": disposition, "quality": None if unresolved_boundary else evidence["measurement"]["volume_m3"], "margin": None, "cost": archive_cost, "novelty": novelty, "parents": parents, "evidence_scope": EVIDENCE_SCOPE}
        archive_events.append(archive.update(record))
        deterministic[cid] = {"parents": parents, "operator": None if trace is None else trace["operator"], "genotype_sha256": digest(genome), "functional_signature": evidence["functional_signature"], "status": status, "geometry_sha256": evidence["geometry_sha256"], "measurement_sha256": evidence["measurement_sha256"], "measurement": evidence["measurement"], "boundary_sha256": None if unresolved_boundary else boundary}
        timings[cid] = {"cad_wall_s": wall_s, "cad_cpu_s": cpu_s}
        return evidence

    for seed in config["seeds"]:
        parent = root_genome(seed)
        validate_genome(parent, config["limits"])
        parent_id = parent["genome_id"]
        parent_evidence = evaluate_program(parent, parent_id, [], None)
        for step, operator in enumerate(OPERATORS, start=1):
            proposal = mutate(parent, operator, seed=seed, step=step, limits=config["limits"])
            child, trace = proposal["child"], proposal["trace"]
            cid = child["genome_id"]
            unresolved = seed == config["seeds"][-1] and operator == "rewire_interface"
            child_evidence = evaluate_program(child, cid, [parent_id], trace, unresolved_boundary=unresolved)
            if operator in GEOMETRY_OPERATORS:
                changed_hash = child_evidence["geometry_sha256"] != parent_evidence["geometry_sha256"]
                changed_measurement = _different_measurement(parent_evidence["measurement"], child_evidence["measurement"], config["measurement"]["relative_tolerance"], config["measurement"]["absolute_position_tolerance_m"])
                if not changed_hash or not changed_measurement:
                    raise CadExecutionViolation(f"geometry operator {operator} did not change executable measured geometry")
                geometry_change_proofs.append({"candidate_id": cid, "operator": operator, "geometry_hash_changed": True, "measured_field_changed": True})
            parent, parent_id, parent_evidence = child, cid, child_evidence

        invalid = deepcopy(root_genome(seed))
        invalid["genome_id"] = f"invalid_{seed}"
        invalid["parts"][0]["nodes"][1]["point_m"] = list(invalid["parts"][0]["nodes"][0]["point_m"])
        cid = invalid["genome_id"]
        trace = {"operator": "injected_invalid_edge", "seed": seed, "reason": "zero_length_edge_fixture"}
        ledger.append({"type": "candidate", "candidate": _candidate(registration, invalid, cid, parents=[], trace=None)})
        aid = f"work099_attempt_{attempt_index:04d}"
        attempt_index += 1
        _reserve(ledger, cid, "representation", aid, cad=True)
        wall_start, cpu_start = time.perf_counter(), time.process_time()
        try:
            validate_genome(invalid, config["limits"])
        except MorphologyViolation as error:
            failure = str(error)
        else:
            raise CadExecutionViolation("invalid fixture unexpectedly passed representation validation")
        wall_s, cpu_s = time.perf_counter() - wall_start, time.process_time() - cpu_start
        observed = _cost(wall_s=wall_s, cpu_s=cpu_s, cad=False)
        _settle_representation(ledger, cid, aid, "representation_invalid", {"executed_cad": False, "physical_evaluator_executed": False, "failure": failure, "failed_invariant": "minimum_edge_length_m"}, observed, geometry_sha256=None)
        context = ledger.replay()["state"]["states"][cid]["context"]
        descriptors = topology_descriptors(root_genome(seed))
        archive_cost = observed["attempts"] + observed["geometry_executions"] + observed["cad_calls"]
        failed_record = {"candidate_id": cid, "context_sha256": contract_digest(context), "functional_signature": functional_signature(root_genome(seed)), "descriptors": descriptors, "disposition": "failed", "quality": None, "margin": -float(config["limits"]["minimum_edge_length_m"]), "cost": archive_cost, "novelty": 0.0, "parents": [], "evidence_scope": EVIDENCE_SCOPE}
        archive_events.append(archive.update(failed_record))
        deterministic[cid] = {"parents": [], "operator": trace["operator"], "genotype_sha256": digest(invalid), "functional_signature": failed_record["functional_signature"], "status": "representation_invalid", "geometry_sha256": None, "measurement_sha256": None, "measurement": None, "boundary_sha256": None, "failure": failure}
        timings[cid] = {"validation_wall_s": wall_s, "validation_cpu_s": cpu_s}

    replay = ledger.replay()
    trusted = DiscoveryLedger(output_dir / "ledger.jsonl", dict(registration), expected_head=replay["head_sha256"]).replay()
    if replay != trusted:
        raise CadExecutionViolation("trusted-head decision replay mismatch")
    archive_snapshot = archive.snapshot()
    functional_signatures = {row["functional_signature"] for row in deterministic.values() if row["status"] != "representation_invalid"}
    if len(functional_signatures) < 3:
        raise CadExecutionViolation("functional architecture diversity is insufficient")
    deterministic_evidence = {
        "schema": "work099_executable_morphology_qd_result_v1",
        "config_sha256": validation["config_sha256"],
        "registration_sha256": registration["registration_sha256"],
        "candidates": deterministic,
        "geometry_change_proofs": geometry_change_proofs,
        "functional_signature_count": len(functional_signatures),
        "archive": archive_snapshot,
        "archive_events": archive_events,
        "reproduction_selection": archive.select_reproducers(),
        "claim_boundary": clone(dict(config["claim_boundary"])),
    }
    deterministic_evidence["deterministic_sha256"] = digest(deterministic_evidence)
    report = {
        "deterministic_evidence": deterministic_evidence,
        "decision_replay": {"status": "exact", "head_sha256": replay["head_sha256"], "state_sha256": replay["state_sha256"], "trusted_head_reopened": True},
        "timing_observations": timings,
        "scientific_admission": scientific_summary(replay["state"]),
        "limitations": ["software_fixture_evidence_class", "cad_geometry_only", "no_field_solver", "no_physical_or_manufacturing_feasibility", "no_race_or_discovery_claim", "timing_excluded_from_cross_run_identity"],
    }
    if report["scientific_admission"]["scientific_survivors"] != 0:
        raise CadExecutionViolation("Work 099 software fixture created a scientific survivor")
    if replay_reference is not None:
        report["execution_replay"] = _compare_reference(report, replay_reference, config["measurement"]["relative_tolerance"], config["measurement"]["absolute_position_tolerance_m"])
    _write_json(output_dir / "result.json", report)
    return report


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=ROOT / "config/experiments/executable_morphology_qd_v1.json")
    parser.add_argument("--registration", type=Path, default=ROOT / "config/experiments/discovery_contract_fixture_v1.json")
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()
    try:
        config = strict_json(args.config.read_text(encoding="utf-8"))
        registration = strict_json(args.registration.read_text(encoding="utf-8"))
        reference = strict_json(args.replay_reference.read_text(encoding="utf-8")) if args.replay_reference else None
        report = run(config, registration, args.output_dir, reference)
        summary = {
            "status": "passed",
            "candidate_count": len(report["deterministic_evidence"]["candidates"]),
            "functional_signature_count": report["deterministic_evidence"]["functional_signature_count"],
            "deterministic_sha256": report["deterministic_evidence"]["deterministic_sha256"],
            "decision_replay": report["decision_replay"]["status"],
        }
        print(json.dumps(summary, sort_keys=True))
        return 0
    except (CadExecutionViolation, MorphologyViolation, DiscoveryViolation, OSError, KeyError, ValueError) as error:
        print(f"Work 099 failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
