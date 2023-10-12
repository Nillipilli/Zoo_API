import uuid
import datetime
from typing import TypeAlias

# use this when normal type aliases for classes do not work correctly
animal_: TypeAlias = 'Animal'
enclosure_: TypeAlias = 'Enclosure'
caretaker_: TypeAlias = 'Caretaker'


class Animal:
    def __init__(self, species_name: str, common_name: str, age: int) -> None:
        self.id: str = str(uuid.uuid4())
        self.species_name = species_name
        self.common_name = common_name
        self.age = age
        self.enclosure: Enclosure | None = None
        self.caretaker: Caretaker | None = None
        self.feeding_record: list[datetime.datetime] = []
        self.medical_record: list[datetime.datetime] = []

    def set_home(self, enclosure: enclosure_):
        """Assign the given enclosure to this animal and add this animal
        to the list of animals in this enclosure.

        If the animal gets moved from one enclosure to another remove
        the animal from the old enclosure's list of animals."""
        if isinstance(enclosure, Enclosure):
            if self.enclosure is not None:
                self.enclosure.remove_animal(self)
            self.enclosure = enclosure
            enclosure.add_animal(self)

    def unset_home(self):
        """Remove the animal from the enclosure it used to live in and 
        set its enclosure to its default value."""
        if self.enclosure is not None:
            self.enclosure.remove_animal(self)
            self.enclosure = None

    def set_caretaker(self, caretaker: caretaker_):
        """Assign the given caretaker to this animal and add this animal
        to the list of animals assigned to the caretaker.

        If the animal gets moved from one caretaker to another remove
        the animal from the old caretakers' list of animals."""
        if isinstance(caretaker, Caretaker):
            if self.caretaker is not None:
                self.caretaker.remove_animal(self)
            self.caretaker = caretaker
            caretaker.add_animal(self)

    def feed(self):
        """Add a new feeding record."""
        self.feeding_record.append(datetime.datetime.now())

    def vet(self):
        """Add a new medical record."""
        self.medical_record.append(datetime.datetime.now())

    def birth(self) -> animal_:
        """Give birth to a new animal.

        The newborn shares the same species name, common name and 
        enclosure to live in."""
        new_animal = Animal(self.species_name, self.common_name, 0)
        new_animal.enclosure = self.enclosure
        return new_animal

    def to_json(self):
        """To avoid circular references use this custom json encoding,
        when displaying an Animal.

        Instead of displaying the whole 'enclosure' and 'caretaker' 
        objects just show the corresponding ID."""
        return {
            "id": self.id,
            "species_name": self.species_name,
            "common_name": self.common_name,
            "age": self.age,
            "enclosure": self.enclosure.id if self.enclosure else None,
            "caretaker": self.caretaker.id if self.caretaker else None,
            "feeding_record": self.feeding_record,
            "medical_record": self.medical_record,
        }


class Caretaker:
    def __init__(self, name: str, address: str) -> None:
        self.id: str = str(uuid.uuid4())
        self.name = name
        self.address = address
        self.animals: list[Animal] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal, but only if it does not already exist."""
        if isinstance(animal, Animal):
            if animal not in self.animals:
                self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal, but only if it exists."""
        if isinstance(animal, Animal):
            if animal in self.animals:
                self.animals.remove(animal)

    def to_json(self):
        """To avoid circular references use this custom json encoding,
        when displaying a Caretaker.

        Instead of displaying all 'animal' objects just show the 
        corresponding IDs."""
        return {
            "id": self.id,
            "name": self.name,
            "address": self.address,
            "animals": [animal.id for animal in self.animals],
        }


class Enclosure:
    def __init__(self, name: str, area: float) -> None:
        self.id: str = str(uuid.uuid4())
        self.name = name
        self.area = area
        self.animals: list[Animal] = []
        self.cleaning_record: list[datetime.datetime] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal, but only if it does not already exist."""
        if isinstance(animal, Animal):
            if animal not in self.animals:
                self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal, but only if it exists."""
        if isinstance(animal, Animal):
            if animal in self.animals:
                self.animals.remove(animal)

    def get_animals(self) -> list[Animal]:
        """Return a list of animals that live in this enclosure."""
        return self.animals

    def clean(self):
        """Add a new cleaning record."""
        self.cleaning_record.append(datetime.datetime.now())

    def to_json(self):
        """To avoid circular references use this custom json encoding,
        when displaying an Enclosure.

        Instead of displaying all 'animal' objects just show the 
        corresponding IDs."""
        return {
            "id": self.id,
            "name": self.name,
            "area": self.area,
            "animals": [animal.id for animal in self.animals],
            "cleaning_record": self.cleaning_record,
        }


if __name__ == '__main__':
    a = Animal('Tigris', 'Tiger', 1)
    a.feed()
    print(a.feeding_record)

    e = Enclosure('cage', 100)
    a.set_home(e)
    print(a.enclosure)
