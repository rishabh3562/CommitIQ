### agents/harvester_orchestrator.py
from pprint import pprint
from configs.constants import DATA_SHARDS
from utils.v2.github_helper import get_full_commit,get_incident_issues

def harvester_orchestrator(state):
    print("[HARVESTER_ORCHESTRATOR] Orchestrating harvesters with state:", state)
    owner = state["owner"]
    repo = state["repo"]
    since = state["since"]
    until = state["until"]

    all_commits = get_full_commit(owner, repo, since, until)
    if not all_commits:
        return {"data_segments": [[] for _ in range(DATA_SHARDS)]}

    print(f"[HARVESTER_ORCHESTRATOR] Total commits fetched: {len(all_commits)}")
    if not all_commits:
        return {"data_segments": [[] for _ in range(DATA_SHARDS)]}
    # fetch incidents for MTTR
    print(f"[HARVESTER_ORCHESTRATOR] fetching incidents...")
    incidents = get_incident_issues(owner, repo, since)
    print(f"[HARVESTER_ORCHESTRATOR] {len(incidents)} incidents fetched")
    state["incidents"] = [{"created": i["created_at"], "resolved": i["closed_at"]} for i in incidents]

    # attach incidents list to state
    state["incidents"] = [
        {"created": i["created_at"], "resolved": i["closed_at"]}
        for i in incidents
    ]

    # Divide commits into DATA_SHARDS
    segments = [all_commits[i::DATA_SHARDS] for i in range(DATA_SHARDS)]
    return {
        "data_segments": [
            [{"segment_id": i, "total_segments": DATA_SHARDS, **c} for c in segment] if segment else []
            for i, segment in enumerate(segments)
        ]
    }

