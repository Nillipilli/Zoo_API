import pytest
from zoo import Zoo
from animal import Animal


@pytest.fixture
def zoo1() -> Zoo:
    return Zoo()


@pytest.fixture
def tiger1() -> Animal:
    return Animal(12, "tiger", "ti")


@pytest.fixture
def tiger2() -> Animal:
    return Animal(2, "tiger2", "ti")


def test_add_animal(zoo1, tiger1, tiger2):
    zoo1.add_animal(tiger1)
    assert (tiger1 in zoo1.animals)
    zoo1.add_animal(tiger2)

    assert (len(zoo1.animals) == 2)


def test_feed_animal(zoo1, tiger1):
    zoo1.add_animal(tiger1)

    tiger1.feed()

    assert (len(tiger1.feeding_record) == 1)
