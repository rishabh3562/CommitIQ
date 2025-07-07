# main.py
from dotenv import load_dotenv
load_dotenv(override=True)

import os
import asyncio

# CONFIG
FLOW_VERSION = os.getenv("FLOW_VERSION", "v2")  # Options: v1, v2, etc.

# ---- V1 Slack Bot  ----
if FLOW_VERSION == "v1":
    from configs.slack import socket_handler
    from bot.slack_bot import app

    if __name__ == "__main__":
        print("Starting Slack bot (v1)...")
        socket_handler.start()

# ---- V2 Parallel Flow (default)----
elif FLOW_VERSION == "v2":
    from schemas.parallel_workflow_state import ParallelWorkflowStateV2 as State
    from workflow.parallel_flow_v2 import build_graph_parallel_v2  # or graph_builder if not renamed
    from datetime import datetime, timedelta, timezone
    import json

    def sanitize(obj):
        if isinstance(obj, set):
            return list(obj)
        elif isinstance(obj, dict):
            return {k: sanitize(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [sanitize(v) for v in obj]
        else:
            return obj

    def load_existing_logs(path):
        if not os.path.exists(path):
            return {}
        try:
            with open(path, "r") as f:
                content = f.read().strip()
                return json.loads(content) if content else {}
        except Exception:
            return {}

    def save_logs(path, data):
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    async def main():
        print("Running parallel flow v2...")
        graph = build_graph_parallel_v2(State)

        now = datetime.now(timezone.utc).replace(microsecond=0)
        one_month_ago = now - timedelta(days=30)
        inputs = {
            "owner": "rishabh3562",
            "repo": "PromptOps",
            "since": one_month_ago.isoformat().replace("+00:00", "Z"),
            "until": now.isoformat().replace("+00:00", "Z"),
        }

        result = await graph.ainvoke(inputs)
        os.makedirs("logs", exist_ok=True)
        logs = load_existing_logs("logs/results.json")
        log_key = f"run_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}"
        logs[log_key] = sanitize(result)
        save_logs("logs/results.json", logs)
        print(f"Saved to logs/results.json as '{log_key}'")

    if __name__ == "__main__":
        asyncio.run(main())
