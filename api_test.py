import json
import pytest
import requests
from requests import Response

from zoo_objects import Animal, Enclosure


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


@pytest.fixture
def post_enclosure1(base_url: str, enclosure1: Enclosure) -> None:
    enclosure1_data = {'name': enclosure1.name,
                       'area': enclosure1.area}
    requests.post(base_url + '/enclosure', data=enclosure1_data)


@pytest.fixture
def post_enclosure2(base_url: str, enclosure2: Enclosure) -> None:
    enclosure2_data = {'name': enclosure2.name,
                       'area': enclosure2.area}
    requests.post(base_url + '/enclosure', data=enclosure2_data)


@pytest.fixture
def post_enclosure3(base_url: str, enclosure3: Enclosure) -> None:
    enclosure3_data = {'name': enclosure3.name,
                       'area': enclosure3.area}
    requests.post(base_url + '/enclosure', data=enclosure3_data)


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


class TestZooAnimal:
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

    def test_add_animal_with_negative_age(self, base_url):
        """Test adding an animal with a negative age to the zoo."""
        age = -1
        animal_data = {'species_name': 'Panthera tigris',
                       'common_name': 'Tiger',
                       'age': age}
        r = requests.post(base_url + '/animal', data=animal_data)
        b = r.content
        message = json.loads(b)
        assert message == f'An age of {age} is not possible'

    def test_get_all_animals_empty_zoo(self, base_url):
        """Test retrieving all animals of an empty zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_all_animals(self, base_url, post_animal1, post_animal2):
        """Test retrieving all animals of a zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 2

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

    def test_get_animal_info_unknown_id(self, base_url, unknown_id, post_animal1):
        """Test retrieving information about an animal that does not 
        exist."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        animal_data = json.loads(requests.get(
            base_url + f'/animal/{unknown_id}').content)
        assert animal_data is None

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_delete_animal(self, base_url, post_animal1):
        """Test deleting an existing animal."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_delete_not_existing_animal(self, base_url, unknown_id, post_animal1):
        """Test deleting an animal that does not exist."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        message = json.loads(requests.delete(
            base_url + f'/animal/{unknown_id}').content)
        assert message == f'Animal with ID {unknown_id} has not been found'

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        # Cleanup
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

    def test_feed_animal_unknown_id(self, base_url, unknown_id):
        """Test trying to feed an animal that does not exist."""
        r = requests.post(base_url + f'/animal/{unknown_id}/feed')
        b = r.content
        message = json.loads(b)
        assert message == f'Animal with ID {unknown_id} has not been found'

    def test_vet_animal(self, base_url, post_animal1):
        """Test performing a medical checkup on an animal and see if it
        gets added to the animals' medical record."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.post(base_url + f'/animal/{animal_dict["id"]}/vet')
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert len(new_animal_data['medical_record']) == 1
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_vet_animal_multiple_times(self, base_url, post_animal1):
        """Test performing a medical checkup on an animal multiple times
        and see if it gets added to the animals' medical record."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        for animal_dict in animals:
            requests.post(base_url + f'/animal/{animal_dict["id"]}/vet')
            requests.post(base_url + f'/animal/{animal_dict["id"]}/vet')
            requests.post(base_url + f'/animal/{animal_dict["id"]}/vet')
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert len(new_animal_data['medical_record']) == 3
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_vet_animal_unknown_id(self, base_url, unknown_id):
        """Test trying to perform a medical checkup on an animal that 
        does not exist."""
        r = requests.post(base_url + f'/animal/{unknown_id}/vet')
        b = r.content
        message = json.loads(b)
        assert message == f'Animal with ID {unknown_id} has not been found'


class TestZooEnclosure:
    def test_add_enclosure(self, base_url, post_enclosure1):
        """Test adding a single enclosure to the zoo."""
        x: Response = requests.get(base_url + '/enclosures')
        js: bytes = x.content
        enclosures = json.loads(js)

        assert len(enclosures) == 1
        assert enclosures[0]['name'] == 'Cave1'
        assert enclosures[0]['area'] == 125

        requests.delete(base_url + f'/enclosure/{enclosures[0]["id"]}')
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_add_enclosures(self, base_url, post_enclosure1, post_enclosure2, post_enclosure3):
        """Test adding multiple enclosures to the zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)

        assert len(enclosures) == 3
        assert enclosures[0]['name'] == 'Cave1'
        assert enclosures[0]['area'] == 125
        assert enclosures[1]['name'] == 'Aquarium5'
        assert enclosures[1]['area'] == 500.5
        assert enclosures[2]['name'] == 'Enclosure753'
        assert enclosures[2]['area'] == 4.123

        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_add_enclosure_with_negative_area(self, base_url):
        """Test adding an enclosure with a negative area to the zoo."""
        area = -0.0001
        enclosure_data = {'name': 'Cave1',
                          'area': area}
        r = requests.post(base_url + '/enclosure', data=enclosure_data)
        b = r.content
        message = json.loads(b)
        assert message == f'An area of {area} is not possible'

    def test_add_enclosure_with_zero_area(self, base_url):
        """Test adding an enclosure with an area of 0 to the zoo."""
        area = 0
        enclosure_data = {'name': 'Cave1',
                          'area': area}
        r = requests.post(base_url + '/enclosure', data=enclosure_data)
        b = r.content
        message = json.loads(b)
        assert message == f'An area of {area:.1f} is not possible'

    def test_get_all_enclosures_empty_zoo(self, base_url):
        """Test retrieving all enclosures of an empty zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_get_all_enclosures(self, base_url, post_enclosure1, post_enclosure2):
        """Test retrieving all enclosures of a zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 2

        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

    def test_get_enclosure_info(self, base_url, post_enclosure1, post_enclosure2, post_enclosure3):
        """Test retrieving information about specific enclosures."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 3

        for enclosure_dict in enclosures:
            enclosure_data = json.loads(requests.get(
                base_url + f'/enclosure/{enclosure_dict["id"]}').content)
            assert enclosure_data['name'] == enclosure_dict['name']
            assert enclosure_data['area'] == enclosure_dict['area']

        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_get_enclosure_info_unknown_id(self, base_url, unknown_id, post_enclosure1):
        """Test retrieving information about an enclosure that does not 
        exist."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{unknown_id}').content)
        assert enclosure_data is None

        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_delete_enclosure(self, base_url, post_enclosure1):
        """Test deleting an existing enclosure."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_delete_not_existing_enclosure(self, base_url, unknown_id, post_enclosure1):
        """Test deleting an enclosure that does not exist."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        message = json.loads(requests.delete(
            base_url + f'/enclosure/{unknown_id}').content)
        assert message == f'Enclosure with ID {unknown_id} has not been found'

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        # Cleanup
        for enclosures_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosures_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0
