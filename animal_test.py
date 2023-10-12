import pytest
from datetime import datetime

from zoo import Zoo
from zoo_objects import Animal, Enclosure


class TestAnimal:

    def test_feed_animal(self, animal1: Animal):
        """Test feed an animal once."""
        animal1.feed()
        assert len(animal1.feeding_record) == 1
        assert isinstance(animal1.feeding_record[0], datetime)

    def test_feed_animal_multiple_times(self, animal1: Animal):
        """Test feed an animal multiple_times."""
        animal1.feed()
        animal1.feed()
        animal1.feed()
        animal1.feed()
        animal1.feed()
        
        assert len(animal1.feeding_record) == 5
        for record in animal1.feeding_record:
            assert isinstance(record, datetime)

    def test_vet_animal(self, animal1: Animal):
        """Test vet an animal once."""
        animal1.vet()
        assert len(animal1.medical_record) == 1
        assert isinstance(animal1.medical_record[0], datetime)

    def test_vet_animal_often(self, animal1: Animal):
        """Test vet an animal multiple_times."""
        animal1.vet()
        animal1.vet()
        animal1.vet()
        animal1.vet()
        animal1.vet()
        
        assert len(animal1.medical_record) == 5
        for record in animal1.medical_record:
            assert isinstance(record, datetime)

    def test_set_home(self, animal1: Animal, enclosure1: Enclosure):
        """Test assigning the first home to an existing animal."""
        assert animal1.enclosure is None
        assert len(enclosure1.animals) == 0

        animal1.set_home(enclosure1)

        assert animal1.enclosure == enclosure1
        assert len(enclosure1.animals) == 1
        assert animal1 in enclosure1.animals

    def test_change_home(self, animal1: Animal, enclosure1: Enclosure, enclosure2: Enclosure):
        """Test changing the home of an existing animal."""
        animal1.set_home(enclosure1)
        assert animal1.enclosure == enclosure1
        assert len(enclosure1.animals) == 1
        assert len(enclosure2.animals) == 0
        assert animal1 in enclosure1.animals

        animal1.set_home(enclosure2)
        assert animal1.enclosure == enclosure2
        assert len(enclosure1.animals) == 0
        assert len(enclosure2.animals) == 1
        assert animal1 in enclosure2.animals

    def test_unset_home(self, animal1: Animal, enclosure1: Enclosure):
        """Test unsetting the home of an animal. 

        It should set the value to its default value and remove the 
        animal also from the enclosure's list of animals."""
        animal1.set_home(enclosure1)
        assert animal1.enclosure == enclosure1
        assert len(enclosure1.animals) == 1
        assert animal1 in enclosure1.animals

        animal1.unset_home()
        assert animal1.enclosure is None
        assert len(enclosure1.animals) == 0

    def test_unset_home_no_home(self, animal1: Animal):
        """Test unsetting the home of an animal that has no home."""
        assert animal1.enclosure is None
        animal1.unset_home()
        assert animal1.enclosure is None

    def test_birth_without_enclosure_set(self, animal1: Animal):
        """Test giving birth to a new animal when the mother is not 
        living in any enclosure."""
        new_animal = animal1.birth()
        assert isinstance(new_animal, Animal)
        assert new_animal.enclosure is None

    def test_birth_with_enclosure_set(self, animal1: Animal, enclosure1: Enclosure):
        """Test giving birth to a new animal when the mother is already 
        living in an enclosure."""
        animal1.set_home(enclosure1)
        new_animal = animal1.birth()
        assert isinstance(new_animal, Animal)
        assert new_animal.enclosure == enclosure1
