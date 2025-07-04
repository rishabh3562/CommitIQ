import json, requests
from datetime import datetime
from configs.github import HEADERS, API_BASE

def get_commits(owner, repo, since=None):
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

def get_cycle_time_for_pr(owner, repo, pr_number):
    r = requests.get(f"{API_BASE}/repos/{owner}/{repo}/pulls/{pr_number}", headers=HEADERS)
    pr = r.json()
    if not pr.get("merged_at"): return 0
    created = datetime.fromisoformat(pr["created_at"].rstrip("Z"))
    merged = datetime.fromisoformat(pr["merged_at"].rstrip("Z"))
    return round((merged - created).total_seconds() / 3600, 2)
