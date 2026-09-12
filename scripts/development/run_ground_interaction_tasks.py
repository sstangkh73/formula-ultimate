"""Execute Work 118 bounded ground-interaction evidence."""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import math
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SRC = ROOT / "src"
for item in (ROOT, SRC):
    if str(item) not in sys.path:
        sys.path.insert(0, str(item))

from formula_ultimate.simulation.ground_interaction_tasks import (  # noqa: E402
    GroundInteractionViolation,
    analytic_stop,
    canonical_sha256,
    contact_force,
    net_wrench,
    simulate_stopping,
    validate_protocol,
)


def read(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
        newline="\n",
    )


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1e-30)


def rejected(action, phrase: str) -> dict:
    try:
        action()
    except GroundInteractionViolation as exc:
        if phrase not in str(exc):
            raise
        return {"status": "rejected", "reason": str(exc)}
    raise GroundInteractionViolation("negative control was accepted")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=Path, required=True)
    parser.add_argument("--output-root", type=Path, required=True)
    parser.add_argument("--replay-reference", type=Path)
    args = parser.parse_args()

    config_path = (ROOT / args.config).resolve() if not args.config.is_absolute() else args.config
    output_root = (ROOT / args.output_root).resolve() if not args.output_root.is_absolute() else args.output_root
    output_root.mkdir(parents=True, exist_ok=True)
    raw = read(config_path)
    validation = validate_protocol(raw)

    for dependency in raw["dependencies"]:
        if sha256(ROOT / dependency["contract_path"]) != dependency["contract_sha256"]:
            raise GroundInteractionViolation("stale dependency contract")
        commit = subprocess.run(
            ["git", "cat-file", "-e", dependency["commit"] + "^{commit}"],
            cwd=ROOT,
            capture_output=True,
        )
        if commit.returncode:
            raise GroundInteractionViolation("missing dependency commit")

    inputs = {}
    for item in raw["inputs"]:
        result = read(ROOT / item["path"])
        if result.get("result_sha256") != item["result_sha256"]:
            raise GroundInteractionViolation(f"stale Work {item['work']} result")
        inputs[item["work"]] = result
    moving_load = inputs[114]["body"]["levels"][-1]["maximum_contact_force_n"]
    scoped_load = inputs[116]["body"]["input_evidence"]["work114_maximum_dynamic_contact_force_n"]
    if moving_load != scoped_load:
        raise GroundInteractionViolation("Work 114 load identity differs from Work 116 scope")
    if inputs[116]["body"]["candidate"]["claim_eligibility"] != "blocked_no_measured_process-qualified_material":
        raise GroundInteractionViolation("Work 116 material limitation was not preserved")
    if raw["route"]["surface_id"] != raw["surface"]["surface_id"]:
        raise GroundInteractionViolation("route and surface identity mismatch")

    mu = raw["surface"]["friction_coefficient"]
    contacts = raw["contacts"]
    propulsion = net_wrench(contacts, raw["commands"]["propulsion"], mu)
    direction = net_wrench(contacts, raw["commands"]["direction"], mu)
    saturation = net_wrench(contacts, raw["commands"]["saturation"], mu)
    for wrench in (propulsion, direction, saturation):
        for port in wrench["ports"]:
            force = port["force"]
            resultant = math.hypot(force["longitudinal_force_n"], force["lateral_force_n"])
            if resultant - force["capacity_n"] > raw["tolerances"]["force_circle_absolute_n"]:
                raise GroundInteractionViolation("force-circle gate failed")
    direction["yaw_acceleration_rad_s2"] = direction["yaw_moment_n_m"] / raw["body"]["yaw_inertia_kg_m2"]
    if direction["yaw_moment_n_m"] == 0:
        raise GroundInteractionViolation("direction command produced no yaw response")

    normal_load = sum(port["normal_load_n"] for port in contacts)
    braking_capacity = mu * normal_load
    reference = analytic_stop(
        raw["body"]["mass_kg"], raw["body"]["initial_velocity_m_s"], braking_capacity
    )
    levels = []
    for step in raw["time_steps_s"]:
        level = simulate_stopping(
            raw["body"]["mass_kg"],
            raw["body"]["initial_velocity_m_s"],
            normal_load,
            mu,
            step,
            max_time_s=raw["body"]["maximum_time_s"],
        )
        history = level.pop("history")
        history_path = output_root / f"stopping_history_{step:.3f}.json"
        write(history_path, history)
        level["history_file"] = history_path.name
        level["history_sha256"] = canonical_sha256(history)
        level["step_count"] = len(history)
        if level["status"] != "stopped":
            raise GroundInteractionViolation("reference did not stop within the registered bound")
        if level["energy_residual_relative"] > raw["tolerances"]["energy_residual_relative"]:
            raise GroundInteractionViolation("stopping energy gate failed")
        for key in ("stopping_time_s", "stopping_distance_m", "dissipated_energy_j"):
            if abs(abs(level[key]) - reference[key]) > raw["tolerances"]["analytic_stop_absolute"]:
                raise GroundInteractionViolation("analytic stopping gate failed")
        levels.append(level)
    convergence = {
        key: relative(abs(levels[-2][key]), abs(levels[-1][key]))
        for key in ("stopping_time_s", "stopping_distance_m", "dissipated_energy_j")
    }
    if any(value > raw["tolerances"]["last_two_relative_change"] for value in convergence.values()):
        raise GroundInteractionViolation("stopping refinement gate failed")

    zero = simulate_stopping(
        raw["body"]["mass_kg"],
        raw["body"]["initial_velocity_m_s"],
        normal_load,
        0.0,
        raw["time_steps_s"][-1],
        max_time_s=raw["body"]["maximum_time_s"],
    )
    reverse = simulate_stopping(
        raw["body"]["mass_kg"],
        -raw["body"]["initial_velocity_m_s"],
        normal_load,
        mu,
        raw["time_steps_s"][-1],
        max_time_s=raw["body"]["maximum_time_s"],
    )
    positive_fine = levels[-1]
    if abs(reverse["stopping_distance_m"] + positive_fine["stopping_distance_m"]) > raw["tolerances"]["analytic_stop_absolute"]:
        raise GroundInteractionViolation("reverse-motion symmetry failed")

    lift_off = contact_force(0.0, 100.0, 100.0, mu)
    disconnected = net_wrench(
        contacts, raw["commands"]["propulsion"], mu, actuation_connected=False
    )
    absent = net_wrench(
        contacts, raw["commands"]["propulsion"], mu, interaction_enabled=False
    )
    for control in (lift_off,):
        if control["longitudinal_force_n"] or control["lateral_force_n"]:
            raise GroundInteractionViolation("lift-off generated ground force")
    for control in (disconnected, absent):
        if control["longitudinal_force_n"] or control["lateral_force_n"]:
            raise GroundInteractionViolation("forbidden interaction generated ground force")
    centered_contacts = copy.deepcopy(contacts)
    centered_contacts[0]["x_m"] = 0.0
    centered = net_wrench(centered_contacts, raw["commands"]["direction"], mu)
    if centered["yaw_moment_n_m"] == direction["yaw_moment_n_m"]:
        raise GroundInteractionViolation("contact placement did not change yaw moment")

    unsupported = copy.deepcopy(raw)
    unsupported["surface"]["applicability"] = "soft_soil"
    local_loads = {}
    for wrench in (propulsion, direction, saturation):
        for port in wrench["ports"]:
            force = port["force"]
            resultant = math.hypot(force["longitudinal_force_n"], force["lateral_force_n"])
            local_loads[port["port_id"]] = max(local_loads.get(port["port_id"], 0.0), resultant)
    controls = {
        "zero_friction": {
            "status": zero["status"],
            "braking_force_n": zero["braking_force_n"],
            "dissipated_energy_j": zero["dissipated_energy_j"],
        },
        "lift_off": lift_off,
        "reverse_motion": {
            "stopping_distance_m": reverse["stopping_distance_m"],
            "braking_force_n": reverse["braking_force_n"],
        },
        "saturation": saturation,
        "disconnected_actuation": disconnected,
        "no_physical_interaction": absent,
        "placement": {
            "registered_yaw_moment_n_m": direction["yaw_moment_n_m"],
            "centered_yaw_moment_n_m": centered["yaw_moment_n_m"],
        },
        "unsupported_surface": rejected(lambda: validate_protocol(unsupported), "unsupported surface"),
    }
    body = {
        "status": "passed",
        "claim_scope": "synthetic rigid/dry Coulomb contact reference for architecture-neutral force, stopping and direction tasks; not tire, terrain, locomotion, control, or physical validation",
        "validation": validation,
        "dependencies": raw["dependencies"],
        "input_result_sha256": {str(work): result["result_sha256"] for work, result in sorted(inputs.items())},
        "surface": raw["surface"],
        "route": raw["route"],
        "force_map": {"propulsion": propulsion, "direction": direction, "saturation": saturation},
        "analytic_stop": reference,
        "stopping_levels": levels,
        "convergence": convergence,
        "controls": controls,
        "part_model_handoff": {
            "maximum_ground_resultant_by_port_n": local_loads,
            "maximum_abs_yaw_moment_n_m": max(abs(direction["yaw_moment_n_m"]), abs(saturation["yaw_moment_n_m"])),
            "work114_dynamic_contact_force_n": moving_load,
            "material_claim_eligibility": inputs[116]["body"]["candidate"]["claim_eligibility"],
        },
        "coverage": raw["coverage"],
        "review": {
            "supporting_evidence": [
                "all admitted port forces obeyed the registered Coulomb force circle",
                "three stopping resolutions matched analytic time, distance and energy references",
                "zero-friction, lift-off, reverse, saturation, disconnection, no-interaction and placement controls behaved causally",
            ],
            "contradicting_evidence": [
                "the friction coefficient and rigid surface are synthetic rather than measured"
            ],
            "alternative_explanations": [
                "constant normal load and rigid contact remove load-transfer and compliant-contact effects"
            ],
            "missing_evidence": [
                "measured surface adapter",
                "tire or other chosen interaction-device law",
                "soft-soil behavior",
                "wear and thermal evolution",
                "physical validation",
            ],
            "confidence": "high for analytic reference behavior; none for real ground-interaction prediction",
        },
    }
    result = {"body": body, "result_sha256": canonical_sha256(body)}
    write(output_root / "result.json", result)

    if args.replay_reference:
        reference_path = (ROOT / args.replay_reference).resolve() if not args.replay_reference.is_absolute() else args.replay_reference
        previous = read(reference_path)
        exact = previous.get("result_sha256") == result["result_sha256"]
        write(
            output_root / "replay.json",
            {
                "reference_result_sha256": previous.get("result_sha256"),
                "current_result_sha256": result["result_sha256"],
                "exact": exact,
            },
        )
        if not exact:
            raise GroundInteractionViolation("replay differs from reference")

    print(
        json.dumps(
            {
                "status": "passed",
                "result_sha256": result["result_sha256"],
                "stopping_distance_m": levels[-1]["stopping_distance_m"],
                "stopping_time_s": levels[-1]["stopping_time_s"],
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
