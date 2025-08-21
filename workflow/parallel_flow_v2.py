
### graph_builder.py
from langgraph.graph import StateGraph, END, START
# from schemas.parallel_workflow_state import ParallelWorkflowStateV2
from agents.v2.start_node import start_node
from agents.v2.harvest_orchestrator import harvester_orchestrator
from agents.v2.harvester import make_data_collector
from agents.v2.analyst import make_code_reviewer
from agents.v2.batch_collector import batch_collector
from agents.v2.aggregator import aggregator
# For parallel flow:
from agents.v2.narrator import narrator_parallel as narrator
from agents.v2.slack_reporter import slack_reporter
from configs.constants import CONCURRENT_WORKERS

def build_graph_parallel_v2(State):
    builder = StateGraph(State)

    builder.add_node("start", start_node)
    builder.add_node("harvester_orchestrator", harvester_orchestrator)
    builder.add_node("batch_collector", batch_collector)
    builder.add_node("aggregator", aggregator)
    builder.add_node("narrator", narrator)
    builder.add_node("slack_reporter", slack_reporter)

    builder.add_edge(START, "start")
    builder.add_edge("start", "harvester_orchestrator")

    for i in range(CONCURRENT_WORKERS):
        h = f"data_collector_{i}"
        a = f"code_reviewer_{i}"

        builder.add_node(h, make_data_collector(i))
        builder.add_node(a, make_code_reviewer(i))

        builder.add_edge("harvester_orchestrator", h)
        builder.add_edge(h, a)
        builder.add_edge(a, "batch_collector")

    builder.add_edge("batch_collector", "aggregator")
    builder.add_edge("aggregator", "narrator")
    builder.add_edge("narrator", "slack_reporter")
    builder.add_edge("slack_reporter", END)

    return builder.compile()

