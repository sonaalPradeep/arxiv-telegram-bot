#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import os

import dotenv

from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
)

from arxiv_telegram_bot.functions.handlers import (
    start,
    uid,
    fetch,
    preference_conversation_handler,
    error,
)


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

dotenv.load_dotenv()
PORT = int(os.environ.get("PORT", 8443))
TOKEN = os.environ.get("TOKEN")
HEROKU_URL = os.environ.get("HEROKU_URL")


def main():
    """Start the bot."""

    updater = Updater(TOKEN, use_context=True)
    dp: Dispatcher = updater.dispatcher

    dp.add_handler(CommandHandler("test", start))
    dp.add_handler(CommandHandler("uid", uid))
    dp.add_handler(CommandHandler("latest", fetch))
    dp.add_handler(preference_conversation_handler())
    dp.add_error_handler(error)

    if os.environ.get("ENV") == "HEROKU":
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=f"{HEROKU_URL}/{TOKEN}",
        )
    else:
        updater.start_polling()

    updater.idle()
