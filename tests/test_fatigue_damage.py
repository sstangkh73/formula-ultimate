from __future__ import annotations

from dataclasses import replace
from decimal import Decimal
import unittest

from formula_ultimate.structural import FatigueMaterialRecord, RainflowCycle, StructuralEvidenceError, aggregate_cycles, corrected_amplitude_goodman, evaluate_damage_blocks, rainflow_cycles, reversal_history


def record() -> FatigueMaterialRecord:
    return FatigueMaterialRecord("r", 200e6, 1000, 5, 80e6, 300e6, 500e6, 2, "synthetic only", False)


class FatigueDamageTests(unittest.TestCase):
    def test_constant_amplitude_rainflow_count_is_exact(self) -> None:
        cycles = aggregate_cycles(rainflow_cycles(reversal_history(-200e6, 200e6, 12)))
        self.assertEqual(12.0, sum(item.count for item in cycles))
        self.assertEqual({400e6}, {item.range_pa for item in cycles})

    def test_constant_damage_crosses_at_reference_life_without_clipping(self) -> None:
        cycles = rainflow_cycles(reversal_history(-200e6, 200e6, 1200))
        result = evaluate_damage_blocks(record(), (("constant", cycles),))
        self.assertEqual(Decimal("1.2"), Decimal(result.cumulative_damage))
        self.assertEqual(1000.0, result.event_cycle)
        self.assertTrue(result.failed)

    def test_goodman_and_curve_domain_fail_closed(self) -> None:
        self.assertAlmostEqual(200e6, corrected_amplitude_goodman(record(), RainflowCycle(200e6, 250e6, 1)))
        with self.assertRaisesRegex(StructuralEvidenceError, "above"):
            corrected_amplitude_goodman(record(), RainflowCycle(640e6, 0, 1))
        with self.assertRaisesRegex(StructuralEvidenceError, "below"):
            corrected_amplitude_goodman(record(), RainflowCycle(100e6, 0, 1))
        with self.assertRaisesRegex(StructuralEvidenceError, "ultimate"):
            corrected_amplitude_goodman(record(), RainflowCycle(100e6, 500e6, 1))

    def test_replay_is_exact_and_unsourced_curve_is_rejected(self) -> None:
        blocks = (("a", rainflow_cycles(reversal_history(-160e6, 160e6, 10))),)
        self.assertEqual(evaluate_damage_blocks(record(), blocks), evaluate_damage_blocks(record(), blocks))
        with self.assertRaises(StructuralEvidenceError):
            replace(record(), provenance="")


if __name__ == "__main__":
    unittest.main()
