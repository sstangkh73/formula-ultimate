"""Functional (goal v2) vehicle manifest helpers (pure Python).

The v2 package is the v1 package plus four top-level fields: ``up_axis``
(``"z"``), ``motions``, ``function_evidence`` and ``vehicle_inertia_kg_m2``.
The inertia tensor is integrated from the re-read exported leaf meshes, never
estimated. Representation only; nothing here is physical validation.
"""

from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

import numpy as np

from .part_tree import canonical_sha256


DESIGN_LANGUAGE_VERSION_V2 = "func-composition-v2"
UP_AXIS = "z"

# Second moments of the unit tetrahedron (0, e1, e2, e3): integral of x_i x_j
# over it equals CANONICAL[i, j] times the frame determinant.
_CANONICAL = np.array([[2.0, 1.0, 1.0], [1.0, 2.0, 1.0], [1.0, 1.0, 2.0]]) / 120.0


def mesh_inertia(meshes_and_density: Iterable[tuple[np.ndarray, float]]) -> tuple[float, np.ndarray, np.ndarray]:
    """Mass (kg), centre of mass (m) and inertia tensor about it (kg m^2).

    Each mesh is an ``(n, 3, 3)`` array of closed, outward-oriented triangles
    in metres with a uniform density in kg/m^3. Every triangle spans a signed
    tetrahedron with the origin; volume, first and second moments are summed
    exactly, then shifted to the centre of mass.
    """

    mass, first, second = 0.0, np.zeros(3), np.zeros((3, 3))
    for tris, density in meshes_and_density:
        tris = np.asarray(tris, dtype=np.float64)
        a, b, c = tris[:, 0], tris[:, 1], tris[:, 2]
        det = np.einsum("ij,ij->i", a, np.cross(b, c))
        mass += density * det.sum() / 6.0
        first += density * (det[:, None] * (a + b + c)).sum(axis=0) / 24.0
        frames = np.stack([a, b, c], axis=2)
        second += density * np.einsum("n,nij,jk,nlk->il", det, frames, _CANONICAL, frames)
    if not mass > 0.0:
        raise ValueError(f"non-positive total mass {mass!r}")
    com = first / mass
    covariance = second - mass * np.outer(com, com)
    inertia = np.trace(covariance) * np.eye(3) - covariance
    return float(mass), com, inertia


def config_sha256_v2(v1_config_sha256: str) -> str:
    """Configuration hash of the v2 generator over the v1 composition hash."""

    return canonical_sha256({"design_language_version": DESIGN_LANGUAGE_VERSION_V2,
                             "v1_composition_config_sha256": v1_config_sha256})


def build_functional_manifest(v1_manifest: Mapping[str, Any], motions: Sequence[Mapping[str, Any]],
                              function_evidence: Mapping[str, Any], inertia_kg_m2: np.ndarray,
                              config_sha256: str) -> dict:
    """The v1 manifest extended with exactly the v2 top-level fields."""

    inertia = np.asarray(inertia_kg_m2, dtype=float)
    if inertia.shape != (3, 3) or not np.all(np.isfinite(inertia)):
        raise ValueError("vehicle inertia must be a finite 3x3 matrix")
    manifest = dict(v1_manifest)
    manifest.update({
        "design_language_version": DESIGN_LANGUAGE_VERSION_V2,
        "config_sha256": config_sha256,
        "up_axis": UP_AXIS,
        "motions": [dict(m) for m in motions],
        "function_evidence": {k: dict(v) for k, v in function_evidence.items()},
        "vehicle_inertia_kg_m2": [[float(v) for v in row] for row in inertia],
    })
    return manifest
