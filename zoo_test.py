import json
import pytest
import requests
from animal import Animal


@pytest.fixture
def post_tiger1(base_url: str, tiger1: Animal) -> None:
    tiger1_data = {"species": tiger1.species_name,
                   "name": tiger1.common_name,
                   "age": tiger1.age}
    requests.post(base_url + "/animal", data=tiger1_data)


class Testzoo ():

    def test_one(self, base_url: str, post_tiger1: None):
        x = requests.get(base_url+"/animals")
        js = x.content
        animals = json.loads(js)
        assert (len(animals) == 1)
