from datetime import datetime, timedelta
from configs.constants import NUM_PARALLEL
import requests
from configs.github import HEADERS, API_BASE
from datetime import datetime
from configs.constants import NUM_PARALLEL
from pprint import pprint
from configs.constants import NUM_SHARDS
### agents/harvester_orchestrator.py
from utils.github_helper import get_commits,get_full_commit,get_incident_issues
import json


def harvester_orchestrator(state):
    print("Orchestrating harvesters with state:", state)
    owner = state["owner"]
    repo = state["repo"]
    since = state["since"]
    until = state["until"]

    all_commits = get_full_commit(owner, repo, since, until)
    if not all_commits:
        return {"shards": [[] for _ in range(NUM_SHARDS)]}

    print("Sample commit object:")
    print(json.dumps(all_commits[0], indent=2))  # move after check

    print("Sample commit object:")
    
    print(json.dumps(all_commits[0], indent=2))
    #print commit count
    print(f"Total commits fetched: {len(all_commits)}")
    if not all_commits:
        return {"shards": [[] for _ in range(NUM_SHARDS)]}
    # fetch incidents for MTTR
    incidents = get_incident_issues(owner, repo, since)
    state["incidents"] = [{"created": i["created_at"], "resolved": i["closed_at"]} for i in incidents]

    # attach incidents list to state
    state["incidents"] = [
        {"created": i["created_at"], "resolved": i["closed_at"]}
        for i in incidents
    ]

    # Divide commits into NUM_SHARDS
    shards = [all_commits[i::NUM_SHARDS] for i in range(NUM_SHARDS)]
    return {
        "shards": [
            [{"shard_id": i, "total_shards": NUM_SHARDS, **c} for c in shard] if shard else []
            for i, shard in enumerate(shards)
        ]
    }

#     return {
#     "shards": [
#         [{"shard_id": i, "total_shards": NUM_SHARDS, **c} for c in shard]
#         for i, shard in enumerate(shards)
#     ]
# }


