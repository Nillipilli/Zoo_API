from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource

from zoo import Zoo
from zoo_json_utils import CustomJSONProvider
from animal import Animal, Caretaker, Enclosure

my_zoo = Zoo()

app = Flask(__name__)
# had to change this using this post: https://shorturl.at/qEJZ6
app.json = CustomJSONProvider(app)
api = Api(app)

animal_parser = reqparse.RequestParser()
animal_parser.add_argument('species', type=str, required=True,
                           help='The scientific name of the animal, e,g. Panthera tigris')
animal_parser.add_argument('name', type=str, required=True,
                           help='The common name of the animal, e.g., Tiger')
animal_parser.add_argument(
    'age', type=int, required=True, help='The age of the animal, e.g., 12')


@api.route('/animal')
class AddAnimalAPI(Resource):
    @api.doc(parser=animal_parser)
    def post(self):
        # get the post parameters
        args = animal_parser.parse_args()
        name = args['name']
        species = args['species']
        age = args['age']
        # create a new animal object
        new_animal = Animal(species, name, age)
        # add the animal to the zoo
        my_zoo.add_animal(new_animal)
        return jsonify(new_animal)


@api.route('/animal/<animal_id>')
class Animal_ID(Resource):
    def get(self, animal_id):
        search_result = my_zoo.get_animal(animal_id)
        # this is automatically jsonified by flask-restx
        return jsonify(search_result)

    def delete(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")
        my_zoo.remove_animal(targeted_animal)
        return jsonify("Animal with ID {animal_id} was removed")


@api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        return jsonify(my_zoo.animals)


@api.route('/animals/<animal_id>/feed')
class FeedAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify("Animal with ID {animal_id} was not found")
        targeted_animal.feed()
        return jsonify(targeted_animal)


if __name__ == '__main__':
    app.run(debug=False, port=7890)
