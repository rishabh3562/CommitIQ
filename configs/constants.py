from dotenv import load_dotenv
import os

load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
USE_FAKE_DATA = os.getenv("USE_FAKE_DATA", "False").lower() == "true"

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_USER_OAUTH_TOKEN = os.getenv("SLACK_USER_OAUTH_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
# LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")
# LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
# LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")
