import pytest

from zoo import Zoo
from zoo_objects import Animal, Caretaker, Enclosure


class TestZooAnimal:
    def test_add_animal(self, zoo1: Zoo, animal1: Animal):
        """Test adding a single animal to the zoo."""
        zoo1.add_animal(animal1)
        assert len(zoo1.animals) == 1
        assert animal1 in zoo1.animals

    def test_add_multiple_animals(self, zoo1: Zoo, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test adding multiple animals to the zoo."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)
        zoo1.add_animal(animal3)

        assert (len(zoo1.animals) == 3)
        assert (animal1 in zoo1.animals)
        assert (animal2 in zoo1.animals)
        assert (animal3 in zoo1.animals)

    def test_add_animal_twice(self, zoo1: Zoo, animal1: Animal):
        """Test adding an animal twice to the zoo."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal1)

        assert (len(zoo1.animals) == 1)
        assert (animal1 in zoo1.animals)


class TestZooCaretaker:
    def test_add_caretaker(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test adding a single caretaker to the zoo."""
        zoo1.add_caretaker(caretaker1)
        assert len(zoo1.caretakers) == 1
        assert caretaker1 in zoo1.caretakers

    def test_add_multiple_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker):
        """Test adding multiple caretakers to the zoo."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)

        assert len(zoo1.caretakers) == 3
        assert caretaker1 in zoo1.caretakers
        assert caretaker2 in zoo1.caretakers
        assert caretaker3 in zoo1.caretakers

    def test_add_caretaker_twice(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test adding a caretaker twice to the zoo."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker1)

        assert len(zoo1.caretakers) == 1
        assert caretaker1 in zoo1.caretakers


class TestZooEnclosure:
    def test_add_enclosure(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test adding a single enclosure to the zoo."""
        zoo1.add_enclosure(enclosure1)
        assert len(zoo1.enclosures) == 1
        assert enclosure1 in zoo1.enclosures

    def test_add_multiple_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure):
        """Test adding multiple enclosures to the zoo."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        zoo1.add_enclosure(enclosure3)

        assert (len(zoo1.enclosures) == 3)
        assert (enclosure1 in zoo1.enclosures)
        assert (enclosure2 in zoo1.enclosures)
        assert (enclosure3 in zoo1.enclosures)

    def test_add_enclosure_twice(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test adding an enclosure twice to the zoo."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure1)

        assert (len(zoo1.enclosures) == 1)
        assert (enclosure1 in zoo1.enclosures)
