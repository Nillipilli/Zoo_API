import pytest
from zoo import Zoo
from animal import Animal


def test_add_animal(zoo1: Zoo, animal1: Animal, animal2: Animal):
    """Test adding animals to the zoo."""
    zoo1.add_animal(animal1)
    zoo1.add_animal(animal2)
    
    assert (len(zoo1.animals) == 2)
    assert (animal1 in zoo1.animals)
    assert (animal2 in zoo1.animals)


# def test_feed_animal(zoo1: Zoo, animal1: Animal):
#     zoo1.add_animal(animal1)

#     animal1.feed()

#     assert (len(animal1.feeding_record) == 1)
