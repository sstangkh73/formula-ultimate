"""Generate deterministic Work 023 typed-input evidence."""

from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.simulation import (  # noqa: E402
    AdapterReadView,
    CircuitEnvironmentInputAdapter,
    CircuitInputScenario,
    ComponentHealthState,
    ContactRuntimeState,
    RuntimeSignal,
    SharedVehicleState,
    SpatialStepEvidence,
    StrategyStepCommand,
    TrafficStepEvidence,
    WeatherStepEvidence,
    resolve_step_inputs,
)

CATALOG = ROOT / "config" / "circuits" / "real_circuits_v1.json"


def state() -> SharedVehicleState:
    return SharedVehicleState(
        0.0, 0.0, (0.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.0, 0.0,
        1.0e6, 0.0, 0,
        (ContactRuntimeState("reference", 1.0, 0.0, 0.0, 0.0, 0.0),),
        (ComponentHealthState("store", 300.0, 0.0, 0.0, False),),
    )


def command() -> StrategyStepCommand:
    return StrategyStepCommand(0.5, 0.0, 0.0, 0.0)


def missing(profile) -> CircuitInputScenario:
    circuit_id = profile.circuit_id
    return CircuitInputScenario(
        profile, 0.0,
        SpatialStepEvidence(circuit_id, "missing", reason="surveyed local corridor unavailable"),
        WeatherStepEvidence(circuit_id, "missing", reason="event-time weather unavailable"),
        TrafficStepEvidence(circuit_id, "missing", "catalog-gap", None, "traffic scenario unavailable"),
    )


def ready(profile) -> CircuitInputScenario:
    circuit_id = profile.circuit_id
    return CircuitInputScenario(
        profile, 10.0,
        SpatialStepEvidence(circuit_id, "available", "analytical-fixture", "segment-1", 0.01, 0.02, 0.03, 5.0, 5.0, 0.1),
        WeatherStepEvidence(circuit_id, "observed", "analytical-fixture", 300.0, 100_000.0, 0.5, (1.0, 2.0, 0.0), 0.0, 310.0),
        TrafficStepEvidence(circuit_id, "isolated_control", "analytical-control", 0),
    )


def adapter_output(scenario):
    current = state()
    view = AdapterReadView("input_bridge", current, (
        RuntimeSignal("manifest.circuit_profile", scenario),
        RuntimeSignal("manifest.current_state", current),
        RuntimeSignal("manifest.strategy_command", command()),
    ))
    return CircuitEnvironmentInputAdapter().execute(view)


def main() -> int:
    profiles = load_circuit_catalog(CATALOG)
    if len(profiles) != 10:
        raise RuntimeError(f"expected ten profiles; received {len(profiles)}")
    resolutions = [resolve_step_inputs(missing(profile), command()) for profile in profiles]
    replay = [resolve_step_inputs(missing(profile), command()) for profile in reversed(profiles)]
    first_map = {item.scenario.profile.circuit_id: item.fingerprint_sha256 for item in resolutions}
    replay_map = {item.scenario.profile.circuit_id: item.fingerprint_sha256 for item in replay}
    if first_map != replay_map:
        raise RuntimeError("catalog permutation changed input fingerprints")
    if any(item.status != "incomplete" or item.missing_evidence != ("spatial", "weather", "traffic") for item in resolutions):
        raise RuntimeError("catalog gaps were not retained exactly")

    complete = resolve_step_inputs(ready(profiles[0]), command())
    good_output = adapter_output(complete.scenario)
    bad_output = adapter_output(resolutions[0].scenario)
    if good_output.status != "ok" or len(good_output.signals) != 4:
        raise RuntimeError("complete fixture did not emit four signals")
    if bad_output.status != "invalid" or bad_output.signals:
        raise RuntimeError("incomplete fixture emitted candidate writes")

    evidence = {
        "schema_version": "1.0",
        "claim_boundary": "Work 023 typed evidence inputs only; no real local corridor/weather and no physical validation",
        "catalog_profile_count": len(profiles),
        "catalog_resolution": [
            {
                "circuit_id": item.scenario.profile.circuit_id,
                "status": item.status,
                "missing_evidence": item.missing_evidence,
                "fingerprint_sha256": item.fingerprint_sha256,
            }
            for item in resolutions
        ],
        "catalog_permutation_replay_equal": first_map == replay_map,
        "analytical_complete_fixture": {
            "status": complete.status,
            "fingerprint_sha256": complete.fingerprint_sha256,
            "adapter_status": good_output.status,
            "emitted_signal_ids": sorted(signal.signal_id for signal in good_output.signals),
            "traffic_mode": complete.scenario.traffic.mode,
        },
        "incomplete_adapter": {
            "status": bad_output.status,
            "reason": bad_output.reason,
            "emitted_signal_count": len(bad_output.signals),
        },
        "real_physics_ready_profile_count": 0,
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
