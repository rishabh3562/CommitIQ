# workflow/chunked_parallel_flow.py
from langgraph.graph import StateGraph
from schemas.parallel_workflow_state import ParallelWorkflowState
from agents.harvester import Harvester
from agents.harvest_orchestrator import harvest_orchestrator
from agents.analyst import DiffAnalyst
from agents.batch_orchestrator import BatchOrchestrator
from agents.batch_collector import BatchCollector
from agents.narrator import Narrator
from agents.slack_reporter import SlackReporter
import json


def build_parallel_graph(N: int = 3) -> StateGraph: 
    graph = StateGraph(
        state_class=ParallelWorkflowState,
        state_schema=json.dumps(ParallelWorkflowState.schema())
    )

    graph.add_node("start", lambda state: state)
    graph.add_node("harvest_orchestrator", harvest_orchestrator)
    graph.add_edge("start", "harvest_orchestrator")  # <-- remove key argument here

    for i in range(N):
        graph.add_node(f"harvester_{i}", Harvester(i))
        graph.add_node(f"batch_orch_{i}", BatchOrchestrator(i))
        graph.add_node(f"diff_{i}", DiffAnalyst(i))

        graph.add_edge("harvest_orchestrator", f"harvester_{i}")
        graph.add_edge(f"harvester_{i}", f"batch_orch_{i}")
        graph.add_edge(f"batch_orch_{i}", f"diff_{i}")

    graph.add_node("batch_collector", BatchCollector(N))
    graph.add_node("narrator", Narrator())
    graph.add_node("slack_reporter", SlackReporter())

    for i in range(N):
        graph.add_edge(f"diff_{i}", "batch_collector")

    graph.add_edge("batch_collector", "narrator")
    graph.add_edge("narrator", "slack_reporter")
    graph.set_entry_point("start")

    return graph

def run_parallel_flow(initial_state: ParallelWorkflowState, N: int = 3) -> ParallelWorkflowState:
    workflow = build_parallel_graph(N).compile()
    final_state = workflow.invoke(initial_state)
    return final_state