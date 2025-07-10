
from configs.constants import NUM_SHARDS
from utils.v2.github_helper import (
    get_pr_for_commit, get_review_latency_for_pr,
    get_cycle_time_for_pr, get_ci_failures_for_pr,
    compute_lead_time
)
from configs.constants import NUM_SHARDS, SPIKE_THRESHOLD
def safe_float(val):
    try:
        return float(val) if val is not None else 0.0
    except:
        return 0.0

def analyze_diff(commit):
    sha    = commit["sha"]
    owner  = commit["owner"]
    repo   = commit["repo"]

    # robust stats extraction
    additions     = int(commit.get("additions", 0))
    deletions     = int(commit.get("deletions", 0))
    files_list    = commit.get("files", [])
    files_changed = max(len(files_list), 1)

    lines_changed = additions + deletions
    churn_score = round(lines_changed / files_changed, 2) if files_changed else 0.0

    spike_flag    = lines_changed >= SPIKE_THRESHOLD

    # PR metadata
    pr_list    = get_pr_for_commit(owner, repo, sha) or []
    is_pr      = bool(pr_list)
    pr_number  = pr_list[0]["number"] if is_pr else None

    # timings
    if is_pr:
        ci_failed            = get_ci_failures_for_pr(owner, repo, pr_number) > 0
        lead_time_hours      = compute_lead_time(commit["date"], pr_list[0]["merged_at"])
        review_latency_hours = get_review_latency_for_pr(owner, repo, pr_number) or 0.0
        cycle_time_hours     = get_cycle_time_for_pr(owner, repo, pr_number)
    else:
        ci_failed = False
        # skip zero–values for non‑PRs so aggregator can filter them out
        lead_time_hours = review_latency_hours = cycle_time_hours = None

    return {
        "sha": sha,
        "author": commit["author"],
        "author_email": commit["author_email"],
        "is_pr": is_pr,
        "pr_id": pr_number,
        "is_deploy": "deploy" in commit["message"].lower(),
        "ci_failed": ci_failed,
        "lead_time_hours": round(safe_float(lead_time_hours), 2),
        "review_latency_hours": round(safe_float(review_latency_hours), 2),
        "cycle_time_hours": round(safe_float(cycle_time_hours), 2),
        "lines_added": additions,
        "lines_deleted": deletions,
        "files_changed": files_changed,
        "lines_changed": lines_changed,
        "churn_score": churn_score,
        "spike_flag": spike_flag
    }

def make_diff_analyst(i):
    def diff_fn(state):
        shard_data = state.get("harvested_shards", [])
        commits = shard_data[i] if i < len(shard_data) else []
        inc_map = {i["incident_sha"]: i for i in state.get("incidents", [])}

        for c in commits:
            inc = inc_map.get(c["sha"])
            if inc:
                c["incident_created_at"] = inc.get("created")
                c["incident_resolved_at"] = inc.get("resolved")

        print(f"[DIFF_ANALYST-{i}] Analyzing {len(commits)} commits")
        results = [{ **analyze_diff(c), "shard_id": c.get("shard_id", i), "total_shards": c.get("total_shards", NUM_SHARDS) }
                for c in commits]
        return { "diff_results": results }

    return diff_fn

