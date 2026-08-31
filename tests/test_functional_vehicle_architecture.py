from __future__ import annotations

from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.topology import (
    FunctionalVehicleViolation,
    from_functional_mapping,
    functional_declaration_sha256,
    functional_mass_properties,
    validate_functional_vehicle,
)


ROOT = Path(__file__).resolve().parents[1]


def raw() -> dict:
    return json.loads((ROOT / "config/vehicle/functional_vehicle_architecture_v2.json").read_text(encoding="utf-8"))


def remove_connection(value: dict, identity: str) -> None:
    value["connections"] = [item for item in value["connections"] if item["connection_id"] != identity]


class FunctionalVehicleArchitectureTests(unittest.TestCase):
    def test_reference_has_complete_capabilities_paths_and_deterministic_mass(self):
        value = raw()
        vehicle = from_functional_mapping(value)
        first = validate_functional_vehicle(vehicle)
        second = validate_functional_vehicle(from_functional_mapping(deepcopy(value)))
        self.assertEqual(first, second)
        self.assertEqual(10, first["component_count"])
        self.assertEqual(48, first["port_count"])
        self.assertEqual(23, first["connection_count"])
        self.assertEqual(2, first["ground_contact_count"])
        self.assertAlmostEqual(272.55249331647553, functional_mass_properties(vehicle)["mass_kg"])
        self.assertEqual(functional_declaration_sha256(value), functional_declaration_sha256(deepcopy(value)))

    def test_missing_power_path_is_force_from_nowhere(self):
        value = raw(); remove_connection(value, "storage_to_converter")
        with self.assertRaisesRegex(FunctionalVehicleViolation, "force-from-nowhere"):
            validate_functional_vehicle(from_functional_mapping(value))

    def test_domain_direction_and_unknown_ports_fail_before_graph_admission(self):
        value = raw(); value["connections"][9]["domain"] = "thermal"
        with self.assertRaisesRegex(FunctionalVehicleViolation, "domain mismatch"):
            from_functional_mapping(value)
        value = raw(); value["connections"][9]["from_port"] = "missing"
        with self.assertRaisesRegex(FunctionalVehicleViolation, "unknown port"):
            from_functional_mapping(value)
        value = raw(); value["components"][1]["ports"][1]["direction"] = "in"
        with self.assertRaisesRegex(FunctionalVehicleViolation, "direction mismatch"):
            from_functional_mapping(value)

    def test_structural_thermal_and_control_paths_fail_independently(self):
        scenarios = (
            ("mount_heat", "structural"),
            ("converter_to_heat", "heat source"),
            ("control_brake", "uncontrolled"),
        )
        for connection, message in scenarios:
            value = raw(); remove_connection(value, connection)
            with self.subTest(connection=connection), self.assertRaisesRegex(FunctionalVehicleViolation, message):
                validate_functional_vehicle(from_functional_mapping(value))

    def test_invalid_limits_efficiency_and_created_power_or_torque_fail(self):
        value = raw(); value["connections"][9]["efficiency"] = 1.01
        with self.assertRaisesRegex(FunctionalVehicleViolation, "exceed one"):
            from_functional_mapping(value)
        value = raw(); value["components"][2]["parameters"]["maximum_output_power_w"] = 119000.0
        with self.assertRaisesRegex(FunctionalVehicleViolation, "creates undeclared power"):
            validate_functional_vehicle(from_functional_mapping(value))
        value = raw(); value["components"][3]["parameters"]["maximum_output_torque_nm"] = 1300.0
        with self.assertRaisesRegex(FunctionalVehicleViolation, "creates undeclared torque"):
            validate_functional_vehicle(from_functional_mapping(value))
        value = raw(); value["components"][0]["ports"][0]["limits"]["maximum_force_n"] = 0
        with self.assertRaisesRegex(FunctionalVehicleViolation, "positive"):
            from_functional_mapping(value)

    def test_overlap_outside_port_ground_and_connection_length_fail(self):
        value = raw(); value["components"][2]["translation_m"] = value["components"][1]["translation_m"]
        with self.assertRaisesRegex(FunctionalVehicleViolation, "overlap"):
            validate_functional_vehicle(from_functional_mapping(value))
        value = raw(); value["components"][1]["ports"][1]["local_position_m"][0] = 0.2
        with self.assertRaisesRegex(FunctionalVehicleViolation, "outside"):
            validate_functional_vehicle(from_functional_mapping(value))
        value = raw(); value["components"][4]["ports"][-1]["local_position_m"][2] = -0.13
        with self.assertRaisesRegex(FunctionalVehicleViolation, "z=0"):
            validate_functional_vehicle(from_functional_mapping(value))
        value = raw(); value["connections"][-1]["maximum_length_m"] = 0.01
        with self.assertRaisesRegex(FunctionalVehicleViolation, "length exceeded"):
            validate_functional_vehicle(from_functional_mapping(value))

    def test_cylinder_y_inertia_axis_is_geometry_derived(self):
        vehicle = from_functional_mapping(raw())
        left = next(item for item in vehicle.components if item.component_id == "left_ground_unit")
        ix, iy, iz, *_ = left.centroidal_inertia_kg_m2
        self.assertAlmostEqual(ix, iz)
        self.assertNotEqual(ix, iy)


if __name__ == "__main__":
    unittest.main()
