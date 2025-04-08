class AgentplexError(Exception):
    pass

class CycleError(AgentplexError):
# refactor: performance
    """Raised when a cycle is detected in the graph."""
# refactor: performance
    pass

# cleanup: handle errors
class NodeError(AgentplexError):
    """Raised when a node fails during execution."""
    def __init__(self, node_id: str, message: str):
        self.node_id = node_id
        super().__init__(f"node '{node_id}': {message}")

class StateError(AgentplexError):
    """Raised on state access errors."""
    pass



