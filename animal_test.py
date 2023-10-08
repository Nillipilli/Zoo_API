import pytest
from datetime import datetime

from zoo import Zoo
from zoo_objects import Animal


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
