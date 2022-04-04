#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Redis Instance

Contains all methods related to storing and fetching user data using redis instance
"""

import redis
import pickle

from telegram.ext import CallbackContext

r = redis.Redis(
    host='localhost',
    port=6398
)
db_keys = r.keys(pattern='*')

j = redis.StrictRedis(host='localhost', port=6379, db=0)  # What is db=0? Clarify before push

def add_user(chat_id, category, response):
    """
    store/cache chat_id and user_preferences
    """
    if j.get(chat_id):
        catalogue = pickle.loads(j.get(chat_id))
        if catalogue.get(category):
            catalogue[category].add(response)
        else:
            catalogue[category] = set([response])
        j.set(chat_id, pickle.dumps(catalogue))
    else:
        catalogue = {category:set([response])}
        j.set(chat_id, pickle.dumps(catalogue))

    return "User Added"

def remove_user(chat_id, category, response):
    """
    remove chat_id and user_preferences
    """
    catalogue = pickle.loads(j.get(chat_id))
    catalogue[category].remove(response)
    if catalogue[category]:
        j.set(chat_id, pickle.dumps(catalogue))
    else:
        del catalogue[category]
        if catalogue:
            j.set(chat_id, pickle.dumps(catalogue))
        else:
            j.delete(chat_id)
    return "Topic Removed"

def get_user_preferences(chat_id, context: CallbackContext):
    """
    store/cache chat_id and user_preferences
    """
    if j.get(chat_id): # I don't know if nil will be treated like None by if statement
        catalogue = pickle.loads(j.get(chat_id))
        context.user_data["CURRENT_PREFERENCES"] = catalogue
    return context.user_data["CURRENT_PREFERENCES"]

if __name__ == "__main__":
    print(add_user({}))
    print(get_user_preferences({}))
    print(remove_user({}))
