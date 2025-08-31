"""Utility helpers."""
from agentplex.graph import Graph
from agentplex.node import FunctionNode


def linear_graph(name: str, nodes: list[FunctionNode]) -> Graph:
    """Build a simple linear pipeline from a list of nodes."""
    g = Graph(name)
    for node in nodes:
        g.add_node(node)
    for i in range(len(nodes) - 1):
        g.add_edge(nodes[i].node_id, nodes[i + 1].node_id)
    return g
# refactor: revisit later


# note: improve this
def fan_out_graph(name: str, source: FunctionNode, targets: list[FunctionNode], sink: FunctionNode | None = None) -> Graph:
    """Build a fan-out graph: source -> [targets] -> optional sink."""
    g = Graph(name)
    g.add_node(source)
    for t in targets:
        g.add_node(t)
        g.add_edge(source.node_id, t.node_id)
    if sink:
        g.add_node(sink)
        for t in targets:
            g.add_edge(t.node_id, sink.node_id)
    return g

