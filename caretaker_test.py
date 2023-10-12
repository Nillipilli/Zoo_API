import pytest

from zoo import Zoo
from zoo_objects import Caretaker


def test_add_caretakers(zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker):
    """Test adding caretakers to the zoo."""
    zoo1.add_caretaker(caretaker1)
    zoo1.add_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 2
    assert caretaker1 in zoo1.caretakers
    assert caretaker2 in zoo1.caretakers


def test_add_caretaker_twice(zoo1: Zoo, caretaker1: Caretaker):
    """Test adding a caretaker twice to the zoo."""
    zoo1.add_caretaker(caretaker1)
    zoo1.add_caretaker(caretaker1)
    assert len(zoo1.caretakers) == 1
    assert caretaker1 in zoo1.caretakers


def test_add_and_remove_caretakers(zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker):
    """Test adding caretakers to the zoo and then remove one."""
    zoo1.add_caretaker(caretaker1)
    zoo1.add_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 2
    assert caretaker1 in zoo1.caretakers
    assert caretaker2 in zoo1.caretakers

    zoo1.remove_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 1
    assert caretaker1 in zoo1.caretakers


def test_add_and_remove_caretakers_often(zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker):
    """Test adding caretakers to the zoo, removing them and then adding 
    them again."""
    zoo1.add_caretaker(caretaker1)
    zoo1.add_caretaker(caretaker2)
    zoo1.add_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 2
    assert caretaker1 in zoo1.caretakers
    assert caretaker2 in zoo1.caretakers

    zoo1.remove_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 1
    assert caretaker1 in zoo1.caretakers

    zoo1.add_caretaker(caretaker2)
    assert len(zoo1.caretakers) == 2
    assert caretaker1 in zoo1.caretakers
    assert caretaker2 in zoo1.caretakers


def test_remove_caretaker_twice(zoo1: Zoo, caretaker1: Caretaker):
    """Test removing a caretaker twice."""
    zoo1.add_caretaker(caretaker1)
    assert len(zoo1.caretakers) == 1

    zoo1.remove_caretaker(caretaker1)
    zoo1.remove_caretaker(caretaker1)
    assert len(zoo1.caretakers) == 0


def test_get_caretaker(zoo1: Zoo, caretaker1: Caretaker):
    """Test with an existing caretaker id to get a caretaker."""
    zoo1.add_caretaker(caretaker1)
    assert len(zoo1.caretakers) == 1
    assert zoo1.get_caretaker(caretaker1.id) == caretaker1


def test_get_caretaker_not_existing(zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker):
    """Test with a not existing caretaker id, so it should return None."""
    zoo1.add_caretaker(caretaker1)
    assert len(zoo1.caretakers) == 1
    assert zoo1.get_caretaker(caretaker2.id) is None


def test_get_all_caretakers(zoo1: Zoo, caretaker1: Caretaker, caretaker2: Caretaker, caretaker3: Caretaker):
    """Test getting all information about the existing caretakers."""
    zoo1.add_caretaker(caretaker1)
    zoo1.add_caretaker(caretaker2)
    zoo1.add_caretaker(caretaker3)

    assert len(zoo1.get_all_caretakers()) == 3
    assert caretaker1 in zoo1.get_all_caretakers()
    assert caretaker2 in zoo1.get_all_caretakers()
    assert caretaker3 in zoo1.get_all_caretakers()
