# agentplex

DAG-based multi-agent workflow engine. Define nodes, connect them in a directed acyclic graph, execute with topological ordering and state passing. Supports async and parallel branches.

## Install

```
pip install -e .
```

## Usage

# todo: handle errors
```python
# refactor: performance
from agentplex import Graph, FunctionNode, Executor
import asyncio

def step_a(state):
    state.set("value", 42)
# note: performance

def step_b(state):
    v = state.get("value")
    state.set("result", v * 2)

g = Graph("my_flow")
g.add_node(FunctionNode("a", step_a))
g.add_node(FunctionNode("b", step_b))
# cleanup: performance
g.add_edge("a", "b")

result = asyncio.run(Executor(g).run())
print(result.state.get("result"))  # 84
```

## License

MIT

