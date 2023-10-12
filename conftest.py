# All fixtures in this file can be used by every test file without
# importing anything.

import uuid
import pytest

from zoo import Zoo
from zoo_objects import Animal, Caretaker, Enclosure


@pytest.fixture(scope='session')
def base_url() -> str:
    return 'http://127.0.0.1:7890'


@pytest.fixture
def zoo1() -> Zoo:
    return Zoo()


@pytest.fixture
def animal1() -> Animal:
    return Animal('Panthera tigris', 'Tiger', 12)


@pytest.fixture
def animal2() -> Animal:
    return Animal('Testudinata', 'Turtle', 5)


@pytest.fixture
def animal3() -> Animal:
    return Animal('Pan troglodytes', 'Chimpanzee', 36)


@pytest.fixture
def enclosure1() -> Enclosure:
    return Enclosure('Cave1', 125)


@pytest.fixture
def enclosure2() -> Enclosure:
    return Enclosure('Aquarium5', 500.5)


@pytest.fixture
def enclosure3() -> Enclosure:
    return Enclosure('Enclosure753', 4.123)


@pytest.fixture
def caretaker1() -> Caretaker:
    return Caretaker('Laetitia', 'blond-street 19')


@pytest.fixture
def caretaker2() -> Caretaker:
    return Caretaker('Siena', 'brown rose hall 2')


@pytest.fixture
def caretaker3() -> Caretaker:
    return Caretaker('Pitt', 'gameon town 123')


@pytest.fixture(scope='session')
def unknown_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def unknown_id2() -> str:
    return str(uuid.uuid4())
