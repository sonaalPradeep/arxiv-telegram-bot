#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - EconomicsCategory

Enumerator for the ECON subjects
"""

from enum import Enum


class EconomicsCategory(dict, Enum):  # type: ignore[misc]
    """
    Economics Category

    This enumerator holds all categories required for Economics subjects.
    """

    # Name of the category
    __cat_name__: str = "econ"

    EM: dict = {"code": "EM", "name": "Econometrics"}
    GN: dict = {"code": "GN", "name": "General Economics"}
    TH: dict = {"code": "TH", "name": "Theoretical Economics"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{EconomicsCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
