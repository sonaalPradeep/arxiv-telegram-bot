#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Arxiv Base Imports

All Imports Necessary for Arxiv Bot 
"""

# -- IMPORTS: LIBRARIES
# - Standard Library Imports
import logging
import os

# - DotENV
import dotenv

# - Telegram Extended Imports
from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
)

# - Custom Functions
from arxiv_telegram_bot.functions.handlers import (
    start,
    uid,
    fetch,
    preference_conversation_handler,
    error,
)

# -- SETUP

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# - Load DotENV
dotenv.load_dotenv()

# - Enable Logging
logger = logging.getLogger(__name__)


# - Application Port
PORT = int(os.environ.get("PORT", 8443))

# - Application Token
TOKEN = os.environ.get("TOKEN")

HEROKU_URL = os.environ.get("HEROKU_URL")


# -- MAIN FUNCTION
def main():
    """Start the bot."""

    # Create Updater and pass it the bot's token
    updater = Updater(TOKEN, use_context=True)

    # Get dispatcher to register handlers

    dp: Dispatcher = updater.dispatcher

    # Test Ping
    dp.add_handler(CommandHandler("test", start))

    # Test UID Ping
    dp.add_handler(CommandHandler("uid", uid))

    # Send the latest paper
    dp.add_handler(CommandHandler("latest", fetch))

    dp.add_handler(preference_conversation_handler())

    # log all errors
    dp.add_error_handler(error)

    # Start the bot
    if os.environ.get("ENV") == "HEROKU":
        updater.start_webhook(
            listen="0.0.0.0",
            port=int(PORT),
            url_path=TOKEN,
            webhook_url=f"{HEROKU_URL}/{TOKEN}",
        )
    else:
        updater.start_polling()

    # Run bot until stopped
    updater.idle()
