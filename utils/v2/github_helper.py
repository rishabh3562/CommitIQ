import json, requests
from datetime import datetime
from configs.github import HEADERS, API_BASE

def get_commits(owner, repo, since=None, until=None):
    commits, page = [], 1
    while True:
        params = {"since": since, "per_page": 100, "page": page}
        r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/commits", headers=HEADERS, params=params)
        r.raise_for_status()
        batch = r.json()
        if not batch: break
        commits += batch
        page += 1
    return commits
def get_full_commit(owner, repo, since=None, until=None):
    commits, page = [], 1
    while True:
        params = {"since": since, "until": until, "per_page": 100, "page": page}
        r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/commits", headers=HEADERS, params=params)
        r.raise_for_status()
        batch = r.json()
        if not batch: break

        for c in batch:
            full_commit = requests.get(c["url"], headers=HEADERS)
            full_commit.raise_for_status()
            commits.append(full_commit.json())

        page += 1
    return commits

def get_incident_issues(owner, repo, since=None):
    params = {"labels": "bug", "state": "closed", "since": since, "per_page": 100}
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/issues", headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def get_commit_by_sha(owner, repo, sha):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_pr_files(owner, repo, pr_number):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/files", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_pr_for_commit(owner, repo, sha):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/commits/{sha}/pulls", headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_ci_failures_for_pr(owner, repo, pr_number):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}/checks", headers=HEADERS)
    fails = [c for c in r.json().get("check_runs", []) if c["conclusion"] == "failure"]
    return len(fails)

def get_review_latency_for_pr(owner, repo, pr_number):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}", headers=HEADERS)
    pr = r.json()
    created = datetime.fromisoformat(pr["created_at"].rstrip("Z"))
    comments = requests.get(pr["review_comments_url"], headers=HEADERS).json()
    if not comments: return 0
    submitted = comments[0].get("submitted_at")
    if not submitted: return None
    first = datetime.fromisoformat(submitted.rstrip("Z"))
    return round((first - created).total_seconds() / 3600, 2)

def get_lead_time_for_pr(pr: dict, harvested_shards: list[list[dict]]) -> float:
    pr_created_at = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
    all_commits = [commit for shard in harvested_shards for commit in shard]
    related_commits = [
        c for c in all_commits
        if c["repo"] == pr["repo"] and c["owner"] == pr["owner"] and c["sha"] in pr.get("commit_shas", [])
    ]
    if not related_commits:
        return 0.0
    first_commit_time = min(datetime.fromisoformat(c["date"].replace("Z", "+00:00")) for c in related_commits)
    return (pr_created_at - first_commit_time).total_seconds() / 3600



from datetime import datetime

def compute_lead_time(commit_date: str, pr_merged_at: str) -> float:
    try:
        commit_dt = datetime.fromisoformat(commit_date.replace("Z", "+00:00"))
        merged_dt = datetime.fromisoformat(pr_merged_at.replace("Z", "+00:00"))
        return (merged_dt - commit_dt).total_seconds() / 3600
    except Exception:
        return 0.0
def get_cycle_time_for_pr(owner, repo, pr_number):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}", headers=HEADERS)
    pr = r.json()
    if not pr.get("merged_at"): return 0
    created = datetime.fromisoformat(pr["created_at"].rstrip("Z"))
    merged = datetime.fromisoformat(pr["merged_at"].rstrip("Z"))
    return round((merged - created).total_seconds() / 3600, 2)
