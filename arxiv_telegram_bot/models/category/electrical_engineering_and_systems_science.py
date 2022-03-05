from enum import Enum


class ElectricalEngineeringAndSystemsScience(dict, Enum):
    """
    # Computer Science Category

    This enumerator holds all categories required for Computer Science Categories.
    """

    # Name of the category
    __cat_name__: str = "eess"

    AS: dict = {"code": "AS", "name": "Audio and Speech Processing"}
    IV: dict = {"code": "IV", "name": "Image and Video Processing"}
    SP: dict = {"code": "SP", "name": "Signal Processing"}
    SY: dict = {"code": "SY", "name": "Systems and Control"}

    def get_code(self) -> str:
        return f"{ElectricalEngineeringAndSystemsScience.__cat_name__}.{self.value.get('code')}"

    def get_name(self) -> str:
        return f"{self.value.get('name')}"
