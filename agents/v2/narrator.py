from configs.langchain import parallel_insight_chain
from utils.v2.dora import * # etc.


def generate_dora_summary(prs, ci_failed_prs, incidents):
    return {
        "dora": {
            "deploy_count": calc_deploy_count(prs),
            "ci_failures": calc_ci_failures(prs, ci_failed_prs),
            "avg_lead_time_hours": calc_avg_lead_time(prs),
            "avg_review_latency_hours": calc_avg_review_latency(prs),
            "avg_cycle_time_hours": calc_avg_cycle_time(prs),
            "change_failure_rate": calc_change_failure_rate(prs, ci_failed_prs),
            "mttr_hours": calc_mttr(incidents),
        }
    }
def calculate_change_failure_rate(prs: list[dict], incident_issues: list[dict]) -> float:
    if not prs:
        return 0.0
    all_pr_numbers = {pr["number"] for pr in prs}
    failing_prs = set()
    for incident in incident_issues:
        for pr in incident.get("linked_prs", []):
            if pr in all_pr_numbers:
                failing_prs.add(pr)
    return len(failing_prs) / len(prs)

def extract_dora_v2(repo_metrics):
    return {
        "deploy_count": repo_metrics.get("deploy_count", 0),
        "ci_failures": repo_metrics.get("ci_failures", 0),
        "avg_lead_time_hours": repo_metrics.get("avg_lead_time_hours", 0),
        "avg_review_latency_hours": repo_metrics.get("avg_review_latency_hours", 0),
        "avg_cycle_time_hours": repo_metrics.get("avg_cycle_time_hours", 0),
        "change_failure_rate": repo_metrics.get("change_failure_rate", 0),
        "mttr_hours": repo_metrics.get("mttr_hours", 0),
        # "change_failure_rate": calculate_change_failure_rate(merged_prs, incident_issues)

    }

def extract_other_v2(repo, authors):
    authors = authors or {}
    top_authors = sorted(
        authors.items(),
        key=lambda x: x[1].get("commits", 0),
        reverse=True
    )[:3]

    author_summaries = [
        f"{name} → Commits: {data.get('commits', 0)}, PRs: {data.get('prs_merged', 0)}, Files Changed: {data.get('files_changed', 0)}"
        for name, data in top_authors
    ]

    spikes = repo.get("notable_spikes", [])[:2]
    spike_summaries = [
        f"{s.get('author')} → {int(s.get('lines_changed', 0))} lines, {int(s.get('files_changed', 0))} files – “{s.get('message', '')}”"
        for s in spikes
    ]

    return {
        "total_commits": repo.get("total_commits", 0),
        "total_prs": repo.get("total_prs", 0),
        "code_spike_count": repo.get("code_spike_count", 0),
        "notable_spikes": spike_summaries,
        "top_authors": author_summaries,
    }

async def narrator_parallel(state):
    print("[NARRATOR] Started")
    repo = state.get("aggregated", {}).get("repo", {}) or {}
    authors = state.get("aggregated", {}).get("authors", {}) or {}

    dora = extract_dora_v2(repo)
    other = extract_other_v2(repo, authors)

    dora_summary = (
        f"- Deploys: {dora['deploy_count']}\n"
        f"- CI Failures: {dora['ci_failures']}\n"
        f"- Lead Time: {dora['avg_lead_time_hours']} hrs\n"
        f"- Review Latency: {dora['avg_review_latency_hours']} hrs\n"
        f"- Cycle Time: {dora['avg_cycle_time_hours']} hrs\n"
        f"- Change Failure Rate: {dora['change_failure_rate']}\n"
        f"- MTTR: {dora['mttr_hours']} hrs"
    )

    notable_spikes = (
        "\n  ".join(other["notable_spikes"]) if other["notable_spikes"] else "None"
    )
    top_contributors = (
        "\n  ".join(other["top_authors"]) if other["top_authors"] else "No active contributors"
    )

    other_summary = (
        f"- Commits: {other['total_commits']}\n"
        f"- PRs: {other['total_prs']}\n"
        f"- Code Spikes: {other['code_spike_count']}\n"
        f"- Notable Spikes:\n  {notable_spikes}\n"
        f"- Top Contributors:\n  {top_contributors}"
    )

    try:
        llm_response = await parallel_insight_chain.ainvoke({
            "dora_summary": dora_summary,
            "other_summary": other_summary,
        })
    except Exception as e:
        llm_response = f"[ERROR] Failed to generate LLM insights: {e}"
    print("[NARRATOR] End")
    return {
        "dora": dora,
        "other": other,
        "dora_summary": dora_summary,
        "other_summary": other_summary,
        "llm_summary": llm_response,
        "insights": [llm_response],
    }
