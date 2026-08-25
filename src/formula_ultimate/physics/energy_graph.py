"""Typed, deterministic energy-component graph compilation.

Compilation validates interfaces and topology only. It deliberately performs no
power-flow solve, energy integration, efficiency, depletion, or conservation
claim; those belong to later work items.
"""

from __future__ import annotations

from dataclasses import dataclass
import heapq
import math


class EnergyGraphInputError(ValueError):
    """Raised when a component graph violates its declared interface contract."""


ENERGY_CARRIERS = {
    "chemical",
    "electrical",
    "mechanical_rotational",
    "mechanical_translational",
    "thermal",
}
PORT_DIRECTIONS = {"input", "output"}
COMPONENT_ROLES = {"source", "converter", "transmission", "tyre", "sink"}


def _identifier(name: str, value: str) -> None:
    if not value.strip():
        raise EnergyGraphInputError(f"{name} must not be blank")


def _positive_finite(name: str, value: float) -> None:
    if not math.isfinite(value) or value <= 0.0:
        raise EnergyGraphInputError(
            f"{name} must be finite and > 0; received {value!r}"
        )


@dataclass(frozen=True, slots=True)
class EnergyPort:
    port_id: str
    direction: str
    carrier: str
    maximum_power_w: float

    def __post_init__(self) -> None:
        _identifier("port_id", self.port_id)
        if self.direction not in PORT_DIRECTIONS:
            raise EnergyGraphInputError(f"unsupported direction {self.direction!r}")
        if self.carrier not in ENERGY_CARRIERS:
            raise EnergyGraphInputError(f"unsupported carrier {self.carrier!r}")
        _positive_finite("maximum_power_w", self.maximum_power_w)


@dataclass(frozen=True, slots=True)
class EnergyComponent:
    component_id: str
    role: str
    ports: tuple[EnergyPort, ...]

    def __post_init__(self) -> None:
        _identifier("component_id", self.component_id)
        if self.role not in COMPONENT_ROLES:
            raise EnergyGraphInputError(f"unsupported component role {self.role!r}")
        if not self.ports:
            raise EnergyGraphInputError("component must contain at least one port")
        ids = [port.port_id for port in self.ports]
        if len(ids) != len(set(ids)):
            raise EnergyGraphInputError(
                f"component {self.component_id!r} has duplicate port_id values"
            )
        directions = {port.direction for port in self.ports}
        if self.role == "source" and directions != {"output"}:
            raise EnergyGraphInputError("source components may contain only outputs")
        if self.role == "sink" and directions != {"input"}:
            raise EnergyGraphInputError("sink components may contain only inputs")
        if self.role in {"converter", "transmission", "tyre"} and not {
            "input",
            "output",
        }.issubset(directions):
            raise EnergyGraphInputError(
                f"{self.role} components require input and output ports"
            )
        if self.role == "transmission" and any(
            port.carrier != "mechanical_rotational" for port in self.ports
        ):
            raise EnergyGraphInputError(
                "transmission ports must use mechanical_rotational carrier"
            )
        if self.role == "tyre" and any(
            (port.direction == "input" and port.carrier != "mechanical_rotational")
            or (
                port.direction == "output"
                and port.carrier != "mechanical_translational"
            )
            for port in self.ports
        ):
            raise EnergyGraphInputError(
                "tyre inputs must be mechanical_rotational and outputs must be mechanical_translational"
            )


@dataclass(frozen=True, slots=True)
class EnergyConnection:
    connection_id: str
    source_component_id: str
    source_port_id: str
    target_component_id: str
    target_port_id: str

    def __post_init__(self) -> None:
        for name, value in (
            ("connection_id", self.connection_id),
            ("source_component_id", self.source_component_id),
            ("source_port_id", self.source_port_id),
            ("target_component_id", self.target_component_id),
            ("target_port_id", self.target_port_id),
        ):
            _identifier(name, value)


@dataclass(frozen=True, slots=True)
class EnergyGraph:
    schema_version: str
    graph_id: str
    components: tuple[EnergyComponent, ...]
    connections: tuple[EnergyConnection, ...]

    def __post_init__(self) -> None:
        if self.schema_version != "1.0":
            raise EnergyGraphInputError(
                f"unsupported graph schema_version {self.schema_version!r}"
            )
        _identifier("graph_id", self.graph_id)
        if not self.components:
            raise EnergyGraphInputError("graph must contain at least one component")
        if not self.connections:
            raise EnergyGraphInputError("graph must contain at least one connection")


@dataclass(frozen=True, slots=True)
class CompiledConnection:
    connection_id: str
    source_component_id: str
    source_port_id: str
    target_component_id: str
    target_port_id: str
    carrier: str
    maximum_power_w: float


@dataclass(frozen=True, slots=True)
class CompiledEnergyGraph:
    schema_version: str
    graph_id: str
    component_order: tuple[str, ...]
    connections: tuple[CompiledConnection, ...]


def source_component(
    component_id: str, *, carrier: str, maximum_power_w: float
) -> EnergyComponent:
    return EnergyComponent(
        component_id,
        "source",
        (EnergyPort("power_out", "output", carrier, maximum_power_w),),
    )


def converter_component(
    component_id: str,
    *,
    input_carrier: str,
    output_carrier: str,
    maximum_input_power_w: float,
    maximum_output_power_w: float,
) -> EnergyComponent:
    return EnergyComponent(
        component_id,
        "converter",
        (
            EnergyPort("power_in", "input", input_carrier, maximum_input_power_w),
            EnergyPort(
                "power_out", "output", output_carrier, maximum_output_power_w
            ),
        ),
    )


def transmission_component(
    component_id: str,
    *,
    maximum_input_power_w: float,
    maximum_output_power_w: float,
) -> EnergyComponent:
    return EnergyComponent(
        component_id,
        "transmission",
        (
            EnergyPort(
                "shaft_in",
                "input",
                "mechanical_rotational",
                maximum_input_power_w,
            ),
            EnergyPort(
                "shaft_out",
                "output",
                "mechanical_rotational",
                maximum_output_power_w,
            ),
        ),
    )


def tyre_component(
    component_id: str,
    *,
    maximum_input_power_w: float,
    maximum_output_power_w: float,
) -> EnergyComponent:
    return EnergyComponent(
        component_id,
        "tyre",
        (
            EnergyPort(
                "shaft_in",
                "input",
                "mechanical_rotational",
                maximum_input_power_w,
            ),
            EnergyPort(
                "road_power_out",
                "output",
                "mechanical_translational",
                maximum_output_power_w,
            ),
        ),
    )


def sink_component(
    component_id: str, *, carrier: str, maximum_power_w: float
) -> EnergyComponent:
    return EnergyComponent(
        component_id,
        "sink",
        (EnergyPort("power_in", "input", carrier, maximum_power_w),),
    )


def compile_energy_graph(graph: EnergyGraph) -> CompiledEnergyGraph:
    """Validate and deterministically compile a one-to-one directed graph."""

    component_by_id: dict[str, EnergyComponent] = {}
    port_by_key: dict[tuple[str, str], EnergyPort] = {}
    for component in graph.components:
        if component.component_id in component_by_id:
            raise EnergyGraphInputError(
                f"duplicate component_id {component.component_id!r}"
            )
        component_by_id[component.component_id] = component
        for port in component.ports:
            port_by_key[(component.component_id, port.port_id)] = port

    connection_ids: set[str] = set()
    connected_outputs: dict[tuple[str, str], str] = {}
    connected_inputs: dict[tuple[str, str], str] = {}
    compiled_connections: list[CompiledConnection] = []
    adjacency = {component_id: set() for component_id in component_by_id}
    indegree = {component_id: 0 for component_id in component_by_id}

    for connection in graph.connections:
        if connection.connection_id in connection_ids:
            raise EnergyGraphInputError(
                f"duplicate connection_id {connection.connection_id!r}"
            )
        connection_ids.add(connection.connection_id)
        if connection.source_component_id == connection.target_component_id:
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} is a self-loop"
            )
        source_key = (connection.source_component_id, connection.source_port_id)
        target_key = (connection.target_component_id, connection.target_port_id)
        if source_key not in port_by_key:
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} references missing source port {source_key!r}"
            )
        if target_key not in port_by_key:
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} references missing target port {target_key!r}"
            )
        source_port = port_by_key[source_key]
        target_port = port_by_key[target_key]
        if source_port.direction != "output":
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} source is not an output"
            )
        if target_port.direction != "input":
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} target is not an input"
            )
        if source_port.carrier != target_port.carrier:
            raise EnergyGraphInputError(
                f"connection {connection.connection_id!r} carrier mismatch: "
                f"{source_port.carrier!r} -> {target_port.carrier!r}"
            )
        if source_key in connected_outputs:
            raise EnergyGraphInputError(
                f"output port {source_key!r} has implicit fan-out through "
                f"{connected_outputs[source_key]!r} and {connection.connection_id!r}"
            )
        if target_key in connected_inputs:
            raise EnergyGraphInputError(
                f"input port {target_key!r} has multiple sources through "
                f"{connected_inputs[target_key]!r} and {connection.connection_id!r}"
            )
        connected_outputs[source_key] = connection.connection_id
        connected_inputs[target_key] = connection.connection_id
        compiled_connections.append(
            CompiledConnection(
                connection.connection_id,
                connection.source_component_id,
                connection.source_port_id,
                connection.target_component_id,
                connection.target_port_id,
                source_port.carrier,
                min(source_port.maximum_power_w, target_port.maximum_power_w),
            )
        )
        if connection.target_component_id not in adjacency[connection.source_component_id]:
            adjacency[connection.source_component_id].add(
                connection.target_component_id
            )
            indegree[connection.target_component_id] += 1

    unconnected = sorted(
        key
        for key, port in port_by_key.items()
        if (port.direction == "output" and key not in connected_outputs)
        or (port.direction == "input" and key not in connected_inputs)
    )
    if unconnected:
        raise EnergyGraphInputError(f"required ports are unconnected: {unconnected!r}")

    ready = [component_id for component_id, degree in indegree.items() if degree == 0]
    heapq.heapify(ready)
    order: list[str] = []
    while ready:
        component_id = heapq.heappop(ready)
        order.append(component_id)
        for target_id in sorted(adjacency[component_id]):
            indegree[target_id] -= 1
            if indegree[target_id] == 0:
                heapq.heappush(ready, target_id)
    if len(order) != len(component_by_id):
        cyclic = sorted(
            component_id for component_id, degree in indegree.items() if degree > 0
        )
        raise EnergyGraphInputError(f"component graph contains a cycle: {cyclic!r}")

    compiled_connections.sort(
        key=lambda item: (
            item.source_component_id,
            item.source_port_id,
            item.target_component_id,
            item.target_port_id,
            item.connection_id,
        )
    )
    return CompiledEnergyGraph(
        schema_version=graph.schema_version,
        graph_id=graph.graph_id,
        component_order=tuple(order),
        connections=tuple(compiled_connections),
    )
