#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Arxiv Base Imports

All Imports Necessary for Arxiv Bot 
"""

# -- IMPORTS: LIBRARIES
# - Standard Library Imnports
import logging
import os
import re

# - DotENV
import dotenv

# - Telegram Imports
import telegram
from telegram import Update

# - Telegram Extended Imports
from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
    CallbackContext,
)

# - Custom Functions
from arxiv_telegram_bot.functions.fetch import fetch_latest_paper


# -- SETUP

# - Load DotENV
dotenv.load_dotenv()

# - Enable Logging
logger = logging.getLogger(__name__)


# -- CONSTANTS

# - Application Port
PORT = int(os.environ.get("PORT", 5000))

# - Application Token
TOKEN = dotenv.get_key(".env", "TOKEN")


# -- COMMAND HANDLERS

# - 'start' Command Handler
def start(update: Update, context: CallbackContext):
    """Send a message when the command 'start' is issued."""
    print(context._user_id_and_data[0])
    update.message.reply_text("Hi! Your userid")


# - 'uid' Command Handler
def uid(update: Update, context: CallbackContext):
    """Ping back the userid whose command created"""
    message_to_send = f"Your user ID is {context._user_id_and_data[0]}"
    print(message_to_send)
    update.message.reply_text(message_to_send)


# - 'fetch' Command Handler
def fetch(update: Update, context: CallbackContext):
    """Fetch the latest papers"""
    title, date, summary = fetch_latest_paper()
    escaper = re.compile(r"(\W)")
    title = escaper.sub(r"\\\1", title)
    date = escaper.sub(r"\\\1", date)
    summary = escaper.sub(r"\\\1", summary)
    message_to_send = f"*{title}*\n_{date}_\n\n{summary}"
    message_to_send.replace("-", "\\-")
    update.message.reply_text(
        message_to_send, parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


# - Error Handler
def error(update: Update, context: CallbackContext):
    logger.warning("Update %s caused error %s", update, context.error)


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

    # log all errors
    dp.add_error_handler(error)

    # Start the bot

    updater.start_polling()

    # Run bot until stopped
    updater.idle()
