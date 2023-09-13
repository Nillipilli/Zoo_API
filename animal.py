import uuid
import datetime


class Animal:
    def __init__(self, age: int, species_name: str, common_name: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.age = age
        self.species_name = species_name
        self.common_name = common_name
        self.enclosure: Enclosure | None = None
        self.caretaker: Caretaker | None = None
        self.feeding_record: list[str] = []
        self.medical_record: list[str] = []

    def set_home(self):
        pass

    def set_caretaker(self):
        pass

    def feed(self):
        pass
        # self.feeding_record.append(datetime.datetime.now())

    def medical_checkup(self):
        pass


class Caretaker:
    def __init__(self, name: str, address: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals: list[Animal] = []

    def add_animal(self):
        pass

    def remove_animal(self):
        pass


class Enclosure:
    def __init__(self, name: str, space: float) -> None:
        self.name = name
        self.space = space
        self.animals: list[Animal] = []
        self.cleaning_record: list[str] = []

    def add_animal(self):
        pass

    def remove_animal(self):
        pass

    def clean(self):
        pass
