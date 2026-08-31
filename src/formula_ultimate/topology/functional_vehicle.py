"""Technology-neutral functional vehicle architecture contracts for Work 066."""

from __future__ import annotations

from dataclasses import dataclass
import hashlib
import json
import math
from typing import Any, Mapping, Sequence


GRAMMAR_VERSION = "functional_vehicle_architecture_v2"
PORT_DOMAINS = frozenset({"structural", "electrical", "mechanical_rotary", "thermal", "control", "ground"})
PORT_DIRECTIONS = frozenset({"in", "out", "bidirectional"})
REQUIRED_CAPABILITIES = frozenset({
    "energy_storage", "energy_converter", "power_transmission", "ground_propulsion",
    "direction_control", "braking", "load_structure", "heat_rejection", "controller",
})


class FunctionalVehicleViolation(ValueError):
    """Raised when architecture evidence is incomplete or physically inconsistent."""


def _vector(values: Sequence[Any], name: str) -> tuple[float, float, float]:
    if not isinstance(values, Sequence) or isinstance(values, (str, bytes)) or len(values) != 3:
        raise FunctionalVehicleViolation(f"{name} must contain three values")
    result = tuple(float(value) for value in values)
    if not all(math.isfinite(value) for value in result):
        raise FunctionalVehicleViolation(f"{name} must be finite")
    return result  # type: ignore[return-value]


def _positive(value: Any, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise FunctionalVehicleViolation(f"{name} must be numeric")
    result = float(value)
    if not math.isfinite(result) or result <= 0.0:
        raise FunctionalVehicleViolation(f"{name} must be finite and positive")
    return result


def _efficiency(value: Any, name: str) -> float:
    result = _positive(value, name)
    if result > 1.0:
        raise FunctionalVehicleViolation(f"{name} must not exceed one")
    return result


@dataclass(frozen=True, slots=True)
class FunctionalPort:
    port_id: str
    component_id: str
    domain: str
    direction: str
    local_position_m: tuple[float, float, float]
    limits: Mapping[str, float]


@dataclass(frozen=True, slots=True)
class FunctionalComponent:
    component_id: str
    function_tags: tuple[str, ...]
    material_id: str
    primitive_kind: str
    dimensions_m: tuple[float, ...]
    position_m: tuple[float, float, float]
    density_kg_per_m3: float
    parameters: Mapping[str, float]
    ports: tuple[FunctionalPort, ...]

    @property
    def cylinder_axis(self) -> int | None:
        return {"cylinder_x": 0, "cylinder_y": 1, "cylinder_z": 2}.get(self.primitive_kind)

    @property
    def volume_m3(self) -> float:
        if self.primitive_kind == "box":
            return math.prod(self.dimensions_m)
        radius, length = self.dimensions_m
        return math.pi * radius * radius * length

    @property
    def mass_kg(self) -> float:
        return self.volume_m3 * self.density_kg_per_m3

    @property
    def half_extents_m(self) -> tuple[float, float, float]:
        if self.primitive_kind == "box":
            return tuple(value / 2.0 for value in self.dimensions_m)  # type: ignore[return-value]
        radius, length = self.dimensions_m
        axis = self.cylinder_axis
        return tuple(length / 2.0 if index == axis else radius for index in range(3))  # type: ignore[return-value]

    @property
    def bounds_m(self) -> tuple[tuple[float, float, float], tuple[float, float, float]]:
        half = self.half_extents_m
        return tuple(
            tuple(self.position_m[index] + sign * half[index] for index in range(3))
            for sign in (-1.0, 1.0)
        )  # type: ignore[return-value]

    @property
    def centroidal_inertia_kg_m2(self) -> tuple[float, float, float, float, float, float]:
        mass = self.mass_kg
        if self.primitive_kind == "box":
            x, y, z = self.dimensions_m
            diagonal = (mass * (y*y + z*z) / 12.0, mass * (x*x + z*z) / 12.0, mass * (x*x + y*y) / 12.0)
        else:
            radius, length = self.dimensions_m
            axial = mass * radius * radius / 2.0
            transverse = mass * (3.0 * radius * radius + length * length) / 12.0
            diagonal = tuple(axial if index == self.cylinder_axis else transverse for index in range(3))
        return diagonal + (0.0, 0.0, 0.0)  # type: ignore[return-value]


@dataclass(frozen=True, slots=True)
class FunctionalConnection:
    connection_id: str
    domain: str
    from_port_id: str
    to_port_id: str
    efficiency: float
    maximum_length_m: float


@dataclass(frozen=True, slots=True)
class GroundContact:
    contact_id: str
    component_id: str
    port_id: str
    maximum_normal_force_n: float
    maximum_longitudinal_force_n: float
    maximum_lateral_force_n: float


@dataclass(frozen=True, slots=True)
class FunctionalVehicle:
    protocol_id: str
    candidate_id: str
    components: tuple[FunctionalComponent, ...]
    connections: tuple[FunctionalConnection, ...]
    ground_contacts: tuple[GroundContact, ...]
    envelope_m: tuple[tuple[float, float, float], tuple[float, float, float]]
    tolerances: Mapping[str, float]


_REQUIRED_PARAMETERS: Mapping[str, tuple[str, ...]] = {
    "energy_storage": ("capacity_j", "maximum_output_power_w"),
    "energy_converter": ("maximum_input_power_w", "maximum_output_power_w", "maximum_torque_nm", "maximum_speed_rad_s", "efficiency"),
    "power_transmission": ("ratio", "maximum_input_torque_nm", "maximum_output_torque_nm", "efficiency"),
    "ground_propulsion": ("maximum_drive_torque_nm",),
    "direction_control": ("maximum_angle_rad", "maximum_rate_rad_per_s"),
    "braking": ("maximum_brake_torque_nm",),
    "load_structure": ("maximum_force_n", "maximum_moment_nm"),
    "heat_rejection": ("maximum_heat_rejection_w", "maximum_temperature_k"),
    "controller": ("maximum_update_rate_hz",),
}


_DOMAIN_LIMITS: Mapping[str, tuple[str, ...]] = {
    "structural": ("maximum_force_n", "maximum_moment_nm"),
    "electrical": ("maximum_power_w",),
    "mechanical_rotary": ("maximum_torque_nm", "maximum_speed_rad_per_s"),
    "thermal": ("maximum_heat_flow_w",),
    "control": ("maximum_signal_rate_hz",),
    "ground": ("maximum_normal_force_n", "maximum_longitudinal_force_n", "maximum_lateral_force_n"),
}


def _primitive(raw: Mapping[str, Any]) -> tuple[str, tuple[float, ...]]:
    kind = str(raw.get("type", ""))
    if kind == "box":
        dimensions = _vector(raw.get("size_m", ()), "box size")
    elif kind in {"cylinder_x", "cylinder_y", "cylinder_z"}:
        dimensions = (_positive(raw.get("radius_m"), "cylinder radius"), _positive(raw.get("length_m"), "cylinder length"))
    else:
        raise FunctionalVehicleViolation("unsupported functional component primitive")
    if any(value <= 0.0 for value in dimensions):
        raise FunctionalVehicleViolation("primitive dimensions must be positive")
    return kind, dimensions


def from_functional_mapping(raw: Mapping[str, Any]) -> FunctionalVehicle:
    if raw.get("grammar_version") != GRAMMAR_VERSION:
        raise FunctionalVehicleViolation("functional grammar version mismatch")
    materials = raw.get("materials")
    if not isinstance(materials, Mapping) or not materials:
        raise FunctionalVehicleViolation("functional materials are missing")
    components: list[FunctionalComponent] = []
    port_ids: set[str] = set()
    for item in raw.get("components", ()):
        component_id = str(item.get("component_id", ""))
        if not component_id:
            raise FunctionalVehicleViolation("component identity must be nonblank")
        material_id = str(item.get("material_id", ""))
        try:
            density = _positive(materials[material_id]["density_kg_per_m3"], "material density")
        except KeyError as exc:
            raise FunctionalVehicleViolation("unknown functional material") from exc
        kind, dimensions = _primitive(item.get("primitive", {}))
        tags = tuple(str(tag) for tag in item.get("function_tags", ()))
        if not tags or len(tags) != len(set(tags)):
            raise FunctionalVehicleViolation("component function tags must be nonempty and unique")
        parameters = {str(key): _positive(value, f"component parameter {key}") for key, value in item.get("parameters", {}).items()}
        for tag in tags:
            for name in _REQUIRED_PARAMETERS.get(tag, ()):
                if name not in parameters:
                    raise FunctionalVehicleViolation(f"component {component_id} missing parameter {name}")
        for name in ("efficiency",):
            if name in parameters:
                _efficiency(parameters[name], f"component {component_id} efficiency")
        ports: list[FunctionalPort] = []
        for port_raw in item.get("ports", ()):
            port_id = str(port_raw.get("port_id", ""))
            domain, direction = str(port_raw.get("domain", "")), str(port_raw.get("direction", ""))
            if not port_id or port_id in port_ids:
                raise FunctionalVehicleViolation("port identity is blank or duplicate")
            if domain not in PORT_DOMAINS or direction not in PORT_DIRECTIONS:
                raise FunctionalVehicleViolation("port domain or direction is invalid")
            limits_raw = port_raw.get("limits")
            if not isinstance(limits_raw, Mapping) or set(limits_raw) != set(_DOMAIN_LIMITS[domain]):
                raise FunctionalVehicleViolation(f"port {port_id} limit schema mismatch")
            limits = {str(key): _positive(value, f"port limit {key}") for key, value in limits_raw.items()}
            ports.append(FunctionalPort(port_id, component_id, domain, direction, _vector(port_raw.get("local_position_m", ()), "port position"), limits))
            port_ids.add(port_id)
        if not ports:
            raise FunctionalVehicleViolation("functional component has no ports")
        components.append(FunctionalComponent(
            component_id, tags, material_id, kind, dimensions,
            _vector(item.get("translation_m", ()), "component translation"), density, parameters, tuple(ports),
        ))
    component_ids = [component.component_id for component in components]
    if not components or len(component_ids) != len(set(component_ids)):
        raise FunctionalVehicleViolation("component identity is missing or duplicate")
    ports = {port.port_id: port for component in components for port in component.ports}
    connections: list[FunctionalConnection] = []
    connection_ids: set[str] = set()
    for item in raw.get("connections", ()):
        identity = str(item.get("connection_id", ""))
        if not identity or identity in connection_ids:
            raise FunctionalVehicleViolation("connection identity is blank or duplicate")
        from_id, to_id, domain = str(item.get("from_port", "")), str(item.get("to_port", "")), str(item.get("domain", ""))
        if from_id not in ports or to_id not in ports:
            raise FunctionalVehicleViolation("connection references unknown port")
        if ports[from_id].domain != domain or ports[to_id].domain != domain:
            raise FunctionalVehicleViolation("connection domain mismatch")
        if ports[from_id].direction not in {"out", "bidirectional"} or ports[to_id].direction not in {"in", "bidirectional"}:
            raise FunctionalVehicleViolation("connection direction mismatch")
        efficiency = _efficiency(item.get("efficiency"), "connection efficiency")
        maximum_length = _positive(item.get("maximum_length_m"), "connection maximum length")
        connections.append(FunctionalConnection(identity, domain, from_id, to_id, efficiency, maximum_length))
        connection_ids.add(identity)
    contacts: list[GroundContact] = []
    contact_ids: set[str] = set()
    for item in raw.get("ground_contacts", ()):
        identity, component_id, port_id = str(item.get("contact_id", "")), str(item.get("component_id", "")), str(item.get("port_id", ""))
        if not identity or identity in contact_ids:
            raise FunctionalVehicleViolation("ground contact identity is blank or duplicate")
        if port_id not in ports or ports[port_id].component_id != component_id or ports[port_id].domain != "ground":
            raise FunctionalVehicleViolation("ground contact port is invalid")
        contacts.append(GroundContact(
            identity, component_id, port_id,
            _positive(item.get("maximum_normal_force_n"), "ground normal force"),
            _positive(item.get("maximum_longitudinal_force_n"), "ground longitudinal force"),
            _positive(item.get("maximum_lateral_force_n"), "ground lateral force"),
        ))
        contact_ids.add(identity)
    envelope = raw.get("envelope")
    tolerances = {str(key): _positive(value, f"tolerance {key}") for key, value in raw.get("tolerances", {}).items()}
    for required in ("geometry_m", "connection_length_m", "mass_property_relative"):
        if required not in tolerances:
            raise FunctionalVehicleViolation(f"missing tolerance {required}")
    return FunctionalVehicle(
        str(raw.get("protocol_id", "")), str(raw.get("candidate_id", "")), tuple(components), tuple(connections), tuple(contacts),
        (_vector(envelope["minimum_m"], "envelope minimum"), _vector(envelope["maximum_m"], "envelope maximum")), tolerances,
    )


def functional_mass_properties(vehicle: FunctionalVehicle) -> dict[str, Any]:
    total = math.fsum(component.mass_kg for component in vehicle.components)
    if total <= 0.0:
        raise FunctionalVehicleViolation("functional vehicle mass must be positive")
    centre = tuple(math.fsum(component.mass_kg * component.position_m[index] for component in vehicle.components) / total for index in range(3))
    inertia = [0.0] * 6
    for component in vehicle.components:
        dx, dy, dz = (component.position_m[index] - centre[index] for index in range(3))
        parallel = (
            component.mass_kg * (dy*dy + dz*dz), component.mass_kg * (dx*dx + dz*dz), component.mass_kg * (dx*dx + dy*dy),
            -component.mass_kg * dx * dy, -component.mass_kg * dx * dz, -component.mass_kg * dy * dz,
        )
        inertia = [inertia[index] + component.centroidal_inertia_kg_m2[index] + parallel[index] for index in range(6)]
    return {"mass_kg": total, "centre_of_mass_m": centre, "inertia_kg_m2": tuple(inertia)}


def _world_port(component: FunctionalComponent, port: FunctionalPort) -> tuple[float, float, float]:
    return tuple(component.position_m[index] + port.local_position_m[index] for index in range(3))  # type: ignore[return-value]


def _reachable(edges: Sequence[tuple[str, str]], starts: Sequence[str]) -> set[str]:
    graph: dict[str, set[str]] = {}
    for source, target in edges:
        graph.setdefault(source, set()).add(target)
    seen: set[str] = set()
    pending = list(starts)
    while pending:
        node = pending.pop()
        if node in seen:
            continue
        seen.add(node)
        pending.extend(graph.get(node, set()) - seen)
    return seen


def _undirected_reachable(edges: Sequence[tuple[str, str]], starts: Sequence[str]) -> set[str]:
    return _reachable(tuple(edges) + tuple((b, a) for a, b in edges), starts)


def validate_functional_vehicle(vehicle: FunctionalVehicle) -> dict[str, Any]:
    if not vehicle.protocol_id or not vehicle.candidate_id:
        raise FunctionalVehicleViolation("protocol and candidate identities must be nonblank")
    components = {component.component_id: component for component in vehicle.components}
    ports = {port.port_id: port for component in vehicle.components for port in component.ports}
    capability_components = {tag: {component.component_id for component in vehicle.components if tag in component.function_tags} for tag in REQUIRED_CAPABILITIES}
    missing = sorted(tag for tag, members in capability_components.items() if not members)
    if missing:
        raise FunctionalVehicleViolation(f"missing required capabilities: {missing}")

    tolerance = vehicle.tolerances["geometry_m"]
    envelope_low, envelope_high = vehicle.envelope_m
    world_ports: dict[str, tuple[float, float, float]] = {}
    for component in vehicle.components:
        low, high = component.bounds_m
        if any(low[index] < envelope_low[index] - tolerance or high[index] > envelope_high[index] + tolerance for index in range(3)):
            raise FunctionalVehicleViolation("functional component envelope violation")
        half = component.half_extents_m
        for port in component.ports:
            if any(abs(port.local_position_m[index]) > half[index] + tolerance for index in range(3)):
                raise FunctionalVehicleViolation("functional port lies outside component solid")
            world_ports[port.port_id] = _world_port(component, port)
    for index, first in enumerate(vehicle.components):
        for second in vehicle.components[index + 1:]:
            if all(min(first.bounds_m[1][axis], second.bounds_m[1][axis]) - max(first.bounds_m[0][axis], second.bounds_m[0][axis]) > tolerance for axis in range(3)):
                raise FunctionalVehicleViolation("functional component solid overlap")

    edges_by_domain: dict[str, list[tuple[str, str]]] = {domain: [] for domain in PORT_DOMAINS}
    maximum_connection_residual = 0.0
    for connection in vehicle.connections:
        source, target = ports[connection.from_port_id], ports[connection.to_port_id]
        distance = math.dist(world_ports[source.port_id], world_ports[target.port_id])
        maximum_connection_residual = max(maximum_connection_residual, distance)
        if distance > connection.maximum_length_m + vehicle.tolerances["connection_length_m"]:
            raise FunctionalVehicleViolation("functional connection length exceeded")
        for limit_name in _DOMAIN_LIMITS[connection.domain]:
            source_limit, target_limit = source.limits[limit_name], target.limits[limit_name]
            if min(source_limit, target_limit) <= 0.0:
                raise FunctionalVehicleViolation("functional connection capacity is invalid")
        edges_by_domain[connection.domain].append((source.component_id, target.component_id))

    if not vehicle.ground_contacts:
        raise FunctionalVehicleViolation("functional vehicle has no ground contact")
    ground_components: set[str] = set()
    for contact in vehicle.ground_contacts:
        port = ports[contact.port_id]
        world = world_ports[port.port_id]
        if abs(world[2]) > tolerance:
            raise FunctionalVehicleViolation("functional ground contact is not on z=0")
        for key, declared in (
            ("maximum_normal_force_n", contact.maximum_normal_force_n),
            ("maximum_longitudinal_force_n", contact.maximum_longitudinal_force_n),
            ("maximum_lateral_force_n", contact.maximum_lateral_force_n),
        ):
            if declared > port.limits[key] + tolerance:
                raise FunctionalVehicleViolation("ground contact exceeds port capacity")
        ground_components.add(contact.component_id)

    structural = _undirected_reachable(edges_by_domain["structural"], tuple(ground_components))
    if structural != set(components):
        raise FunctionalVehicleViolation("disconnected structural load path")

    energy_edges = edges_by_domain["electrical"] + edges_by_domain["mechanical_rotary"]
    storage = tuple(capability_components["energy_storage"])
    powered = _reachable(energy_edges, storage)
    if not capability_components["ground_propulsion"] <= powered:
        raise FunctionalVehicleViolation("force-from-nowhere or disconnected power path")

    thermal_reachable = _reachable(edges_by_domain["thermal"], tuple(component.component_id for component in vehicle.components if "heat_source" in component.function_tags))
    heat_sources = {component.component_id for component in vehicle.components if "heat_source" in component.function_tags}
    heat_sinks = capability_components["heat_rejection"]
    if not heat_sources or not (thermal_reachable & heat_sinks):
        raise FunctionalVehicleViolation("disconnected thermal path")
    for heat_source in heat_sources:
        if not (_reachable(edges_by_domain["thermal"], (heat_source,)) & heat_sinks):
            raise FunctionalVehicleViolation("heat source lacks heat-rejection path")

    controlled = _reachable(edges_by_domain["control"], tuple(capability_components["controller"]))
    actuators = capability_components["energy_converter"] | capability_components["direction_control"] | capability_components["braking"]
    if not actuators <= controlled:
        raise FunctionalVehicleViolation("uncontrolled functional actuator")

    for component in vehicle.components:
        if "energy_converter" in component.function_tags:
            if component.parameters["maximum_output_power_w"] > component.parameters["maximum_input_power_w"] * component.parameters["efficiency"] + tolerance:
                raise FunctionalVehicleViolation("energy converter creates undeclared power")
        if "power_transmission" in component.function_tags:
            available = component.parameters["maximum_input_torque_nm"] * component.parameters["ratio"] * component.parameters["efficiency"]
            if component.parameters["maximum_output_torque_nm"] > available + tolerance:
                raise FunctionalVehicleViolation("transmission creates undeclared torque")

    draft = {
        "status": "passed",
        "grammar_version": GRAMMAR_VERSION,
        "candidate_id": vehicle.candidate_id,
        "component_count": len(vehicle.components),
        "port_count": len(ports),
        "connection_count": len(vehicle.connections),
        "ground_contact_count": len(vehicle.ground_contacts),
        "capability_counts": {tag: len(capability_components[tag]) for tag in sorted(REQUIRED_CAPABILITIES)},
        "maximum_connection_length_m": maximum_connection_residual,
        "mass_properties": functional_mass_properties(vehicle),
    }
    return {**draft, "validation_sha256": canonical_sha256(draft)}


def canonical_sha256(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def functional_declaration_sha256(raw: Mapping[str, Any]) -> str:
    return canonical_sha256(raw)
