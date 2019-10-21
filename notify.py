import os
import slack
import datetime
import time
import threading
from lunch import Lunch


class Notify:

    def __init__(self):
        self.slack_token = os.environ.get('SLACK_BOT_TOKEN')
        self.slack_client = slack.WebClient(self.slack_token)
        self.slack_channel = os.environ.get('SLACK_CHANNEL')
        self.current_hour = -1
        self.current_minute = -1
        self.target_hour = 20

    def notify_channel(self):
        print('Worker is running..., waiting till 11:00 ')
        # while True:
        #     curent_time = datetime.datetime.today().now()
        #     current_hour = curent_time.hour
        #     current_minute = curent_time.minute
        #     # print(curent_time)
        #     if current_hour - 9 > 0:
        #         sleep_time = 24 - current_hour + 9 - (current_minute / 60)
        #     elif current_hour - 9 < 0:
        #         sleep_time = 9 - current_hour - (current_minute / 60)
        #     elif current_hour == 9:
        #         if current_minute == 0:
        #             sleep_time = 0
        #         else:
        #             sleep_time = 24 - current_hour + 9 - (current_minute / 60)
        #     print('message sent for today-waiting till 11:00a.m next day')
        lunch = Lunch(self.slack_channel)

        if(lunch.getDayOfWeek() == None):  # weekends
            threading.Timer(3600, self.notify_channel).start()
            return
        postmessage = lunch.get_message_payload()
        self.slack_client.chat_postMessage(**postmessage)
        threading.Timer(5, self.notify_channel).start()
