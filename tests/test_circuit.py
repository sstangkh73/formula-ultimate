from __future__ import annotations

import math
from pathlib import Path
import unittest

from formula_ultimate.physics.circuit import (
    CircuitInputError,
    isa_air_density_kg_per_m3,
    load_circuit_catalog,
)


ROOT = Path(__file__).resolve().parents[1]
CATALOG = ROOT / "config" / "circuits" / "real_circuits_v1.json"


class CircuitPhysicsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.profiles = load_circuit_catalog(CATALOG)
        cls.by_id = {profile.circuit_id: profile for profile in cls.profiles}

    def test_catalog_contains_exactly_ten_distinct_real_profiles(self) -> None:
        self.assertEqual(10, len(self.profiles))
        self.assertEqual(10, len(self.by_id))
        self.assertTrue(all(profile.sources for profile in self.profiles))

    def test_pressure_vectors_are_distinct_and_bounded(self) -> None:
        vectors = {profile.design_pressure.as_tuple() for profile in self.profiles}
        self.assertEqual(10, len(vectors))
        self.assertTrue(
            all(0.0 <= value <= 1.0 for vector in vectors for value in vector)
        )

    def test_mexico_altitude_reduces_isa_density(self) -> None:
        mexico = self.by_id["mexico_city_2025"]
        self.assertEqual(2_285.0, mexico.reference_altitude_m)
        self.assertIsNotNone(mexico.isa_air_density_kg_per_m3)
        self.assertLess(mexico.isa_air_density_kg_per_m3, 1.0)
        self.assertAlmostEqual(1.225, isa_air_density_kg_per_m3(0.0), places=3)

    def test_oversized_vehicle_is_rejected_by_sourced_narrow_track(self) -> None:
        monaco = self.by_id["monaco_2026"]
        assessment = monaco.assess_static_width(
            vehicle_width_m=7.0,
            clearance_per_side_m=0.25,
        )
        self.assertEqual("rejected", assessment.status)
        self.assertEqual(7.0, assessment.available_published_width_m)
        self.assertGreater(
            assessment.required_static_corridor_m,
            assessment.available_published_width_m,
        )

    def test_realistic_width_only_passes_static_screen(self) -> None:
        monaco = self.by_id["monaco_2026"]
        assessment = monaco.assess_static_width(vehicle_width_m=2.0)
        self.assertEqual("screen_passed", assessment.status)
        self.assertIn("swept-path", assessment.reason)

    def test_missing_width_is_observable_not_silently_admitted(self) -> None:
        spa = self.by_id["spa_2026"]
        assessment = spa.assess_static_width(vehicle_width_m=2.0)
        self.assertEqual("indeterminate", assessment.status)
        self.assertIsNone(assessment.available_published_width_m)
        self.assertTrue(assessment.reason)

    def test_width_evidence_is_linked_to_a_declared_source(self) -> None:
        sourced = [
            profile for profile in self.profiles if profile.published_width is not None
        ]
        self.assertGreaterEqual(len(sourced), 4)
        for profile in sourced:
            with self.subTest(circuit=profile.circuit_id):
                source_ids = {source.source_id for source in profile.sources}
                self.assertIn(profile.published_width.source_id, source_ids)

    def test_official_race_distance_difference_stays_observable(self) -> None:
        monza = self.by_id["monza_2026"]
        self.assertNotEqual(0.0, monza.race_start_offset_m)
        self.assertAlmostEqual(-309.0, monza.race_start_offset_m)

    def test_invalid_physics_inputs_are_rejected(self) -> None:
        with self.assertRaises(CircuitInputError):
            isa_air_density_kg_per_m3(math.inf)
        with self.assertRaises(CircuitInputError):
            isa_air_density_kg_per_m3(12_000.0)
        with self.assertRaises(CircuitInputError):
            self.by_id["monza_2026"].assess_static_width(vehicle_width_m=-1.0)

    def test_replay_is_deterministic(self) -> None:
        self.assertEqual(
            load_circuit_catalog(CATALOG),
            load_circuit_catalog(CATALOG),
        )


if __name__ == "__main__":
    unittest.main()
