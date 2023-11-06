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

from new_event import new_event_conv_handler

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

    return None


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    list_sport_events_conv_handler = ConversationHandler(
        entry_points=[CommandHandler("lista", list_sport_events)],
        states={},
        fallbacks=[CallbackQueryHandler(None)],
    )

    application.add_handler(new_event_conv_handler)
    application.add_handler(list_sport_events_conv_handler)

    application.run_polling()


if __name__ == "__main__":
    main()
