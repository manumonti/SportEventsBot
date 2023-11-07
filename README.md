# Sport Events Telegram Bot

![](https://i.imgur.com/Qcjs0fA.png)

A Telegram bot to track and manage the sport events organized by your social group. Create new
football or volleyball matches. Tell your friends to join them and keep track of the date, place
and who goes.

## Features

- Creation/cancellation of events [TBD]
- Users join/sign out events [TBD]
- Logs are shown in chats (users join, events created...) [TBD]
- Automatic reminders before the event [TBD]
- Management of Google calendar [TBD]

## Installation

A running MongoDB server is needed:

https://www.mongodb.com/try/download/community

Also, it is needed to have your own Telegram Bot Token:

[Obtain Your Bot Token](https://core.telegram.org/bots/tutorial#obtain-your-bot-token)

You can set the Telegram token by setting it in .env file:

```dotenv
BOT_TOKEN=<TG_BOT_TOKEN>
```

Install the requirements packages:

```bash
pip install -r requirements.txt
```

### Running the Bot

You have to be running the bot code:

```bash
python bot.py
```

## Contribution

`pre-commit` is enabled in this repo. Please, run:

```bash
pre-commit install
```
