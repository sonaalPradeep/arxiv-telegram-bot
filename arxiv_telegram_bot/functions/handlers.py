#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Handlers

Contains all handlers for the telegram bot.
"""
import datetime
import logging

import pytz
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, TelegramError

from telegram.ext import (
    CallbackContext,
    ConversationHandler,
    CommandHandler,
    CallbackQueryHandler,
)

from arxiv_telegram_bot.functions.fetch import fetch_latest_paper
from arxiv_telegram_bot.functions.store import (
    store_paper_update,
    get_stored_paper,
    add_user,
    store_update_time,
    get_update_time,
)
from arxiv_telegram_bot.models.category.category_helper import CategoryHelper

logger = logging.getLogger(__name__)

CHOOSE_CATEGORY, CHOOSE_TOPIC, FALLBACK = range(3)


def start(update: Update, context: CallbackContext):  # pylint: disable=unused-argument
    """
    Send a message when the command 'start' is issued.
    """
    update.message.reply_text("Hi! Your userid")


def fetch(update: Update, context: CallbackContext):
    """
    Fetch the latest papers
    """
    add_user(update.effective_chat.id)  # Adds user incase missing in DB

    context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action=telegram.ChatAction.TYPING
    )

    title, date, summary, categories, abs_url, pdf_url = fetch_latest_paper(
        context.user_data.get("CURRENT_PREFERENCES")
    )

    try:
        message_to_send = f"""
*{title}* `\({categories}\)`\n
Publication Date: _{date}_\n\n
{summary}\n

[Click here to open the Arxiv page]({abs_url})
[Click here to open the PDF]({pdf_url})"""

        update.message.reply_text(
            message_to_send, parse_mode=telegram.ParseMode.MARKDOWN_V2
        )
    except (TelegramError, Exception) as e:
        logger.error("Exception occurred while getting message", e)

        failure_message = (
            f"Something went wrong while trying to get paper\.\n\n"
            f"You can access the paper from [this URL]({abs_url})\."
        )
        update.message.reply_text(
            failure_message, parse_mode=telegram.ParseMode.MARKDOWN_V2
        )


def updater(context: CallbackContext) -> None:
    """Check for new papers in category"""
    add_user(context.job.context.get("chat_id"))

    catalogue = CategoryHelper()

    if get_update_time() is not None:
        if (datetime.datetime.now() - get_update_time()) >= datetime.timedelta(hours=6):
            for category, topics in catalogue.name_code_mapping.items():
                store_paper_update(category, topics)
            store_update_time()
    else:
        for category, topics in catalogue.name_code_mapping.items():
            store_paper_update(category, topics)
        store_update_time()

    job = context.job

    if (
        job.context.get("context") is not None
        and job.context.get("context").items() is not None
    ):
        for category, topics in job.context.get("context").items():
            for topic in topics:
                topicCode = catalogue.name_code_mapping[category][topic]
                paper = get_stored_paper(category, topicCode)
                if paper:
                    title = paper["title"]
                    date = paper["date"]
                    summary = paper["summary"]
                    categories = paper["categories"]
                    abs_url = paper["abs_url"]
                    pdf_url = paper["pdf_url"]
                    try:
                        message_to_send = f"""
*{title}* `\({categories}\)`\n
Publication Date: _{date}_\n\n
{summary}\n

[Click here to open the Arxiv page]({abs_url})
[Click here to open the PDF]({pdf_url})"""

                        context.bot.send_message(
                            job.context.get("chat_id"),
                            text=message_to_send,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2,
                        )

                    except (TelegramError, Exception) as e:
                        logger.error("Exception occurred while getting message", e)

                        failure_message = (
                            f"Something went wrong while trying to get paper\.\n\n"
                            f"You can access the paper from [this URL]({abs_url})\."
                        )
                        context.bot.send_message(
                            job.context.get("chat_id"),
                            text=failure_message,
                            parse_mode=telegram.ParseMode.MARKDOWN_V2,
                        )


def remove_job_if_exists(name: str, context: CallbackContext) -> bool:
    """Remove job with given name. Returns whether job was removed."""
    current_jobs = context.job_queue.get_jobs_by_name(name)
    if not current_jobs:
        return False
    for job in current_jobs:
        job.schedule_removal()
    return True


def schedule(update: Update, context: CallbackContext) -> None:
    """Add a job to the queue."""
    chat_id = update.message.chat_id
    try:
        if (
            len(context.user_data) == 0
            or len(context.user_data.get("CURRENT_PREFERENCES")) == 0
        ):
            update.message.reply_text(
                "We cannot set scheduler, as your preferences are empty"
            )
            return

        # args[0] should contain the number of hours separating daily update time from UTC time
        difference = int(context.args[0])
        updateTime = datetime.datetime.now(tz=pytz.UTC) + datetime.timedelta(
            hours=difference
        )

        if (
            int(updateTime.time().strftime("%H")) >= 24
            or int(updateTime.time().strftime("%H")) <= 0
        ):
            update.message.reply_text(
                "Sorry, we can't update you at that time, please try again!"
            )
            return

        variable = {}
        variable["context"] = context.user_data.get("CURRENT_PREFERENCES")
        variable["chat_id"] = chat_id

        job_removed = remove_job_if_exists(str(chat_id) + "job", context)
        # context.job_queue.run_once(
        #     updater, int(context.args[0]), context=variable, name=str(chat_id) + "job"
        # )
        context.job_queue.run_repeating(updater, int(context.args[0]), context=variable, name=str(chat_id) + "job")
        # context.job_queue.run_daily(
        #     updater,
        #     time=updateTime.time(),
        #     days=(0, 1, 2, 3, 4, 5, 6),
        #     context=chat_id,
        #     name=str(chat_id) + "job",
        # )

        text = "Timer successfully set!"
        if job_removed:
            text += " Old one was removed."
        update.message.reply_text(text)

    except (IndexError, ValueError):
        update.message.reply_text("Usage: /schedule <hours>")


def unschedule(update: Update, context: CallbackContext) -> None:
    """Remove job if user doesn't want scheduled updates"""
    chat_id = update.message.chat_id
    job_removed = remove_job_if_exists(str(chat_id), context)
    text = (
        "Timer successfully cancelled!" if job_removed else "You have no active timer."
    )
    update.message.reply_text(text)


def preferences_entry(update: Update, context: CallbackContext):
    """
    preferences_entry is the entry point for the conversation handler
    """
    add_user(update.effective_chat.id)  # Adds user incase missing in DB

    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = (
            "Hey there! Looks like you don't have any preferences set. "
            "Let me help you out"
        )
    else:
        reply_text = (
            f"Welcome back! Looks like we already have your "
            f"preferences: {user_preferences}"
        )

    keyboard = [
        [InlineKeyboardButton("Choose Category", callback_data="Choose Category")],
        [InlineKeyboardButton("Exit", callback_data="Exit")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text(
        reply_text,
        reply_markup=reply_markup,
    )

    return CHOOSE_CATEGORY


def pick_categories(
    update: Update, context: CallbackContext
):  # pylint: disable=unused-argument
    """
    pick_categories method is the entry point for the preferences conversation handler and
    is used to pick the category of a subject
    """
    query = update.callback_query
    query.answer()

    categories = CategoryHelper()
    buttons = [
        InlineKeyboardButton(category, callback_data=category)
        for category in categories.get_categories_list()
    ]
    buttons.extend([InlineKeyboardButton("Exit", callback_data="Exit")])
    keyboard = list(map(lambda button: [button], buttons))

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        "Please choose your category",
        reply_markup=reply_markup,
    )

    return CHOOSE_TOPIC


def pick_topic(update: Update, context: CallbackContext):
    """
    pick_topic method is the entry point for the preferences conversation handler to
    pick a topic within a category
    """
    query = update.callback_query
    query.answer()

    categories = CategoryHelper()
    response = update.callback_query.data
    context.user_data["CURRENT_CATEGORY"] = response

    if context.user_data.get("CURRENT_PREFERENCES") is None:
        context.user_data["CURRENT_PREFERENCES"] = {}

    enum_category = categories.get_enumerate_from_name(response)
    catalogues = list(map(lambda x: [x.get_name()], list(enum_category)))

    buttons = [
        InlineKeyboardButton(catalogue[0], callback_data=catalogue[0])
        for catalogue in catalogues
    ]
    buttons.extend([InlineKeyboardButton("Go back", callback_data="Go back")])

    keyboard = list(map(lambda button: [button], buttons))

    reply_markup = InlineKeyboardMarkup(keyboard)

    query.edit_message_text(
        "Please choose your topic",
        reply_markup=reply_markup,
    )

    return CHOOSE_TOPIC


def pick_topic_again(update: Update, context: CallbackContext):
    """
    pick_topic_again is used to loop and select a subject in the same category
    """
    query = update.callback_query
    category = context.user_data["CURRENT_CATEGORY"]
    response = update.callback_query.data

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

    query.answer(text=reply_text, show_alert=False)

    return CHOOSE_TOPIC


def preferences_done(update: Update, context: CallbackContext):
    """
    preferences_done is used to end the preferences conversation handler
    """
    query = update.callback_query
    query.answer()

    user_preferences = context.user_data.get("CURRENT_PREFERENCES")

    if user_preferences is None or len(user_preferences) == 0:
        reply_text = "Ohh... We see that you're preferences are empty"
    else:
        reply_text = f"Excellent choice! Your preferences now are {user_preferences}"

    query.edit_message_text(reply_text)

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
                CallbackQueryHandler(pick_categories, pattern="^Choose Category$"),
                CallbackQueryHandler(preferences_done, pattern="^Exit$"),
            ],
            CHOOSE_TOPIC: [
                CallbackQueryHandler(pick_topic, pattern=catalogues_filter),
                CallbackQueryHandler(pick_categories, pattern="^Go back$"),
                CallbackQueryHandler(preferences_done, pattern="^Exit$"),
                CallbackQueryHandler(pick_topic_again),
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
