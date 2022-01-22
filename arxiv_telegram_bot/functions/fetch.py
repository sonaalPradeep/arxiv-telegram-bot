#!/usr/bin/env python
# -*- coding: utf-8 -*-

import arxiv

query_catalogues = ["cs.CV", "cs.LG", "cs.CL", "cs.AI", "cs.NE", "cs.RO"]
query_string = " OR ".join(query_catalogues)


def fetch_latest_paper():
    search = arxiv.Search(
        query=query_string,
        max_results=1,
        sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_order=arxiv.SortOrder.Descending,
    )

    result = search.results().__next__()
    return result.title, result.published, result.summary


if __name__ == "__main__":
    print(fetch_latest_paper())
