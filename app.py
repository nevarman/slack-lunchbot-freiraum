import os
import logging
import slack
import ssl as ssl_lib
import certifi
from lunch import Lunch
from boto.s3.connection import S3Connection

# For simplicity we'll store our app data in-memory with the following data structure.
#onboarding_tutorials_sent = {"channel": {"user_id": Lunch}}
onboarding_tutorials_sent = {}


def show_lunch(web_client: slack.WebClient, user_id: str, channel: str):
    # Create a new onboarding tutorial.
    lunch = Lunch(channel)

    # Get the lunch message payload
    message = lunch.get_message_payload()

    # Post the onboarding message in Slack
    response = web_client.chat_postMessage(**message)

    # Capture the timestamp of the message we've just posted so
    # we can use it to update the message after a user
    # has completed an onboarding task.
    lunch.timestamp = response["ts"]

    # Store the message sent in onboarding_tutorials_sent
    if channel not in onboarding_tutorials_sent:
        onboarding_tutorials_sent[channel] = {}
    onboarding_tutorials_sent[channel][user_id] = lunch

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
    slack_token = os.environ.get('SLACK_BOT_TOKEN')
    rtm_client = slack.RTMClient(token=slack_token)
    rtm_client.start()
