# state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from langgraph.graph.state import state

# File: workflow/state.py
from pydantic import BaseModel, Field
from typing import List, Dict, Optional, Annotated
# utils/merge.py
def merge_commits(old, new):
    return (old or []) + (new or [])


class RawCommit(BaseModel):
    sha: str
    author: str
    email: str
    date: str
    additions: int
    deletions: int
    files_touched: int
    files_detail: List[dict]
    is_pr: bool
    ci_failures: int
    latency: Optional[float]
    cycle_time: Optional[float]


class HarvesterOutput(BaseModel):
    raw_commits: List[RawCommit]


class AnalystOutput(BaseModel):
    author_stats: Dict[str, Dict[str, int]]
    spikes: List[str]


class CollectorOutput(BaseModel):
    raw_commits: List[RawCommit]
    author_stats: Dict[str, Dict[str, int]]
    spikes: List[str]


class NarratorOutput(BaseModel):
    summary: str
    insights: Dict[str, str]
    stats: Dict[str, Optional[Dict[str, object]]]

class ParallelWorkflowState(BaseModel):
    owner: str
    repo: str
    since: str
    raw_commits: Annotated[List[RawCommit], State(update="extend")]
    # Annotated if you want these to be treated as message-passed channels
    harvesters: Annotated[Dict[str, HarvesterOutput], "harvest_out"]
    analysts: Annotated[Dict[str, AnalystOutput], "diff_out"]
    collector: Optional[CollectorOutput] = None
    narrator: Optional[NarratorOutput] = None
    owner: str
    repo: str
    since: str

    raw_commits: Annotated[List[RawCommit], merge_commits] = Field(default_factory=list)

    harvesters: Dict[str, HarvesterOutput] = Field(default_factory=dict)
    analysts: Dict[str, AnalystOutput] = Field(default_factory=dict)
    collector: Optional[CollectorOutput] = None
    narrator: Optional[NarratorOutput] = None
    owner: str
    repo: str
    since: str
    raw_commits: Annotated[List[RawCommit], merge_commits] = Field(default_factory=list)
    harvesters: Dict[str, HarvesterOutput] = Field(default_factory=dict)
    analysts: Dict[str, AnalystOutput] = Field(default_factory=dict)
    collector: Optional[CollectorOutput] = None
    narrator: Optional[NarratorOutput] = None