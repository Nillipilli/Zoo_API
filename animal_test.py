import pytest
from datetime import datetime

from zoo_objects import Animal, Caretaker, Enclosure


class TestAnimal:
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
        """Test unsetting the home of an animal."""
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

    def test_set_caretaker(self, animal1: Animal, caretaker1: Caretaker):
        """Test assigning the first caretaker to an existing animal."""
        assert animal1.caretaker is None
        assert len(caretaker1.animals) == 0

        animal1.set_caretaker(caretaker1)
        assert animal1.caretaker == caretaker1
        assert len(caretaker1.animals) == 1
        assert animal1 in caretaker1.animals

    def test_change_caretaker(self, animal1: Animal, caretaker1: Caretaker, caretaker2: Caretaker):
        """Test changing the caretaker of an existing animal."""
        animal1.set_caretaker(caretaker1)
        assert animal1.caretaker == caretaker1
        assert len(caretaker1.animals) == 1
        assert len(caretaker2.animals) == 0
        assert animal1 in caretaker1.animals

        animal1.set_caretaker(caretaker2)
        assert animal1.caretaker == caretaker2
        assert len(caretaker1.animals) == 0
        assert len(caretaker2.animals) == 1
        assert animal1 in caretaker2.animals

    def test_unset_caretaker(self, animal1: Animal, caretaker1: Caretaker):
        """Test unsetting the caretaker of an animal."""
        animal1.set_caretaker(caretaker1)
        assert animal1.caretaker == caretaker1
        assert len(caretaker1.animals) == 1
        assert animal1 in caretaker1.animals

        animal1.unset_caretaker()
        assert animal1.caretaker is None
        assert len(caretaker1.animals) == 0

    def test_unset_caretaker_no_caretaker(self, animal1: Animal):
        """Test unsetting the caretaker of an animal that has no 
        caretaker."""
        assert animal1.caretaker is None
        animal1.unset_caretaker()
        assert animal1.caretaker is None

    def test_feed_animal_once(self, animal1: Animal):
        """Test feeding an animal once."""
        animal1.feed()
        assert len(animal1.feeding_record) == 1
        assert isinstance(animal1.feeding_record[0], datetime)

    def test_feed_animal_multiple_times(self, animal1: Animal):
        """Test feeding an animal multiple times."""
        animal1.feed()
        animal1.feed()
        animal1.feed()
        animal1.feed()
        animal1.feed()

        assert len(animal1.feeding_record) == 5
        for record in animal1.feeding_record:
            assert isinstance(record, datetime)

    def test_vet_animal_once(self, animal1: Animal):
        """Test vet an animal once."""
        animal1.vet()
        assert len(animal1.medical_record) == 1
        assert isinstance(animal1.medical_record[0], datetime)

    def test_vet_animal_multiple_times(self, animal1: Animal):
        """Test vet an animal multiple times."""
        animal1.vet()
        animal1.vet()
        animal1.vet()
        animal1.vet()
        animal1.vet()

        assert len(animal1.medical_record) == 5
        for record in animal1.medical_record:
            assert isinstance(record, datetime)

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

    def test_to_json_without_enclosure_and_caretaker(self, animal1: Animal):
        """Test converting the animal data to json like format with 
        caretaker and enclosure set to None."""
        assert animal1.to_json() == {
            "id": animal1.id,
            "species_name": animal1.species_name,
            "common_name": animal1.common_name,
            "age": animal1.age,
            "enclosure": None,
            "caretaker": None,
            "feeding_record": [],
            "medical_record": [],
        }

    def test_to_json_with_enclosure_and_caretaker(self, animal1: Animal, caretaker1: Caretaker, enclosure1: Enclosure):
        """Test converting the animal data to json like format with
        caretaker and enclosure specified."""
        animal1.set_caretaker(caretaker1)
        animal1.set_home(enclosure1)

        assert animal1.to_json() == {
            "id": animal1.id,
            "species_name": animal1.species_name,
            "common_name": animal1.common_name,
            "age": animal1.age,
            "enclosure": enclosure1.id,
            "caretaker": caretaker1.id,
            "feeding_record": [],
            "medical_record": [],
        }

    def test_to_json_records(self, animal1: Animal):
        """Test converting the animal data to json like format with
        feeding and medical records."""
        animal1.feed()
        animal1.vet()

        assert animal1.to_json() == {
            "id": animal1.id,
            "species_name": animal1.species_name,
            "common_name": animal1.common_name,
            "age": animal1.age,
            "enclosure": None,
            "caretaker": None,
            "feeding_record": [animal1.feeding_record[0]],
            "medical_record": [animal1.medical_record[0]],
        }
