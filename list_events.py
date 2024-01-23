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

SELECTING_EVENT, DETAILING_EVENT = range(2)

events = [
    {
        "id": 0,
        "game": "🏐 Volleyball",
        "date": 1701448200,
        "place": "Ilunion",
        "players": ["Manu M", "Eugenia", "Laura"],
    },
    {
        "id": 1,
        "game": "⚽️ Football",
        "date": 1701540000,
        "place": "Campito peq",
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
    },
    {
        "id": 2,
        "game": "🏎️ Karting",
        "date": 1701597600,
        "place": "Campillos",
        "players": ["Rafa", "Benji", "Eugenia", "María", "Carlos", "Álvaro", "Miguel"],
    },
]


async def list_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s listed events", user.full_name)

    keyboard = []
    for event in events:
        date = datetime.fromtimestamp(event["date"]).strftime("%a %-d/%-m %-I:%M")
        text = (
            f"{event["game"]} - {event["place"]} - {date} - 👫 {len(event["players"])}"
        )
        keyboard.append([InlineKeyboardButton(text=text, callback_data=event["id"])])

    keyboard.append([InlineKeyboardButton(text="Cancelar", callback_data="cancel")])

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Próximos eventos", reply_markup=reply_markup)

    return SELECTING_EVENT


async def detail_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("User %s detailed event #%s", query.from_user.full_name, query.data)

    event = events[int(query.data)]

    date = datetime.fromtimestamp(event["date"]).strftime("%a %-d/%-m %-I:%M")
    text = (
        f"*{event["game"]}*\n"
        + f"📅 {date}\n"
        + f"📍 {event["place"]}\n"
        + f"👫 {len(event["players"])}\n"
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

    return DETAILING_EVENT


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the listing of sport events", user.full_name)

    return ConversationHandler.END


list_events_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("lista", list_events)],
    states={
        SELECTING_EVENT: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(detail_event),
        ],
        DETAILING_EVENT: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
        ]
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
