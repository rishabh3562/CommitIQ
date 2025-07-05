from utils.github_helper import (
    get_commits, get_commit_by_sha, get_pr_files, get_pr_for_commit,
    get_ci_failures_for_pr, get_review_latency_for_pr, get_cycle_time_for_pr
)
from schemas.workflow_state import WorkflowState
from utils.logger import logger
import requests
from copy import deepcopy
from pprint import pprint
from utils.bot_utils import slack_progress_message


def run_data_harvester(state: WorkflowState) -> dict:
    # logger.slack_log_func
    logger.terminal_log("[HARVESTER] ⛏ Starting data harvest")
    logger.terminal_log(f"[HARVESTER] Target repo: {state.owner}/{state.repo} since {state.since}")
    

    commits = get_commits(state.owner, state.repo, state.since)
    logger.terminal_log(f"[HARVESTER] Retrieved {len(commits)} commits")
    slack_progress_message("[HARVESTER]", len(commits))
    raw = []
    # counters; we’ll compute throughput/CI-failures/latency/cycle-time from raw
    for idx, c in enumerate(commits, 1):
        sha = c["sha"]
        author = c["commit"]["author"]["name"]
        date = c["commit"]["author"]["date"]
        # fetch full commit stats (additions/deletions/files)
        detail = get_commit_by_sha(state.owner, state.repo, sha)
        files = detail.get("files", [])
        additions = sum(f.get("additions",0) for f in files)
        deletions = sum(f.get("deletions",0) for f in files)
        touched = len(files)

        record = {
            "sha":         sha,
            "author":      author,
            "date":        date,
            # code‑change metrics
            "additions":  additions,
            "deletions":  deletions,
            "files_touched": touched,
            "files_detail": files,
            "is_pr":       False,
            "ci_failures": 0,
            "latency":     None,
            "cycle_time":  None,
        }
        raw.append(record)

        logger.terminal_log(f"[HARVESTER] ({idx}/{len(commits)}) Processing commit {sha[:7]} by {author} on {date}")

        prs = get_pr_for_commit(state.owner, state.repo, sha)
        if not prs:
            continue

        pr_num = prs[0]["number"]
        record["is_pr"] = True
        logger.terminal_log(f"[HARVESTER] ↳ Linked to PR #{pr_num}")

        # CI failures
        fails = get_ci_failures_for_pr(state.owner, state.repo, pr_num)
        record["ci_failures"] = fails

        # review latency
        lat = get_review_latency_for_pr(state.owner, state.repo, pr_num)
        record["latency"] = lat if lat is not None else 0

        # cycle time
        ct = get_cycle_time_for_pr(state.owner, state.repo, pr_num)
        record["cycle_time"] = ct if ct is not None else 0

    # derive top‑level metrics
    pr_records   = [r for r in raw if r["is_pr"]]
    pr_throughput = len(pr_records)
    total_ci      = sum(r["ci_failures"] for r in pr_records)
    avg_lat       = (sum(r["latency"] for r in pr_records) / pr_throughput) if pr_throughput else 0
    avg_cycle     = (sum(r["cycle_time"] for r in pr_records) / pr_throughput) if pr_throughput else 0

    result = {
        "raw_commits": raw,
        "pr_throughput": pr_throughput,
        "ci_failures": total_ci,
        "review_latency": round(avg_lat, 2),
        "cycle_time": round(avg_cycle, 2),
    }

    # logger.terminal_log("[HARVESTER] ✅ Harvest complete", **result)
    logger.terminal_log("[HARVESTER] ✅ Harvest complete")
    pretty = deepcopy(result)
    for r in pretty["raw_commits"]:
        r.pop("files_detail", None)
    pprint(pretty)    
    return {"harvester": result}
