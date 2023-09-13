from animal import Animal, Caretaker, Enclosure


class Zoo:
    def __init__(self) -> None:
        self.animals: list[Animal] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal to the zoo, but only if it is not already part 
        of it"""
        if isinstance(animal, Animal):
            if animal not in self.animals:
                self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal from the zoo, but only if it is part of the 
        zoo."""
        if isinstance(animal, Animal):
            if animal in self.animals:
                self.animals.remove(animal)

    def get_animal(self, animal_id: str) -> Animal | None:
        """Return an animal, but only if an animal with the given id 
        exists."""
        if isinstance(animal_id, str):
            for animal in self.animals:
                if animal.id == animal_id:
                    return animal
