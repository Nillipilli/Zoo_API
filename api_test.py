import json
import pytest
import requests
from animal import Animal
from requests import Response


@pytest.fixture
def post_animal1(base_url: str, animal1: Animal) -> None:
    animal1_data = {'species_name': animal1.species_name,
                    'common_name': animal1.common_name,
                    'age': animal1.age}
    requests.post(base_url + '/animal', data=animal1_data)


@pytest.fixture
def post_animal2(base_url: str, animal2: Animal) -> None:
    animal2_data = {'species_name': animal2.species_name,
                    'common_name': animal2.common_name,
                    'age': animal2.age}
    requests.post(base_url + '/animal', data=animal2_data)


@pytest.fixture
def post_animal3(base_url: str, animal3: Animal) -> None:
    animal3_data = {'species_name': animal3.species_name,
                    'common_name': animal3.common_name,
                    'age': animal3.age}
    requests.post(base_url + '/animal', data=animal3_data)


# @pytest.fixture
# def zoo_with_one_animal(base_url) -> bytes:
#     requests.post(base_url + '/animal',
#                   {'species_name': 'Panthera tigris',
#                    'common_name': 'Tiger',
#                    'age': 5})

#     response = requests.get(base_url + '/animals')
#     return response.content


# @pytest.fixture
# def zoo_with_multiple_animals(base_url) -> bytes:
#     requests.post(base_url + '/animal',
#                   {'species_name': 'Panthera tigris',
#                    'common_name': 'Tiger',
#                    'age': 5})

#     response = requests.get(base_url + '/animals')
#     return response.content


class TestZoo:
    def test_add_animal(self, base_url, post_animal1):
        """Test adding a single animal to the zoo."""
        x: Response = requests.get(base_url + '/animals')
        js: bytes = x.content
        animals = json.loads(js)

        assert len(animals) == 1
        assert animals[0]['species_name'] == 'Panthera tigris'
        assert animals[0]['common_name'] == 'Tiger'
        assert animals[0]['age'] == 12

        requests.delete(base_url + f'/animal/{animals[0]["id"]}')
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_add_animals(self, base_url, post_animal1, post_animal2, post_animal3):
        """Test adding multiple animals to the zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)

        assert len(animals) == 3
        assert animals[0]['species_name'] == 'Panthera tigris'
        assert animals[0]['common_name'] == 'Tiger'
        assert animals[0]['age'] == 12
        assert animals[1]['species_name'] == 'Testudinata'
        assert animals[1]['common_name'] == 'Turtle'
        assert animals[1]['age'] == 5
        assert animals[2]['species_name'] == 'Pan troglodytes'
        assert animals[2]['common_name'] == 'Chimpanzee'
        assert animals[2]['age'] == 36

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_all_animals_empty_zoo(self, base_url):
        """Test retrieving all animals of an empty zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_all_animals(self, base_url, post_animal1):
        """Test retriving all animals of a zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

    def test_get_animal_info(self, base_url, post_animal1, post_animal2, post_animal3):
        """Test retrieving information about specific animals."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 3

        for animal_dict in animals:
            animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert animal_data['species_name'] == animal_dict['species_name']
            assert animal_data['common_name'] == animal_dict['common_name']
            assert animal_data['age'] == animal_dict['age']

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_animal_info_wrong_id(self, base_url, post_animal1):
        """Test retrieving information about an animal that does not 
        exist."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        # not existing ID
        animal_data = json.loads(requests.get(
            base_url + '/animal/bc889d3a-f378-416c-9c88-2dae19fc0f3c').content)
        assert animal_data is None

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_feed_animal(self, base_url, post_animal1):
        """Test feeding an animal and see if it gets added to the 
        animals' feeding record."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.post(base_url + f'/animal/{animal_dict["id"]}/feed')
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert len(new_animal_data['feeding_record']) == 1
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_feed_animal_multiple_times(self, base_url, post_animal1):
        """Test feeding an animal multiple times and see if it gets 
        added to the animals' feeding record."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.post(base_url + f'/animal/{animal_dict["id"]}/feed')
            requests.post(base_url + f'/animal/{animal_dict["id"]}/feed')
            requests.post(base_url + f'/animal/{animal_dict["id"]}/feed')
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert len(new_animal_data['feeding_record']) == 3
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_feed_animal_wrong_id(self, base_url):
        """Test trying to feed an animal that does not exist."""
        r = requests.post(
            base_url + '/animal/bc889d3a-f378-416c-9c88-2dae19fc0f3c/feed')
        b = r.content
        message = json.loads(
            b) == f'Animal with ID bc889d3a-f378-416c-9c88-2dae19fc0f3c has not been found'
