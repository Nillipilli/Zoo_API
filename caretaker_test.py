import pytest

from zoo_objects import Animal, Caretaker


class TestCaretaker:
    def test_get_animals_empty_enclosure(self, caretaker1: Caretaker):
        """Test retrieving all animals of a caretaker with no animals 
        assigned."""
        assert len(caretaker1.get_animals()) == 0

    def test_get_animals_single_animal(self, caretaker1: Caretaker, animal1: Animal):
        """Test retrieving all animals of a caretaker with a single 
        animal assigned."""
        animal1.set_caretaker(caretaker1)
        assert len(caretaker1.get_animals()) == 1
        assert animal1 in caretaker1.get_animals()

    def test_get_animals_multiple_animals(self, caretaker1: Caretaker, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test retrieving all animals of a caretaker with multiple 
        animals assigned."""
        animal1.set_caretaker(caretaker1)
        animal2.set_caretaker(caretaker1)
        animal3.set_caretaker(caretaker1)

        assert len(caretaker1.get_animals()) == 3
        assert animal1 in caretaker1.get_animals()
        assert animal2 in caretaker1.get_animals()
        assert animal3 in caretaker1.get_animals()

    def test_to_json_without_animals(self, caretaker1: Caretaker):
        """Test converting the caretaker data to json like format 
        without any animals assigned."""
        assert caretaker1.to_json() == {
            "id": caretaker1.id,
            "name": caretaker1.name,
            "address": caretaker1.address,
            "animals": [],
        }

    def test_to_json_with_animals(self, caretaker1: Caretaker, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test converting the caretaker data to json like format with 
        animals assigned."""
        animal1.set_caretaker(caretaker1)
        animal2.set_caretaker(caretaker1)
        animal3.set_caretaker(caretaker1)
        assert caretaker1.to_json() == {
            "id": caretaker1.id,
            "name": caretaker1.name,
            "address": caretaker1.address,
            "animals": [animal1.id, animal2.id, animal3.id]
        }
