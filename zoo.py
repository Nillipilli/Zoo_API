from animal import Animal, Caretaker, Enclosure


class Zoo:
    def __init__(self) -> None:
        self.animals: list[Animal] = []

    def add_animal(self, animal: Animal) -> None:
        self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        self.animals.remove(animal)

    def get_animal(self, animal_id: str) -> Animal | None:
        for animal in self.animals:
            if animal.id == animal_id:
                return animal
