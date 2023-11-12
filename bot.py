import locale
import logging
import os

from dotenv import load_dotenv
from telegram.ext import ApplicationBuilder

from list_events import list_events_conv_handler
from new_event import new_event_conv_handler

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

# set time format to Spanish
locale.setlocale(locale.LC_TIME, "es_ES")

load_dotenv()
BOT_TOKEN = os.environ.get("BOT_TOKEN")
if BOT_TOKEN is None:
    raise AssertionError("BOT_TOKEN variable not found in .env file")


def main() -> None:
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    application.add_handler(new_event_conv_handler)
    application.add_handler(list_events_conv_handler)
    application.run_polling()


if __name__ == "__main__":
    main()
