#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Arxiv Telegram Bot - Mathematics

Enumerator for the MCAH subjects
"""

from enum import Enum


class MathematicsCategory(dict, Enum):
    """
    Mathematics Category

    This enumerator holds all categories required for Mathematics subjects.
    """

    # Name of the category
    __cat_name__: str = "math"

    AC: dict = {"code": "AC", "name": "Commutative Algebra"}
    AG: dict = {"code": "AG", "name": "Algebraic Geometry"}
    AP: dict = {"code": "AP", "name": "Analysis of PDEs"}
    AT: dict = {"code": "AT", "name": "Algebraic Topology"}
    CA: dict = {"code": "CA", "name": "Classical Analysis and ODEs"}
    CO: dict = {"code": "CO", "name": "Combinatronics"}
    CT: dict = {"code": "CT", "name": "Category Theory"}
    CV: dict = {"code": "CV", "name": "Complex Variables"}
    DG: dict = {"code": "DG", "name": "Differential Geometry"}
    DS: dict = {"code": "DS", "name": "Dynamical Systems"}
    FA: dict = {"code": "FA", "name": "Functional Analysis"}
    GM: dict = {"code": "GM", "name": "General Mathematics"}
    GN: dict = {"code": "GN", "name": "General Topology"}
    GR: dict = {"code": "GR", "name": "Group Theory"}
    GT: dict = {"code": "GT", "name": "Geometric Topology"}
    HO: dict = {"code": "HO", "name": "History and Overview"}
    IT: dict = {"code": "IT", "name": "Information Theory"}
    KT: dict = {"code": "KT", "name": "K-Theory and Homology"}
    LO: dict = {"code": "LO", "name": "Logic"}
    MG: dict = {"code": "MG", "name": "Metric Geometry"}
    MP: dict = {"code": "MP", "name": "Mathematical Physics"}
    NA: dict = {"code": "NA", "name": "Numerical Analysis"}
    NT: dict = {"code": "NT", "name": "Number Theory"}
    OA: dict = {"code": "OA", "name": "Operator Algebras"}
    OC: dict = {"code": "OC", "name": "Optimization and Control"}
    PR: dict = {"code": "PR", "name": "Probability"}
    QA: dict = {"code": "QA", "name": "Quantum Algebra"}
    RA: dict = {"code": "RA", "name": "Rings and Algebras"}
    RT: dict = {"code": "RT", "name": "Representation Theory"}
    SG: dict = {"code": "SG", "name": "Symplectic Geometry"}
    SP: dict = {"code": "SP", "name": "Spectral Theory"}
    ST: dict = {"code": "ST", "name": "Statistics Theory"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{MathematicsCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
