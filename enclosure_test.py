import pytest
from datetime import datetime

from zoo_objects import Enclosure, Animal


class TestEnclosure:
    def test_get_all_animals_empty_enclosure(self, enclosure1: Enclosure):
        """Test retrieving all animals inside an empty enclosure."""
        assert len(enclosure1.get_animals()) == 0

    def test_get_all_animals_single_animal(self, enclosure1: Enclosure, animal1: Animal):
        """Test retrieving all animals in an enclosure with a single 
        animal in it."""
        animal1.set_home(enclosure1)
        assert len(enclosure1.get_animals()) == 1
        assert animal1 in enclosure1.get_animals()

    def test_get_all_animals_multiple_animals(self, enclosure1: Enclosure, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test retrieving all animals in an enclosure with many 
        animals."""
        animal1.set_home(enclosure1)
        animal2.set_home(enclosure1)
        animal3.set_home(enclosure1)

        assert len(enclosure1.get_animals()) == 3
        assert animal1 in enclosure1.get_animals()
        assert animal2 in enclosure1.get_animals()
        assert animal3 in enclosure1.get_animals()

    def test_clean_enclosure(self, enclosure1: Enclosure):
        """Test clean an enclosure once."""
        enclosure1.clean()
        assert len(enclosure1.cleaning_record) == 1
        assert isinstance(enclosure1.cleaning_record[0], datetime)

    def test_clean_enclosure_multiple_times(self, enclosure1: Enclosure):
        """Test clean an enclosure multiple_times."""
        enclosure1.clean()
        enclosure1.clean()
        enclosure1.clean()
        enclosure1.clean()
        enclosure1.clean()

        assert len(enclosure1.cleaning_record) == 5
        for record in enclosure1.cleaning_record:
            assert isinstance(record, datetime)

    def test_to_json_without_animals_or_records(self, enclosure1: Enclosure):
        """Test converting the enclosure data to json like format."""
        assert enclosure1.to_json() == {
            "id": enclosure1.id,
            "name": enclosure1.name,
            "area": enclosure1.area,
            "animals": [],
            "cleaning_record": []
        }

    def test_to_json_with_animals(self, enclosure1: Enclosure, animal1: Animal, animal2: Animal, animal3: Animal):
        """Test converting the enclosure data to json like format."""
        animal1.set_home(enclosure1)
        animal2.set_home(enclosure1)
        animal3.set_home(enclosure1)
        assert enclosure1.to_json() == {
            "id": enclosure1.id,
            "name": enclosure1.name,
            "area": enclosure1.area,
            "animals": [animal1.id, animal2.id, animal3.id],
            "cleaning_record": []
        }

    def test_to_json_with_records(self, enclosure1: Enclosure):
        """Test converting the enclosure data to json like format."""
        enclosure1.clean()
        assert enclosure1.to_json() == {
            "id": enclosure1.id,
            "name": enclosure1.name,
            "area": enclosure1.area,
            "animals": [],
            "cleaning_record": [enclosure1.cleaning_record[0]]
        }
