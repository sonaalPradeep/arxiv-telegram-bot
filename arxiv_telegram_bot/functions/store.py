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

r = redis.StrictRedis(host='localhost', port=6379, db=0)  # What is db=0? Clarify before push


def add_user(chat_id):
    """store user chat id"""
    if r.get('Users'):
        users = pickle.loads(r.get('Users'))
        users.add(chat_id)
        r.set('Users', pickle.dumps(users))
    else:
        users = set([chat_id])
        r.set('Users', pickle.dumps(users))


def get_users():
    """get stored user chat ids"""
    if r.get('Users'):
        return pickle.loads(r.get('Users'))
    else:
        return set([])


def store_update_time():
    r.set('Time', pickle.dumps(datetime.datetime.now()))


def get_update_time():
    if r.get('Time'):
        return pickle.loads(r.get('Time'))


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
        setTime = setTime - datetime.timedelta(hours=100)    # TODO hours need to be altered
        if result.published > setTime:
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
                Category[topic[1]] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))
            except:
                r.delete(category)
                Category[topic[1]] = paper_dict
                # Only supports one paper right now, make it into a list once we confirm that this works
                r.set(category, pickle.dumps(Category))


def get_stored_paper(category, topicCode):
    if r.get(category):
        category = pickle.loads(r.get(category))
        if topicCode in category:
            return category[topicCode]
        else:
            return None

def format_content(content):
    escaper = re.compile(r"(\W)")
    return escaper.sub(r"\\\1", content)


if __name__ == "__main__":
    print(get_stored_paper({}))