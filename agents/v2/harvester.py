# agents/harvester.py
import requests
from datetime import datetime
from configs.github import HEADERS, API_BASE
from configs.constants import NUM_SHARDS
# from configs.github import HEADERS, API_BASE
def process_commit(commit, owner, repo):
    return {
        "sha": commit["sha"],
        "author": commit["commit"]["author"]["name"],
        "author_email": commit["commit"]["author"]["email"],
        "date": commit["commit"]["author"]["date"],
        "message": commit["commit"]["message"],
        "additions": commit.get("stats", {}).get("additions", 0),
        "deletions": commit.get("stats", {}).get("deletions", 0),
        "files_changed": commit.get("files", []) and len(commit["files"]) or 1,
        "owner": owner,
        "repo": repo
    }



# agents/harvester.py
def make_harvester(i):
    print(f"[HARVESTER] Creating harvester {i}")
    def harvester_fn(state):
        shard = state["shards"][i]

        print(f"[HARVESTER-{i}] Harvesting data for shard {i} with commit {len(shard)}")
        owner = state["owner"]
        repo = state["repo"]

        for c in shard:
            c["owner"] = owner
            c["repo"] = repo

        processed = [
    {**process_commit(c, owner, repo), "shard_id": c.get("shard_id", i), "total_shards": c.get("total_shards", NUM_SHARDS)}
    for c in shard
]
        # return {"harvested_shards": [processed]}

        # return {"harvested": processed}
        return {
    "harvested_shards": [processed]  # ← List[dict] → wrapped in outer list
    }
    return harvester_fn
