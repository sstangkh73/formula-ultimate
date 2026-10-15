"""Power transmission: a chain of rolling rollers on the deck (goal v2, pure Python).

One root-level assembly ``m<k>-power_transmission`` tagged
``[power_transmission]`` sits on the Work 160 deck top in the part of the
reserved bay that the earlier bay modules leave free (from ``bay_x0`` up to
the nearest occupant's sweep circle). It holds 2 or 3 stations laid along y;
each station has three ``func-leaf-mechanism-v2`` prisms extruded along +z
(world frame, metres):

- boss: regular ``N_b``-gon plate on the deck top (``bonded`` to the deck);
- post: regular ``N_p``-gon prism standing on the boss top (``bonded``);
- roller: regular ``N_r``-gon disc (``N_r`` even) with a bore around the post,
  floating ``c`` above the boss top and joined to the post by a ``bearing``.

The bore is the Work 162 steering bore (apothem ``r_p + c``, a vertex at every
post vertex direction). Neighbouring roller centres are ``R_i + R_j + c``
apart (circumradii) and each roller has a vertex pointing at each neighbour,
so the sampled vertex gap of the ``rolling`` interface is ``c``. Every roller
turns fully about +z and its sweep stays inside its circumscribed circle, so
no rotation brings one roller into a neighbour, a post or the steering arm.

Nothing here transmits torque, models slip or links the rollers to the wheels
or a converter; it is a representation gate only.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass, replace
from typing import Any, Sequence

import numpy as np

from .composition import LeafMaterial
from .direction_control import _z_prism, steering_bore
from .ground_contacts import _assembly_index, _polygon_radii, regular_polygon
from .mechanisms import (
    DECK_ID,
    MechanismAssembly,
    MechanismLayer,
    MechanismPart,
    _derived_seed,
    _loop_points,
    _material,
    prism_vertices,
)


POWER_TRANSMISSION_VERSION = "func-power-transmission-v1"
TRANSMISSION_FUNCTIONS = ("power_transmission",)
TRANSMISSION_SUFFIX = "power_transmission"
ROLES = ("boss", "post", "roller")


@dataclass(frozen=True)
class PowerTransmissionConfig:
    stations: tuple[int, ...] = (2, 3)
    boss_sides: tuple[int, ...] = (6, 8, 10)
    #: boss circumradius as a fraction of the roller apothem
    boss_radius_fraction: tuple[float, float] = (0.5, 0.9)
    boss_height_m: tuple[float, float] = (0.01, 0.02)
    #: smallest radial step from the post outline to the boss outline
    min_boss_ring_m: float = 0.003
    post_sides: tuple[int, ...] = (6, 8)
    post_radius_m: tuple[float, float] = (0.008, 0.015)
    #: post length above the roller top
    post_overhang_m: tuple[float, float] = (0.01, 0.03)
    roller_sides: tuple[int, ...] = (48, 64, 96)
    roller_radius_m: tuple[float, float] = (0.04, 0.12)
    roller_thickness_m: tuple[float, float] = (0.01, 0.02)
    #: smallest material ring between the bore and the roller outline
    min_roller_ring_m: float = 0.006
    bearing_clearance_m: float = 2.5e-5
    #: bore polygon sides; a multiple of every post side count
    bore_sides: int = 96
    max_contact_vertex_gap_m: float = 7.5e-5
    #: every sweep circle stays this far inside the free strip and the deck
    sweep_margin_m: float = 0.02


DEFAULT_POWER_TRANSMISSION_CONFIG = PowerTransmissionConfig()


def power_transmission_config_record(
        config: PowerTransmissionConfig = DEFAULT_POWER_TRANSMISSION_CONFIG) -> dict[str, Any]:
    return {"version": POWER_TRANSMISSION_VERSION,
            **{k: list(v) if isinstance(v, tuple) else v for k, v in asdict(config).items()}}


def transmission_ids(index: int, stations: int) -> dict[str, Any]:
    assembly = f"m{index}-{TRANSMISSION_SUFFIX}"
    return {"assembly": assembly,
            "stations": [{"boss": f"{assembly}.s{i}.boss", "post": f"{assembly}.s{i}.post",
                          "roller": f"{assembly}.s{i}.roller", "motion": f"{assembly}.r{i}"}
                         for i in range(stations)]}


def bay_occupants(layer: MechanismLayer) -> list[tuple[np.ndarray, float]]:
    """(xy centre, radius) discs covering every non-deck part above the deck top within the deck's y span.

    A part in a motion about +z is covered by its full sweep circle; a fixed
    part by the circle around its vertex box.
    """

    b = layer.backbone
    moving = {p: m for m in layer.motions for p in m["parts"]}
    discs = []
    for part in layer.parts:
        if part.id == DECK_ID:
            continue
        verts = prism_vertices(part.program)
        if float(verts[:, 2].min()) < b.z_top - 1e-9 or float(verts[:, 1].max()) <= b.y0 \
                or float(verts[:, 1].min()) >= b.y1:
            continue
        motion = moving.get(part.id)
        if motion is not None and motion["axis_dir"] == [0.0, 0.0, 1.0]:
            centre = np.asarray(motion["axis_point_m"][:2], dtype=float)
        else:
            centre = (verts[:, :2].min(axis=0) + verts[:, :2].max(axis=0)) / 2
        discs.append((centre, float(np.linalg.norm(verts[:, :2] - centre, axis=1).max())))
    return discs


def free_strip(layer: MechanismLayer, margin: float, exclude: Sequence[str] = ()) -> tuple[float, float]:
    """x interval of the bay (after margins) left of every bay occupant's disc."""

    b = layer.backbone
    keep = replace(layer, parts=tuple(p for p in layer.parts if p.id not in set(exclude)))
    limit = b.core_x1
    for centre, radius in bay_occupants(keep):
        if centre[0] + radius > b.bay_x0:
            limit = min(limit, float(centre[0]) - radius)
    return b.bay_x0 + margin, limit - margin


def add_power_transmission(layer: MechanismLayer, seed: int, catalogue: Sequence[LeafMaterial],
                           config: PowerTransmissionConfig = DEFAULT_POWER_TRANSMISSION_CONFIG) -> MechanismLayer:
    """The layer with a rolling roller chain in the free part of the deck bay; deterministic per seed."""

    rng = random.Random(_derived_seed(POWER_TRANSMISSION_VERSION, "rollers", seed))
    b = layer.backbone
    c = config.bearing_clearance_m
    m = config.sweep_margin_m
    count = rng.choice(config.stations)
    boss_height = rng.uniform(*config.boss_height_m)
    thickness = rng.uniform(*config.roller_thickness_m)
    stations = []
    for _ in range(count):
        post_sides = rng.choice(config.post_sides)
        post_radius = rng.uniform(*config.post_radius_m)
        sides = rng.choice(config.roller_sides)
        bore_circum = (post_radius + c) / math.cos(math.pi / config.bore_sides)
        stations.append({
            "boss_sides": rng.choice(config.boss_sides), "boss_fraction": rng.uniform(*config.boss_radius_fraction),
            "post_sides": post_sides, "post_radius": post_radius, "overhang": rng.uniform(*config.post_overhang_m),
            "sides": sides, "radius": rng.uniform(*config.roller_radius_m),
            "min_radius": (bore_circum + config.min_roller_ring_m) / math.cos(math.pi / sides),
        })
    offset_draw = rng.uniform(-1.0, 1.0)

    x0, x1 = free_strip(layer, m)
    span_y = (b.y1 - b.y0) - 2 * m
    # Fit the chain: every circle inside the strip width, the whole chain inside
    # the deck's y span; drop the last station while even the minimum radii do
    # not fit.
    while True:
        for s in stations:
            s["radius"] = min(s["radius"], (x1 - x0) / 2)
        length = sum(2 * s["radius"] for s in stations) + (len(stations) - 1) * c
        if length > span_y:
            shrink = (span_y - (len(stations) - 1) * c) / (length - (len(stations) - 1) * c)
            for s in stations:
                s["radius"] *= shrink
        if all(s["radius"] >= s["min_radius"] for s in stations):
            break
        if len(stations) <= 2:
            raise ValueError("deck bay is too small for a two-roller transmission")
        stations.pop()
    length = sum(2 * s["radius"] for s in stations) + (len(stations) - 1) * c
    x_c = (x0 + x1) / 2
    y_mid = (b.y0 + b.y1) / 2 + offset_draw * max(0.0, (span_y - length) / 2)
    y = y_mid - length / 2

    first = 1 + max((_assembly_index(a.id) for a in layer.assemblies), default=-1)
    ids = transmission_ids(first, len(stations))
    boss_top = b.z_top + boss_height
    parts: list[MechanismPart] = []
    interfaces: list[dict] = []
    motions: list[dict] = []
    for index, (s, sid) in enumerate(zip(stations, ids["stations"])):
        y_c = y + s["radius"]
        y = y_c + s["radius"] + c
        apothem = s["radius"] * math.cos(math.pi / s["sides"])
        post_circum = s["post_radius"]
        boss_radius = max(s["boss_fraction"] * apothem,
                          (post_circum + config.min_boss_ring_m) / math.cos(math.pi / s["boss_sides"]))
        programs = {
            "boss": _z_prism(sid["boss"], "transmission_boss",
                             regular_polygon(s["boss_sides"], boss_radius, 0.0), boss_height, x_c, y_c, b.z_top),
            "post": _z_prism(sid["post"], "transmission_post",
                             regular_polygon(s["post_sides"], s["post_radius"], 0.0),
                             c + thickness + s["overhang"], x_c, y_c, boss_top),
            # Even side count with a vertex at +y: vertices point at both neighbours.
            "roller": _z_prism(sid["roller"], "transmission_roller",
                               regular_polygon(s["sides"], s["radius"], math.pi / 2), thickness, x_c, y_c,
                               boss_top + c,
                               holes=[steering_bore(s["post_sides"], s["post_radius"], c, config.bore_sides)]),
        }
        parts.extend(MechanismPart(id=sid[role], parent=ids["assembly"], program=programs[role],
                                   material=_material(seed, sid[role], catalogue)) for role in ROLES)
        interfaces.extend([
            {"id": sid["boss"] + ".seat", "a": sid["boss"], "b": DECK_ID, "kind": "bonded"},
            {"id": sid["post"] + ".seat", "a": sid["post"], "b": sid["boss"], "kind": "bonded"},
            {"id": sid["roller"] + ".bearing", "a": sid["roller"], "b": sid["post"], "kind": "bearing"},
        ])
        if index:
            previous = ids["stations"][index - 1]["roller"]
            interfaces.append({"id": sid["roller"] + ".rolling", "a": previous, "b": sid["roller"],
                               "kind": "rolling"})
        motions.append({"id": sid["motion"], "parts": [sid["roller"]], "type": "revolute",
                        "axis_point_m": [float(x_c), float(y_c), float(boss_top)], "axis_dir": [0.0, 0.0, 1.0],
                        "range_rad": float(2 * math.pi)})
    assembly = MechanismAssembly(id=ids["assembly"], children=tuple(p.id for p in parts),
                                 functions=TRANSMISSION_FUNCTIONS)
    evidence = dict(layer.evidence)
    evidence["power_transmission"] = {"chain": [m_["id"] for m_ in motions]}
    return replace(layer, parts=layer.parts + tuple(parts), assemblies=layer.assemblies + (assembly,),
                   root_children=layer.root_children + (assembly.id,),
                   interfaces=layer.interfaces + tuple(interfaces), motions=layer.motions + tuple(motions),
                   evidence=evidence)


# --------------------------------------------------------------------------
# Re-check from the programs
# --------------------------------------------------------------------------

def power_transmission_problems(layer: MechanismLayer,
                                config: PowerTransmissionConfig = DEFAULT_POWER_TRANSMISSION_CONFIG) -> list[str]:
    """Every violated power-transmission rule, recomputed from the program vertices."""

    found = [a for a in layer.assemblies if a.id.endswith("-" + TRANSMISSION_SUFFIX)]
    if len(found) != 1:
        return [f"expected 1 power-transmission assembly, found {len(found)}"]
    assembly = found[0]
    count = len(assembly.children) // len(ROLES)
    ids = transmission_ids(_assembly_index(assembly.id), count)
    expected = {sid[role] for sid in ids["stations"] for role in ROLES}
    if assembly.functions != TRANSMISSION_FUNCTIONS or set(assembly.children) != expected or count < 2:
        return [f"{assembly.id}: unexpected children or functions"]
    problems: list[str] = []
    b = layer.backbone
    c = config.bearing_clearance_m
    m = config.sweep_margin_m
    programs = {p.id: p.program for p in layer.parts}
    motions = {mo["id"]: mo for mo in layer.motions}
    kinds = {(i["a"], i["b"]): i["kind"] for i in layer.interfaces}
    x0, x1 = free_strip(layer, m, exclude=expected)
    circles = []
    for index, sid in enumerate(ids["stations"]):
        boss, post, roller = (prism_vertices(programs[sid[r]]) for r in ROLES)
        motion = motions.get(sid["motion"])
        if (motion is None or motion["parts"] != [sid["roller"]] or motion["type"] != "revolute"
                or motion["axis_dir"] != [0.0, 0.0, 1.0] or motion["range_rad"] < 2 * math.pi - 1e-9):
            problems.append(f"{sid['motion']}: missing full-turn roller motion about +z")
            continue
        for pair, kind in (((sid["boss"], DECK_ID), "bonded"), ((sid["post"], sid["boss"]), "bonded"),
                           ((sid["roller"], sid["post"]), "bearing")):
            if kinds.get(pair) != kind:
                problems.append(f"{pair[0]}: missing {kind} interface to {pair[1]}")
        centre = np.asarray(motion["axis_point_m"][:2], dtype=float)
        boss_top = float(boss[:, 2].max())
        if abs(float(boss[:, 2].min()) - b.z_top) > 1e-9:
            problems.append(f"{sid['boss']}: not on the deck top")
        if abs(float(post[:, 2].min()) - boss_top) > 1e-9:
            problems.append(f"{sid['post']}: not on the boss top")
        if abs(float(motion["axis_point_m"][2]) - boss_top) > 1e-9:
            problems.append(f"{sid['motion']}: axis point is not on the boss top")
        if not float(roller[:, 2].min()) > boss_top or not float(roller[:, 2].max()) < float(post[:, 2].max()):
            problems.append(f"{sid['roller']}: not between the boss top and the post top")
        boss_apothem, boss_circum = _polygon_radii(_loop_points(programs[sid["boss"]]["profile"]["loops"][0]))
        post_outline = np.asarray(_loop_points(programs[sid["post"]]["profile"]["loops"][0]))
        _, post_circum = _polygon_radii(post_outline)
        loops = programs[sid["roller"]]["profile"]["loops"]
        roller_apothem, roller_circum = _polygon_radii(_loop_points(loops[0]))
        if not post_circum < boss_apothem:
            problems.append(f"{sid['post']}: footprint is not inside the boss top")
        if not boss_circum < roller_apothem:
            problems.append(f"{sid['boss']}: reaches beyond the roller")
        if len(loops) != 2:
            problems.append(f"{sid['roller']}: needs exactly one bore")
        else:
            bore = np.asarray(_loop_points(loops[1]))
            bore_apothem, _ = _polygon_radii(bore)
            if not bore_apothem > post_circum:
                problems.append(f"{sid['roller']}: bore does not clear the rotating post")
            gaps = np.linalg.norm(post_outline[:, None, :] - bore[None, :, :], axis=2).min(axis=1)
            if float(gaps.max()) > config.max_contact_vertex_gap_m:
                problems.append(f"{sid['roller']}: no bore vertex faces each post vertex closely")
        if (centre[0] - roller_circum < x0 - 1e-9 or centre[0] + roller_circum > x1 + 1e-9
                or centre[1] - roller_circum < b.y0 + m - 1e-9 or centre[1] + roller_circum > b.y1 - m + 1e-9):
            problems.append(f"{sid['roller']}: sweep circle leaves the free bay strip")
        for verts, role in ((boss, "boss"), (post, "post")):
            if float(np.linalg.norm(verts[:, :2] - centre, axis=1).max()) > roller_circum:
                problems.append(f"{sid[role]}: reaches beyond the roller sweep circle")
        circles.append((sid, centre, roller_circum, roller))
    for (sa, ca, ra, va), (sb, cb, rb, vb) in zip(circles, circles[1:]):
        if kinds.get((sa["roller"], sb["roller"])) != "rolling":
            problems.append(f"{sb['roller']}: missing rolling interface to {sa['roller']}")
        if float(np.linalg.norm(cb - ca)) < ra + rb + c * (1 - 1e-6):
            problems.append(f"{sb['roller']}: sweep circle overlaps {sa['roller']}")
        gap = float(np.linalg.norm(va[:, None, :2] - vb[None, :, :2], axis=2).min())
        if gap > config.max_contact_vertex_gap_m:
            problems.append(f"{sb['roller']}: no vertex pair within the rolling contact gap")
        if abs(float(va[:, 2].min()) - float(vb[:, 2].min())) > 1e-9 or \
                abs(float(va[:, 2].max()) - float(vb[:, 2].max())) > 1e-9:
            problems.append(f"{sb['roller']}: not at the same height as {sa['roller']}")
    for i, (sa, ca, ra, _) in enumerate(circles):
        for sb, cb, rb, _ in circles[i + 2:]:
            if float(np.linalg.norm(cb - ca)) < ra + rb + c * (1 - 1e-6):
                problems.append(f"{sb['roller']}: sweep circle overlaps {sa['roller']}")
    chain = [sid["motion"] for sid in ids["stations"]]
    if layer.evidence.get("power_transmission") != {"chain": chain}:
        problems.append("power_transmission evidence does not name the roller chain")
    return problems
