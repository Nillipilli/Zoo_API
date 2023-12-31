import datetime

from zoo_objects import Animal, Caretaker, Enclosure


class Zoo:
    def __init__(self) -> None:
        self.animals: list[Animal] = []
        self.caretakers: list[Caretaker] = []
        self.enclosures: list[Enclosure] = []

    def add_animal(self, animal: Animal) -> None:
        """Add an animal to the zoo, but only if it does not already 
        exist."""
        # guard clause for invalid input
        if not isinstance(animal, Animal):
            return

        if animal not in self.animals:
            self.animals.append(animal)

    def remove_animal(self, animal: Animal) -> None:
        """Remove an animal from the zoo, but only if it exists.

        Also unset its home and the assigned caretaker."""
        if not isinstance(animal, Animal):
            return

        if animal in self.animals:
            animal.unset_home()
            animal.unset_caretaker()
            self.animals.remove(animal)

    def get_animal(self, animal_id: str) -> Animal | None:
        """Return an animal, but only if an animal with the given ID 
        exists."""
        if not isinstance(animal_id, str):
            return

        for animal in self.animals:
            if animal.id == animal_id:
                return animal

    def get_all_animals(self) -> list[Animal]:
        """Return a list of all animals."""
        return self.animals

    def get_animal_stats(self) -> dict:
        """Return some statistics about animals:

        - Amount of animals per species."""
        species_count = {}
        for animal in self.get_all_animals():
            species_name = animal.species_name
            if species_name in species_count:
                species_count[species_name] += 1
            else:
                species_count[species_name] = 1

        return {'animals_per_species': species_count}

    def add_caretaker(self, caretaker: Caretaker) -> None:
        """Add a new caretaker to the zoo, but only if she/he does not 
        already exist."""
        if not isinstance(caretaker, Caretaker):
            return

        if caretaker not in self.caretakers:
            self.caretakers.append(caretaker)

    def remove_caretaker(self, caretaker: Caretaker) -> bool | None:
        """Remove a caretaker from the zoo, but only if she/he
        exists."""
        if not isinstance(caretaker, Caretaker):
            return

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
                        animal.set_caretaker(new_caretaker)
                self.caretakers.remove(caretaker)
        return True

    def get_caretaker(self, caretaker_id: str) -> Caretaker | None:
        """Return a caretaker, but only if a caretaker with the given 
        ID exists."""
        if not isinstance(caretaker_id, str):
            return

        for caretaker in self.caretakers:
            if caretaker.id == caretaker_id:
                return caretaker

    def get_all_caretakers(self) -> list[Caretaker]:
        """Return a list of all caretakers."""
        return self.caretakers

    def get_caretaker_stats(self) -> dict:
        """Return some statistics about caretakers:

        - minimum number of animals assigned to one caretaker
        - maximum number of animals assigned to one caretaker
        - average number of animals assigned to caretakers."""
        animals_under_supervision = [
            len(caretaker.get_animals()) for caretaker in self.caretakers]
        return {
            'minimum_animals_under_supervision': 0 if not animals_under_supervision else min(animals_under_supervision),
            'maximum_animals_under_supervision': 0 if not animals_under_supervision else max(animals_under_supervision),
            'average_animals_under_supervision': 0 if not animals_under_supervision else sum(animals_under_supervision) / len(animals_under_supervision)
        }

    def add_enclosure(self, enclosure: Enclosure) -> None:
        """Add a new enclosure to the zoo, but only if it does not 
        already exist."""
        if not isinstance(enclosure, Enclosure):
            return

        if enclosure not in self.enclosures:
            self.enclosures.append(enclosure)

    def remove_enclosure(self, enclosure: Enclosure) -> bool | None:
        """Remove an enclosure from the zoo, but only if it exists.

        Also make sure to move all animals that live in the given 
        enclosure to another enclosure before deleting it. If no other 
        enclosure exists that can provide housing to the animals, it is 
        not possible to delete the enclosure."""
        if not isinstance(enclosure, Enclosure):
            return

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
        ID exists."""
        if not isinstance(enclosure_id, str):
            return

        for enclosure in self.enclosures:
            if enclosure.id == enclosure_id:
                return enclosure

    def get_all_enclosures(self) -> list[Enclosure]:
        """Return a list of all enclosures."""
        return self.enclosures

    def get_enclosure_stats(self) -> dict:
        """Return some statistics about enclosures:

        - average number of animals in enclosures
        - enclosures with multiple different animal species
        - available space per animal per enclosure

        I decided to use enclosure ID as key instead of the whole object
        because I could not manage to encode the dictionaries in the API
        otherwise."""
        animals_in_enclosures = [len(enclosure.get_animals())
                                 for enclosure in self.enclosures]

        enclosures_with_multiple_species = {}
        for enclosure in self.enclosures:
            animal_species_names = sorted({animal.species_name for animal in enclosure.get_animals()})
            if len(animal_species_names) > 1:
                enclosures_with_multiple_species[enclosure.id] = animal_species_names

        available_space_per_animal_per_enclosure = {}
        for enclosure in self.enclosures:
            animals = len(enclosure.get_animals())
            if animals == 0:
                available_space_per_animal_per_enclosure[enclosure.id] = enclosure.area
            else:
                available_space_per_animal_per_enclosure[enclosure.id] = enclosure.area / animals

        return {
            'average_animals_per_enclosure': 0 if not animals_in_enclosures else sum(animals_in_enclosures) / len(animals_in_enclosures),
            'enclosures_with_multiple_species': enclosures_with_multiple_species,
            'available_space_per_animal_per_enclosure': available_space_per_animal_per_enclosure
        }

    def generate_feeding_plan(self) -> dict:
        """Generate a feeding plan for every animal."""
        feeding_plan = {}
        idx = 0
        for animal in self.animals:
            feeding_date = self._calculate_next_date(animal.feeding_record, 2)
            selected_caretaker, idx = self._select_caretaker(idx)

            feeding_plan[animal.id] = {
                'date': feeding_date, 'caretaker': selected_caretaker}

        return feeding_plan

    def generate_medical_plan(self) -> dict:
        """Generate a medical checkup plan for every animal."""
        medical_plan = {}
        idx = 0
        for animal in self.animals:
            medical_date = self._calculate_next_date(animal.medical_record, 35)
            selected_caretaker, idx = self._select_caretaker(idx)

            medical_plan[animal.id] = {
                'date': medical_date, 'caretaker': selected_caretaker}

        return medical_plan

    def generate_cleaning_plan(self) -> dict:
        """Generate a cleaning plan for every enclosure."""
        cleaning_plan = {}
        idx = 0
        for enclosure in self.enclosures:
            cleaning_date = self._calculate_next_date(
                enclosure.cleaning_record, 3)
            selected_caretaker, idx = self._select_caretaker(idx)

            cleaning_plan[enclosure.id] = {
                'date': cleaning_date, 'caretaker': selected_caretaker}

        return cleaning_plan

    def _calculate_next_date(self, records: list[datetime.datetime], days: int) -> datetime.datetime:
        """Calculate the next cleaning, feeding or medical checkup 
        date based on the last record."""
        if not records:
            next_date = datetime.datetime.now()
        else:
            next_date = records[-1] + datetime.timedelta(days=days)
        return next_date

    def _select_caretaker(self, idx: int) -> tuple[str, int]:
        """Select a responsibl caretaker by just going through the 
        list of available caretakers. If at the end of the list start
        again from the beginning."""
        if self.caretakers:
            selected_caretaker = self.caretakers[idx].id
            idx = (idx + 1) % len(self.caretakers)
        else:
            selected_caretaker = ''
        return selected_caretaker, idx
