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

from telegram.ext import CallbackContext


r = redis.StrictRedis(host='localhost', port=6379, db=0)  # What is db=0? Clarify before push


def add_user(chat_id):
    """store user chat id"""
    if r.get('Users'):
        users = pickle.loads(r.get('Users'))
        users.add(chat_id)
        r.set('Users', pickle.dumps(users))
        print(pickle.loads(r.get('Users')))
    else:
        users = set([chat_id])
        # users.add(chat_id)
        r.set('Users', pickle.dumps(users))
        print(pickle.loads(r.get('Users')))


def get_users():
    """get stored user chat ids"""
    if r.get('Users'):
        print(pickle.loads(r.get('Users')))
        return pickle.loads(r.get('Users'))
    else:
        return set([])


def add_user_preferences(chat_id, category, response):
    """store/cache chat_id and user_preferences"""
    if r.get(chat_id):
        catalogue = pickle.loads(r.get(chat_id))
        if catalogue.get(category):
            catalogue[category].add(response)
        else:
            catalogue[category] = set([response])
        r.set(chat_id, pickle.dumps(catalogue))
    else:
        catalogue = {category: set([response])}
        r.set(chat_id, pickle.dumps(catalogue))

    return "User Added"


def remove_user_preferences(chat_id, category, response):
    """remove chat_id and user_preferences"""
    catalogue = pickle.loads(r.get(chat_id))
    catalogue[category].remove(response)
    if catalogue[category]:
        r.set(chat_id, pickle.dumps(catalogue))
    else:
        del catalogue[category]
        if catalogue:
            r.set(chat_id, pickle.dumps(catalogue))
        else:
            r.delete(chat_id)
    return "Topic Removed"


def get_user_preferences(chat_id, context: CallbackContext):
    """store/cache chat_id and user_preferences"""
    if r.get(chat_id):  # I don't know if nil will be treated like None by if statement
        catalogue = pickle.loads(r.get(chat_id))
        context.user_data["CURRENT_PREFERENCES"] = catalogue
    return context.user_data["CURRENT_PREFERENCES"]


def store_paper_update(category, topics):
    """store latest papers for each category"""
    Category = {}

    print(topics.items())
    for topic in topics.items():
        (topicer, code) = topic
        print(f"{topicer} {code}")
        search = arxiv.Search(
            query=code,
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        result = search.results().__next__()
        setTime = datetime.datetime.now()
        setTime = setTime.replace(tzinfo=pytz.utc)
        print(setTime)
        setTime = setTime - datetime.timedelta(hours=100)
        # hours need to be altered
        print(setTime)
        if result.published > setTime:
            print(result.published)

            paper_dict = {}

            title = format_content(result.title)
            paper_dict['title'] = title

            date = format_content(str(result.published).split()[0])
            paper_dict['date'] = date

            summary = format_content(result.summary)
            summary = summary.replace("\n", " ")
            paper_dict['summary'] = summary

            categories = format_content(", ".join(result.categories))
            paper_dict['categories'] = categories

            abs_url = [str(link) for link in result.links if "abs" in str(link)][0]
            abs_url = format_content(re.sub(r"v\d+\b", "", abs_url))
            paper_dict['abs_url'] = abs_url

            pdf_url = [str(link) for link in result.links if "pdf" in str(link)][0]
            pdf_url = format_content(re.sub(r"v\d+\b", "", pdf_url))
            paper_dict['pdf_url'] = pdf_url

            try:
                Category = pickle.loads(r.get(category))
                Category[code] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))
            except:
                r.delete(category)
                Category[code] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))


def get_stored_papers(category, topics):
    """get stored papers for categories"""
    Category = {}

    print(topics.items())
    for topic in topics.items():
        (topicer, code) = topic
        print(f"{topicer} {code}")
        search = arxiv.Search(
            query=code,
            max_results=1,
            sort_by=arxiv.SortCriterion.SubmittedDate,
            sort_order=arxiv.SortOrder.Descending,
        )

        result = search.results().__next__()
        setTime = datetime.datetime.now()
        setTime = setTime.replace(tzinfo=pytz.utc)
        print(setTime)
        setTime = setTime - datetime.timedelta(hours=100)
        # hours need to be altered
        print(setTime)
        if result.published > setTime:
            print(result.published)

            paper_dict = {}

            title = format_content(result.title)
            paper_dict['title'] = title

            date = format_content(str(result.published).split()[0])
            paper_dict['date'] = date

            summary = format_content(result.summary)
            summary = summary.replace("\n", " ")
            paper_dict['summary'] = summary

            categories = format_content(", ".join(result.categories))
            paper_dict['categories'] = categories

            abs_url = [str(link) for link in result.links if "abs" in str(link)][0]
            abs_url = format_content(re.sub(r"v\d+\b", "", abs_url))
            paper_dict['abs_url'] = abs_url

            pdf_url = [str(link) for link in result.links if "pdf" in str(link)][0]
            pdf_url = format_content(re.sub(r"v\d+\b", "", pdf_url))
            paper_dict['pdf_url'] = pdf_url

            try:
                Category = pickle.loads(r.get(category))
                Category[code] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))
            except:
                r.delete(category)
                Category[code] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))


def format_content(content):
    escaper = re.compile(r"(\W)")
    return escaper.sub(r"\\\1", content)


if __name__ == "__main__":
    print(add_user_preferences({}))
    print(get_user_preferences({}))
    print(remove_user_preferences({}))
