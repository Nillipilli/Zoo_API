import json
import pytest
import requests
from requests import Response


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
        # Make the request
        r: Response = requests.get(base_url + '/animals')

        # Get the content of the Response
        b: bytes = r.content

        # Deserialize the data into a python object
        animals = json.loads(b)
        assert len(animals) == 1

        assert animals[0]['species_name'] == post_animal1['species_name']
        assert animals[0]['common_name'] == post_animal1['common_name']
        assert animals[0]['age'] == post_animal1['age']

        # Cleanup
        requests.delete(base_url + f'/animal/{post_animal1["id"]}')
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_add_multiple_animals(self, base_url, post_animal1, post_animal2, post_animal3):
        """Test adding multiple animals to the zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 3

        assert animals[0]['species_name'] == post_animal1['species_name']
        assert animals[0]['common_name'] == post_animal1['common_name']
        assert animals[0]['age'] == post_animal1['age']
        assert animals[1]['species_name'] == post_animal2['species_name']
        assert animals[1]['common_name'] == post_animal2['common_name']
        assert animals[1]['age'] == post_animal2['age']
        assert animals[2]['species_name'] == post_animal3['species_name']
        assert animals[2]['common_name'] == post_animal3['common_name']
        assert animals[2]['age'] == post_animal3['age']

        # Cleanup
        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_add_animal_with_negative_age(self, base_url):
        """Test adding an animal with a negative age to the zoo."""
        age = -1
        data = {'species_name': 'Panthera tigris',
                'common_name': 'Tiger',
                'age': age}
        message = json.loads(requests.post(
            base_url + '/animal', data=data).content)
        assert message == f'An age of {age} is not possible'

    def test_get_all_animals_empty_zoo(self, base_url):
        """Test retrieving all animals of an empty zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_all_animals(self, base_url, post_animal1, post_animal2, post_animal3):
        """Test retrieving all animals of a zoo."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 3

        # Cleanup
        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

    def test_get_animal(self, base_url, post_animal1, post_animal2, post_animal3):
        """Test retrieving information about specific animals."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 3

        for animal_dict in animals:
            animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert animal_data['species_name'] == animal_dict['species_name']
            assert animal_data['common_name'] == animal_dict['common_name']
            assert animal_data['age'] == animal_dict['age']

        # Cleanup
        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_get_animal_unknown_id(self, base_url, unknown_id):
        """Test retrieving information about an animal that does not 
        exist."""
        animal_data = json.loads(requests.get(
            base_url + f'/animal/{unknown_id}').content)
        assert animal_data is None

    def test_delete_animal(self, base_url, post_animal1):
        """Test deleting an existing animal."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1

        message = json.loads(requests.delete(base_url + f'/animal/{post_animal1["id"]}').content)
        assert message == f'Animal with ID {post_animal1["id"]} has been removed'

        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 0

    def test_delete_not_existing_animal(self, base_url, unknown_id):
        """Test deleting an animal that does not exist."""
        message = json.loads(requests.delete(
            base_url + f'/animal/{unknown_id}').content)
        assert message == f'Animal with ID {unknown_id} has not been found'

    def test_delete_animal_with_home(self, base_url, post_animal1, post_enclosure1):
        """Test deleting an animal that already lives in an 
        enclosure."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 1
        assert len(enclosures) == 1

        data = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data)
        
        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure1["id"]
        assert len(new_enclosure_data['animals']) == 1
        assert post_animal1["id"] in new_enclosure_data['animals']

        message = json.loads(requests.delete(
            base_url + f'/animal/{post_animal1["id"]}').content)
        assert message == f'Animal with ID {post_animal1["id"]} has been removed'

        new_enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert len(new_enclosure_data['animals']) == 0

        # Cleanup
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0
        
    def test_delete_animal_with_caretaker(self, base_url, post_animal1, post_caretaker1):
        """Test deleting an animal that is already assigned to a
        caretaker."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(animals) == 1
        assert len(caretakers) == 1

        data = {'animal_id': post_animal1["id"],
                'caretaker_id': post_caretaker1["id"]}
        requests.post(base_url + f'/caretaker/{post_caretaker1["id"]}/care/{post_animal1["id"]}', data)
        
        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_caretaker_data = json.loads(requests.get(
            base_url + f'/caretaker/{post_caretaker1["id"]}').content)
        assert new_animal_data['caretaker'] == post_caretaker1["id"]
        assert len(new_caretaker_data['animals']) == 1
        assert post_animal1["id"] in new_caretaker_data['animals']

        message = json.loads(requests.delete(
            base_url + f'/animal/{post_animal1["id"]}').content)
        assert message == f'Animal with ID {post_animal1["id"]} has been removed'

        new_caretaker_data = json.loads(requests.get(
            base_url + f'/caretaker/{post_caretaker1["id"]}').content)
        assert len(new_caretaker_data['animals']) == 0

        # Cleanup
        requests.delete(base_url + f'/caretaker/{post_caretaker1["id"]}')
        animals = json.loads(requests.get(base_url + '/animals').content)
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(animals) == 0
        assert len(caretakers) == 0
        
    def test_delete_animal_with_home_and_caretaker(self, base_url, post_animal1, post_enclosure1, post_caretaker1):
        """Test deleting an animal that already lives in an enclosure 
        and is assigned to a caretaker."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(animals) == 1
        assert len(enclosures) == 1
        assert len(caretakers) == 1

        data1 = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        data2 = {'animal_id': post_animal1["id"],
                'caretaker_id': post_caretaker1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data1)
        requests.post(base_url + f'/caretaker/{post_caretaker1["id"]}/care/{post_animal1["id"]}', data2)
        
        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        new_caretaker_data = json.loads(requests.get(
            base_url + f'/caretaker/{post_caretaker1["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure1["id"]
        assert new_animal_data['caretaker'] == post_caretaker1["id"]
        assert len(new_enclosure_data['animals']) == 1
        assert len(new_caretaker_data['animals']) == 1
        assert post_animal1["id"] in new_enclosure_data['animals']
        assert post_animal1["id"] in new_caretaker_data['animals']

        message = json.loads(requests.delete(
            base_url + f'/animal/{post_animal1["id"]}').content)
        assert message == f'Animal with ID {post_animal1["id"]} has been removed'

        new_enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        new_caretaker_data = json.loads(requests.get(
            base_url + f'/caretaker/{post_caretaker1["id"]}').content)
        assert len(new_enclosure_data['animals']) == 0
        assert len(new_caretaker_data['animals']) == 0

        # Cleanup
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')
        requests.delete(base_url + f'/caretaker/{post_caretaker1["id"]}')
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(animals) == 0
        assert len(enclosures) == 0
        assert len(caretakers) == 0

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

    def test_set_home(self, base_url, post_animal1, post_enclosure1):
        """Test setting the first home of an animal."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 1
        assert len(enclosures) == 1

        for animal_dict in animals:
            assert animal_dict['enclosure'] is None

            data = {'animal_id': animal_dict["id"],
                    'enclosure_id': enclosures[0]["id"]}
            requests.post(base_url + f'/animal/{animal_dict["id"]}/home', data)
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert new_animal_data['enclosure'] == enclosures[0]["id"]

            requests.delete(base_url + f'/animal/{animal_dict["id"]}')
        requests.delete(base_url + f'/enclosure/{enclosures[0]["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

    def test_change_home(self, base_url, post_animal1, post_enclosure1, post_enclosure2):
        """Test changing the home of an animal."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 1
        assert len(enclosures) == 2

        for animal_dict in animals:
            assert animal_dict['enclosure'] is None

            data = {'animal_id': animal_dict["id"],
                    'enclosure_id': enclosures[0]["id"]}
            requests.post(base_url + f'/animal/{animal_dict["id"]}/home', data)
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert new_animal_data['enclosure'] == enclosures[0]["id"]

            data = {'animal_id': animal_dict["id"],
                    'enclosure_id': enclosures[1]["id"]}
            requests.post(base_url + f'/animal/{animal_dict["id"]}/home', data)
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert new_animal_data['enclosure'] == enclosures[1]["id"]

            requests.delete(base_url + f'/animal/{animal_dict["id"]}')
        requests.delete(base_url + f'/enclosure/{enclosures[0]["id"]}')
        requests.delete(base_url + f'/enclosure/{enclosures[1]["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

    def test_set_home_unknown_enclosure(self, base_url, post_animal1, unknown_id):
        """Test setting the home of an animal by using an invalid 
        enclosure ID."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 1
        assert len(enclosures) == 0

        for animal_dict in animals:
            assert animal_dict['enclosure'] is None

            data = {'animal_id': animal_dict["id"],
                    'enclosure_id': unknown_id}
            r = requests.post(
                base_url + f'/animal/{animal_dict["id"]}/home', data)
            b = r.content
            message = json.loads(b)
            assert message == f'Enclosure with ID {unknown_id} has not been found'

            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert new_animal_data['enclosure'] is None

            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

    def test_set_home_unknown_animal(self, base_url, post_enclosure1, unknown_id):
        """Test setting the home of a not existing animal."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 1

        data = {'animal_id': unknown_id,
                'enclosure_id': enclosures[0]["id"]}
        r = requests.post(base_url + f'/animal/{unknown_id}/home', data)
        b = r.content
        message = json.loads(b)
        assert message == f'Animal with ID {unknown_id} has not been found'

        requests.delete(base_url + f'/enclosure/{enclosures[0]["id"]}')

        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

    def test_set_home_unknown_animal_and_unknown_enclosure(self, base_url, unknown_id, unknown_id2):
        """Test setting the home of a not existing animal with a not 
        existing enclosure."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

        data = {'animal_id': unknown_id,
                'enclosure_id': unknown_id2}
        r = requests.post(base_url + f'/animal/{unknown_id}/home', data)
        b = r.content
        message = json.loads(b)
        assert message == f'Animal with ID {unknown_id} has not been found'

    def test_give_birth_no_home(self, base_url, post_animal1):
        """Test giving birth to a new animal when the mother is not 
        living in any enclosure so far."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(animals) == 1
        assert post_animal1["enclosure"] is None

        data = {'animal_id': post_animal1['id']}
        child = json.loads(requests.post(
            base_url + f'/animal/birth', data).content)

        animals = json.loads(requests.get(base_url + f'/animals').content)
        assert len(animals) == 2
        assert post_animal1['enclosure'] is None
        assert child['enclosure'] is None

        # cleanup
        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')

        animals = json.loads(requests.get(base_url + f'/animals').content)
        assert len(animals) == 0

    def test_give_birth_with_home(self, base_url, post_animal1, post_enclosure1):
        """Test giving birth to a new animal when the mother is already 
        living in an enclosure."""
        animals = json.loads(requests.get(base_url + '/animals').content)
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(animals) == 1
        assert len(enclosures) == 1

        data = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data)
        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure1['id']

        data = {'animal_id': post_animal1['id']}
        child = json.loads(requests.post(
            base_url + f'/animal/birth', data).content)

        animals = json.loads(requests.get(base_url + f'/animals').content)
        assert len(animals) == 2
        assert new_animal_data['enclosure'] == post_enclosure1['id']
        assert child['enclosure'] == post_enclosure1['id']

        # cleanup
        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        animals = json.loads(requests.get(base_url + f'/animals').content)
        enclosures = json.loads(requests.get(
            base_url + f'/enclosures').content)
        assert len(animals) == 0
        assert len(enclosures) == 0

    def test_give_birth_unknown_id(self, base_url, unknown_id):
        """Test giving birth with an unknown animal ID."""
        data = {'animal_id': unknown_id}
        message = json.loads(requests.post(
            base_url + f'/animal/birth', data).content)
        assert message == f'Animal with ID {unknown_id} has not been found'


class TestZooEnclosure:
    def test_add_enclosure(self, base_url, post_enclosure1):
        """Test adding a single enclosure to the zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        assert enclosures[0]['name'] == post_enclosure1['name']
        assert enclosures[0]['area'] == post_enclosure1['area']

        # Cleanup
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_add_multiple_enclosures(self, base_url, post_enclosure1, post_enclosure2, post_enclosure3):
        """Test adding multiple enclosures to the zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 3

        assert enclosures[0]['name'] == post_enclosure1['name']
        assert enclosures[0]['area'] == post_enclosure1['area']
        assert enclosures[1]['name'] == post_enclosure2['name']
        assert enclosures[1]['area'] == post_enclosure2['area']
        assert enclosures[2]['name'] == post_enclosure3['name']
        assert enclosures[2]['area'] == post_enclosure3['area']

        # Cleanup
        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_add_enclosure_with_negative_area(self, base_url):
        """Test adding an enclosure with a negative area to the zoo."""
        area = -5
        data = {'name': 'NegativeCave1', 'area': area}
        message = json.loads(requests.post(
            base_url + '/enclosure', data).content)
        assert message == f'An area of {area:.1f} is not possible'

    def test_add_enclosure_with_zero_area(self, base_url):
        """Test adding an enclosure with an area of 0 to the zoo."""
        area = 0
        data = {'name': 'ZeroCage5', 'area': area}
        message = json.loads(requests.post(
            base_url + '/enclosure', data).content)
        assert message == f'An area of {area:.1f} is not possible'

    def test_get_all_enclosures_empty_zoo(self, base_url):
        """Test retrieving all enclosures of an empty zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_get_all_enclosures(self, base_url, post_enclosure1, post_enclosure2, post_enclosure3):
        """Test retrieving all enclosures of a zoo."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 3

        # Cleanup
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

        # Cleanup
        for enclosure_dict in enclosures:
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_get_enclosure_info_unknown_id(self, base_url, unknown_id):
        """Test retrieving information about an enclosure that does not 
        exist."""
        enclosure_data = json.loads(requests.get(
            base_url + f'/enclosure/{unknown_id}').content)
        assert enclosure_data is None

    def test_delete_empty_enclosure(self, base_url, post_enclosure1):
        """Test deleting an existing empty enclosure."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        message = json.loads(requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert message == f'Enclosure with ID {post_enclosure1["id"]} has been removed'

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_delete_not_existing_enclosure(self, base_url, unknown_id):
        """Test deleting an enclosure that does not exist."""
        message = json.loads(requests.delete(
            base_url + f'/enclosure/{unknown_id}').content)
        assert message == f'Enclosure with ID {unknown_id} has not been found'

    def test_delete_enclosure_with_animal_transfer(self, base_url, post_enclosure1, post_enclosure2, post_enclosure3, post_animal1):
        """Test deleting an existing enclosure that is the home of 
        some animals, while other enclosures exist."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 3
        assert len(animals) == 1

        data = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data)

        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure1_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure1["id"]
        assert post_animal1["id"] in new_enclosure1_data['animals']

        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure2_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure2["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure2["id"]
        assert post_animal1["id"] in new_enclosure2_data['animals']

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 2

        requests.delete(base_url + f'/enclosure/{post_enclosure2["id"]}')

        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure3_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure3["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure3["id"]
        assert post_animal1["id"] in new_enclosure3_data['animals']

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        # cleanup
        requests.delete(base_url + f'/animal/{post_animal1["id"]}')
        requests.delete(base_url + f'/enclosure/{post_enclosure3["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 0
        assert len(animals) == 0

    def test_delete_enclosure_cannot_transfer(self, base_url, post_enclosure1, post_animal1):
        """Test deleting an existing enclosure that is the home of 
        some animals, while no other enclosure exists"""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 1
        assert len(animals) == 1

        data = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data)

        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        new_enclosure1_data = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert new_animal_data['enclosure'] == post_enclosure1["id"]
        assert post_animal1["id"] in new_enclosure1_data['animals']

        message = json.loads(requests.delete(
            base_url + f'/enclosure/{post_enclosure1["id"]}').content)
        assert message == (f'Enclosure with ID {post_enclosure1["id"]} has '
                           'not been removed because the animals cannot be '
                           'transferred to another enclosure')

        # cleanup
        requests.delete(base_url + f'/animal/{post_animal1["id"]}')
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 0
        assert len(animals) == 0

    def test_clean_enclosure(self, base_url, post_enclosure1):
        """Test cleaning an enclosure and see if it gets added to the 
        enclosures' cleaning record."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        for enclosure_dict in enclosures:
            requests.post(
                base_url + f'/enclosure/{enclosure_dict["id"]}/clean')
            new_enclosure_data = json.loads(requests.get(
                base_url + f'/enclosure/{enclosure_dict["id"]}').content)
            assert len(new_enclosure_data['cleaning_record']) == 1
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_clean_enclosure_multiple_times(self, base_url, post_enclosure1):
        """Test cleaning an enclosure multiple times and see if it gets 
        added to the enclosures' cleaning record."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        for enclosure_dict in enclosures:
            requests.post(
                base_url + f'/enclosure/{enclosure_dict["id"]}/clean')
            requests.post(
                base_url + f'/enclosure/{enclosure_dict["id"]}/clean')
            requests.post(
                base_url + f'/enclosure/{enclosure_dict["id"]}/clean')
            new_enclosure_data = json.loads(requests.get(
                base_url + f'/enclosure/{enclosure_dict["id"]}').content)
            assert len(new_enclosure_data['cleaning_record']) == 3
            requests.delete(base_url + f'/enclosure/{enclosure_dict["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_clean_enclosure_unknown_id(self, base_url, unknown_id):
        """Test trying to clean an enclosure that does not exist."""
        r = requests.post(base_url + f'/enclosure/{unknown_id}/clean')
        b = r.content
        message = json.loads(b)
        assert message == f'Enclosure with ID {unknown_id} has not been found'

    def test_get_animals_empty_enclosure(self, base_url, post_enclosure1):
        """Test getting all animals of an empty enclosure."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 1

        enclosure_animals = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}/animals').content)
        assert len(enclosure_animals) == 0

        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        assert len(enclosures) == 0

    def test_get_animals_single_animal(self, base_url, post_enclosure1, post_animal1):
        """Test getting all animals of an enclosure with a single 
        animal."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 1
        assert len(animals) == 1

        data = {'animal_id': post_animal1["id"],
                'enclosure_id': post_enclosure1["id"]}
        requests.post(base_url + f'/animal/{post_animal1["id"]}/home', data)

        enclosure_animals = json.loads(requests.get(
            base_url + f'/enclosure/{post_enclosure1["id"]}/animals').content)
        new_animal_data = json.loads(requests.get(
            base_url + f'/animal/{post_animal1["id"]}').content)
        assert len(enclosure_animals) == 1
        assert new_animal_data in enclosure_animals

        requests.delete(base_url + f'/animal/{post_animal1["id"]}')
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 0
        assert len(animals) == 0

    def test_get_animals_multiple_animals(self, base_url, post_enclosure1, post_animal1, post_animal2, post_animal3):
        """Test getting all animals of an enclosure with multiple 
        animals."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 1
        assert len(animals) == 3

        count = 1
        for animal_dict in animals:
            data = {'animal_id': animal_dict["id"],
                    'enclosure_id': post_enclosure1["id"]}
            requests.post(base_url + f'/animal/{animal_dict["id"]}/home', data)
            enclosure_animals = json.loads(requests.get(
                base_url + f'/enclosure/{post_enclosure1["id"]}/animals').content)
            new_animal_data = json.loads(requests.get(
                base_url + f'/animal/{animal_dict["id"]}').content)
            assert len(enclosure_animals) == count
            assert enclosure_animals[-1] == new_animal_data
            count += 1

        for animal_dict in animals:
            requests.delete(base_url + f'/animal/{animal_dict["id"]}')
        requests.delete(base_url + f'/enclosure/{post_enclosure1["id"]}')

        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 0
        assert len(animals) == 0

    def test_get_animals_unknown_enclosure_id(self, base_url, unknown_id):
        """Test getting all animals of a not existing enclosure."""
        enclosures = json.loads(requests.get(base_url + '/enclosures').content)
        animals = json.loads(requests.get(base_url + '/animals').content)
        assert len(enclosures) == 0
        assert len(animals) == 0

        message = json.loads(requests.get(
            base_url + f'/enclosure/{unknown_id}/animals').content)
        assert message == f'Enclosure with ID {unknown_id} has not been found'


class TestZooCaretaker:
    def test_add_caretaker(self, base_url, post_caretaker1):
        """Test adding a single caretaker to the zoo."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 1

        assert caretakers[0]['name'] == post_caretaker1['name']
        assert caretakers[0]['address'] == post_caretaker1['address']

        # Cleanup
        requests.delete(base_url + f'/caretaker/{post_caretaker1["id"]}')
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 0

    def test_add_multiple_caretakers(self, base_url, post_caretaker1, post_caretaker2, post_caretaker3):
        """Test adding multiple caretakers to the zoo."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 3

        assert caretakers[0]['name'] == post_caretaker1['name']
        assert caretakers[0]['address'] == post_caretaker1['address']
        assert caretakers[1]['name'] == post_caretaker2['name']
        assert caretakers[1]['address'] == post_caretaker2['address']
        assert caretakers[2]['name'] == post_caretaker3['name']
        assert caretakers[2]['address'] == post_caretaker3['address']

        # Cleanup
        for caretaker_dict in caretakers:
            requests.delete(base_url + f'/caretaker/{caretaker_dict["id"]}')

        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 0

    def test_get_all_caretakers_empty_zoo(self, base_url):
        """Test retrieving all caretakers of an empty zoo."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 0

    def test_get_all_caretakers(self, base_url, post_caretaker1, post_caretaker2, post_caretaker3):
        """Test retrieving all caretakers of a zoo."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 3

        # Cleanup
        for caretaker_dict in caretakers:
            requests.delete(base_url + f'/caretaker/{caretaker_dict["id"]}')

    def test_get_caretaker_info(self, base_url, post_caretaker1, post_caretaker2, post_caretaker3):
        """Test retrieving information about specific caretakers."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 3

        for caretaker_dict in caretakers:
            caretaker_data = json.loads(requests.get(
                base_url + f'/caretaker/{caretaker_dict["id"]}').content)
            assert caretaker_data['name'] == caretaker_dict['name']
            assert caretaker_data['address'] == caretaker_dict['address']

        # Cleanup
        for caretaker_dict in caretakers:
            requests.delete(base_url + f'/caretaker/{caretaker_dict["id"]}')

        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 0

    def test_get_caretaker_info_unknown_id(self, base_url, unknown_id):
        """Test retrieving information about a caretaker that does not 
        exist."""
        caretaker_data = json.loads(requests.get(
            base_url + f'/caretaker/{unknown_id}').content)
        assert caretaker_data is None

    def test_delete_caretaker_without_animals(self, base_url, post_caretaker1):
        """Test deleting an existing caretaker that does not care for 
        any animals so far."""
        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 1

        message = json.loads(requests.delete(
            base_url + f'/caretaker/{post_caretaker1["id"]}').content)
        assert message == f'Caretaker with ID {post_caretaker1["id"]} has been removed'

        caretakers = json.loads(requests.get(base_url + '/caretakers').content)
        assert len(caretakers) == 0

    def test_delete_not_existing_caretaker(self, base_url, unknown_id):
        """Test deleting a caretaker that does not exist."""
        message = json.loads(requests.delete(
            base_url + f'/caretaker/{unknown_id}').content)
        assert message == f'Caretaker with ID {unknown_id} has not been found'
