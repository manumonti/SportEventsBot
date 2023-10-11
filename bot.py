import logging
import os

from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    raise AssertionError("BOT_TOKEN variable not found in .env file")


"""
Sport events listing
"""


async def list_sport_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton(
                text="🏐 *Vie 15/10 16:30 Volleyball Ilunion 3/6* 👎",
                callback_data="15/10",
            )
        ],
        [
            InlineKeyboardButton(
                text="⚽️ Sáb 16/10 18:00 Football Cañadón 7/10 🤏",
                callback_data="16/10",
            )
        ],
        [
            InlineKeyboardButton(
                text="🏎️ Dom 17/10 09:00 Karting Campillos 11/6 👍",
                callback_data="17/10",
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Próximos eventos", reply_markup=reply_markup)

    return None


"""
Sport events creation
"""
# TODO: Delete /crear message when finishing the creation or when cancelling
TYPE_STATE, DATE_STATE, PLACE_STATE, MIN_PLAYERS_STATE = range(4)


async def new_sport_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started creating a new sport event", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton(text="Football", callback_data="football"),
            InlineKeyboardButton(text="Volleyball", callback_data="volleyball"),
            InlineKeyboardButton(text="Otro", callback_data="other"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Tipo de evento", reply_markup=reply_markup)

    return TYPE_STATE


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the creation of a new sport event", user.first_name)

    return ConversationHandler.END


async def event_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event type
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Hoy", callback_data="today"),
            InlineKeyboardButton(text="Mañana", callback_data="tomorrow"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Fecha", reply_markup=reply_markup)

    return DATE_STATE


async def event_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event date
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="Campito", callback_data="campito"),
            InlineKeyboardButton(text="Cañadón", callback_data="cañadon"),
        ],
        [
            InlineKeyboardButton(text="Ilunion", callback_data="ilunion"),
            InlineKeyboardButton(text="Otro", callback_data="ilunion"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Lugar", reply_markup=reply_markup)

    return PLACE_STATE


async def event_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event place
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton(text="4", callback_data="4"),
            InlineKeyboardButton(text="6", callback_data="6"),
            InlineKeyboardButton(text="10", callback_data="10"),
            InlineKeyboardButton(text="14", callback_data="14"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Mínimo de jugadores", reply_markup=reply_markup)

    return MIN_PLAYERS_STATE


async def event_min_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event min players
    # TODO: save the new event in DB
    user = update.callback_query.from_user

    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="Evento registrado!")

    logger.info("User %s created a new event", user.first_name)

    return ConversationHandler.END


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    new_sport_event_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("crear", new_sport_event)],
        states={
            TYPE_STATE: [
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(event_type),
            ],
            DATE_STATE: [
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(event_date),
            ],
            PLACE_STATE: [
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(event_place),
            ],
            MIN_PLAYERS_STATE: [
                CallbackQueryHandler(cancel, pattern="^cancel$"),
                CallbackQueryHandler(event_min_players),
            ],
        },
        fallbacks=[CallbackQueryHandler(cancel)],
    )

    list_sport_events_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("lista", list_sport_events)],
        states={},
        fallbacks=[CallbackQueryHandler(cancel)],
    )

    application.add_handler(new_sport_event_conv_handler)
    application.add_handler(list_sport_events_conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
