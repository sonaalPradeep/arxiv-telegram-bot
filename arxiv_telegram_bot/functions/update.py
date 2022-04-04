#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import arxiv
import re
import pytz

def paper_updates(user_preference):
    search = arxiv.Search(
        query=user_preference,
        max_results=1,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    result = search.results().__next__()
    setTime = datetime.datetime.now()
    setTime = setTime.replace(tzinfo=pytz.utc)
    print(setTime)
    # print statements need to be removed
    setTime = setTime - datetime.timedelta(hours=100)
    # hours need to be altered
    print(setTime)
    print(result.published)
    # setTime = setTime.strftime("%m/%d/%Y, %H:%M:%S")
    # print(type(setTime))
    if result.published > setTime:
        print(result.published)

        title = format_content(result.title)
        date = format_content(str(result.published).split()[0])
        summary = format_content(result.summary)
        summary = summary.replace("\n", " ")

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
    print(paper_updates())
