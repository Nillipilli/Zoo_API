import pytest
from datetime import datetime

from zoo import Zoo
from zoo_objects import Enclosure, Animal


def test_add_enclosures(zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure):
    """Test adding enclosures to the zoo."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    assert (len(zoo1.enclosures) == 2)
    assert (enclosure1 in zoo1.enclosures)
    assert (enclosure2 in zoo1.enclosures)


def test_add_enclosure_twice(zoo1: Zoo, enclosure1: Enclosure):
    """Test adding an enclosure twice to the zoo."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure1)

    assert (len(zoo1.enclosures) == 1)
    assert (enclosure1 in zoo1.enclosures)


def test_add_and_remove_enclosure(zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure):
    """Test adding enclosures to the zoo and then remove one."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)

    assert (len(zoo1.enclosures) == 2)
    assert (enclosure1 in zoo1.enclosures)
    assert (enclosure2 in zoo1.enclosures)

    zoo1.remove_enclosure(enclosure2)

    assert (len(zoo1.enclosures) == 1)
    assert (enclosure1 in zoo1.enclosures)


def test_add_and_remove_enclosures_often(zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure):
    """Test adding enclosures to the zoo, removing them and then adding 
    them again."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure2)

    assert (len(zoo1.enclosures) == 2)
    assert (enclosure1 in zoo1.enclosures)
    assert (enclosure2 in zoo1.enclosures)

    zoo1.remove_enclosure(enclosure2)

    assert (len(zoo1.enclosures) == 1)
    assert (enclosure1 in zoo1.enclosures)

    zoo1.add_enclosure(enclosure2)
    assert (len(zoo1.enclosures) == 2)
    assert (enclosure1 in zoo1.enclosures)
    assert (enclosure2 in zoo1.enclosures)


def test_remove_enclosure_twice(zoo1: Zoo, enclosure1: Enclosure):
    """Test removing an enclosure twice."""
    zoo1.add_enclosure(enclosure1)

    assert (len(zoo1.enclosures) == 1)

    zoo1.remove_enclosure(enclosure1)
    zoo1.remove_enclosure(enclosure1)

    assert (len(zoo1.enclosures) == 0)


def test_get_enclosure(zoo1: Zoo, enclosure1: Enclosure):
    """Test with an existing enclosure id to get an enclosure."""
    zoo1.add_enclosure(enclosure1)

    assert (len(zoo1.enclosures) == 1)
    assert zoo1.get_enclosure(enclosure1.id) == enclosure1


def test_get_enclosure_not_existing(zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure):
    """Test with a not existing enclosure id, so it should return None."""
    zoo1.add_enclosure(enclosure1)

    assert (len(zoo1.enclosures) == 1)
    assert zoo1.get_enclosure(enclosure2.id) is None


def test_get_all_enclosures(zoo1: Zoo, enclosure1: Enclosure, enclosure2: Enclosure, enclosure3: Enclosure):
    """Test getting all information about the existing enclosures."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_enclosure(enclosure2)
    zoo1.add_enclosure(enclosure3)

    assert len(zoo1.get_all_enclosures()) == 3
    assert enclosure1 in zoo1.get_all_enclosures()
    assert enclosure2 in zoo1.get_all_enclosures()
    assert enclosure3 in zoo1.get_all_enclosures()


def test_clean_enclosure(zoo1: Zoo, enclosure1: Enclosure):
    """Test clean an enclosure once."""
    zoo1.add_enclosure(enclosure1)
    enclosure1.clean()

    assert (len(enclosure1.cleaning_record) == 1)
    assert isinstance(enclosure1.cleaning_record[0], datetime)


def test_clean_enclosure_often(zoo1: Zoo, enclosure1: Enclosure):
    """Test clean an enclosure multiple_times."""
    zoo1.add_enclosure(enclosure1)
    enclosure1.clean()
    enclosure1.clean()
    enclosure1.clean()
    enclosure1.clean()
    enclosure1.clean()

    assert (len(enclosure1.cleaning_record) == 5)
    for record in enclosure1.cleaning_record:
        assert isinstance(record, datetime)


def test_get_all_animals_empty_enclosure(zoo1: Zoo, enclosure1: Enclosure):
    """Test retrieving all animals inside an empty enclosure."""
    zoo1.add_enclosure(enclosure1)
    assert len(enclosure1.get_animals()) == 0


def test_get_all_animals_single_animal(zoo1: Zoo, enclosure1: Enclosure, animal1: Animal):
    """Test retrieving all animals in an enclosure with one animal."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_animal(animal1)

    assert len(enclosure1.get_animals()) == 0
    animal1.set_home(enclosure1)
    assert len(enclosure1.get_animals()) == 1
    assert animal1 in enclosure1.get_animals()


def test_get_all_animals_multiple_animals(zoo1: Zoo, enclosure1: Enclosure, animal1: Animal, animal2: Animal, animal3: Animal):
    """Test retrieving all animals in an enclosure with many animals."""
    zoo1.add_enclosure(enclosure1)
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)
    zoo1.add_animal(animal3)

    assert len(enclosure1.get_animals()) == 0
    animal1.set_home(enclosure1)
    animal2.set_home(enclosure1)
    animal3.set_home(enclosure1)
    assert len(enclosure1.get_animals()) == 3
    assert animal1 in enclosure1.get_animals()
    assert animal2 in enclosure1.get_animals()
    assert animal3 in enclosure1.get_animals()
