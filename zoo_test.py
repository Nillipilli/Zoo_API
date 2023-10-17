import pytest

from zoo import Zoo
from zoo_objects import Animal, Caretaker, Enclosure


class TestZooAnimal:
    def test_add_animal(self, zoo1: Zoo, animal1: Animal):
        """Test adding a single animal."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1
        assert animal1 in zoo1.animals

    def test_add_multiple_animals(self, zoo1: Zoo, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test adding multiple animals."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)
        zoo1.add_animal(animal3)

        assert len(zoo1.animals) == 3
        assert animal1 in zoo1.animals
        assert animal2 in zoo1.animals
        assert animal3 in zoo1.animals

    def test_add_animal_twice(self, zoo1: Zoo, animal1: Animal):
        """Test adding an animal twice."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal1)

        assert len(zoo1.animals) == 1
        assert animal1 in zoo1.animals

    def test_remove_animal(self, zoo1: Zoo, animal1: Animal):
        """Test removing a single animal."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1
        assert animal1 in zoo1.animals

        zoo1.remove_animal(animal1)
        assert len(zoo1.animals) == 0

    def test_remove_multiple_animals(self, zoo1: Zoo, animal1: Animal, animal2: Animal):
        """Test removing multiple animals."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)

        assert len(zoo1.animals) == 2
        assert animal1 in zoo1.animals
        assert animal2 in zoo1.animals

        zoo1.remove_animal(animal1)
        zoo1.remove_animal(animal2)
        assert len(zoo1.animals) == 0

    def test_remove_animal_twice(self, zoo1: Zoo, animal1: Animal):
        """Test removing the same animal twice."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1

        zoo1.remove_animal(animal1)
        zoo1.remove_animal(animal1)
        assert len(zoo1.animals) == 0

    def test_remove_animal_with_home(self, zoo1: Zoo, animal1: Animal, enclosure1: Enclosure):
        """Test removing an animal that has a home assigned to it."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1

        animal1.set_home(enclosure1)
        assert animal1.enclosure == enclosure1
        assert len(enclosure1.animals) == 1
        assert animal1 in enclosure1.animals

        zoo1.remove_animal(animal1)
        assert len(zoo1.animals) == 0
        assert animal1.enclosure is None
        assert len(enclosure1.animals) == 0

    def test_remove_animal_with_caretaker(self, zoo1: Zoo, animal1: Animal, caretaker1: Caretaker):
        """Test removing an animal that has a caretaker assigned 
        to it."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1

        animal1.set_caretaker(caretaker1)
        assert animal1.caretaker == caretaker1
        assert len(caretaker1.animals) == 1
        assert animal1 in caretaker1.animals

        zoo1.remove_animal(animal1)
        assert len(zoo1.animals) == 0
        assert animal1.caretaker is None
        assert len(caretaker1.animals) == 0

    def test_remove_animal_with_home_and_caretaker(self, zoo1: Zoo, animal1: Animal, enclosure1: Enclosure, caretaker1: Caretaker):
        """Test removing an animal that has a home and a caretaker 
        assigned to it."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1

        animal1.set_home(enclosure1)
        animal1.set_caretaker(caretaker1)
        assert animal1.enclosure == enclosure1
        assert animal1.caretaker == caretaker1
        assert len(enclosure1.animals) == 1
        assert len(caretaker1.animals) == 1
        assert animal1 in enclosure1.animals
        assert animal1 in caretaker1.animals

        zoo1.remove_animal(animal1)
        assert animal1.enclosure == None
        assert animal1.caretaker == None
        assert len(enclosure1.animals) == 0
        assert len(caretaker1.animals) == 0

    def test_get_animal(self, zoo1: Zoo, animal1: Animal):
        """Test getting an animal via an existing animal ID."""
        zoo1.add_animal(animal1)
        assert zoo1.get_animal(animal1.id) == animal1

    def test_get_animal_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting an animal via a not existing animal ID."""
        assert zoo1.get_animal(unknown_id) is None

    def test_get_all_animals_empty(self, zoo1: Zoo):
        """Test getting all animal information without animals."""
        assert len(zoo1.get_all_animals()) == 0

    def test_get_all_animals(self, zoo1: Zoo, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test getting all information about the existing animals."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)
        zoo1.add_animal(animal3)

        assert len(zoo1.get_all_animals()) == 3
        assert animal1 in zoo1.get_all_animals()
        assert animal2 in zoo1.get_all_animals()
        assert animal3 in zoo1.get_all_animals()


class TestZooCaretaker:
    def test_add_caretaker(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test adding a single caretaker."""
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 1
        assert caretaker1 in zoo1.caretakers

    def test_add_multiple_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker):
        """Test adding multiple caretakers."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)

        assert len(zoo1.caretakers) == 3
        assert caretaker1 in zoo1.caretakers
        assert caretaker2 in zoo1.caretakers
        assert caretaker3 in zoo1.caretakers

    def test_add_caretaker_twice(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test adding a caretaker twice."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker1)

        assert len(zoo1.caretakers) == 1
        assert caretaker1 in zoo1.caretakers

    def test_remove_caretaker(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test removing a single caretaker."""
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 1
        assert caretaker1 in zoo1.caretakers

        zoo1.remove_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 0

    def test_remove_multiple_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker):
        """Test removing multiple caretakers."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)

        assert len(zoo1.caretakers) == 2
        assert caretaker1 in zoo1.caretakers
        assert caretaker2 in zoo1.caretakers

        zoo1.remove_caretaker(caretaker1)
        zoo1.remove_caretaker(caretaker2)
        assert len(zoo1.caretakers) == 0

    def test_remove_caretaker_twice(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test removing a caretaker twice."""
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 1

        zoo1.remove_caretaker(caretaker1)
        zoo1.remove_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 0

    def test_remove_caretaker_with_animal_no_other_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, animal1: Animal):
        """Test removing a caretaker that has an animal assigned,
        while no other caretaker exists.

        It is not possible to delete this caretaker."""
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 1

        animal1.set_caretaker(caretaker1)

        assert zoo1.remove_caretaker(caretaker1) is False
        assert len(zoo1.caretakers) == 1

    def test_remove_caretaker_with_animal_and_other_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker, animal1: Animal):
        """Test removing a caretaker that has an animal assigned,
        while at least one other caretaker exists.

        It is possible to delete the caretaker. The animal gets added to
        the next caretaker in the list."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)
        assert len(zoo1.caretakers) == 3

        animal1.set_caretaker(caretaker1)
        assert animal1.caretaker == caretaker1
        assert len(caretaker1.animals) == 1
        assert animal1 in caretaker1.animals

        assert zoo1.remove_caretaker(caretaker1) is True
        assert len(zoo1.caretakers) == 2

        assert animal1.caretaker == caretaker2
        assert len(caretaker1.animals) == 0
        assert len(caretaker2.animals) == 1
        assert animal1 in caretaker2.animals

    def test_get_caretaker(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test getting a caretaker via an existing caretaker ID."""
        zoo1.add_caretaker(caretaker1)
        assert zoo1.get_caretaker(caretaker1.id) == caretaker1

    def test_get_caretaker_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting a caretaker via a not existing caretaker ID."""
        assert zoo1.get_caretaker(unknown_id) is None

    def test_get_all_caretakers_empty(self, zoo1: Zoo):
        """Test getting all caretaker information without caretakers."""
        assert len(zoo1.get_all_caretakers()) == 0

    def test_get_all_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker):
        """Test getting all information about the existing caretakers."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)

        assert len(zoo1.get_all_caretakers()) == 3
        assert caretaker1 in zoo1.get_all_caretakers()
        assert caretaker2 in zoo1.get_all_caretakers()
        assert caretaker3 in zoo1.get_all_caretakers()

    def test_get_caretaker_stats_no_caretakers(self, zoo1: Zoo):
        """Test getting all caretaker stats without any caretakers added
        to the zoo so far."""
        assert zoo1.get_caretaker_stats() == {
            'minimum_animals_under_supervision': None,
            'maximum_animals_under_supervision': None,
            'average_animals_under_supervision': None
        }

    def test_get_caretaker_stats_no_animals(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test getting all caretaker stats with no animals added to any
        caretaker."""
        zoo1.add_caretaker(caretaker1)
        assert zoo1.get_caretaker_stats() == {
            'minimum_animals_under_supervision': 0,
            'maximum_animals_under_supervision': 0,
            'average_animals_under_supervision': 0
        }

    def test_get_caretaker_stats_with_animals(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker,
                                              animal1: Animal, animal2: Animal, animal3: Animal):
        """Test getting all caretaker stats with animals added to 
        caretakers."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)

        caretaker1.add_animal(animal1)
        caretaker2.add_animal(animal2)
        caretaker2.add_animal(animal3)

        assert zoo1.get_caretaker_stats() == {
            'minimum_animals_under_supervision': 0,
            'maximum_animals_under_supervision': 2,
            'average_animals_under_supervision': 1
        }


class TestZooEnclosure:
    def test_add_enclosure(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test adding a single enclosure."""
        zoo1.add_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 1
        assert enclosure1 in zoo1.enclosures

    def test_add_multiple_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure):
        """Test adding multiple enclosures."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        zoo1.add_enclosure(enclosure3)

        assert len(zoo1.enclosures) == 3
        assert enclosure1 in zoo1.enclosures
        assert enclosure2 in zoo1.enclosures
        assert enclosure3 in zoo1.enclosures

    def test_add_enclosure_twice(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test adding an enclosure twice."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure1)

        assert len(zoo1.enclosures) == 1
        assert enclosure1 in zoo1.enclosures

    def test_remove_enclosure(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test removing a single enclosure."""
        zoo1.add_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 1
        assert enclosure1 in zoo1.enclosures

        zoo1.remove_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 0

    def test_remove_multiple_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure):
        """Test removing multiple enclosures."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)

        assert len(zoo1.enclosures) == 2
        assert enclosure1 in zoo1.enclosures
        assert enclosure2 in zoo1.enclosures

        zoo1.remove_enclosure(enclosure1)
        zoo1.remove_enclosure(enclosure2)
        assert len(zoo1.enclosures) == 0

    def test_remove_enclosure_twice(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test removing an enclosure twice."""
        zoo1.add_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 1

        zoo1.remove_enclosure(enclosure1)
        zoo1.remove_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 0

    def test_remove_enclosure_with_animal_no_other_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, animal1: Animal):
        """Test removing an enclosure that is the home of an animal 
        while no other enclosure exists.

        It is not possible to delete this enclosure."""
        zoo1.add_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 1

        animal1.set_home(enclosure1)

        assert zoo1.remove_enclosure(enclosure1) is False
        assert len(zoo1.enclosures) == 1

    def test_remove_enclosure_with_animal_and_other_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure, animal1: Animal):
        """Test removing an enclosure that is the home of an animal 
        while at least one other enclosure exists.

        It is possible to delete the enclosure. The animal gets added to
        the next enclosure in the list."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        zoo1.add_enclosure(enclosure3)
        assert len(zoo1.enclosures) == 3

        animal1.set_home(enclosure1)
        assert animal1.enclosure == enclosure1
        assert len(enclosure1.animals) == 1
        assert animal1 in enclosure1.animals

        assert zoo1.remove_enclosure(enclosure1) is True
        assert len(zoo1.enclosures) == 2

        assert animal1.enclosure == enclosure2
        assert len(enclosure1.animals) == 0
        assert len(enclosure2.animals) == 1
        assert animal1 in enclosure2.animals

    def test_get_enclosure(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test getting an enclosure via an existing enclosure ID."""
        zoo1.add_enclosure(enclosure1)
        assert zoo1.get_enclosure(enclosure1.id) == enclosure1

    def test_get_enclosure_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting an enclosure via a not existing enclosure ID."""
        assert zoo1.get_enclosure(unknown_id) is None

    def test_get_all_enclosures_empty(self, zoo1: Zoo):
        """Test getting all enclosure information without enclosures."""
        assert len(zoo1.get_all_enclosures()) == 0

    def test_get_all_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure):
        """Test getting all information about the existing 
        enclosures."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        zoo1.add_enclosure(enclosure3)

        assert len(zoo1.get_all_enclosures()) == 3
        assert enclosure1 in zoo1.get_all_enclosures()
        assert enclosure2 in zoo1.get_all_enclosures()
        assert enclosure3 in zoo1.get_all_enclosures()
