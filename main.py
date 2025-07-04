# main.py
from dotenv import load_dotenv
load_dotenv(override=True)

from bot.slack_bot import app, SLACK_APP_TOKEN

if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    print("Starting Slack bot...")
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
