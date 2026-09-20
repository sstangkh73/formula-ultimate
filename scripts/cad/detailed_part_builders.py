#!/usr/bin/env python3
"""Parts modelled at part resolution, for Work 142.

Each builder produces one valid solid that carries the geometry its function
implies: a thread that bears, a bearing face, a chamfer that lets a part enter
its mate, a groove that retains, a slot that carries flux. Nothing here claims
a part is correct for the vehicle — only that it is modelled at the resolution
the Work 140 gate requires.

Runs under the pinned CadQuery runtime.
"""

from __future__ import annotations

import math
from typing import Any

import cadquery as cq
from OCP.BOPAlgo import BOPAlgo_Options

# Parallel booleans returned volumes differing in the last unit in the
# last place between runs, which broke exact replay (Work 142).
BOPAlgo_Options.SetParallelMode_s(False)

MM = 1000.0


def _chamfer_ends(shape: cq.Shape, chamfer_mm: float, selectors: tuple[str, ...] = (">Z", "<Z")) -> cq.Shape:
    """Chamfer the end faces, tolerating a kernel refusal on either end."""

    work = cq.Workplane(obj=shape)
    for selector in selectors:
        try:
            work = work.faces(selector).edges("%CIRCLE").chamfer(chamfer_mm)
        except Exception:  # noqa: BLE001 - a refusal on one end is not fatal
            continue
    return work.val()


def thread_solid(core_radius_mm: float, pitch_mm: float, length_mm: float, inset_mm: float = 0.25) -> cq.Solid:
    """One swept ISO-form thread helix, in millimetres."""

    height = 0.866025 * pitch_mm
    points = [
        (core_radius_mm - inset_mm, 0.0),
        (core_radius_mm + height * 0.625, pitch_mm * 0.25),
        (core_radius_mm - inset_mm, pitch_mm * 0.5),
    ]
    profile = cq.Workplane("XZ").polyline(points).close().wires().val()
    helix = cq.Wire.makeHelix(pitch=pitch_mm, height=length_mm, radius=core_radius_mm)
    return cq.Solid.sweep(profile, [], helix, isFrenet=True)


def build_reference_fastener(parameters: dict[str, Any]) -> cq.Shape:
    """Threaded fastener with a hex head, a hex socket and a head chamfer."""

    diameter = parameters["diameter_m"] * MM
    pitch = parameters["pitch_m"] * MM
    shank = parameters["shank_length_m"] * MM
    thread_length = parameters["thread_length_m"] * MM
    across_flats = parameters["head_across_flats_m"] * MM
    head_height = parameters["head_height_m"] * MM
    socket_across = parameters["socket_across_flats_m"] * MM
    socket_depth = parameters["socket_depth_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    core = diameter / 2.0 - 0.61343 * pitch * 0.5
    body = cq.Workplane("XY").circle(core).extrude(shank).val()
    solid = body.fuse(thread_solid(core, pitch, thread_length)).clean()
    head = (
        cq.Workplane("XY").polygon(6, across_flats / math.cos(math.pi / 6)).extrude(-head_height)
        .faces("<Z").workplane().polygon(6, socket_across / math.cos(math.pi / 6)).cutBlind(socket_depth).val()
    )
    return _chamfer_ends(solid.fuse(head).clean(), chamfer, ("<Z",))


def build_nyloc_nut(parameters: dict[str, Any]) -> cq.Shape:
    """Hex nut with an insert counterbore and chamfered bearing faces.

    The bore is left unthreaded: cutting a swept helix out of the bore removed
    no material in this toolchain (recorded in Work 140), and declaring a
    thread that the geometry does not have would defeat the joint gate.
    """

    across = parameters["across_flats_m"] * MM
    height = parameters["height_m"] * MM
    bore = parameters["bore_m"] * MM
    insert_bore = parameters["insert_bore_m"] * MM
    insert_depth = parameters["insert_depth_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    nut = (
        cq.Workplane("XY").polygon(6, across / math.cos(math.pi / 6)).extrude(height)
        .faces(">Z").workplane().cboreHole(bore, insert_bore, insert_depth)
    )
    return _chamfer_ends(nut.val(), chamfer)


def build_serrated_washer(parameters: dict[str, Any]) -> cq.Shape:
    """Lock washer with external serrations and a chamfered bearing face."""

    outer = parameters["outer_diameter_m"] * MM
    inner = parameters["inner_diameter_m"] * MM
    thickness = parameters["thickness_m"] * MM
    teeth = int(parameters["teeth"])
    tooth_radius = parameters["tooth_radius_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    washer = cq.Workplane("XY").circle(outer / 2).circle(inner / 2).extrude(thickness)
    cutters = cq.Workplane("XY")
    for index in range(teeth):
        angle = 2.0 * math.pi * index / teeth
        cutters = cutters.union(
            cq.Workplane("XY")
            .center(outer / 2 * math.cos(angle), outer / 2 * math.sin(angle))
            .circle(tooth_radius).extrude(thickness)
        )
    return _chamfer_ends(washer.cut(cutters).val(), chamfer, (">Z",))


def build_beaded_gasket(parameters: dict[str, Any]) -> cq.Shape:
    """Rectangular seal with radiused corners and rounded sealing beads."""

    length = parameters["length_m"] * MM
    width = parameters["width_m"] * MM
    band = parameters["band_m"] * MM
    thickness = parameters["thickness_m"] * MM
    corner = parameters["corner_radius_m"] * MM
    bead = parameters["bead_radius_m"] * MM

    outer = cq.Workplane("XY").rect(length, width).extrude(thickness).edges("|Z").fillet(corner)
    inner = cq.Workplane("XY").rect(length - 2 * band, width - 2 * band).extrude(thickness * 3).translate((0, 0, -thickness))
    inner = cq.Workplane(obj=inner.val()).edges("|Z").fillet(max(corner - band, 1.2))
    return outer.cut(inner).edges(">Z or <Z").fillet(bead).val()


def build_stepped_axle(parameters: dict[str, Any]) -> cq.Shape:
    """Axle with a diameter step, a retaining groove, a keyway and chamfers."""

    large = parameters["large_diameter_m"] * MM
    small = parameters["small_diameter_m"] * MM
    large_length = parameters["large_length_m"] * MM
    small_length = parameters["small_length_m"] * MM
    groove_width = parameters["groove_width_m"] * MM
    groove_depth = parameters["groove_depth_m"] * MM
    key_width = parameters["key_width_m"] * MM
    key_depth = parameters["key_depth_m"] * MM
    key_length = parameters["key_length_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    body = cq.Workplane("XY").circle(large / 2).extrude(large_length)
    body = body.faces(">Z").workplane().circle(small / 2).extrude(small_length).val()
    groove = (
        cq.Workplane("XY", origin=(0, 0, large_length + small_length - 12.0))
        .circle(small / 2 + 1.0).circle(small / 2 - groove_depth).extrude(groove_width).val()
    )
    key = (
        cq.Workplane("XY", origin=(0, 0, large_length + small_length - key_length - 6.0))
        .center(0, small / 2 - key_depth / 2)
        .box(key_width, key_depth, key_length, centered=(True, True, False)).val()
    )
    return _chamfer_ends(body.cut(groove).cut(key), chamfer)


def build_flanged_bushing(parameters: dict[str, Any]) -> cq.Shape:
    """Flanged bushing with a bore, an internal oil groove and chamfers."""

    outer = parameters["outer_diameter_m"] * MM
    bore = parameters["bore_diameter_m"] * MM
    length = parameters["length_m"] * MM
    flange = parameters["flange_diameter_m"] * MM
    flange_thickness = parameters["flange_thickness_m"] * MM
    groove_depth = parameters["groove_depth_m"] * MM
    groove_width = parameters["groove_width_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    body = cq.Solid.makeCylinder(outer / 2, length)
    body = body.fuse(cq.Solid.makeCylinder(flange / 2, flange_thickness)).clean()
    body = body.cut(cq.Solid.makeCylinder(bore / 2, length * 2, cq.Vector(0, 0, -length / 2)))
    groove_outer = cq.Solid.makeCylinder(bore / 2 + groove_depth, groove_width, cq.Vector(0, 0, length / 2 - groove_width / 2))
    groove_inner = cq.Solid.makeCylinder(bore / 2, groove_width, cq.Vector(0, 0, length / 2 - groove_width / 2))
    return _chamfer_ends(body.cut(groove_outer.cut(groove_inner)), chamfer)


def build_slotted_rotor(parameters: dict[str, Any]) -> cq.Shape:
    """Rotor with a bore and axial slots, chamfered at both ends."""

    outer = parameters["outer_diameter_m"] * MM
    bore = parameters["bore_diameter_m"] * MM
    length = parameters["length_m"] * MM
    slots = int(parameters["slots"])
    slot_width = parameters["slot_width_m"] * MM
    slot_depth = parameters["slot_depth_m"] * MM
    chamfer = parameters["chamfer_m"] * MM

    rotor = cq.Workplane("XY").circle(outer / 2).extrude(length).faces(">Z").workplane().hole(bore)
    cutters = cq.Workplane("XY")
    for index in range(slots):
        cutters = cutters.union(
            cq.Workplane("XY").center(outer / 2 - slot_depth / 2, 0)
            .box(slot_depth, slot_width, length, centered=(True, True, False))
            .rotate((0, 0, 0), (0, 0, 1), 360.0 * index / slots)
        )
    return _chamfer_ends(rotor.cut(cutters).val(), chamfer)


# Simple reference shapes kept from Work 140: they exist to demonstrate joint
# technologies, not to model a real part, and their classes require no more.
def build_plate(parameters: dict[str, Any]) -> cq.Shape:
    dimensions = [value * MM for value in parameters["dimensions_m"]]
    return cq.Workplane("XY").box(*dimensions).val()


def build_bushing(parameters: dict[str, Any]) -> cq.Shape:
    outer = parameters["outer_radius_m"] * MM
    inner = parameters["inner_radius_m"] * MM
    length = parameters["length_m"] * MM
    blank = cq.Solid.makeCylinder(outer, length, cq.Vector(0, 0, -length / 2.0))
    return blank.cut(cq.Solid.makeCylinder(inner, length * 2.0, cq.Vector(0, 0, -length)))


def build_shaft(parameters: dict[str, Any]) -> cq.Shape:
    radius = parameters["radius_m"] * MM
    length = parameters["length_m"] * MM
    return cq.Solid.makeCylinder(radius, length, cq.Vector(0, 0, -length / 2.0))


BUILDERS = {
    "reference_fastener": build_reference_fastener,
    "nyloc_nut": build_nyloc_nut,
    "serrated_washer": build_serrated_washer,
    "beaded_gasket": build_beaded_gasket,
    "stepped_axle": build_stepped_axle,
    "flanged_bushing": build_flanged_bushing,
    "slotted_rotor": build_slotted_rotor,
    "plate": build_plate,
    "bushing": build_bushing,
    "shaft": build_shaft,
}
