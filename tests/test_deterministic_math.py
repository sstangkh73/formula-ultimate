"""The deterministic elementary functions must not drift between platforms.

These expectations are exact bit patterns, not tolerances. That is the point:
the reason ``deterministic_math`` exists is that a one-ulp difference is enough
to change a recorded run digest, and a tolerance-based test would not notice.

If a case here fails on a platform where it used to pass, the reproducibility
contract is broken and any digest recorded before the change is no longer
comparable with one recorded after it.
"""

from __future__ import annotations

import math
import unittest

from formula_ultimate.physics.deterministic_math import tanh

# Argument and expected result, both as exact hex literals.
TANH_CASES = (
    ('0x1.0000000000000p-1', '0x1.d9353d7568af3p-2'),
    ('0x1.0000000000000p-3', '0x1.fd5992bc4b835p-4'),
    ('0x1.8000000000000p-6', '0x1.7fee010324732p-6'),
    ('0x1.0000000000000p+0', '0x1.85efab514f394p-1'),
    ('0x1.0000000000000p+1', '0x1.ed9505e1bc3d4p-1'),
    ('0x1.c000000000000p+1', '0x1.ff112c63a9077p-1'),
    ('0x1.0624dd2f1a9fcp-10', '0x1.0624d77516ce2p-10'),
    ('0x1.d000000000000p+2', '0x1.ffffde2760a41p-1'),
    ('0x1.1df46a2529d39p-6', '0x1.1decfb7fffb8dp-6'),
    ('0x1.5555555555555p-2', '0x1.493aa293c8802p-2'),
    # The argument at which the Windows and Linux C libraries were first
    # observed to disagree during this investigation: the platform math library
    # returned ...385 on one and ...386 on the other.
    ('0x1.3755407c17994p-10', '0x1.375536e449385p-10'),
)


class DeterministicTanhTests(unittest.TestCase):
    def test_values_are_bit_exact(self) -> None:
        for argument_hex, expected_hex in TANH_CASES:
            with self.subTest(argument=argument_hex):
                result = tanh(float.fromhex(argument_hex))
                self.assertEqual(expected_hex, result.hex())

    def test_stays_close_to_the_c_library(self) -> None:
        """Deterministic does not mean different: it must still be tanh.

        The allowance is expressed in units in the last place of the result,
        via math.ulp, not as a fixed relative bound. A relative bound of 2**-52
        is only an upper estimate of one ulp when the value sits just above a
        power of two, and is too tight everywhere else.

        Two ulp of headroom is deliberate. This function is effectively
        correctly rounded, while a platform C library is typically specified to
        within one or two ulp, so the gap between them can legitimately reach
        two without either being wrong. A tighter bound would test the host
        library rather than this code.
        """
        for index in range(1, 4000):
            value = index / 512.0
            with self.subTest(value=value):
                reference = math.tanh(value)
                result = tanh(value)
                self.assertLessEqual(abs(result - reference), 2.0 * math.ulp(reference))

    def test_saturation_and_sign(self) -> None:
        self.assertEqual(1.0, tanh(25.0))
        self.assertEqual(-1.0, tanh(-25.0))
        self.assertEqual(1.0, tanh(math.inf))
        self.assertEqual(-1.0, tanh(-math.inf))
        self.assertTrue(math.isnan(tanh(math.nan)))

    def test_small_arguments_return_unchanged_and_keep_signed_zero(self) -> None:
        for value in (0.0, 1e-300, 1e-20, 2.0 ** -28):
            with self.subTest(value=value):
                self.assertEqual(value, tanh(value))
                self.assertEqual(-value, tanh(-value))
        self.assertEqual(math.copysign(1.0, -0.0), math.copysign(1.0, tanh(-0.0)))

    def test_is_monotonic_and_odd(self) -> None:
        previous = tanh(-3.0)
        for index in range(-2999, 3000):
            value = index / 1000.0
            current = tanh(value)
            self.assertGreaterEqual(current, previous)
            self.assertEqual(current, -tanh(-value))
            previous = current


if __name__ == "__main__":
    unittest.main()
