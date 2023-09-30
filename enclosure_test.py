import pytest

from zoo import Zoo
from zoo_objects import Enclosure


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
    