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
Sport events creation
"""
# TODO: Delete /crear message when finishing the creation or when cancelling
TYPE_STATE, DATE_STATE, PLACE_STATE, MIN_PLAYERS_STATE = range(4)


async def new_sport_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started creating a new sport event", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Football", callback_data="football"),
            InlineKeyboardButton("Volleyball", callback_data="volleyball"),
            InlineKeyboardButton("Otro", callback_data="other"),
        ],
        [
            InlineKeyboardButton("Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Tipo de evento", reply_markup=reply_markup)

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
            InlineKeyboardButton("Hoy", callback_data="today"),
            InlineKeyboardButton("Mañana", callback_data="tomorrow"),
        ],
        [
            InlineKeyboardButton("Cancelar", callback_data="cancel"),
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
            InlineKeyboardButton("Campito", callback_data="campito"),
            InlineKeyboardButton("Cañadón", callback_data="cañadon"),
        ],
        [
            InlineKeyboardButton("Ilunion", callback_data="ilunion"),
            InlineKeyboardButton("Otro", callback_data="ilunion"),
        ],
        [
            InlineKeyboardButton("Cancelar", callback_data="cancel"),
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
            InlineKeyboardButton("4", callback_data="4"),
            InlineKeyboardButton("6", callback_data="6"),
            InlineKeyboardButton("10", callback_data="10"),
            InlineKeyboardButton("14", callback_data="14"),
        ],
        [
            InlineKeyboardButton("Cancelar", callback_data="cancel"),
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

    application.add_handler(new_sport_event_conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
