from schemas.workflow_state import WorkflowState
from utils.v1.logger import logger

def run_diff_analyst(state: WorkflowState) -> dict:
    raw = state.harvester["raw_commits"]
    logger.terminal_log(f"[ANALYST] 🔍 Starting analysis on {len(raw)} raw commits")

    stats = {}
    for idx, c in enumerate(raw, 1):
        auth = c["author"]
        bucket=stats.setdefault(auth,{
             "commits": 0,
            "lines_added":   0, "lines_deleted": 0, "files_touched": 0,
            # code‑change metrics
            "commits":       0,
            "lines_added":   0,
            "lines_deleted": 0,
            "files_touched": 0,
         })
        bucket["commits"] += 1

        detail = c.get("files") or []
        # logger.terminal_log(f"[ANALYST] ({idx}/{len(raw)}) Processing commit by {auth}, {len(detail)} files")
        bucket["lines_added"]   += c.get("additions", 0)
        bucket["lines_deleted"] += c.get("deletions", 0)
        bucket["files_touched"] += c.get("files_touched", 0)

    spikes = [a for a, s in stats.items() if s["lines_added"] > 1000]
    logger.terminal_log("[ANALYST] ✅ Diff analysis complete", stats=stats, spikes=spikes)

    return {
    "analyst": {
        "author_stats": stats,  
        "spikes": spikes
    }
}

