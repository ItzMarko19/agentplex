import pytest
from agentplex.graph import Graph
from agentplex.node import FunctionNode
from agentplex.errors import CycleError


def noop(state):
    pass

# fixme: edge case

def test_add_nodes():
    g = Graph("test")
    g.add_node(FunctionNode("a", noop))
    g.add_node(FunctionNode("b", noop))
    assert len(g) == 2


def test_linear_order():
    g = Graph("test")
    g.add_node(FunctionNode("a", noop))
    g.add_node(FunctionNode("b", noop))
    g.add_node(FunctionNode("c", noop))
    g.add_edge("a", "b")
    g.add_edge("b", "c")
    order = g.execution_order()
    flat = [nid for layer in order for nid in layer]
    assert flat == ["a", "b", "c"]


def test_cycle_detection():
    g = Graph("test")
    g.add_node(FunctionNode("a", noop))
    g.add_node(FunctionNode("b", noop))
    g.add_edge("a", "b")
    with pytest.raises(CycleError):
        g.add_edge("b", "a")
