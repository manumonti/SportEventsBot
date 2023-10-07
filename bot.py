import locale
import os

import pymongo
import telebot
from dotenv import load_dotenv

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    raise AssertionError("BOT_TOKEN variable not found in .env file")

# Show the dates in spanish format
locale.setlocale(locale.LC_TIME, "es_es")


"""
Database
"""


mongo_client = pymongo.MongoClient("mongodb://localhost:27017/")

"""
Bot
"""


tb = telebot.TeleBot(BOT_TOKEN)
tb.delete_my_commands()
tb.set_my_commands(
    commands=[telebot.types.BotCommand("new", "Create a new event")], language_code="en"
)
tb.set_my_commands(
    commands=[telebot.types.BotCommand("nuevo", "Crea un nuevo evento")],
    language_code="es",
)


@tb.message_handler(commands=["start"])
def send_welcome(message):
    db = mongo_client["SETG"]

    if message.chat.type == "group":
        if str(message.chat.id) not in db.list_collection_names():
            db[str(message.chat.id)].insert_one({"chatName": message.chat.title})

    tb.reply_to(message, "Bot para gestionar eventos")


"""
Event management
"""


@tb.message_handler(commands=["new", "nuevo"])
def new_event(message):
    tb.send_message(message.from_user.id, "Se ha seleccionado crear un nuevo evento", )

tb.infinity_polling()
