#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Arxiv Base Imports


"""

import logging
from setuptools import Command

from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
    MessageHandler,
    Filters,
    CallbackContext,
)
from telegram import Update
import os

port = int(os.environ.get("PORT", 5000))

# enable logging
logger = logging.getLogger(__name__)

TOKEN = "5057319565:AAEX2dcT93FJ4AToOZlrVhvuPxJy051c_nQ"

# Define a few command handlers


def start(update: Update, context: CallbackContext):
    """Send a message when the command 'start' is issued."""
    print(context._user_id_and_data[0])
    update.message.reply_text("Hi! Your userid")


def uid(update: Update, context: CallbackContext):
    """Ping back the userid whose command created"""
    update.message.reply_text(f"Your user ID is {context._user_id_and_data[0]}")


def error(update: Update, context: CallbackContext):
    logger.warning("Update %s caused error %s", update, context.error)


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

    # log all errors
    dp.add_error_handler(error)

    # Start the bot

    updater.start_polling()

    # Run bot until stopped
    updater.idle()
