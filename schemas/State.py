### state.py
from typing import Annotated, List, TypedDict
import operator

class State(TypedDict, total=False):
    # Pre-aggregator
    owner: str
    repo: str
    since: str
    until: str
    shards: List[List[dict]]
    harvested: Annotated[List[dict], operator.add]
    analyzed: Annotated[List[dict], operator.add]
    harvested_shards: Annotated[List[List[dict]], operator.add]
    diff_results: Annotated[List[dict], operator.add]

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
