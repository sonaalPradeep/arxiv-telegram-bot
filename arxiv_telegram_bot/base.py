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
PORT = int(os.environ.get("PORT", 8443))

# - Application Token
TOKEN = os.environ.get("TOKEN")

HEROKU_URL = os.environ.get("HEROKU_URL")


# -- COMMAND HANDLERS

# - 'start' Command Handler
def start(update: Update, context: CallbackContext):
    """Send a message when the command 'start' is issued."""
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
    context.bot.send_chat_action(
        chat_id=update.message.chat_id, action=telegram.ChatAction.TYPING
    )

    title, date, summary, categories, abs_url, pdf_url = fetch_latest_paper()
    message_to_send = f"""
*{title}* \(_{categories}_\)\n
Publication Date: _{date}_\n\n
{summary}\n
    
[Click here to open the Arxiv page]({abs_url})
[Click here to open the PDF]({pdf_url})"""

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
    updater.start_webhook(
        listen="0.0.0.0",
        port=int(PORT),
        url_path=TOKEN,
        webhook_url=f"{HEROKU_URL}/{TOKEN}",
    )

    # Run bot until stopped
    updater.idle()
