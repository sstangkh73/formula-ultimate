from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import unittest

from formula_ultimate.simulation.coupling import (
    ComponentHealthState,
    ContactRuntimeState,
    ResidualEntry,
    SharedVehicleState,
    load_coupling_architecture,
)
from formula_ultimate.simulation.transaction import (
    AdapterOutput,
    CoupledStepResult,
    CoupledTransactionError,
    FunctionCoupledAdapter,
    RuntimeSignal,
    execute_coupled_step,
)


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE_PATH = (
    ROOT / "config" / "simulation" / "coupled_level0_architecture_v1.json"
)


def shared_state(**overrides: object) -> SharedVehicleState:
    values: dict[str, object] = {
        "time_s": 4.0,
        "race_distance_m": 100.0,
        "position_m": (100.0, 0.0, 0.0),
        "velocity_mps": (30.0, 0.0, 0.0),
        "yaw_rad": 0.0,
        "yaw_rate_rad_per_s": 0.0,
        "primary_energy_j": 1.0e8,
        "recovered_energy_j": 0.0,
        "completed_laps": 0,
        "contacts": (
            ContactRuntimeState("front", 1_000.0, 0.0, 0.0, 0.0, 0.0),
            ContactRuntimeState("left", 1_000.0, 0.0, 0.0, 0.0, 0.0),
            ContactRuntimeState("right", 1_000.0, 0.0, 0.0, 0.0, 0.0),
        ),
        "components": (
            ComponentHealthState("store", 300.0, 0.0, 0.0, False),
        ),
    }
    values.update(overrides)
    return SharedVehicleState(**values)  # type: ignore[arg-type]


def initial_signals(
    state: SharedVehicleState, *, strategy: object | None = None
) -> tuple[RuntimeSignal, ...]:
    return (
        RuntimeSignal("manifest.circuit_profile", ("reference", 1)),
        RuntimeSignal("manifest.current_state", state),
        RuntimeSignal(
            "manifest.strategy_command",
            {"throttle": 0.5} if strategy is None else strategy,
        ),
    )


def reference_adapters(
    state: SharedVehicleState,
    *,
    replacements: dict[str, FunctionCoupledAdapter] | None = None,
    execution_log: list[str] | None = None,
) -> tuple[FunctionCoupledAdapter, ...]:
    architecture = load_coupling_architecture(ARCHITECTURE_PATH)
    replacement_map = replacements or {}
    adapters: list[FunctionCoupledAdapter] = []

    for module in architecture.ordered_modules:
        if module.module_id in replacement_map:
            adapters.append(replacement_map[module.module_id])
            continue

        def execute(view, module=module):
            if execution_log is not None:
                execution_log.append(module.module_id)
            outputs = []
            for signal_id in module.produces:
                if signal_id == "state.current":
                    value = view.read("manifest.current_state")
                elif signal_id in {
                    "state.motion_candidate",
                    "state.energy_candidate",
                    "state.health_candidate",
                }:
                    value = state
                elif signal_id == "state.next":
                    value = replace(
                        state,
                        time_s=state.time_s + 0.01,
                        race_distance_m=state.race_distance_m + 0.3,
                        position_m=(state.position_m[0] + 0.3, 0.0, 0.0),
                    )
                else:
                    value = (module.module_id, signal_id, view.signal_ids)
                outputs.append(RuntimeSignal(signal_id, value))
            return AdapterOutput(module.module_id, "ok", tuple(outputs))

        adapters.append(
            FunctionCoupledAdapter(
                module.module_id,
                module.model_version,
                execute,
            )
        )
    return tuple(adapters)


class CoupledTransactionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.architecture = load_coupling_architecture(ARCHITECTURE_PATH)

    def run_reference(
        self,
        *,
        state: SharedVehicleState | None = None,
        signals: tuple[RuntimeSignal, ...] | None = None,
        adapters: tuple[FunctionCoupledAdapter, ...] | None = None,
    ) -> CoupledStepResult:
        current = state or shared_state()
        return execute_coupled_step(
            architecture=self.architecture,
            start_state=current,
            initial_signals=signals or initial_signals(current),
            adapters=adapters or reference_adapters(current),
        )

    def test_reference_transaction_commits_once_in_architecture_order(self) -> None:
        state = shared_state()
        log: list[str] = []
        result = self.run_reference(
            state=state,
            adapters=tuple(reversed(reference_adapters(state, execution_log=log))),
        )
        self.assertEqual("committed", result.status)
        self.assertEqual(state.time_s + 0.01, result.committed_state.time_s)
        self.assertEqual(state.race_distance_m + 0.3, result.committed_state.race_distance_m)
        expected_order = tuple(
            module.module_id for module in self.architecture.ordered_modules
        )
        self.assertEqual(expected_order, tuple(log))
        self.assertEqual(expected_order, tuple(trace.module_id for trace in result.traces))
        self.assertEqual(21, len(result.published_signals))
        self.assertEqual(result.committed_state, result.read_published("state.next"))

    def test_same_inputs_replay_exactly_and_registration_order_is_irrelevant(self) -> None:
        state = shared_state()
        adapters = reference_adapters(state)
        first = self.run_reference(state=state, adapters=adapters)
        second = self.run_reference(state=state, adapters=tuple(reversed(adapters)))
        self.assertEqual(first, second)

    def test_signal_payloads_are_copied_on_ingress_and_read(self) -> None:
        mutable = {"throttle": 0.5, "history": []}
        signal = RuntimeSignal("x", mutable)
        mutable["throttle"] = 1.0
        first = signal.value
        first["history"].append("mutated")
        self.assertEqual({"throttle": 0.5, "history": []}, signal.value)

    def test_undeclared_read_rolls_back_and_stops_execution(self) -> None:
        state = shared_state()
        log: list[str] = []
        target = self.architecture.ordered_modules[2]

        def invalid_read(view):
            log.append(target.module_id)
            view.read("manifest.strategy_command")
            self.fail("undeclared read should raise")

        replacement = FunctionCoupledAdapter(
            target.module_id, target.model_version, invalid_read
        )
        result = self.run_reference(
            state=state,
            adapters=reference_adapters(
                state,
                replacements={target.module_id: replacement},
                execution_log=log,
            ),
        )
        self.assertEqual("invalid", result.status)
        self.assertEqual("adapter_exception", result.failure.code)
        self.assertEqual(target.module_id, result.failure.module_id)
        self.assertEqual(state, result.rolled_back_state)
        self.assertIsNone(result.committed_state)
        self.assertEqual((), result.published_signals)
        self.assertNotIn("vehicle_motion_solver", log)

    def test_preflight_rejects_signal_and_adapter_coverage_without_execution(self) -> None:
        state = shared_state()
        log: list[str] = []
        adapters = reference_adapters(state, execution_log=log)
        missing_signal = execute_coupled_step(
            architecture=self.architecture,
            start_state=state,
            initial_signals=initial_signals(state)[:-1],
            adapters=adapters,
        )
        self.assertEqual("initial_signal_coverage", missing_signal.failure.code)
        self.assertEqual([], log)
        missing_adapter = self.run_reference(state=state, adapters=adapters[:-1])
        self.assertEqual("adapter_coverage", missing_adapter.failure.code)
        self.assertEqual([], log)

    def test_preflight_rejects_state_and_version_mismatch(self) -> None:
        state = shared_state()
        wrong_state = replace(state, time_s=5.0)
        mismatch = self.run_reference(
            state=state, signals=initial_signals(wrong_state)
        )
        self.assertEqual("current_state_mismatch", mismatch.failure.code)

        adapters = list(reference_adapters(state))
        first = adapters[0]
        adapters[0] = FunctionCoupledAdapter(
            first.module_id, "wrong-version", first.function
        )
        wrong_version = self.run_reference(state=state, adapters=tuple(adapters))
        self.assertEqual("adapter_version_mismatch", wrong_version.failure.code)

    def test_missing_extra_wrong_identity_and_non_output_are_rejected(self) -> None:
        state = shared_state()
        target = self.architecture.ordered_modules[1]

        def evaluate(function):
            replacement = FunctionCoupledAdapter(
                target.module_id, target.model_version, function
            )
            return self.run_reference(
                state=state,
                adapters=reference_adapters(
                    state, replacements={target.module_id: replacement}
                ),
            )

        cases = (
            lambda view: AdapterOutput(
                target.module_id,
                "ok",
                (RuntimeSignal(target.produces[0], 1),),
            ),
            lambda view: AdapterOutput(
                target.module_id,
                "ok",
                tuple(RuntimeSignal(item, 1) for item in target.produces)
                + (RuntimeSignal("undeclared", 1),),
            ),
            lambda view: AdapterOutput(
                "wrong-module",
                "ok",
                tuple(RuntimeSignal(item, 1) for item in target.produces),
            ),
            lambda view: object(),
        )
        for function in cases:
            with self.subTest(function=function):
                result = evaluate(function)
                self.assertEqual("invalid", result.status)
                self.assertEqual("adapter_exception", result.failure.code)
                self.assertEqual((), result.published_signals)

    def test_adapter_invalid_and_failed_residual_roll_back(self) -> None:
        state = shared_state()
        target = self.architecture.ordered_modules[3]

        def invalid(view):
            return AdapterOutput(target.module_id, "invalid", (), reason="no contact")

        invalid_adapter = FunctionCoupledAdapter(
            target.module_id, target.model_version, invalid
        )
        invalid_result = self.run_reference(
            state=state,
            adapters=reference_adapters(
                state, replacements={target.module_id: invalid_adapter}
            ),
        )
        self.assertEqual("adapter_invalid", invalid_result.failure.code)
        self.assertEqual((), invalid_result.published_signals)

        def failed_residual(view):
            outputs = tuple(RuntimeSignal(item, 1) for item in target.produces)
            residual = ResidualEntry("force-x", "force", 2.0, "N", 0.1, 0.0, 1.0)
            return AdapterOutput(
                target.module_id, "ok", outputs, residuals=(residual,)
            )

        residual_adapter = FunctionCoupledAdapter(
            target.module_id, target.model_version, failed_residual
        )
        residual_result = self.run_reference(
            state=state,
            adapters=reference_adapters(
                state, replacements={target.module_id: residual_adapter}
            ),
        )
        self.assertEqual("residual_failure", residual_result.failure.code)
        self.assertEqual(state, residual_result.rolled_back_state)
        self.assertEqual((), residual_result.published_signals)
        self.assertEqual(1, len(residual_result.residuals))
        self.assertEqual("force-x", residual_result.residuals[0].residual_id)
        self.assertEqual(2.0, residual_result.residuals[0].value)
        self.assertEqual("N", residual_result.residuals[0].unit)

    def test_invalid_adapter_cannot_return_candidate_writes(self) -> None:
        state = shared_state()
        target = self.architecture.ordered_modules[0]

        def invalid_with_write(view):
            return AdapterOutput(
                target.module_id,
                "invalid",
                (RuntimeSignal(target.produces[0], 1),),
                reason="bad input",
            )

        adapter = FunctionCoupledAdapter(
            target.module_id, target.model_version, invalid_with_write
        )
        result = self.run_reference(
            state=state,
            adapters=reference_adapters(
                state, replacements={target.module_id: adapter}
            ),
        )
        self.assertEqual("adapter_exception", result.failure.code)
        self.assertIn("cannot contain candidate writes", result.failure.reason)

    def test_final_state_type_time_and_distance_are_fail_closed(self) -> None:
        state = shared_state()
        target = self.architecture.ordered_modules[-1]

        def with_next(next_state):
            def execute(view):
                values = []
                for signal_id in target.produces:
                    values.append(
                        RuntimeSignal(
                            signal_id,
                            next_state if signal_id == "state.next" else (),
                        )
                    )
                return AdapterOutput(target.module_id, "ok", tuple(values))

            return FunctionCoupledAdapter(
                target.module_id, target.model_version, execute
            )

        cases = (
            ("not-state", "next_state_type"),
            (replace(state, time_s=state.time_s - 1.0), "time_regression"),
            (
                replace(state, race_distance_m=state.race_distance_m - 1.0),
                "distance_regression",
            ),
        )
        for next_state, code in cases:
            with self.subTest(code=code):
                result = self.run_reference(
                    state=state,
                    adapters=reference_adapters(
                        state,
                        replacements={target.module_id: with_next(next_state)},
                    ),
                )
                self.assertEqual("invalid", result.status)
                self.assertEqual(code, result.failure.code)
                self.assertEqual(state, result.rolled_back_state)
                self.assertEqual((), result.published_signals)

    def test_result_and_output_contracts_reject_inconsistent_records(self) -> None:
        with self.assertRaises(CoupledTransactionError):
            AdapterOutput("x", "invalid", (), reason=None)
        with self.assertRaises(CoupledTransactionError):
            AdapterOutput("x", "ok", (), reason="unexpected")
        with self.assertRaises(CoupledTransactionError):
            AdapterOutput(
                "x",
                "ok",
                (RuntimeSignal("same", 1), RuntimeSignal("same", 2)),
            )


if __name__ == "__main__":
    unittest.main()
