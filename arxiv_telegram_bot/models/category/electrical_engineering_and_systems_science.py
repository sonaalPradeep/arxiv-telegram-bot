#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - ElectricalEngineeringAndSystemsScience

Enumerator for the EESS subjects
"""

from enum import Enum


class ElectricalEngineeringAndSystemsScience(dict, Enum):
    """
    Electrical Engineering and Systems Science Category

    This enumerator holds all categories required for Electrical Engineering and Systems Science
    subjects.
    """

    # Name of the category
    __cat_name__: str = "eess"

    AS: dict = {"code": "AS", "name": "Audio and Speech Processing"}
    IV: dict = {"code": "IV", "name": "Image and Video Processing"}
    SP: dict = {"code": "SP", "name": "Signal Processing"}
    SY: dict = {"code": "SY", "name": "Systems and Control"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{ElectricalEngineeringAndSystemsScience.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
