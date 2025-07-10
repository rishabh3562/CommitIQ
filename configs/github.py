from configs.constants import GITHUB_TOKEN, USE_FAKE_DATA
import os
from dotenv import load_dotenv
load_dotenv(override=True)  # ensure this runs before using the token

token = os.getenv("GITHUB_TOKEN")
if not token:
    raise ValueError("Missing GITHUB_TOKEN in environment")

HEADERS = {
    "Authorization": f"Bearer {token}",
    "Accept": "application/vnd.github+json"
}

API_BASE = "https://api.github.com"
