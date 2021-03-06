#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Base Program

Program is used to start up the telegram bot
"""

import logging
import os

import dotenv

from telegram.ext import (
    Updater,
    MessageHandler,
    CommandHandler,
    Dispatcher,
    PicklePersistence,
)

from arxiv_telegram_bot.functions.handlers import (
    start,
    fetch,
    preference_conversation_handler,
    error,
    schedule,
    unschedule,
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

    # Create the Updater and pass it your bot's token.
    persistence = PicklePersistence(filename="/tmp/arxivTelegramBot")
    updater = Updater(TOKEN, use_context=True, persistence=persistence)
    dispatcher: Dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("test", start))
    dispatcher.add_handler(CommandHandler("latest", fetch))
    dispatcher.add_handler(preference_conversation_handler())
    dispatcher.add_handler(CommandHandler("schedule", schedule))
    dispatcher.add_handler(CommandHandler("unschedule", unschedule))
    dispatcher.add_error_handler(error)

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
