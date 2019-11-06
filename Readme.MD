# Slack Lunch Bot

This repo contains a slack lunch bot for Freiraum restaurant located at Garching where I work: <https://www.freiraum.rest/garching/inforaum>

- Parses the html page where lunch and salat menu is presented.
- Posts a notification daily at 10am (11am in summer time xD). Except weekends and holidays.
- Responds to 'lunch' or ':pretzel:'.

## How to run

- Add your slack token as environment key 'SLACK_BOT_TOKEN'
- Add your channel name as environment key 'SLACK_CHANNEL'
- Run requirements.txt with pip
- Finally run app.py (see Procfile for heroku)

Currently hosted on [Heroku](https://dashboard.heroku.com/), but could be hosted anywhere, even locally.
