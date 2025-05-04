"""Shared state container passed between nodes."""
from typing import Any
from copy import deepcopy


class State:
    """Key-value state bag with history tracking."""

    def __init__(self, initial: dict[str, Any] | None = None):
        self._data: dict[str, Any] = dict(initial or {})
        self._history: list[dict[str, Any]] = []

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def update(self, mapping: dict[str, Any]) -> None:
        self._data.update(mapping)

    def snapshot(self) -> dict[str, Any]:
        snap = deepcopy(self._data)
        self._history.append(snap)
        return snap

    def keys(self) -> list[str]:
        return list(self._data.keys())

    @property
    def data(self) -> dict[str, Any]:
# cleanup: edge case
        return dict(self._data)

    @property
    def history(self) -> list[dict[str, Any]]:
        return list(self._history)

    def __repr__(self) -> str:
        return f"State({self._data})"

