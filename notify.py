import os
import slack
import datetime
import time
from lunch import Lunch


class Notify:

    def __init__(self):
        self.slack_token = os.environ.get('SLACK_BOT_TOKEN')
        self.slack_client = slack.WebClient(self.slack_token)
        self.slack_channel = os.environ.get('SLACK_CHANNEL')
        self.lunch = None

    def notify_channel(self):
        print('Worker is running..., waiting till 11:00 ')
        while True:
            curent_time = datetime.datetime.today().now()
            current_hour = curent_time.hour
            current_minute = curent_time.minute
            print(current_hour + ':'+current_minute)
            if current_hour - 11 > 0:
                sleep_time = 24 - current_hour + 11 - (current_minute / 60)
            elif current_hour - 11 < 0:
                sleep_time = 11 - current_hour - (current_minute / 60)
            elif current_hour == 11:
                if current_minute == 0:
                    sleep_time = 0
                else:
                    sleep_time = 24 - current_hour + 11 - (current_minute / 60)
            print('message sent for today-waiting till 11:00a.m next day')
            if(self.lunch is None):
                self.lunch = Lunch(self.slack_channel)
                postmessage = self.lunch.get_auto_message_payload()
            print(postmessage)
            self.slack_client.chat_postMessage(**postmessage)
            # time.sleep(sleep_time * 3600)
            time.sleep(10)
