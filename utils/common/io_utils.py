import json, os

def dump_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def load_json(path):
    if not os.path.exists(path): return {}
    try:
        with open(path) as f:
            content = f.read().strip()
            return json.loads(content) if content else {}
    except Exception:
        return {}

def sanitize(obj):
    if isinstance(obj, set): return list(obj)
    if isinstance(obj, dict): return {k: sanitize(v) for k, v in obj.items()}
    if isinstance(obj, list): return [sanitize(v) for v in obj]
    return obj
