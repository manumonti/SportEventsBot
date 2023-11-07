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
Sport events listing
"""

INFO_STATE, MODIFY_STATE = range(2)


async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    user = update.callback_query.from_user

    query = update.callback_query
    await query.delete_message()

    logger.info("User %s cancelled the listing of sport events", user.full_name)

    return ConversationHandler.END


async def list_sport_events(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    keyboard = [
        [
            InlineKeyboardButton(
                text="🏐 Vie 15/10 16:30 Volleyball Ilunion 3/6 👎",
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
        [
            InlineKeyboardButton(text="Cancelar", callback_data="cancel"),
        ],
    ]
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
            CallbackQueryHandler(event_info)
            ],
        # MODIFY_STATE: [
        # ]
    },
    fallbacks=[CallbackQueryHandler(cancel)],
)
