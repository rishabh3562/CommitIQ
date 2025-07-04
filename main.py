# main.py
from dotenv import load_dotenv
load_dotenv(override=True)

from configs.slack import socket_handler
from bot.slack_bot import app  # Ensure this only registers commands/events, not starts anything

if __name__ == "__main__":
    print("Starting Slack bot...")
    socket_handler.start()
