#! /usr/bin/env python
import datetime
import io
try:
    # For Python 3.0 and later
    from urllib.request import urlopen
except ImportError:
    # Fall back to Python 2's urllib2
    from urllib2 import urlopen
from bs4 import BeautifulSoup


class Lunch:

    WELCOME_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                ":beer: Mahlzeit!! :pretzel: :yum:\n\n"
            ),
        },
    }
    DIVIDER_BLOCK = {"type": "divider"}

    def __init__(self, channel):
        self.channel = channel
        self.username = "lunchbot"
        self.icon_emoji = ":robot_face:"
        self.timestamp = ""
        self.reaction_task_completed = False
        self.pin_task_completed = False
        self.strings = None

    def getDayOfWeek(self):
        weekday = datetime.datetime.today().weekday()
        if weekday == 0:
            return "Montag"
        elif weekday == 1:
            return "Dienstag"
        elif weekday == 2:
            return "Mittwoch"
        elif weekday == 3:
            return "Donnerstag"
        elif weekday == 4:
            return "Freitag"

        return None

    def scrapFreiraum(self):
        html = urlopen("https://www.freiraum.rest/garching/inforaum").read()
        soup = BeautifulSoup(html, 'html.parser')
        day = self.getDayOfWeek()
        # weekplan
        weekplan = soup.find('div', id="weekplan")
        uls = weekplan.find_all("ul")
        week_strings : list
        for ul in uls:
            dayOfWeek = (ul.find("li", class_="day_of_the_week", text=day))
            if(dayOfWeek):
                trenners = ul.find_all("li", class_="meal-trenner")
                for trenner in trenners:
                    trenner.insert(1, "---------")
                week_strings = list(ul.stripped_strings)
                week_strings[0] = "*Freiraum Mittags Menu für " + \
                    week_strings[0] + "*\n"
                #return strings

        # salat plan
        salatplan = soup.find('div', id="salatplan")
        salat_strings : list
        uls = salatplan.find_all("ul")
        for ul in uls:
            dayOfWeek = (ul.find("li", class_="day_of_the_week", text=day))
            if(dayOfWeek):
                trenners = ul.find_all("li", class_="salat-trenner")
                for trenner in trenners:
                    trenner.insert(1, "---------")
                salat_strings = list(ul.stripped_strings)
                salat_strings[0] = "*Salatkarte" + \
                    salat_strings[0] + "*\n"

        return week_strings + salat_strings

    def get_message_payload(self):
        self.strings = self.scrapFreiraum()
        return {
            "ts": self.timestamp,
            "channel": self.channel,
            "username": self.username,
            "icon_emoji": self.icon_emoji,
            "blocks": [
                self.WELCOME_BLOCK,
                self.DIVIDER_BLOCK,
                *self._get_content_block(self.strings),
            ],
        }

    def _get_content_block(self, strings):
        text = ""
        for string in strings:
            text += string + "\n"
        return self._get_block(text)

    @staticmethod
    def _get_block(text):
        return [
            {"type": "section", "text": {"type": "mrkdwn", "text": text}},
            {"type": "context", "elements": [
                {"type": "mrkdwn", "text": ":information_source: *<https://www.freiraum.rest/garching/inforaum"
                 "|Source>*"}]},
        ]
