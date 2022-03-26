"""
Arxiv Telegram Bot - ComputerScienceCategory

Enumerator for the CS subjects
"""

from enum import Enum


class ComputerScienceCategory(dict, Enum):
    """
    Computer Science Category

    This enumerator holds all categories required for Computer Science subjects.
    """

    # Name of the category
    __cat_name__: str = "cs"

    AI: dict = {"code": "AI", "name": "Artificial Intelligence"}
    CL: dict = {"code": "CL", "name": "Computation and Language"}
    CV: dict = {"code": "CV", "name": "Computer Vision and Pattern Recognition"}
    LG: dict = {"code": "LG", "name": "Machine Learning"}
    NE: dict = {"code": "NE", "name": "Neural and Evolutionary Computing"}
    RO: dict = {"code": "RO", "name": "Robotics"}

    def get_code(self) -> str:
        """
        Retrieve the formatted subject code of the given subject
        """
        return f"{ComputerScienceCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        """
        Retrieve the name of the given subject
        """
        return f"{self.value.get('name')}"
