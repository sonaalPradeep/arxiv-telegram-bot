#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - StatisticsCategory

Enumerator for the STAT subjects
"""

from enum import Enum


class StatisticsCategory(dict, Enum):
    """
    Statistics Category

    This enumerator holds all categories required for Statistics subjects.
    """

    # Name of the category
    __cat_name__: str = "stat"

    AP: dict = {"code": "AP", "name": "Applications"}
    CO: dict = {"code": "CO", "name": "Computation"}
    ME: dict = {"code": "ME", "name": "Methodology"}
    ML: dict = {"code": "ML", "name": "Machine Learning"}
    OT: dict = {"code": "OT", "name": "Other Statistics"}
    TH: dict = {"code": "TH", "name": "Statistics Theory"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{StatisticsCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
