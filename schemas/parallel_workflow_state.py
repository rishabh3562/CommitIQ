### state.py
from typing import Annotated, List, TypedDict
import operator

class ParallelWorkflowStateV2(TypedDict, total=False):
    # Pre-aggregator
    owner: str
    repo: str
    since: str
    until: str
    data_segments: List[List[dict]]
    collected: Annotated[List[dict], operator.add]
    processed: Annotated[List[dict], operator.add]
    collected_data: Annotated[List[List[dict]], operator.add]
    analysis_output: Annotated[List[dict], operator.add]

    # Post-aggregator
    aggregated: dict  # Final metrics & insights
    final_report: dict

    # Narrator output
    dora: dict
    other: dict
    dora_summary: str
    other_summary: str
    llm_summary: str
    insights: Annotated[List[str], operator.add]  # ← preserve for compatibility

    # Slack formatting or combined display
    combined: dict
