from __future__ import annotations

from dataclasses import replace
from copy import deepcopy
import json
from pathlib import Path
import unittest

from formula_ultimate.simulation.linkage_motion_ratio import (
    LinkageMotionRatioError,
    apply_linkage_motion_ratios,
    derive_motion_ratio,
    load_linkage_motion_ratio_config,
)
from formula_ultimate.simulation.sprung_body_vertical_coupling import (
    run_sprung_body_vertical_coupling,
)
from tests.test_sprung_body_vertical_coupling import loaded as loaded_vertical


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "vehicle" / "geometry_linkage_motion_ratio_v1.json"
WORK073_REFERENCE_SHA256 = "802330a0566c746d00beb3f5a6cddb725cfee4a9e9f85e08a8bd509b4a6ce973"


def loaded(section: str = "linkages"):
    _, _, vertical, powertrain = loaded_vertical()
    raw = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    config = load_linkage_motion_ratio_config(raw, geometry_section=section)
    return raw, config, vertical, powertrain


class LinkageMotionRatioTests(unittest.TestCase):
    def test_geometry_derives_expected_ratios_and_virtual_work_scaling(self) -> None:
        _, config, vertical, _ = loaded()
        application = apply_linkage_motion_ratios(config, vertical)
        evidence = {item.contact_id: item for item in application.evidence}
        transformed = {item.contact_id: item for item in application.transformed_vertical.contacts}
        original = {item.contact_id: item for item in vertical.contacts}
        self.assertAlmostEqual(0.8, evidence["left_ground_contact"].motion_ratio)
        self.assertAlmostEqual(1.0, evidence["rear_ground_contact"].motion_ratio)
        self.assertAlmostEqual(0.8, evidence["right_ground_contact"].motion_ratio)
        self.assertAlmostEqual(
            original["left_ground_contact"].suspension_stiffness_n_per_m * 0.64,
            transformed["left_ground_contact"].suspension_stiffness_n_per_m,
        )
        self.assertAlmostEqual(
            original["left_ground_contact"].maximum_compression_m / 0.8,
            transformed["left_ground_contact"].maximum_compression_m,
        )

    def test_unit_ratio_control_preserves_work073_exactly(self) -> None:
        _, config, vertical, powertrain = loaded("unit_ratio_control")
        application = apply_linkage_motion_ratios(config, vertical)
        result = run_sprung_body_vertical_coupling(
            application.transformed_vertical, powertrain, sample_stride=25
        )
        self.assertTrue(all(item.motion_ratio == 1.0 for item in application.evidence))
        self.assertEqual(WORK073_REFERENCE_SHA256, result.result_sha256)

    def test_nonunit_geometry_changes_coupled_response_and_retains_energy(self) -> None:
        _, config, vertical, powertrain = loaded()
        application = apply_linkage_motion_ratios(config, vertical)
        reference = run_sprung_body_vertical_coupling(vertical, powertrain, sample_stride=100)
        changed = run_sprung_body_vertical_coupling(
            application.transformed_vertical, powertrain, sample_stride=100
        )
        self.assertEqual(("passed", "finished"), (changed.status, changed.outcome))
        self.assertNotEqual(reference.result_sha256, changed.result_sha256)
        self.assertNotEqual(reference.maximum_abs_heave_m, changed.maximum_abs_heave_m)
        self.assertLessEqual(
            changed.maximum_total_global_relative_energy_residual,
            application.transformed_vertical.global_energy_relative_tolerance,
        )

    def test_axis_scaling_and_spatial_mirror_preserve_ratio(self) -> None:
        _, config, _, _ = loaded()
        base = config.linkages[0]
        scaled = replace(base, rotation_axis=tuple(3.0 * item for item in base.rotation_axis))
        mirrored = replace(
            base,
            pivot_m=tuple(-item if index == 0 else item for index, item in enumerate(base.pivot_m)),
            wheel_pickup_m=tuple(-item if index == 0 else item for index, item in enumerate(base.wheel_pickup_m)),
            spring_pickup_m=tuple(-item if index == 0 else item for index, item in enumerate(base.spring_pickup_m)),
            rotation_axis=tuple(-item for item in base.rotation_axis),
        )
        self.assertAlmostEqual(
            derive_motion_ratio(base).motion_ratio, derive_motion_ratio(scaled).motion_ratio
        )
        self.assertAlmostEqual(
            derive_motion_ratio(base).motion_ratio, derive_motion_ratio(mirrored).motion_ratio
        )

    def test_permutation_is_canonical_in_vertical_contact_order(self) -> None:
        _, config, vertical, _ = loaded()
        reversed_config = replace(config, linkages=tuple(reversed(config.linkages)))
        first = apply_linkage_motion_ratios(config, vertical)
        second = apply_linkage_motion_ratios(reversed_config, vertical)
        self.assertEqual(first, second)

    def test_geometry_mutation_changes_application_identity(self) -> None:
        _, config, vertical, _ = loaded()
        changed_linkage = replace(
            config.linkages[0], spring_pickup_m=(0.18, 0.0, 0.0)
        )
        changed = replace(config, linkages=(changed_linkage,) + config.linkages[1:])
        self.assertNotEqual(
            apply_linkage_motion_ratios(config, vertical).application_sha256,
            apply_linkage_motion_ratios(changed, vertical).application_sha256,
        )

    def test_degenerate_and_opposed_geometry_fail_closed(self) -> None:
        _, config, _, _ = loaded()
        base = config.linkages[0]
        with self.assertRaises(LinkageMotionRatioError):
            derive_motion_ratio(replace(base, wheel_pickup_m=base.pivot_m))
        with self.assertRaises(LinkageMotionRatioError):
            derive_motion_ratio(replace(base, spring_pickup_m=base.pivot_m))
        with self.assertRaises(LinkageMotionRatioError):
            derive_motion_ratio(
                replace(base, spring_direction=tuple(-item for item in base.spring_direction))
            )

    def test_invalid_contract_and_missing_contact_fail_closed(self) -> None:
        raw, config, vertical, _ = loaded()
        invalid = deepcopy(raw)
        invalid["model_version"] = "wrong"
        with self.assertRaises(LinkageMotionRatioError):
            load_linkage_motion_ratio_config(invalid)
        invalid = deepcopy(raw)
        invalid["linkages"][0]["rotation_axis"] = [0.0, 0.0, 0.0]
        bad = load_linkage_motion_ratio_config(invalid)
        with self.assertRaises(LinkageMotionRatioError):
            apply_linkage_motion_ratios(bad, vertical)
        with self.assertRaises(LinkageMotionRatioError):
            apply_linkage_motion_ratios(replace(config, linkages=config.linkages[:-1]), vertical)


if __name__ == "__main__":
    unittest.main()
