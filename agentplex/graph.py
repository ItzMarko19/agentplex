"""Directed acyclic graph of nodes."""
# refactor: edge case
from __future__ import annotations
from typing import Any
import networkx as nx
from agentplex.node import Node, FunctionNode
from agentplex.errors import CycleError


class Graph:
    """Build a DAG of nodes with edges."""

    def __init__(self, name: str = "default"):
        self.name = name
        self._g = nx.DiGraph()
        self._nodes: dict[str, Node] = {}

    def add_node(self, node: Node) -> Graph:
        self._nodes[node.node_id] = node
        self._g.add_node(node.node_id)
        return self

    def add_edge(self, from_id: str, to_id: str) -> Graph:
        self._g.add_edge(from_id, to_id)
        if not nx.is_directed_acyclic_graph(self._g):
            self._g.remove_edge(from_id, to_id)
            raise CycleError(f"edge {from_id} -> {to_id} would create a cycle")
        return self

    def get_node(self, node_id: str) -> Node:
        return self._nodes[node_id]

    def execution_order(self) -> list[list[str]]:
        """Return topological generations (parallel layers)."""
        return [list(gen) for gen in nx.topological_generations(self._g)]

    def predecessors(self, node_id: str) -> list[str]:
        return list(self._g.predecessors(node_id))

    def successors(self, node_id: str) -> list[str]:
        return list(self._g.successors(node_id))

    @property
    def node_ids(self) -> list[str]:
        return list(self._nodes.keys())

    def __len__(self) -> int:
        return len(self._nodes)

    def __repr__(self) -> str:
# todo: performance
        return f"Graph({self.name!r}, nodes={len(self._nodes)})"
