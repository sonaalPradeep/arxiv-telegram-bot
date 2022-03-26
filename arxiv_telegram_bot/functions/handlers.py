"""
Arxiv Telegram Bot - Handlers

Contains all handlers for the telegram bot.
"""

import logging

import telegram
from telegram import Update

from telegram.ext import (
    CallbackContext,
    MessageHandler,
    Filters,
    ConversationHandler,
    CommandHandler,
)

from arxiv_telegram_bot.functions.fetch import fetch_latest_paper
from arxiv_telegram_bot.models.category.category_helper import CategoryHelper

logger = logging.getLogger(__name__)

CHOOSE_CATEGORY, CHOOSE_TOPIC, FALLBACK = range(3)


def start(update: Update, context: CallbackContext):
    """
    Send a message when the command 'start' is issued.
    """
    update.message.reply_text("Hi! Your userid")


def uid(update: Update, context: CallbackContext):
    """
    Ping back the userid whose command created
    """
    message_to_send = f"Your user ID is {context._user_id_and_data[0]}"
    print(message_to_send)
    update.message.reply_text(message_to_send)


def fetch(update: Update, context: CallbackContext):
    """
    Fetch the latest papers
    """
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
    """
    preferences_entry is the entry point for the conversation handler
    """

    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = f"Hey there! Looks like you don't have any preferences set. " \
                     f"Let me help you out"
    else:
        reply_text = f"Welcome back! Looks like we already have your " \
                     f"preferences: {user_preferences}"

    update.message.reply_text(
        reply_text,
        reply_markup=telegram.ReplyKeyboardMarkup([["Choose Category"], ["Exit"]]),
    )

    return CHOOSE_CATEGORY


def pick_categories(update: Update, context: CallbackContext):
    """
    pick_categories method is the entry point for the preferences conversation handler and
    is used to pick the category of a subject
    """
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
    """
    pick_topic method is the entry point for the preferences conversation handler to
    pick a topic within a category
    """
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
    """
    pick_topic_again is used to loop and select a subject in the same category
    """
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
    """
    preferences_done is used to end the preferences conversation handler
    """
    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = "Ohh... We see that you're preferences are empty"
    else:
        reply_text = f"Excellent choice! Your preferences now are {user_preferences}"

    update.message.reply_text(reply_text, reply_markup=telegram.ReplyKeyboardRemove())

    return ConversationHandler.END


def preference_conversation_handler():
    """
    Preferences conversation handler is used to guide a user to pick their preferences of subjects
    """
    # TODO: Handler must be able to ignore commands
    # TODO: Verify if callback works

    categories = CategoryHelper()
    catalogues_filter = "^(" + "|".join(categories.get_categories_list()) + ")$"

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

    return preference_handler


def error(update: Update, context: CallbackContext):
    """
    Error handler for the telegram bot
    """
    logger.warning("Update %s caused error %s", update, context.error)
