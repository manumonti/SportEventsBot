import logging
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

logger = logging.getLogger(__name__)

"""
Sport events listing
"""

INFO_STATE, MODIFY_STATE = range(2)

events = [
    {
        "id": 0,
        "type": "Volleyball",
        "date": 1701448200,
        "place": "Ilunion",
        "min_players": 6,
        "players": 3,
        "emoji": "🏐",
    },
    {
        "id": 1,
        "type": "Football",
        "date": 1701540000,
        "place": "Campito peq",
        "min_players": 12,
        "players": 10,
        "emoji": "⚽️",
    },
    {
        "id": 2,
        "type": "Karting",
        "date": 1701597600,
        "place": "Campillos",
        "min_players": 6,
        "players": 11,
        "emoji": "🏎️",
    },
]


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the listing of sport events", user.full_name)

    return ConversationHandler.END


async def list_sport_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = []

    for event in events:
        if event["players"] >= event["min_players"]:
            players_emoji = "👍"
        elif event["players"] >= event["min_players"] - 2:
            players_emoji = "🤏"
        else:
            players_emoji = "👎"

        date = datetime.fromtimestamp(event["date"]).strftime("%a %-d/%-m %-I:%M")

        text = (
            f"{event["emoji"]} {event["type"]} - {date} - {event["place"]} - "
            + f"{event["players"]}/{event["min_players"]} {players_emoji}"
        )
        keyboard.append([InlineKeyboardButton(text=text, callback_data=event["id"])])

    (keyboard.append([InlineKeyboardButton(text="Cancelar", callback_data="cancel")]),)

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Próximos eventos", reply_markup=reply_markup)

    return INFO_STATE


async def event_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("User %s requested info of %s", query.from_user.full_name, query.data)

    await query.delete_message()

    return ConversationHandler.END


list_events_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("lista", list_sport_events)],
    states={
        INFO_STATE: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(event_info),
        ],
        # MODIFY_STATE: [
        # ]
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
