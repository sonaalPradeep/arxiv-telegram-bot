#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Redis Instance

Contains all methods related to storing and fetching user data using redis instance
"""

import arxiv
import datetime
import pytz
import re
import redis
import pickle
import os
import dotenv
from urllib.parse import urlparse

dotenv.load_dotenv()
url = urlparse(os.environ.get("REDIS_URL"))
r = redis.StrictRedis(
    host=url.hostname,
    port=url.port,
    username="",
    password=os.environ.get("REDIS_PASSWORD"),
)


# def add_user(chat_id):
#     """store user chat id"""
#     if r.get("Users"):
#         users = pickle.loads(r.get("Users"))
#         users.add(chat_id)
#         r.set("Users", pickle.dumps(users))
#     else:
#         users = set([chat_id])
#         r.set("Users", pickle.dumps(users))


def add_user(chat_id):
    """store user chat id"""

    try:
        with open("Users", "rb+") as pickle_file:
            users = pickle.load(pickle_file)
        with open("Users", "wb") as pickle_file:
            users.add(chat_id)
            pickle.dump(users, pickle_file)
    except:
        print("File does not exist or stored data format is incorrect")

        with open("Users", "wb") as pickle_file:
            users = set([chat_id])
            pickle.dump(users, pickle_file)


# todo change except print/ log


# def get_users():
#     """get stored user chat ids"""
#     if r.get("Users"):
#         return pickle.loads(r.get("Users"))
#     else:
#         return set([])


def get_users():
    """get stored user chat ids"""
    try:
        with open("Users", "rb+") as pickle_file:
            users = pickle.load(pickle_file)
            return users
    except:
        print("File does not exist or stored data format is incorrect")
        with open("Users", "wb") as pickle_file:
            users = set([])
            pickle.dump(users, pickle_file)
            return users
    # todo change except print/ log


def store_update_time():
    try:
        with open("Time", "wb") as pickle_file:
            time = datetime.datetime.now()
            pickle.dump(time, pickle_file)
    except:
        print("Something went wrong while storing last updated time")
    # todo change except print/ log


# def store_update_time():
#     r.set("Time", pickle.dumps(datetime.datetime.now()))


def get_update_time():
    try:
        with open("Time", "rb+") as pickle_file:
            time = pickle.load(pickle_file)
            return time
    except:
        print("Time file does not exist, latest papers will be updated now")
        return None
    # todo change except print/ log


# def get_update_time():
#     if r.get("Time"):
#         return pickle.loads(r.get("Time"))


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
        setTime = setTime - datetime.timedelta(hours=100)  # todo revert to 12
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
                with open(category, "rb+") as pickle_file:
                    Category = pickle.load(pickle_file)
                    Category[topic[1]] = paper_dict
                with open(category, "wb") as pickle_file:
                    pickle.dump(Category, pickle_file)
            except:
                print("Category did not exits or stored data format is incorrect")
                # os.remove(category) #todo check if this is removing correctly
                with open(category, "wb") as pickle_file:
                    Category[topic[1]] = paper_dict
                    pickle.dump(Category, pickle_file)
            # todo change except print/ log


# def store_paper_update(category, topics):
#     """store latest papers for each category"""
#     Category = {}
#     for topic in topics.items():
#         search = arxiv.Search(
#             query=topic[1],
#             max_results=1,
#             sort_by=arxiv.SortCriterion.SubmittedDate,
#             sort_order=arxiv.SortOrder.Descending,
#         )
#
#         result = search.results().__next__()
#         setTime = datetime.datetime.now()
#         setTime = setTime.replace(tzinfo=pytz.utc)
#         setTime = setTime - datetime.timedelta(hours=12)
#         if result.published > setTime:
#             paper_dict = {}
#
#             title = format_content(result.title)
#             paper_dict["title"] = title
#
#             date = format_content(str(result.published).split()[0])
#             paper_dict["date"] = date
#
#             summary = format_content(result.summary)
#             summary = summary.replace("\n", " ")
#             paper_dict["summary"] = summary
#
#             categories = format_content(", ".join(result.categories))
#             paper_dict["categories"] = categories
#
#             abs_url = [str(link) for link in result.links if "abs" in str(link)][0]
#             abs_url = format_content(re.sub(r"v\d+\b", "", abs_url))
#             paper_dict["abs_url"] = abs_url
#
#             pdf_url = [str(link) for link in result.links if "pdf" in str(link)][0]
#             pdf_url = format_content(re.sub(r"v\d+\b", "", pdf_url))
#             paper_dict["pdf_url"] = pdf_url
#
#             try:
#                 Category = pickle.loads(r.get(category))
#                 Category[topic[1]] = paper_dict
#                 # Only support for one paper right now
#                 r.set(category, pickle.dumps(Category))
#             except:
#                 r.delete(category)
#                 Category[topic[1]] = paper_dict
#                 # Only support for one paper right now
#                 r.set(category, pickle.dumps(Category))


def get_stored_paper(category, topicCode):
    try:
        with open(category, "rb+") as pickle_file:
            Category = pickle.load(pickle_file)
            if topicCode in Category:
                return Category[topicCode]
            else:
                return None
    except:
        print("Category does not exist or stored data format is incorrect")
        return None
    # todo change except print/ log


# def get_stored_paper(category, topicCode):
#     if r.get(category):
#         category = pickle.loads(r.get(category))
#         if topicCode in category:
#             return category[topicCode]
#         else:
#             return None


def format_content(content):
    escaper = re.compile(r"(\W)")
    return escaper.sub(r"\\\1", content)


if __name__ == "__main__":
    print(get_stored_paper({}))
