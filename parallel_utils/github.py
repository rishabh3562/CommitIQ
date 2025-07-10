import httpx
from datetime import datetime
from typing import List
from configs.constants import GITHUB_TOKEN
from configs.github import API_BASE as GITHUB_API,HEADERS
# GITHUB_API = "https://api.github.com"
# GITHUB_TOKEN = "your_personal_access_token"

#   # Use env var in prod

# HEADERS = {
#     "Authorization": f"Bearer {GITHUB_TOKEN}",
#     "Accept": "application/vnd.github+json"
# }

def get_commits(owner: str, repo: str, since: str) -> List[dict]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits"
    params = {"since": since, "per_page": 20}
    r = httpx.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json()

def get_commit_by_sha(owner: str, repo: str, sha: str) -> dict:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{sha}"
    r = httpx.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_pr_for_commit(owner: str, repo: str, sha: str) -> List[dict]:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/commits/{sha}/pulls"
    r = httpx.get(url, headers={**HEADERS, "Accept": "application/vnd.github.groot-preview+json"})
    r.raise_for_status()
    return r.json()

def get_pr_details(owner: str, repo: str, pr_number: int) -> dict:
    url = f"{GITHUB_API}/repos/{owner}/{repo}/pulls/{pr_number}"
    r = httpx.get(url, headers=HEADERS)
    r.raise_for_status()
    return r.json()

def get_ci_failures_for_pr(owner: str, repo: str, pr_number: int) -> int:
    # Simplified logic: you can improve by analyzing workflow runs via Actions API
    return 0

def get_review_latency_for_pr(owner: str, repo: str, pr_number: int) -> float:
    pr = get_pr_details(owner, repo, pr_number)
    created = datetime.fromisoformat(pr["created_at"].replace("Z", "+00:00"))
    reviewed = datetime.fromisoformat(pr["updated_at"].replace("Z", "+00:00"))
    return (reviewed - created).total_seconds() / 3600

async def get_incident_issues(owner: str, repo: str, since: str | None = None) -> list[dict]:
    params = {
        "labels": "bug",
        "state": "closed",
        "since": since,
        "per_page": 100,
    }
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"{GITHUB_API}/repos/{owner}/{repo}/issues",
            headers=HEADERS,
            params=params,
        )
        response.raise_for_status()
        return response.json()
