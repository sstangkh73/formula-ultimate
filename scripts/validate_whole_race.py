"""Generate deterministic Work 028 whole-race coupling evidence."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from formula_ultimate.physics.aerodynamics import (  # noqa: E402
    AerodynamicCoefficientMap,
    AerodynamicCoefficientSample,
    AerodynamicEvidence,
    AerodynamicReference,
    AerodynamicStateGrid,
)
from formula_ultimate.physics.circuit import load_circuit_catalog  # noqa: E402
from formula_ultimate.physics.lateral import (  # noqa: E402
    PlanarContact,
    PlanarVehicle,
    PlanarVehicleParameters,
)
from formula_ultimate.physics.suspension_braking import (  # noqa: E402
    BrakeParameters,
    RegenerationParameters,
    SuspensionBrakeModule,
    SuspensionParameters,
)
from formula_ultimate.physics.thermal import ThermalParameters  # noqa: E402
from formula_ultimate.physics.tyre import TyreContactParameters  # noqa: E402
from formula_ultimate.simulation import (  # noqa: E402
    AerodynamicMapAdapter,
    AerodynamicReferenceOrigin,
    CentralEnergyAuditAdapter,
    CentralEnergyConfiguration,
    CentralHealthConfiguration,
    CentralHealthEventAdapter,
    CircuitEnvironmentInputAdapter,
    CircuitInputScenario,
    ComponentHealthConfiguration,
    ComponentHealthState,
    ContactCouplingConfig,
    ContactCouplingSpec,
    ContactLimitCouplingAdapter,
    ContactRuntimeState,
    MotionConfiguration,
    MotionCorridorReference,
    NormalLoadCouplingAdapter,
    RaceProgressAdapter,
    RaceProgressConfiguration,
    SharedVehicleState,
    SpatialStepEvidence,
    StrategyStepCommand,
    TrafficStepEvidence,
    VehicleMotionCouplingAdapter,
    WeatherStepEvidence,
    WholeRaceConfiguration,
    load_coupling_architecture,
    run_whole_race,
)


ARCHITECTURE = load_coupling_architecture(
    ROOT / "config/simulation/coupled_level0_architecture_v4.json"
)
PROFILE = load_circuit_catalog(ROOT / "config/circuits/real_circuits_v1.json")[0]
TYRE = TyreContactParameters(2.0, 2.0)


def _vehicle() -> PlanarVehicle:
    mass_kg = 1000.0
    load_n = mass_kg * 9.81 / 4.0
    contacts = tuple(
        PlanarContact(contact_id, x_m, y_m, load_n, 0.0, 20000.0, 0.0, TYRE)
        for contact_id, x_m, y_m in (
            ("fl", 1.0, 0.8),
            ("fr", 1.0, -0.8),
            ("rl", -1.0, 0.8),
            ("rr", -1.0, -0.8),
        )
    )
    return PlanarVehicle(
        "fixed-four", PlanarVehicleParameters(mass_kg, 1500.0, 0.4), contacts
    )


def _aero_map() -> AerodynamicCoefficientMap:
    sample = AerodynamicCoefficientSample(0.0, 0.0, 0.0, 0.0, 0.0, 0.0)
    return AerodynamicCoefficientMap(
        "zero-aero",
        (10.0,),
        (0.05,),
        (0.0,),
        (AerodynamicStateGrid("nominal", (sample,)),),
        AerodynamicEvidence(
            "analytical-zero", "synthetic_reference", "Work 028 validator fixture"
        ),
    )


def _brake_module(component_id: str, preload_n: float) -> SuspensionBrakeModule:
    return SuspensionBrakeModule(
        component_id,
        SuspensionParameters(100.0, 10000.0, 10.0, preload_n, 0.2, 0.2),
        BrakeParameters(
            0.3, 1.0, 500.0, ThermalParameters(1000.0, 0.0, 0.0, 500.0, 600.0)
        ),
        RegenerationParameters(500.0, 10000.0, 10000.0, 1.0e6, 0.8, 0.0),
    )


@dataclass
class _ReferenceFixture:
    target_distance_m: float = 30.0
    timeout_s: float = 10.0
    evaluation_budget: int = 20
    primary_energy_j: float = 1.0e6
    auxiliary_power_w: float = 0.0
    central_heat_w: float = 0.0
    corridor_width_m: float = 100.0
    reverse_registration: bool = False
    omit_race_adapter: bool = False
    random_seed: int = 17

    def __post_init__(self) -> None:
        self.planar = _vehicle()
        self.load_n = self.planar.parameters.mass_kg * 9.81 / 4.0
        self.initial = SharedVehicleState(
            0.0,
            0.0,
            (0.0, 0.0, 0.0),
            (10.0, 0.0, 0.0),
            0.0,
            0.0,
            self.primary_energy_j,
            0.0,
            0,
            tuple(
                ContactRuntimeState(contact.contact_id, self.load_n, 0.0, 0.0, 0.0, 10.0 / 0.3)
                for contact in self.planar.contacts
            ),
            (ComponentHealthState("store", 300.0, 0.0, 0.0, False),),
        )
        self.energy = CentralEnergyConfiguration(0.9, self.auxiliary_power_w, 1.0e6)

    def _scenario(self, _step_index: int, state: SharedVehicleState) -> CircuitInputScenario:
        circuit_id = PROFILE.circuit_id
        return CircuitInputScenario(
            PROFILE,
            state.race_distance_m,
            SpatialStepEvidence(
                circuit_id,
                "available",
                "analytical-fixture",
                "straight",
                0.0,
                0.0,
                0.0,
                self.corridor_width_m,
                self.corridor_width_m,
                0.0,
            ),
            WeatherStepEvidence(
                circuit_id,
                "synthetic_control",
                "analytical-fixture",
                300.0,
                101325.0,
                0.5,
                (0.0, 0.0, 0.0),
                "local_enu",
                0.0,
                300.0,
            ),
            TrafficStepEvidence(circuit_id, "isolated_control", "analytical-fixture", 0),
        )

    @staticmethod
    def _strategy(_step_index: int, _state: SharedVehicleState) -> StrategyStepCommand:
        return StrategyStepCommand(0.0, 0.0, 0.0, 0.0)

    def _adapters(self, step_index: int, state: SharedVehicleState, duration_s: float):
        specs = tuple(
            ContactCouplingSpec(
                contact.contact_id,
                contact.x_position_m,
                contact.y_position_m,
                0.0,
                0.0,
                0.25,
                0.25,
                TYRE,
                _brake_module(contact.contact_id, self.load_n),
            )
            for contact in self.planar.contacts
        )
        component = ComponentHealthConfiguration(
            "store",
            ThermalParameters(100.0, 0.0, 0.0, 301.0, 302.0),
            self.central_heat_w,
            1.0,
            1.0,
            0.0,
            0.0,
            1.0,
            0.0,
            0.0,
            1.0,
            0.0,
        )
        adapters = (
            CircuitEnvironmentInputAdapter(),
            AerodynamicMapAdapter(
                _aero_map(),
                AerodynamicReference(1.0, 1.0, 0.1, 1005.0, 0.5),
                AerodynamicReferenceOrigin((0.0, 0.0, 0.0)),
                0.05,
                "nominal",
                state.components[0].temperature_k,
            ),
            NormalLoadCouplingAdapter(self.planar),
            ContactLimitCouplingAdapter(ContactCouplingConfig(specs, 0.0, 0.0, duration_s, 300.0)),
            VehicleMotionCouplingAdapter(
                MotionConfiguration(1000.0, 1500.0, duration_s, 1.8),
                MotionCorridorReference(
                    PROFILE.circuit_id,
                    "straight",
                    state.race_distance_m,
                    (state.race_distance_m, 0.0, 0.0),
                    0.0,
                ),
            ),
            CentralEnergyAuditAdapter(self.energy),
            CentralHealthEventAdapter(
                CentralHealthConfiguration((component,), self.random_seed, step_index, 300.0),
                self.energy,
            ),
            RaceProgressAdapter(
                RaceProgressConfiguration(self.target_distance_m, 10.0, self.timeout_s)
            ),
        )
        if self.omit_race_adapter:
            adapters = adapters[:-1]
        return tuple(reversed(adapters)) if self.reverse_registration else adapters

    def configuration(self) -> WholeRaceConfiguration:
        return WholeRaceConfiguration(
            ARCHITECTURE,
            self.initial,
            1.0,
            self.target_distance_m,
            self.timeout_s,
            self.evaluation_budget,
            self.random_seed,
            self._scenario,
            self._strategy,
            self._adapters,
        )


def main() -> int:
    reference = run_whole_race(_ReferenceFixture().configuration())
    replay = run_whole_race(_ReferenceFixture().configuration())
    reversed_registration = run_whole_race(
        _ReferenceFixture(reverse_registration=True).configuration()
    )
    depletion = run_whole_race(
        _ReferenceFixture(
            target_distance_m=100.0, primary_energy_j=5.0, auxiliary_power_w=10.0
        ).configuration()
    )
    thermal = run_whole_race(
        _ReferenceFixture(target_distance_m=100.0, central_heat_w=1000.0).configuration()
    )
    timeout = run_whole_race(
        _ReferenceFixture(target_distance_m=100.0, timeout_s=1.5).configuration()
    )
    invalid = run_whole_race(
        _ReferenceFixture(corridor_width_m=0.5).configuration()
    )

    expected = {
        "reference": ("finished", 3.0, 30.0, 3),
        "depletion": ("depleted", 0.5, 0.0),
        "thermal": ("failed", 0.2),
        "timeout": ("timeout", 1.5),
        "invalid": ("invalid", 0.0, None),
    }
    observed = {
        "reference": (
            reference.outcome,
            reference.final_state.time_s,
            reference.final_state.race_distance_m,
            len(reference.telemetry),
        ),
        "depletion": (
            depletion.outcome,
            depletion.final_state.time_s,
            depletion.final_state.primary_energy_j,
        ),
        "thermal": (thermal.outcome, thermal.final_state.time_s),
        "timeout": (timeout.outcome, timeout.final_state.time_s),
        "invalid": (
            invalid.outcome,
            invalid.final_state.time_s,
            invalid.telemetry[0].end_state_sha256,
        ),
    }
    if observed != expected:
        raise RuntimeError(f"Work 028 terminal matrix mismatch: {observed!r}")
    if reference != replay or reference != reversed_registration:
        raise RuntimeError("same-seed or registration-order replay contract failed")
    if not all(
        len(step.traces) == 8
        and step.transaction_status == "committed"
        and all(residual.passed for residual in step.residuals)
        for step in reference.telemetry
    ):
        raise RuntimeError("reference trace/residual evidence is incomplete")

    print(
        json.dumps(
            {
                "schema_version": "1.0",
                "architecture": {
                    "architecture_id": ARCHITECTURE.architecture_id,
                    "fingerprint_sha256": ARCHITECTURE.fingerprint_sha256,
                    "ordered_stage_count": len(ARCHITECTURE.ordered_modules),
                },
                "reference": {
                    "outcome": reference.outcome,
                    "committed_steps": reference.replay.committed_step_count,
                    "final_time_s": reference.final_state.time_s,
                    "final_distance_m": reference.final_state.race_distance_m,
                    "finish_distance_residual_m": reference.finish_distance_residual_m,
                    "all_residuals_passed": all(
                        residual.passed
                        for step in reference.telemetry
                        for residual in step.residuals
                    ),
                    "replay_fingerprint_sha256": reference.replay_fingerprint_sha256,
                },
                "replay": {
                    "same_seed_exact": reference == replay,
                    "reversed_registration_exact": reference == reversed_registration,
                    "scenario_fingerprint_count": len(reference.replay.scenario_fingerprints),
                    "model_version_count": len(reference.replay.model_versions),
                },
                "terminal_matrix": {
                    "depletion": {
                        "outcome": depletion.outcome,
                        "time_s": depletion.final_state.time_s,
                        "primary_energy_j": depletion.final_state.primary_energy_j,
                    },
                    "thermal": {
                        "outcome": thermal.outcome,
                        "time_s": thermal.final_state.time_s,
                    },
                    "timeout": {
                        "outcome": timeout.outcome,
                        "time_s": timeout.final_state.time_s,
                    },
                    "invalid": {
                        "outcome": invalid.outcome,
                        "committed_state": invalid.telemetry[0].end_state_sha256,
                    },
                },
                "claim_boundary": (
                    "Level-0 deterministic analytical integration evidence only; "
                    "not real-circuit prediction or physical validation"
                ),
            },
            indent=2,
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
