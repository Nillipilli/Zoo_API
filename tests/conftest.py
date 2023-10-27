import uuid
import json
import pytest
import requests

from zoo import Zoo
from zoo_objects import Animal, Caretaker, Enclosure

# NOTE All fixtures in this file can be used by every test file without
# importing anything.


# ---- zoo fixtures ----


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
def animal4() -> Animal:
    return Animal('Pan troglodytes', 'Chimpanzee', 60)


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
    return Caretaker('Laetitia', 'Blond-Street 19')


@pytest.fixture
def caretaker2() -> Caretaker:
    return Caretaker('Siena', 'Brown Rose Hall 2')


@pytest.fixture
def caretaker3() -> Caretaker:
    return Caretaker('Pitt', 'Gameon Town 123')


# ---- API fixtures


@pytest.fixture(scope='session')
def base_url() -> str:
    return 'http://127.0.0.1:7890'


@pytest.fixture(scope='session')
def unknown_id() -> str:
    return str(uuid.uuid4())


@pytest.fixture(scope='session')
def unknown_id2() -> str:
    return str(uuid.uuid4())


@pytest.fixture
def post_animal1(base_url: str, animal1: Animal) -> dict:
    animal1_data = {'species_name': animal1.species_name,
                    'common_name': animal1.common_name,
                    'age': animal1.age}
    return json.loads(requests.post(base_url + '/animal', data=animal1_data).content)


@pytest.fixture
def post_animal2(base_url: str, animal2: Animal) -> dict:
    animal2_data = {'species_name': animal2.species_name,
                    'common_name': animal2.common_name,
                    'age': animal2.age}
    return json.loads(requests.post(base_url + '/animal', data=animal2_data).content)


@pytest.fixture
def post_animal3(base_url: str, animal3: Animal) -> dict:
    animal3_data = {'species_name': animal3.species_name,
                    'common_name': animal3.common_name,
                    'age': animal3.age}
    return json.loads(requests.post(base_url + '/animal', data=animal3_data).content)


@pytest.fixture
def post_animal4(base_url: str, animal4: Animal) -> dict:
    animal4_data = {'species_name': animal4.species_name,
                    'common_name': animal4.common_name,
                    'age': animal4.age}
    return json.loads(requests.post(base_url + '/animal', data=animal4_data).content)


@pytest.fixture
def post_enclosure1(base_url: str, enclosure1: Enclosure) -> dict:
    enclosure1_data = {'name': enclosure1.name,
                       'area': enclosure1.area}
    return json.loads(requests.post(base_url + '/enclosure', data=enclosure1_data).content)


@pytest.fixture
def post_enclosure2(base_url: str, enclosure2: Enclosure) -> dict:
    enclosure2_data = {'name': enclosure2.name,
                       'area': enclosure2.area}
    return json.loads(requests.post(base_url + '/enclosure', data=enclosure2_data).content)


@pytest.fixture
def post_enclosure3(base_url: str, enclosure3: Enclosure) -> dict:
    enclosure3_data = {'name': enclosure3.name,
                       'area': enclosure3.area}
    return json.loads(requests.post(base_url + '/enclosure', data=enclosure3_data).content)


@pytest.fixture
def post_caretaker1(base_url: str, caretaker1: Caretaker) -> dict:
    caretaker1_data = {'name': caretaker1.name,
                       'address': caretaker1.address}
    return json.loads(requests.post(base_url + '/caretaker', data=caretaker1_data).content)


@pytest.fixture
def post_caretaker2(base_url: str, caretaker2: Caretaker) -> dict:
    caretaker2_data = {'name': caretaker2.name,
                       'address': caretaker2.address}
    return json.loads(requests.post(base_url + '/caretaker', data=caretaker2_data).content)


@pytest.fixture
def post_caretaker3(base_url: str, caretaker3: Caretaker) -> dict:
    caretaker3_data = {'name': caretaker3.name,
                       'address': caretaker3.address}
    return json.loads(requests.post(base_url + '/caretaker', data=caretaker3_data).content)
