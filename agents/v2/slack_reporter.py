### agents/slack_reporter.py
### agents/slack_reporter.py
def send_to_slack(message: str):
    print("[SLACK] " + message)  # Replace with real Slack API call later

def slack_reporter(state):
    send_to_slack("Insights:\n" + "\n".join(state.get("insights", [])))
    return {}
