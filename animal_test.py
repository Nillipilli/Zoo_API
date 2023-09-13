import pytest
from zoo import Zoo
from animal import Animal


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


# def test_feed_animal(zoo1: Zoo, animal1: Animal):
#     zoo1.add_animal(animal1)

#     animal1.feed()

#     assert (len(animal1.feeding_record) == 1)
