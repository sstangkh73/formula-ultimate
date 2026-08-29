"""Structural solver contracts and verification evidence."""

from .acceptance import (
    BendingSpec,
    MeshData,
    StructuralEvidenceError,
    TensionSpec,
    TorsionSpec,
    build_bending_calculix_input,
    build_calculix_input,
    build_torsion_calculix_input,
    parse_calculix_dat,
    parse_msh2,
)
from .nonlinear_column import (
    ResponsePoint,
    cantilever_first_mode,
    imperfect_mesh,
    response_is_strictly_monotonic,
    secant_amplification,
    shaped_imperfect_mesh,
    smooth_cubic_crookedness,
)

__all__ = [
    "BendingSpec",
    "MeshData",
    "StructuralEvidenceError",
    "TensionSpec",
    "TorsionSpec",
    "build_bending_calculix_input",
    "build_calculix_input",
    "build_torsion_calculix_input",
    "parse_calculix_dat",
    "parse_msh2",
    "ResponsePoint",
    "cantilever_first_mode",
    "imperfect_mesh",
    "response_is_strictly_monotonic",
    "secant_amplification",
    "shaped_imperfect_mesh",
    "smooth_cubic_crookedness",
]
