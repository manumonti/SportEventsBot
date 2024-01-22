import logging

from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

logger = logging.getLogger(__name__)

"""
Sport events creation
"""

SELECTING_GAME, SELECTING_DATE, SELECTING_PLACE, SELECTING_PLAYERS = range(4)


async def select_game(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    user = update.message.from_user
    logger.info("User %s started creating a new sport event", user.full_name)

    keyboard = [
        [
            InlineKeyboardButton(text="Football", callback_data="football"),
            InlineKeyboardButton(text="Volleyball", callback_data="volleyball"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(text="Tipo de evento", reply_markup=reply_markup)

    return SELECTING_GAME


async def select_date(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:

    query = update.callback_query
    await query.answer()
    logger.info("User %s selected %s game", query.from_user.full_name, query.data)

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

    return SELECTING_DATE


async def select_place(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info("User %s selected %s date", query.from_user.full_name, query.data)
    keyboard = [
        [
            InlineKeyboardButton(text="Campito", callback_data="campito"),
            InlineKeyboardButton(text="Cañadón", callback_data="cañadon"),
        ],
        [
            InlineKeyboardButton(text="Ilunion", callback_data="ilunion"),
        ],
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.edit_message_text(text="Lugar", reply_markup=reply_markup)

    return SELECTING_PLACE





async def select_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info(
        "User %s selected %s place", query.from_user.full_name, query.data
    )
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

    return SELECTING_PLAYERS


async def save(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    query = update.callback_query
    await query.answer()
    logger.info(
        "User %s selected %s min players", query.from_user.full_name, query.data
    )
    logger.info("User %s created a new event", query.from_user.full_name)

    # TODO: save the new event data

    await query.edit_message_text(text="Se ha creado un nuevo evento!")

    return ConversationHandler.END


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the creation of a new sport event", user.full_name)

    return ConversationHandler.END


new_event_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("crear", select_game)],
    states={
        SELECTING_GAME: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(select_date),
        ],
        SELECTING_DATE: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(select_place),
        ],
        SELECTING_PLACE: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(select_players),
        ],
        SELECTING_PLAYERS: [
            CallbackQueryHandler(cancel, pattern="^cancel$"),
            CallbackQueryHandler(save),
        ],
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
