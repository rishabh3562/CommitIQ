# agents/data_collector.py
import requests
from datetime import datetime
from configs.github import HEADERS, API_BASE
from configs.constants import DATA_SHARDS
# from configs.github import HEADERS, API_BASE
def extract_commit_data(commit, owner, repo):
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



# agents/data_collector.py
def make_data_collector(i):
    print(f"[DATA_COLLECTOR] Creating data collector {i}")
    def collector_fn(state):
        segment = state["data_segments"][i]

        print(f"[DATA_COLLECTOR-{i}] Collecting data for segment {i} with commit {len(segment)}")
        owner = state["owner"]
        repo = state["repo"]

        for c in segment:
            c["owner"] = owner
            c["repo"] = repo

        processed = [
    {**extract_commit_data(c, owner, repo), "segment_id": c.get("segment_id", i), "total_segments": c.get("total_segments", DATA_SHARDS)}
    for c in segment
]
        # return {"collected_data": [processed]}

        # return {"collected": processed}
        return {
    "collected_data": [processed]  # ← List[dict] → wrapped in outer list
    }
    return collector_fn
