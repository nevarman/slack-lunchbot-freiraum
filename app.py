import os
import logging
import slack
from lunch import Lunch
from notify import Notify


def show_lunch(web_client: slack.WebClient, user_id: str, channel: str):
    lunch = Lunch(channel)
    # Get the lunch message payload
    postmessage = lunch.get_message_payload()
    # Post the lunch message in Slack
    web_client.chat_postMessage(**postmessage)

# ============== Message Events ============= #
# When a user sends a DM, the event type will be 'message'.
# Here we'll link the message callback to the 'message' event.
@slack.RTMClient.run_on(event="message")
def message(**payload):
    """Display the onboarding welcome message after receiving a message
    that contains "start".
    """
    data = payload["data"]
    web_client = payload["web_client"]
    channel_id = data.get("channel")
    user_id = data.get("user")
    text = data.get("text")
    if text and text.lower() == "lunch" or text.lower() == ":pretzel:":
        return show_lunch(web_client, user_id, channel_id)


if __name__ == "__main__":
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    logger.addHandler(logging.StreamHandler())
    # notify
    notify = Notify()
    notify.notify_channel()
    # rtm client
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
