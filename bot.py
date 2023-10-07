import locale
import os

import pymongo
import telebot
from telebot.util import quick_markup
from telebot.callback_data import CallbackData
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
bot = telebot.TeleBot(BOT_TOKEN)
bot.delete_my_commands()
bot.set_my_commands(
    commands=[telebot.types.BotCommand("nuevo", "Crea un nuevo evento")]
)


@bot.message_handler(commands=["start"])
def send_welcome(message):
    db = mongo_client["sportEventsBot"]

    if message.chat.type == "group":
        if str(message.chat.id) not in db.list_collection_names():
            db[str(message.chat.id)].insert_one({"chatName": message.chat.title})

    bot.reply_to(message, "Bot para gestionar eventos")


"""
Create a new sport event
"""
event_type_cb_data_factory = CallbackData("event_type", prefix="event_type")

event_type_markup = {
    "Football": {
        "callback_data": event_type_cb_data_factory.new(event_type="football")
    },
    "Volleyball": {
        "callback_data": event_type_cb_data_factory.new(event_type="volleyball")
    },
    "Otro": {"callback_data": event_type_cb_data_factory.new(event_type="other")},
    "Cancelar": {"callback_data": "cancel"},
}

date_markup = {
    "Hoy": {"callback_data": "date_today"},
    "Mañana": {"callback_data": "date_tomorrow"},
    "Cancelar": {"callback_data": "cancel"},
}


@bot.callback_query_handler(func=lambda call: call.data == "cancel")
def callback_cancel(call):
    bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.message_id)


@bot.callback_query_handler(func=lambda call: call.data.startswith("event_type"))
def callback_event_type(call):
    cb_data = event_type_cb_data_factory.parse(callback_data=call.data)
    if cb_data["event_type"] == "football":
        bot.answer_callback_query(call.id, "Aún no implementado")
        print("football")
    elif cb_data["event_type"] == "volleyball":
        bot.answer_callback_query(call.id, "Aún no implementado")
        print("volleyball")
    elif cb_data["event_type"] == "other":
        bot.answer_callback_query(call.id, "Aún no implementado")
        print("other")

    bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text="Fecha",
        reply_markup=quick_markup(values=date_markup, row_width=2),
    )


@bot.message_handler(commands=["nuevo"])
def new_event_handler(message):
    bot.send_message(
        chat_id=message.chat.id,
        text="*Nuevo evento*",
        parse_mode="Markdown",
        reply_markup=quick_markup(values=event_type_markup, row_width=3),
    )
    bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)


bot.infinity_polling()
