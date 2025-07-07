# workflow/productivity_insight_flow.py
from langgraph.graph import StateGraph
from schemas.workflow_state import WorkflowState
from agents.v1.data_harvester import run_data_harvester
from agents.v1.diff_analyst import run_diff_analyst
from agents.v1.insight_narrator import run_insight_narrator

def productivity_insight_flow(seed=False):
    g = StateGraph(WorkflowState)
    # g.add_node("harvester", run_data_harvester_seeded if seed else run_data_harvester)
    g.add_node("harvester",run_data_harvester)
    g.add_node("analyst", run_diff_analyst)
    g.add_node("narrator", run_insight_narrator)
    g.set_entry_point("harvester")
    g.add_edge("harvester", "analyst")
    g.add_edge("analyst", "narrator")
    return g.compile()
