import pytest
from zoo import Zoo
from animal import Animal, Caretaker, Enclosure


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


@pytest.fixture(scope='session')
def base_url() -> str:
    return 'http://127.0.0.1:7890'