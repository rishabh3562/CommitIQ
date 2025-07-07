from schemas.workflow_state import WorkflowState
from utils.v1.logger import logger
from utils.v1.github_helper import get_incident_issues
from dateutil.parser import parse
from statistics import mean
from configs.langchain import insight_chain

def run_insight_narrator(state: WorkflowState) -> dict:
    raw_commits = state.harvester["raw_commits"]
    author_stats = state.analyst["author_stats"]
    spikes = state.analyst["spikes"]
    total_commits = len(raw_commits)
    lines_added = sum(c["additions"] for c in raw_commits)
    lines_deleted = sum(c["deletions"] for c in raw_commits)
    files_touched = sum(c["files_touched"] for c in raw_commits)

    issues = get_incident_issues(state.owner, state.repo, state.since)
    mttr = mean([
        (parse(i["closed_at"]) - parse(i["created_at"])).total_seconds() / 3600
        for i in issues if i.get("closed_at")
    ]) if issues else 0

    compact_stats = {
        a: {
            "commits": s["commits"],
            "spike": a in spikes
        } for a, s in author_stats.items()
    }

    inputs = {
        "stats": compact_stats,
        "pr_throughput": state.harvester["pr_throughput"],
        "ci_failures": state.harvester["ci_failures"],
        "review_latency": state.harvester["review_latency"],
        "cycle_time": state.harvester["cycle_time"],
        "spikes": spikes,
        "total_commits": total_commits,
        "lines_added": lines_added,
        "lines_deleted": lines_deleted,
        "files_touched": files_touched,
        "mttr": round(mttr, 2)
    }

    logger.terminal_log("[INSIGHT] 🧠 Generating engineering summary...")
    logger.terminal_log("[INSIGHT] Inputs", **inputs)

    if all(v == 0 or v == 0.0 for v in [
        inputs["pr_throughput"],
        inputs["ci_failures"],
        inputs["review_latency"],
        inputs["cycle_time"]
    ]):
        return {
            "narrator": {
                "summary": "No significant engineering activity this period. All DORA metrics at zero.",
                "insights": {},
                "stats": inputs
            }
        }

    # Get LLM summary
    summary_text = insight_chain.invoke(inputs)

    # Structured insights (optional — could be extracted via another chain or static logic)
    insights = {
        "productivity": f"{inputs['pr_throughput']} PRs merged, {inputs['total_commits']} commits from {len(compact_stats)} contributors.",
        "code_volume": f"{inputs['lines_added']} lines added, {inputs['lines_deleted']} deleted across {inputs['files_touched']} files.",
        "risks": f"{len(inputs['spikes'])} spike(s) in contribution detected. Review for quality.",
        "efficiency": f"Review latency: {inputs['review_latency']}h, Cycle time: {inputs['cycle_time']}h, MTTR: {inputs['mttr']}h.",
        "ci_health": f"{inputs['ci_failures']} CI failure(s) recorded."
    }

    logger.terminal_log("[INSIGHT] ✅ Summary ready")
    logger.terminal_log("[INSIGHT] Summary Output", summary=summary_text)

    return {
        "narrator": {
            "summary": summary_text,
            "insights": insights,
            "stats": inputs
        }
    }
