### agents/harvester_orchestrator.py
from pprint import pprint
from configs.constants import NUM_SHARDS
from utils.v2.github_helper import get_full_commit,get_incident_issues

def harvester_orchestrator(state):
    print("[HARVESTER_ORCHESTRATOR] Orchestrating harvesters with state:", state)
    owner = state["owner"]
    repo = state["repo"]
    since = state["since"]
    until = state["until"]

    all_commits = get_full_commit(owner, repo, since, until)
    if not all_commits:
        return {"shards": [[] for _ in range(NUM_SHARDS)]}

    print(f"[HARVESTER_ORCHESTRATOR] Total commits fetched: {len(all_commits)}")
    if not all_commits:
        return {"shards": [[] for _ in range(NUM_SHARDS)]}
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

    # Divide commits into NUM_SHARDS
    shards = [all_commits[i::NUM_SHARDS] for i in range(NUM_SHARDS)]
    return {
        "shards": [
            [{"shard_id": i, "total_shards": NUM_SHARDS, **c} for c in shard] if shard else []
            for i, shard in enumerate(shards)
        ]
    }

