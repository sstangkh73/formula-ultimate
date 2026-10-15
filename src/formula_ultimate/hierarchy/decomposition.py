"""Seed-driven abstract decomposition of the vehicle into a part hierarchy.

The procedure has no part catalogue. It groups the required capabilities,
assigns each group a leaf budget, and recursively partitions every budget into
children with random compositions. Characteristic lengths in metres are
planning targets for later geometry realization, not measured sizes. Nothing
here is physical validation.
"""

from __future__ import annotations

import math
import random
from dataclasses import asdict, dataclass

from formula_ultimate.topology.functional_vehicle import REQUIRED_CAPABILITIES

from .part_tree import JOINT_KINDS, canonical_sha256


DECOMPOSITION_VERSION = "hier-decomp-v1"
ROOT_ID = "vehicle"


class DecompositionFailure(RuntimeError):
    """Raised when no attempt satisfies the declared constraints."""


@dataclass(frozen=True)
class DecompositionConfig:
    leaf_budget_min: int = 170
    leaf_budget_max: int = 230
    min_total_leaves: int = 150
    min_levels: int = 4
    capability_min_height: int = 2
    capability_min_leaves: int = 5
    group_min_leaves: int = 8
    group_weight_min: float = 0.5
    group_weight_max: float = 2.0
    branching_min: int = 2
    branching_max: int = 5
    max_depth: int = 7
    merge_probability: float = 0.3
    root_length_m: float = 4.0
    anchor_scale_min: float = 0.55
    anchor_scale_max: float = 0.85
    satellite_scale_min: float = 0.12
    satellite_scale_max: float = 0.45
    min_leaf_length_m: float = 0.004
    min_leaf_size_ratio: float = 100.0
    max_attempts: int = 64
    joint_kinds: tuple[str, ...] = JOINT_KINDS


DEFAULT_CONFIG = DecompositionConfig()


def config_sha256(config: DecompositionConfig) -> str:
    return canonical_sha256({"version": DECOMPOSITION_VERSION, **asdict(config)})


@dataclass(frozen=True)
class AbstractNode:
    id: str
    parent: str | None
    depth: int
    children: tuple[str, ...]
    functions: tuple[str, ...]
    anchor_child: str | None
    characteristic_length_m: float

    @property
    def kind(self) -> str:
        return "assembly" if self.children else "part"


@dataclass(frozen=True)
class Attachment:
    id: str
    assembly: str
    source: str
    target: str
    kind: str


@dataclass(frozen=True)
class AbstractTree:
    version: str
    seed: int
    attempt: int
    config_sha256: str
    root: str
    nodes: tuple[AbstractNode, ...]
    attachments: tuple[Attachment, ...]

    def node_map(self) -> dict[str, AbstractNode]:
        return {node.id: node for node in self.nodes}


def _composition(rng: random.Random, total: int, parts: int) -> list[int]:
    """Uniform random composition of total into parts positive integers."""

    cuts = sorted(rng.sample(range(1, total), parts - 1))
    bounds = [0, *cuts, total]
    return [bounds[i + 1] - bounds[i] for i in range(parts)]


def _group_capabilities(rng: random.Random, config: DecompositionConfig) -> list[tuple[str, ...]]:
    capabilities = sorted(REQUIRED_CAPABILITIES)
    rng.shuffle(capabilities)
    groups: list[tuple[str, ...]] = []
    index = 0
    while index < len(capabilities):
        if index + 1 < len(capabilities) and rng.random() < config.merge_probability:
            groups.append(tuple(sorted(capabilities[index:index + 2])))
            index += 2
        else:
            groups.append((capabilities[index],))
            index += 1
    return groups


def _attempt(seed: int, attempt: int, config: DecompositionConfig) -> AbstractTree:
    rng = random.Random(seed * 1_000_003 + attempt)
    groups = _group_capabilities(rng, config)
    total = rng.randint(config.leaf_budget_min, config.leaf_budget_max)
    weights = [rng.uniform(config.group_weight_min, config.group_weight_max) for _ in groups]
    weight_sum = sum(weights)
    budgets = [max(config.group_min_leaves, round(total * w / weight_sum)) for w in weights]

    nodes: dict[str, dict] = {}
    budget_of: dict[str, int] = {}
    order: list[str] = []

    def add(node_id, parent, depth, functions, length):
        nodes[node_id] = {
            "parent": parent, "depth": depth, "children": [], "functions": functions,
            "anchor_child": None, "length": length,
        }
        order.append(node_id)

    def scale(anchor: bool) -> float:
        if anchor:
            return rng.uniform(config.anchor_scale_min, config.anchor_scale_max)
        return rng.uniform(config.satellite_scale_min, config.satellite_scale_max)

    def pick_anchor(child_ids: list[str]) -> str:
        best = max(budget_of[c] for c in child_ids)
        return next(c for c in child_ids if budget_of[c] == best)

    add(ROOT_ID, None, 0, (), config.root_length_m)
    group_ids = []
    for index, (group, budget) in enumerate(zip(groups, budgets)):
        group_id = f"g{index}-" + "-".join(group)
        budget_of[group_id] = budget
        group_ids.append(group_id)
    root_anchor = pick_anchor(group_ids)
    nodes[ROOT_ID]["children"] = group_ids
    nodes[ROOT_ID]["anchor_child"] = root_anchor

    stack: list[tuple[str, tuple[str, ...]]] = []
    for group_id, group in zip(group_ids, groups):
        add(group_id, ROOT_ID, 1, group,
            max(config.min_leaf_length_m, config.root_length_m * scale(group_id == root_anchor)))
        stack.append((group_id, group))

    # Depth-first expansion; children are pushed in reverse to expand in order.
    while stack:
        node_id, functions = stack.pop()
        node = nodes[node_id]
        budget = budget_of[node_id]
        depth = node["depth"]
        if budget == 1:
            continue
        if depth + 1 >= config.max_depth:
            parts = [1] * budget
        else:
            upper = min(config.branching_max, budget)
            if depth == 1:
                # A capability group must keep height >= 2, so not all leaves.
                upper = min(upper, budget - 1)
            lower = min(config.branching_min, upper)
            parts = _composition(rng, budget, rng.randint(lower, upper))
        child_ids = []
        for index, part_budget in enumerate(parts):
            prefix = "a" if part_budget > 1 else "p"
            child_id = f"{node_id}.{prefix}{index}"
            budget_of[child_id] = part_budget
            child_ids.append(child_id)
        anchor = pick_anchor(child_ids)
        node["children"] = child_ids
        node["anchor_child"] = anchor
        expand = []
        for child_id in child_ids:
            length = max(config.min_leaf_length_m, node["length"] * scale(child_id == anchor))
            add(child_id, node_id, depth + 1, functions if budget_of[child_id] > 1 else (), length)
            expand.append((child_id, functions))
        stack.extend(reversed(expand))

    frozen = {
        node_id: AbstractNode(
            id=node_id, parent=data["parent"], depth=data["depth"],
            children=tuple(data["children"]), functions=tuple(data["functions"]),
            anchor_child=data["anchor_child"], characteristic_length_m=float(data["length"]),
        )
        for node_id, data in nodes.items()
    }
    preorder = _preorder(ROOT_ID, frozen)

    def anchor_leaf(node_id: str) -> str:
        while frozen[node_id].children:
            node_id = frozen[node_id].anchor_child
        return node_id

    leaf_memo: dict[str, tuple[str, ...]] = {}
    attachments = []
    for node_id in preorder:
        node = frozen[node_id]
        if not node.children:
            continue
        anchor_leaves = _leaves_in_order(node.anchor_child, frozen, leaf_memo)
        for child_id in node.children:
            if child_id == node.anchor_child:
                continue
            attachments.append(Attachment(
                id=f"j{len(attachments)}",
                assembly=node_id,
                source=anchor_leaf(child_id),
                target=rng.choice(anchor_leaves),
                kind=rng.choice(config.joint_kinds),
            ))

    return AbstractTree(
        version=DECOMPOSITION_VERSION, seed=seed, attempt=attempt,
        config_sha256=config_sha256(config), root=ROOT_ID,
        nodes=tuple(frozen[node_id] for node_id in preorder),
        attachments=tuple(attachments),
    )


def _preorder(root: str, node_by_id: dict[str, AbstractNode]) -> list[str]:
    ordered: list[str] = []
    stack = [root]
    while stack:
        node_id = stack.pop()
        ordered.append(node_id)
        stack.extend(reversed(node_by_id[node_id].children))
    return ordered


def _leaves_in_order(node_id: str, node_by_id: dict[str, AbstractNode],
                     memo: dict[str, tuple[str, ...]]) -> tuple[str, ...]:
    if node_id not in memo:
        memo[node_id] = tuple(
            n for n in _preorder(node_id, node_by_id) if not node_by_id[n].children
        )
    return memo[node_id]


def leaves(tree: AbstractTree) -> tuple[str, ...]:
    return _leaves_in_order(tree.root, tree.node_map(), {})


def levels(tree: AbstractTree) -> int:
    return 1 + max(node.depth for node in tree.nodes)


def subtree_height(tree: AbstractTree, node_id: str) -> int:
    node_by_id = tree.node_map()
    base = node_by_id[node_id].depth
    return max(node_by_id[n].depth for n in _preorder(node_id, node_by_id)) - base


def subtree_leaf_count(tree: AbstractTree, node_id: str) -> int:
    return len(_leaves_in_order(node_id, tree.node_map(), {}))


def topology_signature(tree: AbstractTree, node_id: str) -> str:
    """Order-independent signature with the acceptance-suite definition."""

    node_by_id = tree.node_map()
    memo: dict[str, str] = {}
    for current in reversed(_preorder(node_id, node_by_id)):
        node = node_by_id[current]
        if not node.children:
            memo[current] = "L"
        else:
            kids = "".join(sorted(memo[c] for c in node.children))
            memo[current] = "(" + ",".join(sorted(node.functions)) + ":" + kids + ")"
    return memo[node_id]


def constraint_violations(tree: AbstractTree, config: DecompositionConfig) -> list[str]:
    """Return every declared constraint the tree misses (empty when accepted)."""

    problems: list[str] = []
    node_by_id = tree.node_map()
    leaf_ids = leaves(tree)
    if len(leaf_ids) < config.min_total_leaves:
        problems.append(f"{len(leaf_ids)} leaves < {config.min_total_leaves}")
    if levels(tree) < config.min_levels:
        problems.append(f"{levels(tree)} levels < {config.min_levels}")
    if node_by_id[tree.root].functions:
        problems.append("root must not carry capabilities")
    for capability in sorted(REQUIRED_CAPABILITIES):
        if not any(
            capability in node.functions
            and subtree_height(tree, node.id) >= config.capability_min_height
            and subtree_leaf_count(tree, node.id) >= config.capability_min_leaves
            for node in tree.nodes if node.children
        ):
            problems.append(f"capability {capability} has no deep enough subtree")
    lengths = [node_by_id[n].characteristic_length_m for n in leaf_ids]
    if any(not math.isfinite(x) or x <= 0 for x in lengths):
        problems.append("leaf lengths must be finite and positive")
    elif max(lengths) / min(lengths) < config.min_leaf_size_ratio:
        problems.append(
            f"leaf size ratio {max(lengths) / min(lengths):.1f} < {config.min_leaf_size_ratio}"
        )
    for node in tree.nodes:
        if node.children and len(node.children) < 2 and node.id != tree.root:
            problems.append(f"assembly {node.id} has fewer than 2 children")
        if node.children and node.anchor_child not in node.children:
            problems.append(f"assembly {node.id} anchor is not a child")
    for node in tree.nodes:
        if len(node.children) < 2:
            continue
        owner = {leaf: child for child in node.children
                 for leaf in _leaves_in_order(child, node_by_id, {})}
        parent = {c: c for c in node.children}

        def find(x: str) -> str:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        for item in tree.attachments:
            a, b = owner.get(item.source), owner.get(item.target)
            if a is not None and b is not None and a != b:
                parent[find(a)] = find(b)
        if len({find(c) for c in node.children}) != 1:
            problems.append(f"children of {node.id} are not connected")
    for item in tree.attachments:
        if item.kind not in JOINT_KINDS:
            problems.append(f"attachment {item.id} has unknown kind {item.kind}")
        if node_by_id[item.source].children or node_by_id[item.target].children:
            problems.append(f"attachment {item.id} endpoints must be leaves")
    return problems


def decompose(seed: int, config: DecompositionConfig = DEFAULT_CONFIG,
              start_attempt: int = 0) -> AbstractTree:
    """Return the first attempt >= start_attempt that satisfies every declared constraint.

    ``start_attempt`` lets a later stage (layout) reject an accepted tree and
    continue the same declared search; at most ``config.max_attempts``
    attempts are tried from there.
    """

    if isinstance(seed, bool) or not isinstance(seed, int):
        raise TypeError("seed must be an int")
    if isinstance(start_attempt, bool) or not isinstance(start_attempt, int) or start_attempt < 0:
        raise ValueError("start_attempt must be a non-negative int")
    last: list[str] = []
    for attempt in range(start_attempt, start_attempt + config.max_attempts):
        tree = _attempt(seed, attempt, config)
        last = constraint_violations(tree, config)
        if not last:
            return tree
    raise DecompositionFailure(
        f"seed {seed}: no attempt of {config.max_attempts} met the constraints; last: {last}"
    )
