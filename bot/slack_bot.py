import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")


app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET")
)


@app.command("/test")
def handle_test(ack, say, command):
    try:
        ack()
        say(f"✅ Bot is live!")
    except Exception as e:
        say(f"⚠️ Test command failed.\nError: `{str(e)}`")

@app.command("/explain-me")
def handle_explain(ack, say, command):
    try:
        ack()
        say(
            "*👋 Welcome to Dev Report Bot!*\n\n"
            "*What this bot does:*\n"
            "Provides weekly GitHub commit analysis, visual metrics, and DORA-based summaries.\n\n"
            "*Commands:*\n"
            "• `/dev-report owner repo` → Generate a dev report\n"
            "• `/test` → Check bot status\n"
            "• `/explain-me` → Help guide\n\n"
            "Output: stats, PNG graph, AI-generated summary.\n"
            "_Tip: Schedule this weekly._"
        )
    except Exception as e:
        say(f"⚠️ Failed to explain bot usage.\nError: `{str(e)}`")

@app.error
def handle_errors(error, body, logger):
    logger.error(f"Global error: {error}")

@app.event("app_mention")
def log_event(event, say):
    print("EVENT:", event)
    say("👀 Bot is alive and listening.")

if __name__ == "__main__":
    from dotenv import load_dotenv
    load_dotenv(override=True)
    print("Starting bot in Socket Mode...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
