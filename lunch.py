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
    FOOTER_BLOCK = {"type": "context", "elements": [
        {"type": "mrkdwn", "text": ":information_source: *<https://www.freiraum.rest/garching/inforaum"
         "|Source>*"}]}
    ERROR_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                ":confused: Whopps, something went terribly wrong! :confused:\n"
            ),
        },
    }

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
        week_strings: list
        for ul in uls:
            dayOfWeek = (ul.find("li", class_="day_of_the_week", text=day))
            if(dayOfWeek):
                trenners = ul.find_all("li", class_="meal-trenner")
                for trenner in trenners:
                    trenner.insert(1, "---------")
                week_strings = list(ul.stripped_strings)
                week_strings[0] = "Freiraum Mittags Menu für " + \
                    week_strings[0]
                week_strings.insert(1, "---------")

        # salat plan
        salatplan = soup.find('div', id="salatplan")
        salat_strings: list
        uls = salatplan.find_all("ul")
        for ul in uls:
            dayOfWeek = (ul.find("li", class_="day_of_the_week", text=day))
            if(dayOfWeek):
                trenners = ul.find_all("li", class_="salat-trenner")
                for trenner in trenners:
                    trenner.insert(1, "---------")
                salat_strings = list(ul.stripped_strings)
                salat_strings[0] = "Salatkarte " + \
                    salat_strings[0]
                salat_strings.insert(1, "---------")

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
        text = []
        isSeperator = True
        mainDish = ""
        blockString = ""
        if(len(strings) == 0):
            text.append(self.ERROR_BLOCK)
            return text
        for string in strings:
            if(string != "---------"):
                if(isSeperator):
                    mainDish = string
                    isSeperator = False
                else:
                    blockString += string + " "
            else:
                isSeperator = True
                if(self.getDayOfWeek() in mainDish):  # check if header
                    text.append(self._get_header_block(mainDish))
                else:
                    text.append(self._get_lunch_block(mainDish))  # maindish
                if(len(blockString) > 0):
                    text.append(self._get_lunchcontext_block(blockString))
                else:
                    text.append(self.DIVIDER_BLOCK)
                blockString = ""
                mainDish = ""
        text.append(self.DIVIDER_BLOCK)
        text.append(self.FOOTER_BLOCK)
        return text

    @staticmethod
    def _get_header_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": "*"+text+"*"}}

    @staticmethod
    def _get_lunch_block(text):
        return {"type": "section", "text": {"type": "mrkdwn", "text": "*<https://www.google.com/search?q="+text+"|"+text+">*"}}

    @staticmethod
    def _get_lunchcontext_block(text):
        return {
            "type": "context", "elements": [{"type": "mrkdwn", "text": ":pushpin: " + "_"+text+"_"}]}
