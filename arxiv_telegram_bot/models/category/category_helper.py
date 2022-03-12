from arxiv_telegram_bot.models.category.computer_science import ComputerScienceCategory
from arxiv_telegram_bot.models.category.electrical_engineering_and_systems_science import (
    ElectricalEngineeringAndSystemsScience,
)


class CategoryHelper:
    def __init__(self):
        super(CategoryHelper, self).__init__()

        self.categories_list = [
            "Computer Science",
            "Electrical Engineering and Systems Science",
        ]
        self.enum_list = [
            ComputerScienceCategory,
            ElectricalEngineeringAndSystemsScience,
        ]
        self.category_enum_mapping = dict(zip(self.categories_list, self.enum_list))
        self.name_code_mapping = {}

        for category, enum in self.category_enum_mapping.items():
            topic_code_mapping = {x.get_name(): x.get_code() for x in list(enum)}
            self.name_code_mapping[category] = topic_code_mapping

    def get_code_from_name(self, category, topic):
        return self.name_code_mapping.get(category).get(topic)
