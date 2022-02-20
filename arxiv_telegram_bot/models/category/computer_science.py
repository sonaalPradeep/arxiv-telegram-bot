from enum import Enum


class ComputerScienceCategory(str, Enum):
    """
    # Computer Science Category

    This enumerator holds all categories required for Computer Science Categories.
    """

    # Name of the category
    __cat_name__: str = "cs"

    #   cs.AI: Artificial Intelligence
    AI: str = "AI"
    #   cs.CL: Computation and Language
    CL: str = "CL"
    #   cs.CV: Computer Vision and Pattern Recognition
    CV: str = "CV"
    #   cs.LG: Machine Learning
    LG: str = "LG"
    #   cs.NE: Neural and Evolutionary Computing
    NE: str = "NE"
    #   cs.RO: Robotics
    RO: str = "RO"

    def get_code(self) -> str:
        return f"{ComputerScienceCategory.__cat_name__}.{self.value}"
