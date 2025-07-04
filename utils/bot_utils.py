from dateutil.parser import parse as dt_parse
from datetime import datetime, timedelta
def parse_flags(flags_text):
    opts = {"period": "weekly", "graph": True, "from": None, "to": None}
    tokens = flags_text.strip().split()

    for i, token in enumerate(tokens):
        if token == "--monthly":
            opts["period"] = "monthly"
        elif token == "--weekly":
            opts["period"] = "weekly"
        elif token in ("--not-graph", "--no-graph"):
            opts["graph"] = False
        elif token == "--from" and i + 1 < len(tokens):
            opts["from"] = tokens[i + 1]
        elif token == "--to" and i + 1 < len(tokens):
            opts["to"] = tokens[i + 1]
        elif token == "--help":
            opts["help"] = True
        elif token == "--yesterday":
            y = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
            opts["from"] = y
            opts["to"] = y
        elif token == "--today":
            t = datetime.now().strftime("%Y-%m-%d")
            opts["from"] = t
            opts["to"] = datetime.now().isoformat()  # up to now

    return opts
