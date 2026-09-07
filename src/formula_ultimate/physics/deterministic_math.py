"""Elementary functions whose results do not depend on the host platform.

IEEE 754 requires correctly rounded results for +, -, *, /, and sqrt, but not
for the elementary functions. Two C libraries may therefore return results one
unit in the last place apart for the same input, and both are conforming.

That difference is invisible in a tolerance-based check and fatal to a digest.
Measured on this project, ``math.tanh`` disagreed between the Windows UCRT and
Linux glibc on 35 of 111 sampled arguments, and 9 of the first 40 calls the
slip law actually makes. A single such call changes the requested tyre force,
which changes the slip heat, which changes the run digest — so a result that was
recorded on one platform could not be reproduced on another.

The functions here are computed with :mod:`decimal`, which is a software
implementation with deterministic semantics, at a working precision far above
what a double can hold. The result is then rounded once to a float. The value is
therefore identical on every platform running the same Python, at the cost of
being roughly two orders of magnitude slower than the C library.

Use these wherever a value feeds a recorded digest. Where a value only feeds a
tolerance check, the C library is fine and faster.
"""

from __future__ import annotations

import math
from decimal import Decimal, localcontext
from functools import lru_cache

# 40 significant digits leaves a wide margin over the 17 a double needs, so
# the final rounding to float is decided long before the working precision runs
# out. The point is not extra accuracy but that the decision is made by
# libmpdec, identically everywhere, rather than by the host C library.
WORKING_PRECISION = 40

# Beyond this magnitude tanh is 1.0 (or -1.0) to within a double's resolution,
# and the series work is wasted. tanh(19) already differs from 1.0 by about
# 5e-17, below the spacing of doubles near 1.0.
_TANH_SATURATION = 20.0

# Below this magnitude tanh(x) rounds to x in double precision: the first
# correction term is x**3/3, whose size relative to x is x**2/3, and at
# x = 2**-27 that is under half an ulp. Taking this path also avoids the
# cancellation in (e**2x - 1) when e**2x is indistinguishable from 1.
_TANH_LINEAR = 2.0 ** -27

_ONE = Decimal(1)
_TWO = Decimal(2)


def tanh(value: float) -> float:
    """Return tanh(value), identically on every platform.

    Uses the identity ``tanh(x) = (e**2x - 1) / (e**2x + 1)`` evaluated in
    decimal arithmetic. ``Decimal.exp`` is correctly rounded to the context
    precision and does not consult the platform's math library.
    """
    if not math.isfinite(value):
        # NaN propagates; +-inf saturate. math.tanh already agrees everywhere
        # on these, and Decimal cannot represent them usefully here.
        return math.tanh(value)
    if value >= _TANH_SATURATION:
        return 1.0
    if value <= -_TANH_SATURATION:
        return -1.0
    if -_TANH_LINEAR <= value <= _TANH_LINEAR:
        # Returned before the cache so that -0.0 stays -0.0: a cache keyed on
        # floats cannot tell the two zeros apart, because they compare equal.
        return value
    return _tanh_decimal(value)


@lru_cache(maxsize=8192)
def _tanh_decimal(value: float) -> float:
    with localcontext() as context:
        context.prec = WORKING_PRECISION
        exponential = (_TWO * Decimal(value)).exp()
        return float((exponential - _ONE) / (exponential + _ONE))
