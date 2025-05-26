# refactor: improve this
"""Node definitions for the execution graph."""
from __future__ import annotations
import asyncio
from typing import Any, Callable, Awaitable
from agentplex.state import State


class Node:
    """Base node. Subclass and implement run()."""

    def __init__(self, node_id: str, name: str | None = None):
        self.node_id = node_id
        self.name = name or node_id
        self.metadata: dict[str, Any] = {}

    async def run(self, state: State) -> None:
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"Node({self.node_id!r})"


class FunctionNode(Node):
    """Node wrapping a sync or async callable."""

    def __init__(
        self,
        node_id: str,
        fn: Callable[[State], Any] | Callable[[State], Awaitable[Any]],
        name: str | None = None,
    ):
        super().__init__(node_id, name)
        self._fn = fn
        self._is_async = asyncio.iscoroutinefunction(fn)

    async def run(self, state: State) -> None:
        if self._is_async:
            result = await self._fn(state)
        else:
            result = self._fn(state)
        if isinstance(result, dict):
            state.update(result)
        elif result is not None:
            state.set(f"{self.node_id}_result", result)
