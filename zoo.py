from zoo_objects import Animal, Caretaker, Enclosure


class Zoo:
    def __init__(self) -> None:
        self.animals: list[Animal] = []
        self.caretakers: list[Caretaker] = []
        self.enclosures: list[Enclosure] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal to the zoo, but only if it does not already 
        exist."""
        if isinstance(animal, Animal):
            if animal not in self.animals:
                self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal from the zoo, but only if it exists.

        Take care of unsetting its home and removing it from the 
        corresponding enclosure."""
        if isinstance(animal, Animal):
            if animal in self.animals:
                animal.unset_home()
                animal.unset_caretaker()
                self.animals.remove(animal)

    def get_animal(self, animal_id: str) -> Animal | None:
        """Return an animal, but only if an animal with the given id 
        exists."""
        if isinstance(animal_id, str):
            for animal in self.animals:
                if animal.id == animal_id:
                    return animal

    def get_all_animals(self) -> list[Animal]:
        """Return a list of all animals."""
        return self.animals

    def add_caretaker(self, caretaker: Caretaker) -> None:
        """Add a new caretaker to the zoo, but only if she/he does not 
        already exist."""
        if isinstance(caretaker, Caretaker):
            if caretaker not in self.caretakers:
                self.caretakers.append(caretaker)

    def remove_caretaker(self, caretaker: Caretaker) -> bool:
        """Remove a caretaker from the zoo, but only if she/he
        exists."""
        if isinstance(caretaker, Caretaker):
            if caretaker in self.caretakers:
                if len(self.caretakers) == 1 and caretaker.get_animals():
                    return False
                else:
                    # use a generator expression to find the next
                    # possible caretaker and then move on. If no other
                    # caretaker exists set it to None.
                    new_caretaker = next(
                        (c for c in self.caretakers if c != caretaker), None)

                    if new_caretaker:
                        for animal in caretaker.get_animals():
                            pass
                            # TODO implement care_for method
                            # caretaker.care_for
                    self.caretakers.remove(caretaker)
        return True

    def get_caretaker(self, caretaker_id: str) -> Caretaker | None:
        """Return a caretaker, but only if a caretaker with the given 
        id exists."""
        if isinstance(caretaker_id, str):
            for caretaker in self.caretakers:
                if caretaker.id == caretaker_id:
                    return caretaker

    def get_all_caretakers(self) -> list[Caretaker]:
        """Return a list of all caretakers."""
        return self.caretakers

    def add_enclosure(self, enclosure: Enclosure) -> None:
        """Add a new enclosure to the zoo, but only if it does not 
        already exist."""
        if isinstance(enclosure, Enclosure):
            if enclosure not in self.enclosures:
                self.enclosures.append(enclosure)

    def remove_enclosure(self, enclosure: Enclosure) -> bool:
        """Remove an enclosure from the zoo, but only if it exists.

        Also make sure to move all animals that live in the given 
        enclosure to another enclosure before deleting it. If no other 
        enclosure exists that can provide housing to the animals, it is 
        not possible to delete the enclosure."""
        if isinstance(enclosure, Enclosure):
            if enclosure in self.enclosures:
                if len(self.enclosures) == 1 and enclosure.get_animals():
                    return False
                else:
                    # use a generator expression to find the next
                    # possible enclosure and then move on. If no other
                    # enclosure exists set it to None.
                    new_enclosure = next(
                        (e for e in self.enclosures if e != enclosure), None)

                    if new_enclosure:
                        for animal in enclosure.get_animals():
                            animal.set_home(new_enclosure)
                    self.enclosures.remove(enclosure)
        return True

    def get_enclosure(self, enclosure_id: str) -> Enclosure | None:
        """Return an enclosure, but only if an enclosure with the given 
        id exists."""
        if isinstance(enclosure_id, str):
            for enclosure in self.enclosures:
                if enclosure.id == enclosure_id:
                    return enclosure

    def get_all_enclosures(self) -> list[Enclosure]:
        """Return a list of all enclosures."""
        return self.enclosures
