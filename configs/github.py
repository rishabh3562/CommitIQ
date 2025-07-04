from configs.constants import GITHUB_TOKEN, USE_FAKE_DATA

HEADERS = {
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "Accept": "application/vnd.github+json"
}
API_BASE = "https://api.github.com"
