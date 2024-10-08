from dataclasses import dataclass, field
import random


@dataclass
class CommonData:
    _data: str = "game/data/"

    """Выгружаем дату"""
    def get_data(self, gender: str, need_part: str, ethnicity: str) -> list:
        with open(self._data + gender + "/"
                  + ethnicity + "/"
                  + need_part + ".txt", "r", encoding='utf-8') as file:
            data = file.read().splitlines()
            result: list = data[0].split(",")
        return result


@dataclass
class Player:
    name: str = "None"
    gender: str = "None"
    hit_points: int = 0
    strain: int = 0
    implant_points: int = 0
    inventory: list = field(default_factory=lambda: [])
    implant_in: list = field(default_factory=lambda: [])

    def load_check(self) -> int:
        chance_to_strain: int = self.implant_points // 1000
        return chance_to_strain

    def if_equip(self) -> list:
        equipment: list = []
        for euip in self.inventory:
            if euip.is_equiped is True:
                equipment.append(euip)
        return equipment

    def get_actions(self) -> list:
        implant_actions: list = []
        for implant_action in self.implant_in:
            if implant_action.action != "None":
                implant_actions.append(implant_action)
        return implant_actions


@dataclass
class Action:
    name: str = "None"
    descrip: str = "None"
    type: str = "None"
    value: int = 0

    def action_use(self) -> str:
        return self.descrip

    def value_count(self) -> str:
        return self.value


@dataclass
class Implant:
    name: str = "None"
    descrip: str = "None"
    type: str = "None"
    marks: str = "None"
    value: int = 0
    action: Action = field(default_factory=Action())

    def use_implant(self):
        return self.action.action_use()
    
    def value_count(self):
        return self.value + self.action.value_count()

    def create_implant(self, name,
                       descrip, type,
                       marks, value):
        self.__dict__["name"] = name
        self.__dict__["descrip"] = descrip
        self.__dict__["type"] = type
        self.__dict__["marks"] = marks
        self.__dict__["value"] = value


@dataclass
class NPC:
    name: str = "None"
    age: int = 18
    gender: str = "None"
    view: dict = field(default_factory=lambda: {"face": "",
                                                "eyes": "",
                                                "hair": "",
                                                "hair_color": "",
                                                "breast": "",
                                                "body": ""})
    relation: int = 0
    implant_in: list = field(default_factory=lambda: [])
    inventory: list = field(default_factory=lambda: [])

    def generate_view(self):
        work_dict = {}
        self.__dict__["gender"] = random.choice(["male", "female"])
        ethnicity: str = random.choice(["african", "germanic", "slavic"])
        data = CommonData().get_data(self.gender,
                                     "names",
                                     ethnicity)
        self.__dict__["name"] = random.choice(data)
        self.__dict__["age"] = random.randrange(18, 200)
        for part in self.view.keys():
            part_data: list = CommonData().get_data(self.gender,
                                                    part,
                                                    ethnicity)
            work_dict[part] = random.choice(part_data)
        self.__dict__["view"] = work_dict

    def __post_init__(self):
        self.generate_view()

    def common_view(self) -> str:
        head_descrip: str = self.view["Head"]
        body_descrip: str = self.view["Body"]
        legs_descrip: str = self.view["Legs"]
        return f"{head_descrip} {body_descrip} {legs_descrip}"

    def implant_get_descrip(self) -> dict:
        implant_dict: dict = {"ImplantHead": [],
                              "ImplantBody": [],
                              "ImplantLegs": [],
                              "ImplantHands": []}
        for implant in self.implant_in:
            if implant.type == "Head":
                implant_dict["ImplantHead"].append(implant)
            elif implant.type == "Body":
                implant_dict["ImplantBody"].append(implant)
            elif implant.type == "Legs":
                implant_dict["ImplantLegs"].append(implant)
            elif implant.type == "Hands":
                implant_dict["ImplantHands"].append(implant)
        return implant_dict
    
    def final_descrip(self):
        gender_detected: str = ""
        if self.gender == "male":
            gender_detected = "he"
        else:
            gender_detected = "she"
        return (f"""{self.name}.
                    A {self.gender} with{self.view["body"]} body {gender_detected}
                    have a{self.view["face"]} face with{self.view["eyes"]} eyes.
                    Also {gender_detected} have{self.view["hair_color"]}{self.view["hair"]} hair.
                    And final {gender_detected} have{self.view["breast"]}""")

    def __str__(self) -> str:
        return f"""Имя: {self.name}
Возраст: {self.age}
Пол: {self.gender}
Лицо: {self.view["face"]}
Глаза: {self.view["eyes"]}
Волосы: {self.view["hair"]}
Цвет волос: {self.view["hair_color"]}
Грудь: {self.view["breast"]}
Тело: {self.view["body"]}
Финальное описание:{self.final_descrip()}
"""


x = CommonData().get_data("male", "eyes", "african")
print(x)
example = NPC()
print(example)
