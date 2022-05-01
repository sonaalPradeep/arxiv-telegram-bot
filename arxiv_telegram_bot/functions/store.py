#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Redis Instance

Contains all methods related to storing and fetching user data using redis instance
"""

import datetime
import logging
import pickle
import redis

import re
import arxiv
import pytz

logger = logging.getLogger(__name__)


def add_user(chat_id):
    """store user chat id"""

    try:
        with open("/tmp/Users", "rb+") as pickle_file:
            users = pickle.load(pickle_file)
        with open("/tmp/Users", "wb") as pickle_file:
            users.add(chat_id)
            pickle.dump(users, pickle_file)
    except:
        logger.warning("File does not exist or stored data format is incorrect")

        with open("/tmp/Users", "wb") as pickle_file:
            users = set([chat_id])
            pickle.dump(users, pickle_file)


def get_users():
    """get stored user chat ids"""
    try:
        with open("/tmp/Users", "rb+") as pickle_file:
            users = pickle.load(pickle_file)
            return users
    except:
        logger.warning("File does not exist or stored data format is incorrect")
        with open("/tmp/Users", "wb") as pickle_file:
            users = set([])
            pickle.dump(users, pickle_file)
            return users


def store_update_time():
    try:
        with open("/tmp/Time", "wb") as pickle_file:
            time = datetime.datetime.now()
            pickle.dump(time, pickle_file)
    except:
        logger.warning("Something went wrong while storing last updated time")


def get_update_time():
    try:
        with open("/tmp/Time", "rb+") as pickle_file:
            time = pickle.load(pickle_file)
            return time
    except:
        logger.warning("Time file does not exist, latest papers will be updated now")
        return None


def store_paper_update(category, topics):
    """store latest papers for each category"""
    Category = {}
    for topic in topics.items():
        search = arxiv.Search(
            query=topic[1],
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        result = search.results().__next__()
        setTime = datetime.datetime.now()
        setTime = setTime.replace(tzinfo=pytz.utc)
        setTime = setTime - datetime.timedelta(hours=100)  # todo revert to 12 hours
        if result.published > setTime:
            paper_dict = {}

            title = format_content(result.title)
            paper_dict["title"] = title

            date = format_content(str(result.published).split()[0])
            paper_dict["date"] = date

            summary = format_content(result.summary)
            summary = summary.replace("\n", " ")
            paper_dict["summary"] = summary

            categories = format_content(", ".join(result.categories))
            paper_dict["categories"] = categories

            abs_url = [str(link) for link in result.links if "abs" in str(link)][0]
            abs_url = format_content(re.sub(r"v\d+\b", "", abs_url))
            paper_dict["abs_url"] = abs_url

            pdf_url = [str(link) for link in result.links if "pdf" in str(link)][0]
            pdf_url = format_content(re.sub(r"v\d+\b", "", pdf_url))
            paper_dict["pdf_url"] = pdf_url

            try:
                key = f"/tmp/{category}"
                with open(key, "rb+") as pickle_file:
                    Category = pickle.load(pickle_file)
                    Category[topic[1]] = paper_dict
                with open(key, "wb") as pickle_file:
                    pickle.dump(Category, pickle_file)
            except:
                logger.warning(
                    "Category did not exist or stored data format is incorrect"
                )
                key = f"/tmp/{category}"
                with open(key, "wb") as pickle_file:
                    Category[topic[1]] = paper_dict
                    pickle.dump(Category, pickle_file)


def get_stored_paper(category, topicCode):
    try:
        key = f"/tmp/{category}"
        with open(key, "rb+") as pickle_file:
            Category = pickle.load(pickle_file)
            if topicCode in Category:
                return Category[topicCode]
            else:
                return None
    except:
        logger.warning("Category does not exist or stored data format is incorrect")
        return None


def format_content(content):
    escaper = re.compile(r"(\W)")
    return escaper.sub(r"\\\1", content)


if __name__ == "__main__":
    print(get_stored_paper({}))
