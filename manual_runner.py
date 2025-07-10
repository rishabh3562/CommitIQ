# manual_runner.py
import asyncio, os
from datetime import datetime, timedelta, timezone
from workflow.parallel_flow_v2 import build_graph_parallel_v2
from schemas.parallel_workflow_state import ParallelWorkflowStateV2 as State
from utils.common.io_utils import dump_json, load_json, sanitize

async def run_manual_test():
    print("Running manual test for v2 flow...")
    graph = build_graph_parallel_v2(State)
    now = datetime.now(timezone.utc).replace(microsecond=0)
    one_week_ago=now - timedelta(days=7)
    one_month_ago=now -timedelta(days=30)
    inputs = {
        "owner": "vercel", "repo": "next.js",
        "since": (one_week_ago).isoformat().replace("+00:00", "Z"),
        "until": now.isoformat().replace("+00:00", "Z"),
    }

    result = await graph.ainvoke(inputs)
    logs = load_json("logs/results.json")
    logs[f"run_{now.strftime('%Y-%m-%d_%H-%M-%S')}"] = sanitize(result)
    dump_json("logs/results.json", logs)
    print("✅ Saved to logs/results.json")

if __name__ == "__main__":
    asyncio.run(run_manual_test())
