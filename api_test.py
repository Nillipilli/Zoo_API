import json
import pytest
import requests


@pytest.fixture
def zoo_with_one_animal(base_url):
    requests.post(base_url+"/animal",
                  {"species": "tiger", "name": "btiger", "age": 3})
    response = requests.get(base_url + "/animals")

    return response.content


def test_zoo1(zoo_with_one_animal):
    jo = json.loads(zoo_with_one_animal)

    print(jo)

    assert jo[0]["common_name"] == "btiger"
    assert (len(jo) == 1)
