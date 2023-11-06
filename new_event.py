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

TYPE_STATE, DATE_STATE, PLACE_STATE, MIN_PLAYERS_STATE = range(4)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the creation of a new sport event", user.full_name)

    return ConversationHandler.END


async def new_event(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.message.from_user
    logger.info("User %s started creating a new sport event", user.full_name)
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


async def event_type(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event type
    query = update.callback_query
    await query.answer()
    logger.info("User %s selected %s event type", query.from_user.full_name, query.data)
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
    logger.info("User %s selected %s event date", query.from_user.full_name, query.data)
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
    logger.info(
        "User %s selected %s event place", query.from_user.full_name, query.data
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

    return MIN_PLAYERS_STATE


async def event_min_players(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    # TODO: save the event min players
    # TODO: save the new event in DB
    user = update.callback_query.from_user

    query = update.callback_query
    await query.answer()
    logger.info(
        "User %s selected %s as event min players",
        query.from_user.full_name,
        query.data,
    )

    await query.edit_message_text(text="Se ha creado el evento!")

    logger.info("User %s created a new event", user.full_name)

    return ConversationHandler.END


new_event_conv_handler = ConversationHandler(
    entry_points=[CommandHandler("crear", new_event)],
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
