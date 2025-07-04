from dateutil.parser import parse as dt_parse
from datetime import datetime, timedelta
from utils.logger import logger
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

def slack_progress_message(prefix: str, count: int, time_per_commit: float = 0.2):
    est_time = round(count * time_per_commit, 1)
    if est_time > 10:
        msg = (
            # f"{prefix} Retrieved {count} commits.\n"
            "🟡 This might take a while... grab a coffee or go for a walk."
        )
    else:
        msg = f"{prefix} Retrieved {count} commits. ⏳ Estimated time: {est_time} min."
    logger.log(msg)
