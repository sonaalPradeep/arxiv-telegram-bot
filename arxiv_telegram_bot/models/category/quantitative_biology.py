#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - QuantitativeBiologyCategory

Enumerator for the Q-BIO subjects
"""

from enum import Enum


class QuantitativeBiologyCategory(dict, Enum):  # type: ignore[misc]
    """
    Quantitative Biology Category

    This enumerator holds all categories required for Quantitative Biology subjects.
    """

    # Name of the category
    __cat_name__: str = "q-bio"

    BM: dict = {"code": "BM", "name": "Biomolecules"}
    CB: dict = {"code": "CB", "name": "Cell Behavior"}
    GN: dict = {"code": "GN", "name": "Genomics"}
    MN: dict = {"code": "MN", "name": "Molecular Networks"}
    NC: dict = {"code": "NC", "name": "Neurons and Cognition"}
    OT: dict = {"code": "OT", "name": "Other Quantitative Biology"}
    PE: dict = {"code": "PE", "name": "Populations and Evolution"}
    QM: dict = {"code": "QM", "name": "Quantitative Methods"}
    SC: dict = {"code": "SC", "name": "Subcellular Processes"}
    TO: dict = {"code": "TO", "name": "Tissues and Organs"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{QuantitativeBiologyCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
