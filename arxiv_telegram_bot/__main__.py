#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
# Arxiv Telegram Bot Module

Main Module for Arxiv
"""

"""
# import arxiv

# query_catalogues = ["cs.CV", "cs.LG", "cs.CL", "cs.AI", "cs.NE", "cs.RO"]
# query_string = " OR ".join(query_catalogues)

# search = arxiv.Search(
#     query=query_string,
#     max_results=100,
#     sort_by=arxiv.SortCriterion.SubmittedDate,
#     sort_order=arxiv.SortOrder.Descending,
# )

# for result in search.results():
#     print(
#         f"{result.title} - {result.published}\n{result.categories}\n{result.summary}\n\n"
#     )
"""

from arxiv_telegram_bot.base import main


if __name__ == "__main__":
    main()
