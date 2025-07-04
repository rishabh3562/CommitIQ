from pydantic import BaseModel
from typing import Any, Optional

class WorkflowState(BaseModel):

    owner: str
    repo: str
    since: Optional[str] = None
    harvester: Optional[dict] = None
    # add other state keys like:
    analyst: Optional[dict] = None
    narrator: Optional[dict] = None
    raw_commits: Any = None
    author_stats: Any = None
    spikes: Any = None
    summary: str = ""
    total_commits: int = 0
    lines_added: int = 0
    lines_deleted: int = 0
    files_touched: int = 0
    mttr: float = 0.0

     # DORA metrics
    pr_throughput: int = 0
    ci_failures: int = 0
    review_latency: float = 0
    cycle_time: float = 0
