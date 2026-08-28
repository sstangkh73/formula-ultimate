from __future__ import annotations

from dataclasses import replace
import math
from pathlib import Path
import unittest

from formula_ultimate.physics.suspension_braking import (
    BrakeParameters,
    RegenerationParameters,
    SuspensionBrakeModule,
    SuspensionParameters,
)
from formula_ultimate.physics.thermal import ThermalParameters
from formula_ultimate.physics.tyre import TyreContactParameters
from formula_ultimate.simulation import (
    AdapterReadView,
    AerodynamicCoolingEvidence,
    CentralEnergyAuditAdapter,
    CentralEnergyConfiguration,
    CentralHealthConfiguration,
    CentralHealthEventAdapter,
    ComponentHealthConfiguration,
    ComponentHealthState,
    ContactCouplingConfig,
    ContactCouplingSpec,
    ContactEnergyTransfer,
    ContactEnergyTransfers,
    ContactNormalLoad,
    ContactRuntimeState,
    EnergyHealthCouplingError,
    RuntimeSignal,
    SharedVehicleState,
    StrategyStepCommand,
    couple_contacts,
    evaluate_central_energy,
    evaluate_central_health,
    load_coupling_architecture,
    subsystem_snapshots_from_shared_state,
)


ROOT = Path(__file__).resolve().parents[1]
ARCHITECTURE = ROOT / "config/simulation/coupled_level0_architecture_v3.json"


def shared(*, primary=1.0e6, recovered=0.0, components=None):
    return SharedVehicleState(
        0.0, 0.0, (0.0, 0.0, 0.0), (10.0, 0.0, 0.0), 0.0, 0.0,
        primary, recovered, 0,
        (ContactRuntimeState("c", 1000.0, 0.0, 0.0, 0.0, 10.0),),
        components or (ComponentHealthState("store", 300.0, 0.0, 0.0, False),),
    )


def transfers(*, drive=0.0, wheel=0.0, recovered=0.0, conversion=0.0, heat=0.0, duration=1.0):
    item = ContactEnergyTransfer("c", wheel, recovered, conversion, heat, 0.0, 1.0e6, drive)
    return ContactEnergyTransfers((item,), wheel, recovered, conversion, heat, drive, duration, duration)


def energy_config(**overrides):
    values = dict(drive_efficiency=0.9, auxiliary_power_w=0.0, recovered_capacity_j=1.0e6)
    values.update(overrides)
    return CentralEnergyConfiguration(**values)


def component(component_id="store", **overrides):
    values = dict(
        component_id=component_id,
        thermal=ThermalParameters(1000.0, 0.0, 0.0, 350.0, 400.0),
        base_heat_generation_w=0.0,
        loss_heat_fraction=1.0,
        cooling_fraction=1.0,
        degradation_rate_per_s=0.0,
        degradation_per_heat_j=0.0,
        degradation_limit=1.0,
        damage_rate_per_s=0.0,
        damage_per_heat_j=0.0,
        damage_limit=1.0,
        reliability_base_hazard_per_s=0.0,
    )
    values.update(overrides)
    return ComponentHealthConfiguration(**values)


def health_config(components=None, **overrides):
    values = dict(components=components or (component(),), random_seed=17, step_index=0, ambient_temperature_k=300.0)
    values.update(overrides)
    return CentralHealthConfiguration(**values)


def contact_step(current, duration=1.0):
    thermal = ThermalParameters(1000.0, 0.0, 0.0, 500.0, 600.0)
    module = SuspensionBrakeModule(
        "c", SuspensionParameters(100.0, 10000.0, 10.0, 1000.0, 0.2, 0.2),
        BrakeParameters(0.3, 1.0, 500.0, thermal),
        RegenerationParameters(500.0, 10000.0, 10000.0, 1.0e6, 0.8, 0.0),
    )
    spec = ContactCouplingSpec("c", 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, TyreContactParameters(2.0, 2.0), module)
    return couple_contacts(
        config=ContactCouplingConfig((spec,), 0.0, 0.0, duration, 300.0),
        normal_loads=(ContactNormalLoad("c", 1000.0),),
        command=StrategyStepCommand(0.0, 0.0, 0.0, 0.0),
        shared_state=current,
        subsystem_states=subsystem_snapshots_from_shared_state(current),
    )


def health_run(current=None, *, component_config=None, health=None, central=None, motion=None, cooling=None):
    current = current or shared()
    _, contact_energy, contact_health, _ = contact_step(current)
    central = central or evaluate_central_energy(config=energy_config(), transfers=contact_energy, state=current)
    motion = motion or replace(current, time_s=1.0, race_distance_m=10.0, position_m=(10.0, 0.0, 0.0))
    return evaluate_central_health(
        health_config=health or health_config((component_config or component(),)),
        energy_config=energy_config(),
        cooling=cooling or AerodynamicCoolingEvidence(1.0, 0.0, 0.0, "map", "evidence"),
        contact_health=contact_health,
        energy=central.evidence,
        state=current,
        energy_candidate=central.candidate_state,
        motion_candidate=motion,
    )


class EnergyHealthCouplingTests(unittest.TestCase):
    def test_v3_architecture_routes_energy_and_motion_to_health(self):
        architecture = load_coupling_architecture(ARCHITECTURE)
        health = next(x for x in architecture.ordered_modules if x.module_id == "health_event_solver")
        self.assertEqual("coupled-level0-reference-v3", architecture.architecture_id)
        self.assertIn("energy.residuals", health.consumes)
        self.assertIn("state.motion_candidate", health.consumes)
        self.assertEqual("work027-central-health-v1", health.model_version)

    def test_drive_and_auxiliary_draw_close_independent_audits(self):
        current = shared(primary=2000.0)
        result = evaluate_central_energy(
            config=energy_config(auxiliary_power_w=100.0),
            transfers=transfers(drive=900.0), state=current,
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(900.0, result.candidate_state.primary_energy_j)
        self.assertEqual(1000.0, result.evidence.drive_source_energy_j)
        self.assertEqual(100.0, result.evidence.auxiliary_energy_j)
        self.assertTrue(all(x.status == "valid" for x in (result.evidence.drive_audit, result.evidence.auxiliary_audit, result.evidence.recovery_audit)))
        self.assertTrue(all(x.passed for x in result.residuals))

    def test_recovery_and_brake_heat_close_without_primary_creation(self):
        current = shared(primary=1000.0)
        result = evaluate_central_energy(
            config=energy_config(),
            transfers=transfers(wheel=1000.0, recovered=700.0, conversion=100.0, heat=200.0), state=current,
        )
        self.assertEqual("ok", result.status)
        self.assertEqual(1000.0, result.candidate_state.primary_energy_j)
        self.assertEqual(700.0, result.candidate_state.recovered_energy_j)
        self.assertEqual(0.0, result.evidence.contact_braking_residual_j)

    def test_energy_depletion_is_analytically_localized(self):
        result = evaluate_central_energy(
            config=energy_config(auxiliary_power_w=100.0),
            transfers=transfers(drive=900.0), state=shared(primary=550.0),
        )
        self.assertEqual("ok", result.status)
        self.assertAlmostEqual(0.5, result.evidence.executed_duration_s)
        self.assertEqual("depleted", result.candidate_state.status)
        self.assertAlmostEqual(0.0, result.candidate_state.primary_energy_j)
        self.assertEqual("energy_depletion", result.events[0].event_type)

    def test_hidden_braking_energy_and_capacity_overflow_fail_closed(self):
        hidden = evaluate_central_energy(
            config=energy_config(),
            transfers=transfers(wheel=1000.0, recovered=900.0), state=shared(),
        )
        self.assertEqual("invalid", hidden.status)
        self.assertIsNone(hidden.candidate_state)
        with self.assertRaisesRegex(EnergyHealthCouplingError, "capacity"):
            evaluate_central_energy(
                config=energy_config(recovered_capacity_j=100.0),
                transfers=transfers(wheel=1000.0, recovered=800.0, conversion=200.0), state=shared(),
            )

    def test_thermal_failure_truncates_energy_motion_and_health_to_one_time(self):
        hot = component(
            thermal=ThermalParameters(100.0, 0.0, 0.0, 301.0, 302.0),
            base_heat_generation_w=1000.0,
        )
        result = health_run(component_config=hot)
        self.assertEqual("ok", result.status)
        self.assertEqual("failed", result.candidate_state.status)
        self.assertAlmostEqual(0.2, result.evidence.executed_duration_s)
        self.assertAlmostEqual(0.2, result.candidate_state.time_s)
        self.assertAlmostEqual(2.0, result.candidate_state.position_m[0])
        self.assertAlmostEqual(302.0, result.candidate_state.components[0].temperature_k)
        self.assertEqual("thermal_failure", result.evidence.decision.winner.event_type)

    def test_degradation_damage_and_seeded_reliability_are_observable(self):
        degraded = health_run(component_config=component(degradation_rate_per_s=1.0, degradation_limit=0.25))
        damaged = health_run(component_config=component(damage_rate_per_s=1.0, damage_limit=0.4))
        reliable_a = health_run(component_config=component(reliability_base_hazard_per_s=100.0), health=health_config((component(reliability_base_hazard_per_s=100.0),), random_seed=23))
        reliable_b = health_run(component_config=component(reliability_base_hazard_per_s=100.0), health=health_config((component(reliability_base_hazard_per_s=100.0),), random_seed=23))
        reliable_other = health_run(component_config=component(reliability_base_hazard_per_s=100.0), health=health_config((component(reliability_base_hazard_per_s=100.0),), random_seed=24))
        self.assertAlmostEqual(0.25, degraded.evidence.executed_duration_s)
        self.assertEqual("degradation_failure", degraded.evidence.decision.winner.event_type)
        self.assertAlmostEqual(0.4, damaged.evidence.executed_duration_s)
        self.assertEqual("damage_failure", damaged.evidence.decision.winner.event_type)
        self.assertEqual(reliable_a, reliable_b)
        self.assertNotEqual(reliable_a.evidence.executed_duration_s, reliable_other.evidence.executed_duration_s)

    def test_aerodynamic_conductance_changes_thermal_candidate(self):
        generating = component(base_heat_generation_w=1000.0)
        no_cooling = health_run(component_config=generating)
        cooling = health_run(component_config=generating, cooling=AerodynamicCoolingEvidence(1.0, 1000.0, 0.0, "map", "evidence"))
        self.assertLess(cooling.candidate_state.components[0].temperature_k, no_cooling.candidate_state.components[0].temperature_k)

    def test_contact_persistent_state_merges_when_time_is_exact(self):
        current = shared()
        _, contact_energy, contact_health, _ = contact_step(current)
        central = evaluate_central_energy(config=energy_config(), transfers=contact_energy, state=current)
        result = health_run(current, central=central)
        self.assertEqual(1, result.evidence.exact_contact_state_count)
        self.assertEqual(0, result.evidence.retained_start_contact_state_count)
        self.assertEqual(contact_health.contacts[0].end_state.time_s, result.candidate_state.time_s)

    def test_same_seed_is_component_order_invariant(self):
        components = (component("a", loss_heat_fraction=0.4, cooling_fraction=0.4, reliability_base_hazard_per_s=2.0), component("b", loss_heat_fraction=0.6, cooling_fraction=0.6, reliability_base_hazard_per_s=3.0))
        current = shared(components=(ComponentHealthState("a",300,0,0,False),ComponentHealthState("b",300,0,0,False)))
        first = health_run(current, health=health_config(components, random_seed=11))
        second = health_run(current, health=health_config(tuple(reversed(components)), random_seed=11))
        first_draws={x.component_id:x.reliability_draw for x in first.evidence.components}
        second_draws={x.component_id:x.reliability_draw for x in second.evidence.components}
        self.assertEqual(first_draws,second_draws)
        self.assertEqual(first.evidence.decision,second.evidence.decision)

    def test_adapters_emit_exact_signals_and_invalid_has_zero_writes(self):
        current=shared(); contact_result=contact_step(current); contact_energy=contact_result[1]; contact_health=contact_result[2]
        energy_adapter=CentralEnergyAuditAdapter(energy_config())
        energy_output=energy_adapter.execute(AdapterReadView("energy_graph_audit",current,(
            RuntimeSignal("contact.energy_transfers",contact_energy),RuntimeSignal("state.current",current))))
        self.assertEqual({"energy.residuals","state.energy_candidate"},{x.signal_id for x in energy_output.signals})
        energy_evidence=next(x.value for x in energy_output.signals if x.signal_id=="energy.residuals")
        energy_state=next(x.value for x in energy_output.signals if x.signal_id=="state.energy_candidate")
        motion=replace(current,time_s=1.0,race_distance_m=10.0,position_m=(10.0,0.0,0.0))
        health_adapter=CentralHealthEventAdapter(health_config(),energy_config())
        health_output=health_adapter.execute(AdapterReadView("health_event_solver",current,(
            RuntimeSignal("aero.cooling_evidence",AerodynamicCoolingEvidence(1,0,0,"map","e")),
            RuntimeSignal("contact.health_inputs",contact_health),RuntimeSignal("energy.residuals",energy_evidence),
            RuntimeSignal("state.current",current),RuntimeSignal("state.energy_candidate",energy_state),
            RuntimeSignal("state.motion_candidate",motion))))
        self.assertEqual({"health.event_candidates","health.residuals","state.health_candidate"},{x.signal_id for x in health_output.signals})
        bad=energy_adapter.execute(AdapterReadView("energy_graph_audit",current,(
            RuntimeSignal("contact.energy_transfers","bad"),RuntimeSignal("state.current",current))))
        self.assertEqual("invalid",bad.status); self.assertEqual((),bad.signals)

    def test_invalid_configuration_and_ambient_are_rejected(self):
        with self.assertRaises(EnergyHealthCouplingError): energy_config(drive_efficiency=1.1)
        with self.assertRaises(EnergyHealthCouplingError): health_config(ambient_temperature_k=0.0)
        with self.assertRaises(EnergyHealthCouplingError):
            health_config((component("a",loss_heat_fraction=.2,cooling_fraction=.5),component("b",loss_heat_fraction=.2,cooling_fraction=.5)))


if __name__ == "__main__":
    unittest.main()
