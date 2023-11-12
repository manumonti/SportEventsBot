import logging
from datetime import datetime

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.constants import ParseMode
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
        "emoji": "🏐",
        "date": 1701448200,
        "place": "Ilunion",
        "min_players": 6,
        "players": ["Manu M", "Eugenia", "Laura"],
        "players_emoji": "👎",
    },
    {
        "id": 1,
        "type": "Football",
        "emoji": "⚽️",
        "date": 1701540000,
        "place": "Campito peq",
        "min_players": 12,
        "players": [
            "Laura",
            "María",
            "Manu M",
            "Eugenia",
            "Carlos",
            "Daniel",
            "Álvaro",
            "Miguel",
            "Benji",
            "Rafa",
        ],
        "players_emoji": "🤏",
    },
    {
        "id": 2,
        "type": "Karting",
        "emoji": "🏎️",
        "date": 1701597600,
        "place": "Campillos",
        "min_players": 6,
        "players": ["Rafa", "Benji", "Eugenia", "María", "Carlos", "Álvaro", "Miguel"],
        "players_emoji": "👍",
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
        date = datetime.fromtimestamp(event["date"]).strftime("%a %-d/%-m %-I:%M")

        text = (
            f"{event["emoji"]} {event["type"]} - {date} - {event["place"]} - "
            + f"{len(event["players"])}/{event["min_players"]} {event["players_emoji"]}"
        )
        keyboard.append([InlineKeyboardButton(text=text, callback_data=event["id"])])

    keyboard.append([InlineKeyboardButton(text="Cancelar", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Próximos eventos", reply_markup=reply_markup)

    return INFO_STATE


async def event_info(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("User %s requested info of %s", query.from_user.full_name, query.data)

    event = events[int(query.data)]

    date = datetime.fromtimestamp(event["date"]).strftime("%a %-d/%-m %-I:%M")

    text = (
        f"*{event["emoji"]} {event["type"]} {event["emoji"]}*\n"
        + f"📅 {date}\n"
        + f"📍 {event["place"]}\n"
        + f"👫 {len(event["players"])}/{event["min_players"]} "
        + f"{event["players_emoji"]}\n"
    )

    for player in event["players"]:
        text += f"  🏃 {player}\n"

    keyboard = [
        [
            InlineKeyboardButton(text="Modificar evento", callback_data="cancel"),
            InlineKeyboardButton(text="Apuntarme", callback_data="cancel"),
        ],
        [InlineKeyboardButton(text="Cancelar", callback_data="cancel")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(
        text=text, parse_mode=ParseMode.MARKDOWN_V2, reply_markup=reply_markup
    )

    return ConversationHandler.END


list_events_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("lista", list_sport_events)],
    states={
        INFO_STATE: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(event_info),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
