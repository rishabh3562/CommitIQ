# from dotenv import load_dotenv
# load_dotenv(override=True)

from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from configs.constants import SLACK_BOT_TOKEN, SLACK_SIGNING_SECRET, SLACK_APP_TOKEN

app = App(
    token=SLACK_BOT_TOKEN,
    signing_secret=SLACK_SIGNING_SECRET,
)

socket_handler = SocketModeHandler(app, SLACK_APP_TOKEN)
