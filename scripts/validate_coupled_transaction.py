"""Generate deterministic Work 022 atomic transaction evidence."""

from __future__ import annotations

from dataclasses import replace
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.simulation import (  # noqa: E402
    AdapterOutput,
    ComponentHealthState,
    ContactRuntimeState,
    FunctionCoupledAdapter,
    ResidualEntry,
    RuntimeSignal,
    SharedVehicleState,
    execute_coupled_step,
    load_coupling_architecture,
)


ARCHITECTURE_PATH = (
    ROOT / "config" / "simulation" / "coupled_level0_architecture_v1.json"
)


def make_state() -> SharedVehicleState:
    return SharedVehicleState(
        time_s=4.0,
        race_distance_m=100.0,
        position_m=(100.0, 0.0, 0.0),
        velocity_mps=(30.0, 0.0, 0.0),
        yaw_rad=0.0,
        yaw_rate_rad_per_s=0.0,
        primary_energy_j=1.0e8,
        recovered_energy_j=0.0,
        completed_laps=0,
        contacts=(
            ContactRuntimeState("front", 1_000.0, 0.0, 0.0, 0.0, 0.0),
            ContactRuntimeState("left", 1_000.0, 0.0, 0.0, 0.0, 0.0),
            ContactRuntimeState("right", 1_000.0, 0.0, 0.0, 0.0, 0.0),
        ),
        components=(
            ComponentHealthState("store", 300.0, 0.0, 0.0, False),
        ),
    )


def make_initial(state: SharedVehicleState) -> tuple[RuntimeSignal, ...]:
    return (
        RuntimeSignal("manifest.circuit_profile", ("reference", 1)),
        RuntimeSignal("manifest.current_state", state),
        RuntimeSignal("manifest.strategy_command", ("throttle", 0.5)),
    )


def make_adapters(state, architecture, replacements=None, execution_log=None):
    replacements = replacements or {}
    adapters = []
    for module in architecture.ordered_modules:
        if module.module_id in replacements:
            adapters.append(replacements[module.module_id])
            continue

        def execute(view, module=module):
            if execution_log is not None:
                execution_log.append(module.module_id)
            signals = []
            for signal_id in module.produces:
                if signal_id == "state.current":
                    value = view.read("manifest.current_state")
                elif signal_id.startswith("state."):
                    value = state
                else:
                    value = (module.module_id, signal_id, view.signal_ids)
                if signal_id == "state.next":
                    value = replace(
                        state,
                        time_s=state.time_s + 0.01,
                        race_distance_m=state.race_distance_m + 0.3,
                        position_m=(state.position_m[0] + 0.3, 0.0, 0.0),
                    )
                signals.append(RuntimeSignal(signal_id, value))
            return AdapterOutput(module.module_id, "ok", tuple(signals))

        adapters.append(
            FunctionCoupledAdapter(module.module_id, module.model_version, execute)
        )
    return tuple(adapters)


def require_invalid(result, code, state):
    if result.status != "invalid" or result.failure.code != code:
        raise RuntimeError(f"expected invalid {code!r}; received {result!r}")
    if result.committed_state is not None or result.published_signals:
        raise RuntimeError("invalid transaction exposed partial commit")
    if result.rolled_back_state != state:
        raise RuntimeError("invalid transaction did not retain start state")
    return {
        "code": result.failure.code,
        "module_id": result.failure.module_id,
        "published_signal_count": len(result.published_signals),
        "rolled_back_to_start": result.rolled_back_state == state,
        "trace_count": len(result.traces),
        "retained_residuals": [
            {
                "residual_id": item.residual_id,
                "value": item.value,
                "unit": item.unit,
                "tolerance": item.tolerance,
            }
            for item in result.residuals
        ],
        "retained_event_ids": [item.event_id for item in result.events],
    }


def main() -> int:
    architecture = load_coupling_architecture(ARCHITECTURE_PATH)
    state = make_state()
    initial = make_initial(state)
    execution_log = []
    adapters = make_adapters(state, architecture, execution_log=execution_log)
    reference = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=initial,
        adapters=tuple(reversed(adapters)),
    )
    replay = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=tuple(reversed(initial)),
        adapters=adapters,
    )
    if reference.status != "committed" or reference != replay:
        raise RuntimeError("reference transaction did not commit/replay exactly")

    missing_initial = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=initial[:-1],
        adapters=adapters,
    )

    target = architecture.ordered_modules[3]

    def invalidate(_view):
        return AdapterOutput(target.module_id, "invalid", (), reason="injected")

    invalid_adapter = FunctionCoupledAdapter(
        target.module_id, target.model_version, invalidate
    )
    mid_invalid = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=initial,
        adapters=make_adapters(
            state,
            architecture,
            replacements={target.module_id: invalid_adapter},
        ),
    )

    def fail_residual(_view):
        signals = tuple(RuntimeSignal(signal_id, ()) for signal_id in target.produces)
        return AdapterOutput(
            target.module_id,
            "ok",
            signals,
            residuals=(
                ResidualEntry("force-x", "force", 2.0, "N", 0.1, 0.0, 1.0),
            ),
        )

    residual_adapter = FunctionCoupledAdapter(
        target.module_id, target.model_version, fail_residual
    )
    residual_failure = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=initial,
        adapters=make_adapters(
            state,
            architecture,
            replacements={target.module_id: residual_adapter},
        ),
    )

    next_module = architecture.ordered_modules[-1]

    def regress(view):
        signals = tuple(
            RuntimeSignal(
                signal_id,
                replace(state, time_s=state.time_s - 1.0)
                if signal_id == "state.next"
                else (),
            )
            for signal_id in next_module.produces
        )
        return AdapterOutput(next_module.module_id, "ok", signals)

    regressing_adapter = FunctionCoupledAdapter(
        next_module.module_id, next_module.model_version, regress
    )
    regressing = execute_coupled_step(
        architecture=architecture,
        start_state=state,
        initial_signals=initial,
        adapters=make_adapters(
            state,
            architecture,
            replacements={next_module.module_id: regressing_adapter},
        ),
    )

    evidence = {
        "schema_version": "1.0",
        "claim_boundary": (
            "Work 022 generic atomic adapter transaction only; "
            "no coupled domain physics or physical validation"
        ),
        "architecture_fingerprint_sha256": architecture.fingerprint_sha256,
        "reference": {
            "status": reference.status,
            "adapter_registration_permutation_equal": reference == replay,
            "execution_order": [trace.module_id for trace in reference.traces],
            "trace_count": len(reference.traces),
            "published_signal_count": len(reference.published_signals),
            "start_time_s": state.time_s,
            "committed_time_s": reference.committed_state.time_s,
            "start_distance_m": state.race_distance_m,
            "committed_distance_m": reference.committed_state.race_distance_m,
        },
        "falsification": [
            require_invalid(missing_initial, "initial_signal_coverage", state),
            require_invalid(mid_invalid, "adapter_invalid", state),
            require_invalid(residual_failure, "residual_failure", state),
            require_invalid(regressing, "time_regression", state),
        ],
        "domain_physics_adapter_count": 0,
    }
    print(json.dumps(evidence, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
