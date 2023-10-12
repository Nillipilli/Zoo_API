import pytest
from datetime import datetime

from zoo import Zoo
from zoo_objects import Animal, Enclosure


def test_add_animals(zoo1: Zoo, animal1: Animal, animal2: Animal):
    """Test adding animals to the zoo."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)

    assert (len(zoo1.animals) == 2)
    assert (animal1 in zoo1.animals)
    assert (animal2 in zoo1.animals)


def test_add_animal_twice(zoo1: Zoo, animal1: Animal):
    """Test adding an animal twice to the zoo."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal1)

    assert (len(zoo1.animals) == 1)
    assert (animal1 in zoo1.animals)


def test_add_and_remove_animals(zoo1: Zoo, animal1: Animal, animal2: Animal):
    """Test adding animals to the zoo and then remove one."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)

    assert (len(zoo1.animals) == 2)
    assert (animal1 in zoo1.animals)
    assert (animal2 in zoo1.animals)

    zoo1.remove_animal(animal2)

    assert (len(zoo1.animals) == 1)
    assert (animal1 in zoo1.animals)


def test_add_and_remove_animals_often(zoo1: Zoo, animal1: Animal, animal2: Animal):
    """Test adding animals to the zoo, removing them and then adding 
    them again."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)
    zoo1.add_animal(animal2)

    assert (len(zoo1.animals) == 2)
    assert (animal1 in zoo1.animals)
    assert (animal2 in zoo1.animals)

    zoo1.remove_animal(animal2)

    assert (len(zoo1.animals) == 1)
    assert (animal1 in zoo1.animals)

    zoo1.add_animal(animal2)
    assert (len(zoo1.animals) == 2)
    assert (animal1 in zoo1.animals)
    assert (animal2 in zoo1.animals)


def test_remove_animal_twice(zoo1: Zoo, animal1: Animal):
    """Test removing an animal twice."""
    zoo1.add_animal(animal1)

    assert (len(zoo1.animals) == 1)

    zoo1.remove_animal(animal1)
    zoo1.remove_animal(animal1)

    assert (len(zoo1.animals) == 0)


def test_get_animal(zoo1: Zoo, animal1: Animal):
    """Test with an existing animal id to get an animal."""
    zoo1.add_animal(animal1)

    assert (len(zoo1.animals) == 1)
    assert zoo1.get_animal(animal1.id) == animal1


def test_get_animal_not_existing(zoo1: Zoo, animal1: Animal, animal2: Animal):
    """Test with a not existing animal id, so it should return None."""
    zoo1.add_animal(animal1)

    assert (len(zoo1.animals) == 1)
    assert zoo1.get_animal(animal2.id) is None


def test_get_all_animals(zoo1: Zoo, animal1: Animal, animal2: Animal, animal3: Animal):
    """Test getting all information about the existing animals."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)
    zoo1.add_animal(animal3)

    assert len(zoo1.get_all_animals()) == 3
    assert animal1 in zoo1.get_all_animals()
    assert animal2 in zoo1.get_all_animals()
    assert animal3 in zoo1.get_all_animals()


def test_feed_animal(zoo1: Zoo, animal1: Animal):
    """Test feed an animal once."""
    zoo1.add_animal(animal1)
    animal1.feed()

    assert (len(animal1.feeding_record) == 1)
    assert isinstance(animal1.feeding_record[0], datetime)


def test_feed_animal_often(zoo1: Zoo, animal1: Animal):
    """Test feed an animal multiple_times."""
    zoo1.add_animal(animal1)
    animal1.feed()
    animal1.feed()
    animal1.feed()
    animal1.feed()
    animal1.feed()

    assert (len(animal1.feeding_record) == 5)
    for record in animal1.feeding_record:
        assert isinstance(record, datetime)


def test_vet_animal(zoo1: Zoo, animal1: Animal):
    """Test vet an animal once."""
    zoo1.add_animal(animal1)
    animal1.vet()

    assert (len(animal1.medical_record) == 1)
    assert isinstance(animal1.medical_record[0], datetime)


def test_vet_animal_often(zoo1: Zoo, animal1: Animal):
    """Test vet an animal multiple_times."""
    zoo1.add_animal(animal1)
    animal1.vet()
    animal1.vet()
    animal1.vet()
    animal1.vet()
    animal1.vet()

    assert (len(animal1.medical_record) == 5)
    for record in animal1.medical_record:
        assert isinstance(record, datetime)


def test_set_home(zoo1: Zoo, animal1: Animal, enclosure1: Enclosure):
    """Test assigning the first home to an existing animal."""
    zoo1.add_animal(animal1)
    zoo1.add_enclosure(enclosure1)

    assert animal1.enclosure is None
    assert len(enclosure1.animals) == 0
    animal1.set_home(enclosure1)
    assert animal1.enclosure == enclosure1
    assert len(enclosure1.animals) == 1
    assert animal1 in enclosure1.animals


def test_change_home(zoo1: Zoo, animal1: Animal, enclosure1: Enclosure, enclosure2: Enclosure):
    """Test changing the home of an existing animal."""
    zoo1.add_animal(animal1)
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    assert animal1.enclosure is None
    assert len(enclosure1.animals) == 0
    assert len(enclosure2.animals) == 0

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


def test_unset_home(animal1: Animal, enclosure1: Enclosure):
    """Test unsetting the home of an animal. 

    It should set the value to its default value and remove the animal 
    also from the enclosure's list of animals."""
    assert animal1.enclosure is None
    assert len(enclosure1.animals) == 0

    animal1.set_home(enclosure1)
    assert animal1.enclosure == enclosure1
    assert len(enclosure1.animals) == 1
    assert animal1 in enclosure1.animals

    animal1.unset_home()
    assert animal1.enclosure is None
    assert len(enclosure1.animals) == 0


def test_unset_home_no_home(animal1: Animal):
    """Test unsetting the home of an animal that has no home so far."""
    assert animal1.enclosure is None
    animal1.unset_home()
    assert animal1.enclosure is None


def test_birth_without_enclosure_set(animal1: Animal):
    """Test giving birth to a new animal when the mother is not living
    in any enclosure."""
    new_animal = animal1.birth()
    assert isinstance(new_animal, Animal)
    assert new_animal.enclosure == animal1.enclosure


def test_birth_with_enclosure_set(animal1: Animal, enclosure1: Enclosure):
    """Test giving birth to a new animal when the mother is already 
    living in an enclosure."""
    animal1.set_home(enclosure1)
    new_animal = animal1.birth()
    assert isinstance(new_animal, Animal)
    assert new_animal.enclosure == animal1.enclosure
