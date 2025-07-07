import httpx
from slack_sdk.errors import SlackApiError
import time

def safe_slack_call(func, retries=3, delay=1, **kwargs):
    for attempt in range(retries):
        try:
            return func(**kwargs)
        except (httpx.HTTPError, SlackApiError) as e:
            if attempt < retries - 1:
                time.sleep(delay)
                continue
            raise
