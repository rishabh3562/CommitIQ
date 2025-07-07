from datetime import datetime, timezone

def to_dt(iso):
    return datetime.fromisoformat(iso.replace("Z", "+00:00"))

def calc_deploy_count(prs):
    return sum(1 for pr in prs if pr.get("merged_at"))

def calc_ci_failures(prs, ci_failed_prs):
    return sum(1 for pr in prs if pr["number"] in ci_failed_prs)

def calc_avg_lead_time(prs):
    times = [
        (to_dt(pr["merged_at"]) - to_dt(pr["created_at"])).total_seconds()
        for pr in prs if pr.get("merged_at") and pr.get("created_at")
    ]
    return round(sum(times)/len(times)/3600, 2) if times else 0.0

def calc_avg_review_latency(prs):
    times = []
    for pr in prs:
        if pr.get("reviews"):
            first_review = min((to_dt(r["submitted_at"]) for r in pr["reviews"]), default=None)
            if first_review:
                latency = (first_review - to_dt(pr["created_at"])).total_seconds()
                times.append(latency)
    return round(sum(times)/len(times)/3600, 2) if times else 0.0

def calc_avg_cycle_time(prs):
    times = [
        (to_dt(pr["merged_at"]) - to_dt(pr["commits"][0]["commit"]["author"]["date"])).total_seconds()
        for pr in prs if pr.get("merged_at") and pr.get("commits")
    ]
    return round(sum(times)/len(times)/3600, 2) if times else 0.0

def calc_change_failure_rate(prs, ci_failed_prs):
    merged = [pr for pr in prs if pr.get("merged_at")]
    failed = [pr for pr in merged if pr["number"] in ci_failed_prs]
    return round(len(failed)/len(merged), 2) if merged else 0.0

def calc_mttr(incidents):
    times = [
        (to_dt(i["closed_at"]) - to_dt(i["created_at"])).total_seconds()
        for i in incidents if i.get("closed_at")
    ]
    return round(sum(times)/len(times)/3600, 2) if times else 0.0
