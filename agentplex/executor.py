"""Execute a graph with state passing."""
from __future__ import annotations
import asyncio
import time
from typing import Any
from agentplex.graph import Graph
from agentplex.state import State
from agentplex.errors import NodeError


class ExecutionResult:
    def __init__(self, state: State, elapsed: float, errors: list[str]):
        self.state = state
        self.elapsed = elapsed
        self.errors = errors
        self.success = len(errors) == 0


class Executor:
    """Run a graph in topological order with optional parallelism."""

    def __init__(self, graph: Graph, parallel: bool = True):
        self.graph = graph
        self.parallel = parallel

    async def run(self, initial_state: dict[str, Any] | None = None) -> ExecutionResult:
        state = State(initial_state)
        errors: list[str] = []
        start = time.monotonic()

        layers = self.graph.execution_order()
        for layer in layers:
            if self.parallel and len(layer) > 1:
                tasks = []
                for nid in layer:
                    node = self.graph.get_node(nid)
                    tasks.append(self._run_node(node, state, errors))
                await asyncio.gather(*tasks)
            else:
                for nid in layer:
                    node = self.graph.get_node(nid)
                    await self._run_node(node, state, errors)
            state.snapshot()

        elapsed = time.monotonic() - start
        return ExecutionResult(state, elapsed, errors)

    async def _run_node(self, node, state: State, errors: list[str]) -> None:
        try:
            await node.run(state)
        except Exception as exc:
            errors.append(f"{node.node_id}: {exc}")


