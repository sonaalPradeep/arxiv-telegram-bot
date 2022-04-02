#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - QuantitativeFinanceCategory

Enumerator for the Q-FIN subjects
"""

from enum import Enum


class QuantitativeFinanceCategory(dict, Enum):
    """
    Quantitative Finance Category

    This enumerator holds all categories required for Quantitative Finance subjects.
    """

    # Name of the category
    __cat_name__: str = "q-fin"

    CP: dict = {"code": "CP", "name": "Computational Finance"}
    EC: dict = {"code": "EC", "name": "Economics"}
    GN: dict = {"code": "GN", "name": "General Finance"}
    MF: dict = {"code": "MF", "name": "Mathematical Finance"}
    PM: dict = {"code": "PM", "name": "Portfolio Management"}
    PR: dict = {"code": "PR", "name": "Pricing of Securities"}
    RM: dict = {"code": "RM", "name": "Risk Management"}
    ST: dict = {"code": "ST", "name": "Statistical Finance"}
    TR: dict = {"code": "TR", "name": "Trading and Market Microstructure"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{QuantitativeFinanceCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
