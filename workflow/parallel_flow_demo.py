from typing import Annotated
from typing_extensions import TypedDict
from langgraph.graph import StateGraph, START, END
import operator

# ---------- State ----------
class State(TypedDict):
    harvested: Annotated[list, operator.add]
    analyzed: Annotated[list, operator.add]
    combined: dict
    insights: list

# ---------- Node Factories ----------
def make_harvester(i):
    def node(state: State):
        print(f"Harvester {i} fetched data")
        return {"harvested": [f"data_from_repo{i}"]}
    return node

def make_batch_orchestrator(i):
    def node(state: State):
        print(f"Batch Orchestrator {i} working")
        return {}
    return node

def make_diff_analyst(i):
    def node(state: State):
        print(f"Diff Analyst {i} analyzing")
        return {"analyzed": [f"diff_metrics_{i}"]}
    return node

# ---------- Shared Nodes ----------
def start_node(state: State): return {}
def harvester_orchestrator(state: State): return {}
def batch_collector(state: State): return {}
def aggregator(state: State):
    combined = {"summary": f"{len(state['analyzed'])} analyses combined"}
    return {"combined": combined}
def narrator(state: State): return {"insights": ["Team velocity up 30%"]}
def slack_reporter(state: State): return {}

# ---------- Build Dynamic Graph ----------
builder = StateGraph(State)

builder.add_node("start", start_node)
builder.add_node("harvester_orchestrator", harvester_orchestrator)
builder.add_node("batch_collector", batch_collector)
builder.add_node("aggregator", aggregator)
builder.add_node("narrator", narrator)
builder.add_node("slack_reporter", slack_reporter)

builder.add_edge(START, "start")
builder.add_edge("start", "harvester_orchestrator")

# ---------- Dynamic fan-out ----------
NUM_PARALLEL = 5  # Control here how many parallel harvesters to launch

for i in range(1, NUM_PARALLEL + 1):
    h_name = f"harvester_{i}"
    b_name = f"batch_orchestrator_{i}"
    a_name = f"diff_analyst_{i}"

    builder.add_node(h_name, make_harvester(i))
    builder.add_node(b_name, make_batch_orchestrator(i))
    builder.add_node(a_name, make_diff_analyst(i))

    builder.add_edge("harvester_orchestrator", h_name)
    builder.add_edge(h_name, b_name)
    builder.add_edge(b_name, a_name)
    builder.add_edge(a_name, "batch_collector")

# ---------- Final fan-in path ----------
builder.add_edge("batch_collector", "aggregator")
builder.add_edge("aggregator", "narrator")
builder.add_edge("narrator", "slack_reporter")
builder.add_edge("slack_reporter", END)

# ---------- Run ----------
if __name__ == "__main__":
    inputs = {"harvested": [], "analyzed": [], "combined": {}, "insights": []}
    graph = builder.compile()
    result = graph.invoke(inputs)
    print("\nFinal State:\n", result)
