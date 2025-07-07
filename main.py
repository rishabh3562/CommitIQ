from schemas.State import State
from graph_builder import build_graph
from datetime import datetime, timedelta, timezone
import os, json
import asyncio

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
    except (json.JSONDecodeError, OSError) as e:
        print(f"[WARN] Could not load existing logs: {e}")
        return {}

def save_logs(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[ERROR] Failed to write logs: {e}")

async def main():
    print("Building the graph...")
    graph = build_graph(State)

    now = datetime.now(timezone.utc).replace(microsecond=0)
    one_week_ago = now - timedelta(weeks=1)

    inputs = {
        "owner": "vercel",
        "repo": "next.js",
        "since": one_week_ago.isoformat().replace("+00:00", "Z"),
        "until": now.isoformat().replace("+00:00", "Z"),
    }

    result = await graph.ainvoke(inputs)
    print("Result generated")

    os.makedirs("logs", exist_ok=True)
    log_path = "logs/results.json"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_key = f"run_{timestamp}"

    logs = load_existing_logs(log_path)
    logs[log_key] = sanitize(result)
    save_logs(log_path, logs)
    print(f"Saved under key '{log_key}' in {log_path}")

if __name__ == "__main__":
    asyncio.run(main())
