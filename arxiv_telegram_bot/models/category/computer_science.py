from enum import Enum


class ComputerScienceCategory(dict, Enum):
    """
    # Computer Science Category

    This enumerator holds all categories required for Computer Science Categories.
    """

    # Name of the category
    __cat_name__: str = "cs"

    #   cs.AI: Artificial Intelligence
    AI: dict = {"code": "AI", "name": "Artificial Intelligence"}
    #   cs.CL: Computation and Language
    CL: dict = {"code": "CL", "name": "Computation and Language"}
    #   cs.CV: Computer Vision and Pattern Recognition
    CV: dict = {"code": "CV", "name": "Computer Vision and Pattern Recognition"}
    #   cs.LG: Machine Learning
    LG: dict = {"code": "LG", "name": "Machine Learning"}
    #   cs.NE: Neural and Evolutionary Computing
    NE: dict = {"code": "NE", "name": "Neural and Evolutionary Computing"}
    #   cs.RO: Robotics
    RO: dict = {"code": "RO", "name": "Robotics"}

    def get_code(self) -> str:
        return f"{ComputerScienceCategory.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        return f"{self.value.get('name')}"
