import os
from slack_sdk.web import WebClient
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from dotenv import load_dotenv

load_dotenv(override=True)  
def run_demo_report() -> dict:
    return {
        "harvester": {
            "raw_commits": [],
            "pr_throughput": 9,
            "ci_failures": 0,
            "review_latency": 0.0,
            "cycle_time": 341.45
        },
        "analyst": {
            "author_stats": {
                "Samsondeen": {"commits": 2, "lines_added": 1343, "lines_deleted": 736, "files_touched": 23},
                "Daniel Banck": {"commits": 2, "lines_added": 973, "lines_deleted": 83, "files_touched": 35},
                "Mark DeCrane": {"commits": 3, "lines_added": 122, "lines_deleted": 12, "files_touched": 5},
                "hc-github-team-tf-core": {"commits": 1, "lines_added": 8, "lines_deleted": 2, "files_touched": 2},
                "Sarah French": {"commits": 1, "lines_added": 543, "lines_deleted": 158, "files_touched": 10}
            },
            "spikes": ["Samsondeen"]
        },
        "narrator": {
            "summary": (
                "\n\nThe engineering team had a high deployment frequency of 9, "
                "with a low change-fail rate of 0/9 and a relatively short lead time of 341.45 hours. "
                "However, the MTTR of 21.59 hours suggests some bottlenecks in issue resolution. "
                "The team also had a high number of commits and lines of code, with one spike from a specific member."
            ),
            "stats": {
                "stats": {
                    "Samsondeen": {"commits": 2, "spike": True},
                    "Daniel Banck": {"commits": 2, "spike": False},
                    "Mark DeCrane": {"commits": 3, "spike": False},
                    "hc-github-team-tf-core": {"commits": 1, "spike": False},
                    "Sarah French": {"commits": 1, "spike": False}
                },
                "pr_throughput": 9,
                "ci_failures": 0,
                "review_latency": 0.0,
                "cycle_time": 341.45,
                "spikes": ["Samsondeen"],
                "total_commits": 9,
                "lines_added": 2989,
                "lines_deleted": 991,
                "files_touched": 75,
                "mttr": 21.59
            }
        }
    }

def format_report_text(data: dict) -> str:
    stats = data["narrator"]["stats"]
    summary = data["narrator"]["summary"].strip()

    dora = (
        f"Deploy freq: {stats['pr_throughput']}  |  "
        f"Lead time: {stats['cycle_time']}h  |  "
        f"Fail rate: {stats['ci_failures']}/{stats['pr_throughput']}  |  "
        f"MTTR: {stats['mttr']}h"
    )
    code = (
        f"Commits: {stats['total_commits']}  |  "
        f"+{stats['lines_added']}/-{stats['lines_deleted']} lines  |  "
        f"{stats['files_touched']} files"
    )

    return f"{summary}\n\n*DORA Metrics:*\n{dora}\n*Code Stats:*\n{code}"

# CLI mode
if __name__ == "__main__":
    if os.getenv("RUN_MODE") == "cli":
        data = run_demo_report()
        print(format_report_text(data))
    else:
        pass  # Slack logic handled below

# Slack bot setup (executes only if RUN_MODE != cli)
app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/demo-dev-report")
def handle_demo_dev_report(ack, respond, command):
    ack()
    data = run_demo_report()
    message = format_report_text(data)
    respond(f"*🔎 Demo Developer Report:*\n```{message}```")

if os.getenv("RUN_MODE") != "cli":
    handler = SocketModeHandler(app, os.environ.get("SLACK_APP_TOKEN"))
    handler.start()
