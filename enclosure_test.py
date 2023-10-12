import pytest
from datetime import datetime

from zoo import Zoo
from zoo_objects import Enclosure, Animal


class TestEnclosure:

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

    def test_get_all_animals_empty_enclosure(self, enclosure1: Enclosure):
        """Test retrieving all animals inside an empty enclosure."""
        assert len(enclosure1.get_animals()) == 0

    def test_get_all_animals_single_animal(self, enclosure1: Enclosure, animal1: Animal):
        """Test retrieving all animals in an enclosure with one 
        animal."""
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
