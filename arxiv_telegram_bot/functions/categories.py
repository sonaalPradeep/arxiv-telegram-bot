#!/usr/bin/env python
# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import requests


def scrape_arxiv_subject_codes():
    category_url = "https://arxiv.org/category_taxonomy"

    results = requests.get(category_url).text
    soup = BeautifulSoup(results, "lxml")

    subject_categories = [
        h2.text for h2 in soup.find_all("h2", {"class": "accordion-head"})
    ]
    all_subject_codes = []

    for subject_category in soup.find_all("div", {"class": "accordion-body"}):
        subject_codes = []
        for subject in subject_category.find_all("h4"):
            code, name = subject.text.split(" ", 1)
            name = name.strip("()")
            subject_codes.append((code, name))

        all_subject_codes.append(subject_codes)

    return zip(subject_categories, all_subject_codes)


if __name__ == "__main__":
    subject_code_mappings = scrape_arxiv_subject_codes()
    for category, subjects in subject_code_mappings:
        print(f"{category} -> {subjects}")
