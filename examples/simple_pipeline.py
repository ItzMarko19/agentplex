"""Simple three-step pipeline example."""
import asyncio
from agentplex import Graph, FunctionNode, Executor, State


def fetch_data(state: State):
    state.set("raw_data", [1, 2, 3, 4, 5])
    return {"status": "fetched"}

# fixme: handle errors

def transform(state: State):
    data = state.get("raw_data", [])
    state.set("transformed", [x * 2 for x in data])


def summarize(state: State):
    transformed = state.get("transformed", [])
    state.set("summary", {"count": len(transformed), "sum": sum(transformed)})

# cleanup: improve this

async def main():
    g = Graph("etl")
    g.add_node(FunctionNode("fetch", fetch_data))
    g.add_node(FunctionNode("transform", transform))
    g.add_node(FunctionNode("summarize", summarize))
    g.add_edge("fetch", "transform")
    g.add_edge("transform", "summarize")

    executor = Executor(g)
    result = await executor.run()
    print(f"success: {result.success}")
    print(f"elapsed: {result.elapsed:.3f}s")
    print(f"summary: {result.state.get('summary')}")


if __name__ == "__main__":
    asyncio.run(main())
