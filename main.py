from dotenv import load_dotenv; load_dotenv(override=True)
import os

# Initialize LangSmith safely before importing other modules
from utils.common.langsmith_setup import setup_langsmith
setup_langsmith()

version = os.getenv("FLOW_VERSION", "v2")

if version == "v1":
    from bot.slack_bot_v1 import run_v1
    run_v1()

elif version == "v2":
    from bot.slack_bot_v2 import run_v2
    run_v2()
