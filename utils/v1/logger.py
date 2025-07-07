import logging
from typing import Optional

class SlackLogger:
    def __init__(self):
        self.slack_log_func = None

    def set_slack_logger(self, func):
        self.slack_log_func = func
    
    def terminal_log(self, msg, **kwargs):
        if kwargs:
            print(f"{msg} | {kwargs}")
        else:
            print(msg)

    def log(self, msg, **kwargs):
        self.terminal_log(msg, **kwargs)  # Reuse logic
        if self.slack_log_func:
            try:
                self.slack_log_func(f"{msg} | {kwargs}" if kwargs else msg)
            except Exception as e:
                print(f"[LOGGER ERROR] Failed to send to Slack: {e}")

logger = SlackLogger()
