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

    def test_remove_animal_twice(self, zoo1: Zoo, animal1: Animal, animal2):
        """Test removing the same animal twice."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)
        assert len(zoo1.animals) == 2

        zoo1.remove_animal(animal1)
        zoo1.remove_animal(animal1)
        assert len(zoo1.animals) == 1

    def test_get_animal(self, zoo1: Zoo, animal1: Animal):
        """Test getting an animal via an existing animal ID."""
        zoo1.add_animal(animal1)
        assert zoo1.get_animal(animal1.id) == animal1

    def test_get_animal_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting an animal via a not existing animal ID."""
        assert zoo1.get_animal(unknown_id) is None

    def test_get_all_animals(self, zoo1: Zoo, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test getting all information about the existing animals."""
        zoo1.add_animal(animal1)
        zoo1.add_animal(animal2)
        zoo1.add_animal(animal3)

        assert len(zoo1.get_all_animals()) == 3
        assert animal1 in zoo1.get_all_animals()
        assert animal2 in zoo1.get_all_animals()
        assert animal3 in zoo1.get_all_animals()

    def test_get_all_animals_empty(self, zoo1: Zoo):
        """Test getting all animal information without animals."""
        assert len(zoo1.get_all_animals()) == 0


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

    def test_get_caretaker(self, zoo1: Zoo, caretaker1: Caretaker):
        """Test getting a caretaker via an existing caretaker ID."""
        zoo1.add_caretaker(caretaker1)
        assert zoo1.get_caretaker(caretaker1.id) == caretaker1

    def test_get_caretaker_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting a caretaker via a not existing caretaker ID."""
        assert zoo1.get_caretaker(unknown_id) is None

    def test_get_all_caretakers(self, zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker):
        """Test getting all information about the existing caretakers."""
        zoo1.add_caretaker(caretaker1)
        zoo1.add_caretaker(caretaker2)
        zoo1.add_caretaker(caretaker3)

        assert len(zoo1.get_all_caretakers()) == 3
        assert caretaker1 in zoo1.get_all_caretakers()
        assert caretaker2 in zoo1.get_all_caretakers()
        assert caretaker3 in zoo1.get_all_caretakers()

    def test_get_all_caretakers_empty(self, zoo1: Zoo):
        """Test getting all caretaker information without caretakers."""
        assert len(zoo1.get_all_caretakers()) == 0


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

    def test_get_enclosure(self, zoo1: Zoo, enclosure1: Enclosure):
        """Test getting an enclosure via an existing enclosure ID."""
        zoo1.add_enclosure(enclosure1)
        assert zoo1.get_enclosure(enclosure1.id) == enclosure1

    def test_get_enclosure_not_existing(self, zoo1: Zoo, unknown_id: str):
        """Test getting an enclosure via a not existing enclosure ID."""
        assert zoo1.get_enclosure(unknown_id) is None

    def test_get_all_enclosures(self, zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure):
        """Test getting all information about the existing enclosures."""
        zoo1.add_enclosure(enclosure1)
        zoo1.add_enclosure(enclosure2)
        zoo1.add_enclosure(enclosure3)

        assert len(zoo1.get_all_enclosures()) == 3
        assert enclosure1 in zoo1.get_all_enclosures()
        assert enclosure2 in zoo1.get_all_enclosures()
        assert enclosure3 in zoo1.get_all_enclosures()

    def test_get_all_enclosures_empty(self, zoo1: Zoo):
        """Test getting all enclosure information without enclosures."""
        assert len(zoo1.get_all_enclosures()) == 0
