
### graph_builder.py
from langgraph.graph import StateGraph, END, START
from schemas.State import State
from agents.start_node import start_node
from agents.harvest_orchestrator import harvester_orchestrator
from agents.harvester import make_harvester
from agents.analyst import make_diff_analyst
from agents.batch_collector import batch_collector
from agents.aggregator import aggregator
# For parallel flow:
from agents.narrator import narrator_parallel as narrator
from agents.slack_reporter import slack_reporter
from configs.constants import NUM_PARALLEL

def build_graph(State):
    builder = StateGraph(State)

    builder.add_node("start", start_node)
    builder.add_node("harvester_orchestrator", harvester_orchestrator)
    builder.add_node("batch_collector", batch_collector)
    builder.add_node("aggregator", aggregator)
    builder.add_node("narrator", narrator)
    builder.add_node("slack_reporter", slack_reporter)

    builder.add_edge(START, "start")
    builder.add_edge("start", "harvester_orchestrator")

    for i in range(NUM_PARALLEL):
        h = f"harvester_{i}"
        a = f"diff_analyst_{i}"

        builder.add_node(h, make_harvester(i))
        builder.add_node(a, make_diff_analyst(i))

        builder.add_edge("harvester_orchestrator", h)
        builder.add_edge(h, a)
        builder.add_edge(a, "batch_collector")

    builder.add_edge("batch_collector", "aggregator")
    builder.add_edge("aggregator", "narrator")
    builder.add_edge("narrator", "slack_reporter")
    builder.add_edge("slack_reporter", END)

    return builder.compile()

