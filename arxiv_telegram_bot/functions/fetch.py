#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arxiv
import re

from arxiv_telegram_bot.models.category.computer_science import ComputerScienceCategory

query_catalogues = list(map(lambda x: x.get_code(), list(ComputerScienceCategory)))
query_string = " OR ".join(query_catalogues)


def fetch_latest_paper():
    search = arxiv.Search(
        query=query_string,
        max_results=1,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    result = search.results().__next__()

    title = format_content(result.title)
    date = format_content(str(result.published).split()[0])
    summary = format_content(result.summary)

    categories = format_content(", ".join(result.categories))

    abs_url = [str(link) for link in result.links if "abs" in str(link)][0]
    abs_url = format_content(re.sub(r"v\d+\b", "", abs_url))

    pdf_url = [str(link) for link in result.links if "pdf" in str(link)][0]
    pdf_url = format_content(re.sub(r"v\d+\b", "", pdf_url))

    return title, date, summary, categories, abs_url, pdf_url


def format_content(content):
    escaper = re.compile(r"(\W)")
    return escaper.sub(r"\\\1", content)


if __name__ == "__main__":
    print(fetch_latest_paper())
