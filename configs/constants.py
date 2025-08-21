from dotenv import load_dotenv
import os

load_dotenv()
CONCURRENT_WORKERS = 5  # Change as needed
DATA_SHARDS = CONCURRENT_WORKERS
CHURN_LIMIT = 1000
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO="rishabh3562/PromptOps"
USE_FAKE_DATA = os.getenv("USE_FAKE_DATA", "False").lower() == "true"

FLOW_VERSION = os.getenv("FLOW_VERSION", "none").lower()  # Set to 'v1', 'v2', 'v3', or 'none'
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
SLACK_USER_OAUTH_TOKEN = os.getenv("SLACK_USER_OAUTH_TOKEN")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# LangSmith Configuration
LANGSMITH_TRACING = os.getenv("LANGSMITH_TRACING", "false").lower() == "true"
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT", "commitiq-productivity")
