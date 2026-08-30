"""Frozen physical, CAD, and analysis adapters for the bounded campaign."""

from __future__ import annotations

from collections import Counter
from dataclasses import asdict
import hashlib
import itertools
import json
import math
from pathlib import Path
import random
import subprocess
import time
from typing import Any, Mapping, Sequence

from .main_campaign_protocol import validate_main_campaign_protocol
from .whole_vehicle_search import (
    CandidateEvaluation,
    SearchCandidate,
    canonical_sha256,
    evaluate_candidate,
    mutate_candidate_assembly,
)
from formula_ultimate.structural.vehicle_frame_refinement import (
    FrameSection,
    analytical_cantilever,
    benchmark_model,
    build_calculix_b31_deck,
    build_vehicle_frame,
    loads_from_work048,
    parse_calculix_b31_dat,
    parse_calculix_section_forces_frd,
    section_force_extreme_von_mises,
    solve_frame,
)
from formula_ultimate.topology.vehicle_assembly import from_mapping, mass_properties, validate


class CampaignPhysicsError(ValueError):
    """Raised when frozen campaign adapters or their evidence are invalid."""


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path: Path, value: Mapping[str, Any]) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n", encoding="utf-8")


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def relative_error(actual: float, reference: float) -> float:
    return abs(float(actual) - float(reference)) / max(abs(float(reference)), 1.0e-300)


def validate_campaign_environment(root: Path, protocol: Mapping[str, Any], *, ccx: Path, cadquery_python: Path, freecad_python: Path) -> dict[str, Any]:
    """Validate every pinned upstream identity and record executable identities."""
    root = Path(root)
    summary = validate_main_campaign_protocol(protocol)
    paths = {
        "assembly": root / "config/vehicle/topology_neutral_vehicle_v1.json",
        "load_protocol": root / "config/vehicle/whole_vehicle_load_cases_v1.json",
        "baseline_protocol": root / "config/vehicle/fixed_topology_end_to_end_baseline_v1.json",
        "refinement_config": root / "config/structural/section_force_vehicle_frame_refinement_v2.json",
        "readiness_config": root / "config/experiments/refined_gate_readiness_adjudication_v1.json",
        "work048": root / "artifacts/work048/experiment_summary.json",
        "work049": root / "artifacts/work049/experiment_summary.json",
        "work053": root / "artifacts/work053/experiment_summary.json",
        "work054": root / "artifacts/work054/readiness_summary.json",
    }
    for name, path in paths.items():
        if not path.is_file():
            raise CampaignPhysicsError(f"required campaign input is missing: {name}")
    for name, path in {"ccx": ccx, "cadquery_python": cadquery_python, "freecad_python": freecad_python}.items():
        if not Path(path).is_file():
            raise CampaignPhysicsError(f"required executable is missing: {name}")

    work048, work049 = read_json(paths["work048"]), read_json(paths["work049"])
    work053, work054 = read_json(paths["work053"]), read_json(paths["work054"])
    local = {
        "work047_assembly_config_sha256": file_sha256(paths["assembly"]),
        "work048_protocol_sha256": file_sha256(paths["load_protocol"]),
        "work048_training_partition_sha256": work048["partitions"]["training_sha256"],
        "work048_holdout_partition_sha256": work048["partitions"]["holdout_sha256"],
        "work049_baseline_protocol_sha256": work049["protocol_sha256"],
        "work049_reference_result_sha256": work049["reference"]["result_sha256"],
        "work049_reference_matrix_sha256": work049["replay"]["matrix_sha256"],
        "work053_evaluator_identity": work053["evaluator_identity"],
        "work053_config_sha256": file_sha256(paths["refinement_config"]),
        "work053_replay_fingerprint_sha256": work053["replay"]["fingerprint_sha256"],
        "work053_calculix_sha256": work053["tool_sha256"]["ccx"],
        "work054_config_sha256": file_sha256(paths["readiness_config"]),
        "work054_adjudication_sha256": work054["adjudication_sha256"],
    }
    if local != protocol["upstream_identity"]:
        different = sorted(name for name in set(local) | set(protocol["upstream_identity"]) if local.get(name) != protocol["upstream_identity"].get(name))
        raise CampaignPhysicsError(f"campaign upstream identity mismatch: {different}")
    if file_sha256(ccx) != local["work053_calculix_sha256"]:
        raise CampaignPhysicsError("CalculiX executable differs from frozen Work 053")
    tools = {
        "ccx_sha256": file_sha256(ccx),
        "cadquery_python_sha256": file_sha256(cadquery_python),
        "freecad_python_sha256": file_sha256(freecad_python),
    }
    return {
        "protocol_summary": asdict(summary),
        "upstream_identity": local,
        "tool_identity": tools,
        "inputs": {
            "base_assembly": read_json(paths["assembly"]),
            "work048": work048,
            "baseline_protocol": read_json(paths["baseline_protocol"]),
            "refinement_config": read_json(paths["refinement_config"]),
        },
    }


def training_evaluator_identity(protocol: Mapping[str, Any], environment: Mapping[str, Any]) -> str:
    return canonical_sha256({
        "identity": "bounded_campaign_training_level0_adapter_v1",
        "protocol_fingerprint_sha256": environment["protocol_summary"]["protocol_fingerprint_sha256"],
        "candidate_variables": protocol["design"]["candidate_variables"],
        "assembly_sha256": environment["upstream_identity"]["work047_assembly_config_sha256"],
        "training_partition_sha256": environment["upstream_identity"]["work048_training_partition_sha256"],
        "baseline_protocol_sha256": environment["upstream_identity"]["work049_baseline_protocol_sha256"],
    })


def evaluate_level0(
    execution_protocol: Mapping[str, Any], candidate: SearchCandidate, environment: Mapping[str, Any],
    evaluator_sha256: str, *, partition: str,
) -> CandidateEvaluation:
    inputs = environment["inputs"]
    return evaluate_candidate(
        execution_protocol, candidate, inputs["base_assembly"], inputs["work048"],
        inputs["baseline_protocol"], evaluator_sha256, partition=partition,
    )


def _run_ccx(ccx: Path, run_dir: Path, deck: str, section: FrameSection) -> tuple[dict[str, Any], dict[str, Any]]:
    run_dir.mkdir(parents=True, exist_ok=True)
    for suffix in (".dat", ".frd", ".sta", ".cvg", ".12d"):
        target = run_dir / ("frame" + suffix)
        if target.is_file():
            target.unlink()
    input_path = run_dir / "frame.inp"
    input_path.write_text(deck, encoding="ascii")
    started_ns = time.time_ns()
    before = time.perf_counter()
    process = subprocess.run([str(ccx), "frame"], cwd=run_dir, text=True, capture_output=True)
    wall_time_s = time.perf_counter() - before
    dat_path, frd_path = run_dir / "frame.dat", run_dir / "frame.frd"
    evidence = {
        "command": [str(ccx), "frame"], "exit_code": process.returncode,
        "stdout": process.stdout, "stderr": process.stderr, "wall_time_s": wall_time_s,
        "input_sha256": file_sha256(input_path), "output_section_id": section.section_id,
    }
    if process.returncode or not dat_path.is_file() or not frd_path.is_file():
        raise CampaignPhysicsError("CalculiX did not produce complete frame evidence")
    if dat_path.stat().st_mtime_ns < started_ns or frd_path.stat().st_mtime_ns < started_ns:
        raise CampaignPhysicsError("CalculiX frame evidence is stale")
    parsed = parse_calculix_b31_dat(dat_path.read_text(encoding="ascii", errors="replace"))
    rows = parse_calculix_section_forces_frd(frd_path.read_text(encoding="ascii", errors="replace"))
    parsed.update({"section_force_rows": rows, "maximum_surface_von_mises_pa": section_force_extreme_von_mises(rows, section)})
    evidence.update({"dat_sha256": file_sha256(dat_path), "frd_sha256": file_sha256(frd_path)})
    return parsed, evidence


def run_refinement_benchmark(config: Mapping[str, Any], *, ccx: Path, artifact_root: Path) -> dict[str, Any]:
    material, benchmark = config["material"], config["benchmark"]
    young, poisson = float(material["young_modulus_pa"]), float(material["poisson_ratio"])
    analytical = analytical_cantilever(float(benchmark["length_m"]), float(benchmark["square_side_m"]), float(benchmark["tip_force_n"]), young)
    rows = []
    for subdivisions in config["subdivisions_per_branch"]:
        model, unit = benchmark_model(float(benchmark["length_m"]), float(benchmark["square_side_m"]), int(subdivisions))
        tip = next(iter(unit))
        loads = {tip: (0.0, -float(benchmark["tip_force_n"]), 0.0, 0.0, 0.0, 0.0)}
        project = solve_frame(model, loads, young, poisson)
        calculated, process = _run_ccx(ccx, Path(artifact_root) / f"mesh_{subdivisions}", build_calculix_b31_deck(model, loads, young, poisson, "beam"), model.sections[0])
        errors = {
            "project_displacement": relative_error(project.maximum_displacement_m, analytical["tip_displacement_m"]),
            "project_stress": relative_error(project.maximum_von_mises_pa, analytical["maximum_bending_stress_pa"]),
            "calculix_displacement": relative_error(calculated["maximum_displacement_m"], analytical["tip_displacement_m"]),
            "calculix_stress": relative_error(calculated["maximum_surface_von_mises_pa"], analytical["maximum_bending_stress_pa"]),
        }
        rows.append({"subdivisions": int(subdivisions), "project": asdict(project), "calculix": calculated, "relative_errors": errors, "process": process})
    tolerance = float(config["tolerances"]["analytical_relative"])
    if max(rows[-1]["relative_errors"].values()) > tolerance:
        raise CampaignPhysicsError("fine cantilever analytical benchmark gate failed")
    for metric in ("calculix_displacement", "calculix_stress"):
        if not all(rows[index + 1]["relative_errors"][metric] < rows[index]["relative_errors"][metric] for index in range(len(rows) - 1)):
            raise CampaignPhysicsError("cantilever refinement did not reduce CalculiX error")
    draft = {"status": "passed", "analytical": analytical, "refinements": rows}
    return {**draft, "result_sha256": canonical_sha256(draft)}


def refine_candidate(
    candidate: SearchCandidate, environment: Mapping[str, Any], *, ccx: Path, artifact_root: Path,
) -> dict[str, Any]:
    config = environment["inputs"]["refinement_config"]
    material, tolerances = config["material"], config["tolerances"]
    young, poisson = float(material["young_modulus_pa"]), float(material["poisson_ratio"])
    yield_stress = float(material["yield_stress_pa"])
    base_raw = environment["inputs"]["base_assembly"]
    candidate_raw = mutate_candidate_assembly(base_raw, dict(candidate.variables))
    candidate_raw["candidate_id"] = candidate.candidate_id
    assembly = from_mapping(candidate_raw)
    validate(assembly)
    base_properties = mass_properties(from_mapping(base_raw))
    properties = mass_properties(assembly)
    mass_ratio = properties["mass_kg"] / base_properties["mass_kg"]
    work048 = environment["inputs"]["work048"]
    holdout = {row["case_id"]: row for row in work048["results"] if row["partition"] == "holdout"}
    if set(holdout) != set(work048["partitions"]["holdout"]):
        raise CampaignPhysicsError("frozen holdout evidence is incomplete")
    cases, processes = [], []
    try:
        for case_id, case in sorted(holdout.items()):
            refinements = []
            for subdivisions in config["subdivisions_per_branch"]:
                model = build_vehicle_frame(candidate_raw, int(subdivisions))
                loads = loads_from_work048(model, case, mass_ratio, base_properties["centre_of_mass_m"])
                project = solve_frame(model, loads, young, poisson)
                scale = max(1.0, max(abs(value) for wrench in loads.values() for value in wrench))
                reaction_relative = max(abs(value) for value in project.equilibrium_residual) / scale
                if reaction_relative > float(tolerances["reaction_relative"]):
                    raise CampaignPhysicsError("frame reaction equilibrium gate failed")
                section_outputs = []
                for section in model.sections:
                    run_dir = Path(artifact_root) / candidate.candidate_id / case_id / f"mesh_{subdivisions}" / section.section_id
                    calculated, process = _run_ccx(ccx, run_dir, build_calculix_b31_deck(model, loads, young, poisson, section.section_id), section)
                    section_outputs.append(calculated)
                    processes.append({"case_id": case_id, "subdivisions": int(subdivisions), "section_id": section.section_id, **process})
                displacement_values = [row["maximum_displacement_m"] for row in section_outputs]
                if max(displacement_values) - min(displacement_values) > float(tolerances["absolute"]):
                    raise CampaignPhysicsError("section-output displacement replay mismatch")
                calculated = {
                    "maximum_displacement_m": max(displacement_values),
                    "maximum_surface_von_mises_pa": max(row["maximum_surface_von_mises_pa"] for row in section_outputs),
                    "section_outputs": section_outputs,
                }
                governing = max(project.maximum_von_mises_pa, calculated["maximum_surface_von_mises_pa"])
                refinements.append({
                    "subdivisions": int(subdivisions), "project": asdict(project), "calculix": calculated,
                    "cross_model_relative": {
                        "displacement": relative_error(calculated["maximum_displacement_m"], project.maximum_displacement_m),
                        "stress": relative_error(calculated["maximum_surface_von_mises_pa"], project.maximum_von_mises_pa),
                    },
                    "reaction_relative": reaction_relative, "yield_margin": yield_stress / governing,
                })
            medium, fine = refinements[-2], refinements[-1]
            convergence = {
                name: relative_error(fine[source][key], medium[source][key])
                for name, source, key in (
                    ("project_displacement", "project", "maximum_displacement_m"),
                    ("project_stress", "project", "maximum_von_mises_pa"),
                    ("calculix_displacement", "calculix", "maximum_displacement_m"),
                    ("calculix_stress", "calculix", "maximum_surface_von_mises_pa"),
                )
            }
            converged = max(convergence.values()) <= float(tolerances["last_two_refinement_relative"])
            cross_model_passed = max(fine["cross_model_relative"].values()) <= float(tolerances["calculix_cross_model_relative"])
            stress = max(fine["project"]["maximum_von_mises_pa"], fine["calculix"]["maximum_surface_von_mises_pa"])
            displacement = max(fine["project"]["maximum_displacement_m"], fine["calculix"]["maximum_displacement_m"])
            margin = yield_stress / stress
            passed = converged and cross_model_passed and margin >= float(config["promotion"]["minimum_yield_margin"]) and displacement <= float(config["promotion"]["maximum_displacement_m"])
            cases.append({
                "case_id": case_id, "refinements": refinements, "last_two_relative": convergence,
                "converged": converged, "fine_cross_model_passed": cross_model_passed,
                "governing_yield_margin": margin, "governing_displacement_m": displacement,
                "status": "passed" if passed else "failed",
            })
        status = "passed" if all(case["status"] == "passed" for case in cases) else "failed"
        failure_code = None if status == "passed" else "refined_disagreement"
    except (ArithmeticError, OSError, ValueError, CampaignPhysicsError) as exc:
        status, failure_code = "failed", "numerical_failure"
        cases.append({"status": "failed", "failure_code": failure_code, "reason": str(exc)})
    draft = {
        "candidate_id": candidate.candidate_id, "status": status, "failure_code": failure_code,
        "candidate_geometry_sha256": canonical_sha256(candidate_raw), "mass_kg": properties["mass_kg"],
        "mass_ratio": mass_ratio, "holdout_cases": cases, "processes": processes,
        "evaluator_identity": config["evaluator_identity"],
    }
    return {**draft, "result_sha256": canonical_sha256(draft)}


def run_cad_witness(
    root: Path, candidate: SearchCandidate, environment: Mapping[str, Any], *,
    cadquery_python: Path, freecad_python: Path, artifact_root: Path,
) -> dict[str, Any]:
    artifact_root = Path(artifact_root) / candidate.candidate_id
    config_path = artifact_root / "candidate.json"
    manifest_path = artifact_root / "cadquery_manifest.json"
    freecad_path = artifact_root / "freecad_report.json"
    step_root = artifact_root / "step"
    raw = mutate_candidate_assembly(environment["inputs"]["base_assembly"], dict(candidate.variables))
    raw["candidate_id"] = candidate.candidate_id
    validate(from_mapping(raw))
    write_json(config_path, raw)
    commands = [
        [str(cadquery_python), str(Path(root) / "scripts/cad/generate_vehicle_assembly.py"), "--config", str(config_path), "--output-root", str(step_root), "--manifest", str(manifest_path)],
        [str(freecad_python), str(Path(root) / "scripts/cad/inspect_vehicle_assembly_freecad.py"), str(manifest_path), str(config_path), str(freecad_path)],
    ]
    processes = []
    for command in commands:
        before = time.perf_counter()
        process = subprocess.run(command, cwd=root, text=True, capture_output=True)
        processes.append({"command": command, "exit_code": process.returncode, "stdout": process.stdout, "stderr": process.stderr, "wall_time_s": time.perf_counter() - before})
        if process.returncode:
            draft = {"candidate_id": candidate.candidate_id, "status": "failed", "failure_code": "invalid_geometry", "processes": processes}
            return {**draft, "result_sha256": canonical_sha256(draft)}
    manifest, freecad = read_json(manifest_path), read_json(freecad_path)
    manifest_components = {row["component_id"]: row for row in manifest["components"]}
    freecad_components = {row["component_id"]: row for row in freecad["components"]}
    hashes_match = set(manifest_components) == set(freecad_components) and all(manifest_components[name]["step_sha256"] == freecad_components[name]["step_sha256"] for name in manifest_components)
    assembly_hash_match = manifest["assembly"]["step_sha256"] == freecad["assembly"]["step_sha256"]
    mass_analytical = mass_properties(from_mapping(raw))["mass_kg"]
    mass_relative = relative_error(freecad["mass_properties"]["mass_kg"], mass_analytical)
    passed = (
        manifest["candidate_id"] == candidate.candidate_id and manifest["status"] == "passed"
        and freecad["status"] == "passed" and hashes_match and assembly_hash_match
        and manifest["assembly"]["valid"] and freecad["assembly"]["valid"]
        and manifest["assembly"]["solid_count"] == freecad["assembly"]["solid_count"] == 4
        and mass_relative <= 1.0e-9
    )
    draft = {
        "candidate_id": candidate.candidate_id, "status": "passed" if passed else "failed",
        "failure_code": None if passed else "invalid_geometry", "hidden_geometry_repair": False,
        "candidate_declaration_sha256": manifest["declaration_sha256"],
        "assembly_step_sha256": manifest["assembly"]["step_sha256"],
        "assembly_hash_match": assembly_hash_match, "component_hashes_match": hashes_match,
        "solid_count": freecad["assembly"]["solid_count"], "is_valid": freecad["assembly"]["valid"],
        "analytical_mass_kg": mass_analytical, "freecad_mass_kg": freecad["mass_properties"]["mass_kg"],
        "mass_relative_error": mass_relative, "freecad_version": freecad["freecad_version"],
        "processes": processes,
    }
    return {**draft, "result_sha256": canonical_sha256(draft)}


def downstream_fingerprint(records: Sequence[Mapping[str, Any]]) -> str:
    return canonical_sha256(list(records))


def adjudicate_seed_outcomes(
    treatments: Sequence[str], seeds: Sequence[int], selections: Sequence[Mapping[str, Any]],
    holdouts: Mapping[str, CandidateEvaluation], refinements: Mapping[str, Mapping[str, Any]],
    witnesses: Mapping[str, Mapping[str, Any]],
) -> tuple[dict[str, Any], ...]:
    selected_by_stream = {(row["treatment"], int(row["seed"])): tuple(row["candidate_ids"]) for row in selections}
    outcomes = []
    for treatment in treatments:
        for seed in seeds:
            candidate_ids = selected_by_stream.get((treatment, seed), ())
            eligible = []
            for candidate_id in candidate_ids:
                holdout = holdouts[candidate_id]
                refinement = refinements[candidate_id]
                witness = witnesses[candidate_id]
                if holdout.status == "feasible" and refinement["status"] == "passed" and witness["status"] == "passed":
                    eligible.append((float(holdout.objective), candidate_id))
            eligible.sort()
            outcomes.append({
                "treatment": treatment, "seed": seed, "selected_candidates": list(candidate_ids),
                "supported_finisher_present": bool(eligible),
                "best_frozen_holdout_time_s": eligible[0][0] if eligible else None,
                "best_candidate_id": eligible[0][1] if eligible else None,
            })
    return tuple(outcomes)


def _quantile(values: Sequence[float], probability: float) -> float:
    ordered = sorted(float(value) for value in values)
    if not ordered:
        raise CampaignPhysicsError("quantile requires observations")
    position = probability * (len(ordered) - 1)
    low, high = math.floor(position), math.ceil(position)
    return ordered[low] if low == high else ordered[low] + (position - low) * (ordered[high] - ordered[low])


def analyze_main_campaign(outcomes: Sequence[Mapping[str, Any]], training_results: Sequence[CandidateEvaluation], *, analysis_seed: int, bootstrap_samples: int = 10000) -> dict[str, Any]:
    by = {(row["treatment"], int(row["seed"])): row for row in outcomes}
    seeds = sorted({int(row["seed"]) for row in outcomes})
    pairs = [(bool(by[("EVOLUTION", seed)]["supported_finisher_present"]), bool(by[("RANDOM", seed)]["supported_finisher_present"])) for seed in seeds]
    evolution_only = sum(evolution and not random_value for evolution, random_value in pairs)
    random_only = sum(random_value and not evolution for evolution, random_value in pairs)
    observed_rate = sum(int(evolution) - int(random_value) for evolution, random_value in pairs) / len(seeds)
    discordant = evolution_only + random_only
    if discordant:
        tail = sum(math.comb(discordant, index) for index in range(min(evolution_only, random_only) + 1)) / (2 ** discordant)
        mcnemar_p = min(1.0, 2.0 * tail)
    else:
        mcnemar_p = 1.0
    rng = random.Random(analysis_seed)
    rate_bootstrap = []
    for _ in range(bootstrap_samples):
        sample = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        rate_bootstrap.append(sum(int(evolution) - int(random_value) for evolution, random_value in sample) / len(sample))
    common = []
    for seed in seeds:
        evolution, random_row = by[("EVOLUTION", seed)], by[("RANDOM", seed)]
        if evolution["supported_finisher_present"] and random_row["supported_finisher_present"]:
            common.append(float(evolution["best_frozen_holdout_time_s"]) - float(random_row["best_frozen_holdout_time_s"]))
    if common:
        observed_median = float(sorted(common)[len(common) // 2]) if len(common) % 2 else 0.5 * (sorted(common)[len(common)//2-1] + sorted(common)[len(common)//2])
        permutations = []
        for signs in itertools.product((-1.0, 1.0), repeat=len(common)):
            values = sorted(sign * value for sign, value in zip(signs, common))
            permutations.append(values[len(values)//2] if len(values)%2 else 0.5*(values[len(values)//2-1]+values[len(values)//2]))
        sign_flip_p = sum(abs(value) >= abs(observed_median) - 1e-15 for value in permutations) / len(permutations)
        time_bootstrap = []
        for _ in range(bootstrap_samples):
            sample = sorted(common[rng.randrange(len(common))] for _ in common)
            time_bootstrap.append(sample[len(sample)//2] if len(sample)%2 else 0.5*(sample[len(sample)//2-1]+sample[len(sample)//2]))
        time_interval = [_quantile(time_bootstrap, 0.025), _quantile(time_bootstrap, 0.975)]
    else:
        observed_median, sign_flip_p, time_interval = None, None, [None, None]
    failure_counts = Counter(item.failure_code or "feasible" for item in training_results)
    treatment = {}
    for name in ("GRID", "RANDOM", "EVOLUTION"):
        rows = [row for row in outcomes if row["treatment"] == name]
        treatment[name] = {
            "supported_seed_count": sum(bool(row["supported_finisher_present"]) for row in rows),
            "seed_count": len(rows),
            "supported_finisher_rate": sum(bool(row["supported_finisher_present"]) for row in rows) / len(rows),
        }
    draft = {
        "analysis_seed": analysis_seed, "bootstrap_samples": bootstrap_samples,
        "primary": {
            "evolution_minus_random_rate_difference": observed_rate,
            "evolution_only_pairs": evolution_only, "random_only_pairs": random_only,
            "exact_mcnemar_two_sided_p": mcnemar_p,
            "paired_bootstrap_95_interval": [_quantile(rate_bootstrap, 0.025), _quantile(rate_bootstrap, 0.975)],
            "preferred_hypothesis_supported": observed_rate > 0.0,
        },
        "secondary": {
            "common_success_seed_count": len(common),
            "evolution_minus_random_paired_median_time_s": observed_median,
            "exact_sign_flip_two_sided_p": sign_flip_p,
            "paired_bootstrap_95_interval_s": time_interval,
            "preferred_hypothesis_supported": observed_median is not None and observed_median < 0.0,
        },
        "treatments": treatment, "training_failure_counts": dict(sorted(failure_counts.items())),
    }
    return {**draft, "analysis_sha256": canonical_sha256(draft)}
