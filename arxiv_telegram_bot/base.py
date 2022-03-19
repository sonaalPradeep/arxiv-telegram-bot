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

# - Telegram Imports
import telegram
from telegram import Update

# - Telegram Extended Imports
from telegram.ext import (
    Updater,
    CommandHandler,
    Dispatcher,
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
)

# - Custom Functions
from arxiv_telegram_bot.models.category.computer_science import ComputerScienceCategory
from arxiv_telegram_bot.models.category.electrical_engineering_and_systems_science import (
    ElectricalEngineeringAndSystemsScience,
)
from arxiv_telegram_bot.functions.fetch import fetch_latest_paper
from arxiv_telegram_bot.models.category.category_helper import CategoryHelper


# -- SETUP

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

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

CHOOSE_CATEGORY, CHOOSE_TOPIC, FALLBACK = range(3)
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

    title, date, summary, categories, abs_url, pdf_url = fetch_latest_paper(
        context.user_data.get("CURRENT_PREFERENCES")
    )
    summary = summary.replace("\n", "")
    message_to_send = f"""
*{title}* `\({categories}\)`\n
Publication Date: _{date}_\n\n
{summary}\n
    
[Click here to open the Arxiv page]({abs_url})
[Click here to open the PDF]({pdf_url})"""

    update.message.reply_text(
        message_to_send, parse_mode=telegram.ParseMode.MARKDOWN_V2
    )


def preferences_entry(update: Update, context: CallbackContext):
    """Gather subject preferences of user"""

    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = f"Hey there! Looks like you don't have any preferences set. Let me help you out"
    else:
        reply_text = f"Welcome back! Looks like we already have your preferences: {user_preferences}"

    update.message.reply_text(
        reply_text,
        reply_markup=telegram.ReplyKeyboardMarkup([["Choose Category"], ["Exit"]]),
    )

    return CHOOSE_CATEGORY


def pick_categories(update: Update, context: CallbackContext):
    categories = CategoryHelper()
    catalogues = [[category] for category in categories.get_categories_list()]
    catalogues += [["Exit"]]

    update.message.reply_text(
        "Please choose your category",
        reply_markup=telegram.ReplyKeyboardMarkup(
            catalogues, input_field_placeholder="Category"
        ),
    )

    return CHOOSE_TOPIC


def pick_topic(update: Update, context: CallbackContext):
    categories = CategoryHelper()
    response = update.message.text
    context.user_data["CURRENT_CATEGORY"] = response

    if context.user_data.get("CURRENT_PREFERENCES") is None:
        context.user_data["CURRENT_PREFERENCES"] = {}

    enum_category = categories.get_enumerate_from_name(response)
    catalogues = list(map(lambda x: [x.get_name()], list(enum_category)))

    catalogues += [["Go back"]]
    update.message.reply_text(
        "Please choose your topic",
        reply_markup=telegram.ReplyKeyboardMarkup(
            catalogues, input_field_placeholder="Topic"
        ),
    )

    return CHOOSE_TOPIC


def pick_topic_again(update: Update, context: CallbackContext):
    categories = CategoryHelper()
    category = context.user_data["CURRENT_CATEGORY"]
    response = update.message.text

    if category not in context.user_data["CURRENT_PREFERENCES"]:
        context.user_data["CURRENT_PREFERENCES"][category] = set([])

    if response not in context.user_data.get("CURRENT_PREFERENCES").get(category):
        context.user_data["CURRENT_PREFERENCES"][category].add(response)
        reply_text = f"Added {response} to your preferences"
    else:
        context.user_data["CURRENT_PREFERENCES"][category].remove(response)
        reply_text = f"Removed {response} to your preferences"

        if len(context.user_data["CURRENT_PREFERENCES"][category]) == 0:
            del context.user_data["CURRENT_PREFERENCES"][category]

    enum_category = categories.get_enumerate_from_name(category)
    catalogues = list(map(lambda x: [x.get_name()], list(enum_category)))

    catalogues += [["Go back"]]
    update.message.reply_text(
        reply_text,
        reply_markup=telegram.ReplyKeyboardMarkup(
            catalogues, input_field_placeholder="Topic"
        ),
    )

    return CHOOSE_TOPIC


def preferences_done(update: Update, context: CallbackContext):
    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = "Ohh... We see that you're preferences are empty"
    else:
        reply_text = f"Excellent choice! Your preferences now are {user_preferences}"

    update.message.reply_text(reply_text, reply_markup=telegram.ReplyKeyboardRemove())

    return ConversationHandler.END


# - Error Handler
def error(update: Update, context: CallbackContext):
    logger.warning("Update %s caused error %s", update, context.error)


# -- MAIN FUNCTION
def main():
    """Start the bot."""

    categories = CategoryHelper()
    catalogues_filter = "^(" + "|".join(categories.get_categories_list()) + ")$"

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

    # TODO: Handler must be able to ignore commands
    # TODO: Verify if callback works
    preference_handler = ConversationHandler(
        entry_points=[CommandHandler("preferences", preferences_entry)],
        states={
            CHOOSE_CATEGORY: [
                MessageHandler(
                    filters=Filters.regex("^Choose Category$"), callback=pick_categories
                ),
                MessageHandler(
                    filters=Filters.regex("^Exit$"), callback=preferences_done
                ),
            ],
            CHOOSE_TOPIC: [
                MessageHandler(
                    filters=Filters.regex(catalogues_filter),
                    callback=pick_topic,
                ),
                MessageHandler(
                    filters=Filters.text & ~(Filters.regex("^(Go back|Exit)$")),
                    callback=pick_topic_again,
                ),
                MessageHandler(
                    filters=Filters.regex("^Go back$"), callback=pick_categories
                ),
                MessageHandler(
                    filters=Filters.regex("^Exit$"), callback=preferences_done
                ),
            ],
        },
        fallbacks=[CommandHandler("done", preferences_done)],
    )

    dp.add_handler(preference_handler)

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
