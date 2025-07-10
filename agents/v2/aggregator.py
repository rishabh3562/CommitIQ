from collections import defaultdict
from datetime import datetime

def safe_float(val):
    try:
        return float(val) if val is not None else 0.0
    except:
        return 0.0

def safe_avg(lst): return round(sum(lst) / len(lst), 2) if lst else 0.0

def parse_dt(val):
    try:
        return datetime.fromisoformat(val)
    except:
        return None

def aggregator(state):
    print("[AGGREGATOR] Start")
    analyzed = state.get("analyzed", [])
    since = state.get("since")
    until = state.get("until")

    authors = {}
    repo_metrics = {
        "total_commits": 0,
        "total_prs": 0,
        "deploy_count": 0,
        "deploy_failures": 0,
        "ci_failures": 0,
        "lead_times": [],
        "review_latencies": [],
        "cycle_times": [],
        "overall_churn": {
            "lines_added": 0,
            "lines_deleted": 0,
            "files_changed": 0
        },
        "mttr_list": [],
        "code_spike_count": 0,
        "notable_spikes": []
    }

    seen_shas = set()

    for item in analyzed:
        sha = item.get("sha")
        if not sha or sha in seen_shas:
            continue
        seen_shas.add(sha)

        author = item.get("author", "unknown")
        email = item.get("author_email", "unknown@example.com")

        if author not in authors:
            authors[author] = {
                "email": email,
                "commits": 0,
                "prs_merged": 0,
                "lead_time_hours": 0.0,
                "review_latency_hours": 0.0,
                "cycle_time_hours": 0.0,
                "lines_added": 0,
                "lines_deleted": 0,
                "files_changed": 0,
                "ci_failures": 0,
                "shard_ids": set()
            }

        authors[author]["commits"] += 1
        authors[author]["prs_merged"] += int(bool(item.get("is_pr")))
        authors[author]["lead_time_hours"] += safe_float(item.get("lead_time_hours"))
        authors[author]["review_latency_hours"] += safe_float(item.get("review_latency_hours"))
        authors[author]["cycle_time_hours"] += safe_float(item.get("cycle_time_hours"))
        authors[author]["lines_added"] += safe_float(item.get("lines_added"))
        authors[author]["lines_deleted"] += safe_float(item.get("lines_deleted"))
        authors[author]["files_changed"] += safe_float(item.get("files_changed"))
        authors[author]["ci_failures"] += int(bool(item.get("ci_failed")))
        authors[author]["shard_ids"].add(item.get("shard_id"))

        repo_metrics["total_commits"] += 1
        repo_metrics["total_prs"] += int(bool(item.get("is_pr")))
        repo_metrics["deploy_count"] += int(bool(item.get("is_deploy")))
        repo_metrics["ci_failures"] += int(bool(item.get("ci_failed")))
        repo_metrics["deploy_failures"] += int(bool(item.get("is_deploy") and item.get("deploy_failed")))
        # repo_metrics["lead_times"].append(safe_float(item.get("lead_time_hours")))
        # repo_metrics["cycle_times"].append(safe_float(item.get("cycle_time_hours")))
        # repo_metrics["review_latencies"].append(safe_float(item.get("review_latency_hours")))
        lt = item.get("lead_time_hours")
        if lt is not None: repo_metrics["lead_times"].append(lt)
        review_latency_hours = item.get("review_latency_hours")
        if review_latency_hours is not None: repo_metrics["review_latencies"].append(review_latency_hours)

        cycle_time_hours = item.get("cycle_time_hours")
        if cycle_time_hours is not None: repo_metrics["cycle_times"].append(cycle_time_hours)

        repo_metrics["overall_churn"]["lines_added"] += safe_float(item.get("lines_added"))
        repo_metrics["overall_churn"]["lines_deleted"] += safe_float(item.get("lines_deleted"))
        repo_metrics["overall_churn"]["files_changed"] += safe_float(item.get("files_changed"))

        # MTTR logic
        incident_created = parse_dt(item.get("incident_created_at"))
        incident_resolved = parse_dt(item.get("incident_resolved_at"))
        if incident_created and incident_resolved and incident_resolved > incident_created:
            mttr = (incident_resolved - incident_created).total_seconds() / 3600
            repo_metrics["mttr_list"].append(mttr)

        if item.get("spike_flag"):
            repo_metrics["code_spike_count"] += 1
            repo_metrics["notable_spikes"].append({
                "sha": item.get("sha"),
                "author": author,
                "lines_changed": safe_float(item.get("lines_added")) + safe_float(item.get("lines_deleted")),
                "files_changed": safe_float(item.get("files_changed")),
                "message": item.get("message", "")[:100]
            })

    # Final aggregations
    # repo_metrics["avg_lead_time_hours"] = safe_avg(repo_metrics["lead_times"])
        # only average non‑null, >0 lead times
    clean_leads = [v for v in repo_metrics["lead_times"] if v]
    repo_metrics["avg_lead_time_hours"] = safe_avg(clean_leads)
    # repo_metrics["avg_review_latency_hours"] = safe_avg(repo_metrics["review_latencies"])
    clean_reviews = [v for v in repo_metrics["review_latencies"] if v]
    repo_metrics["avg_review_latency_hours"] = safe_avg(clean_reviews)    

    repo_metrics["avg_cycle_time_hours"] = safe_avg(repo_metrics["cycle_times"])
    clean_cycles = [v for v in repo_metrics["cycle_times"] if v]
    # repo_metrics["avg_cycle_time_hours"] = safe_avg(clean_cycles)
    
    # repo_metrics["change_failure_rate"] = round(repo_metrics["deploy_failures"] / max(repo_metrics["deploy_count"], 1), 2)
    # proportion of deploys that failed
    repo_metrics["change_failure_rate"] = round(
        repo_metrics.get("deploy_failures", 0) / max(repo_metrics["deploy_count"], 1), 2
    ) 

    # repo_metrics["mttr_hours"] = safe_avg(repo_metrics["mttr_list"])
    # MTTR from orchestrator‑fetched incidents
    mttrs = []
    for inc in state.get("incidents", []):
        try:
            created = datetime.fromisoformat(inc["created"].replace("Z","+00:00"))
            resolved = datetime.fromisoformat(inc["resolved"].replace("Z","+00:00"))
            mttrs.append((resolved - created).total_seconds() / 3600)
        except:
            continue
    repo_metrics["mttr_hours"] = round(sum(mttrs) / len(mttrs), 2) if mttrs else 0.0
    print("[AGGREGATOR] END")
    return {
        "aggregated": {
            "since": since,
            "until": until,
            "authors": {
                k: {**v, "shard_ids": list(v["shard_ids"])} for k, v in authors.items()
            },
            "repo": repo_metrics
        }
    }
