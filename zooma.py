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
api.title = 'Zooma'

create_animal_parser = reqparse.RequestParser()
create_animal_parser.add_argument('species_name', type=str, required=True,
                                  help='The scientific name of the animal. For example \'Panthera tigris\'')
create_animal_parser.add_argument('common_name', type=str, required=True,
                                  help='The common name of the animal. For example \'Tiger\'')
create_animal_parser.add_argument('age', type=int, required=True,
                                  help='The age of the animal. For example \'12\'')

set_home_parser = reqparse.RequestParser()
set_home_parser.add_argument('enclosure_id', type=str, required=True,
                             help='The ID of the enclosure where the animal will live. For example \'bc889d3a-f378-416c-9c88-2dae19fc0f3c\'')


@api.route('/animal')
class CreateAnimal(Resource):
    @api.doc(parser=create_animal_parser)
    def post(self):
        # get the post parameters
        args = create_animal_parser.parse_args()
        species_name = args['species_name']
        common_name = args['common_name']
        age = args['age']

        # create a new animal object
        new_animal = Animal(species_name, common_name, age)

        # add the animal to the zoo
        my_zoo.add_animal(new_animal)
        return jsonify(new_animal)


@api.route('/animal/<animal_id>')
class AnimalID(Resource):
    def get(self, animal_id):
        search_result = my_zoo.get_animal(animal_id)
        return jsonify(search_result)

    def delete(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')
        my_zoo.remove_animal(targeted_animal)
        return jsonify(f'Animal with ID {animal_id} has been removed')


@api.route('/animals')
class AllAnimals(Resource):
    def get(self):
        return jsonify(my_zoo.get_all_animals())


@api.route('/animal/<animal_id>/feed')
class FeedAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')
        targeted_animal.feed()
        return jsonify(targeted_animal)


@api.route('/animal/<animal_id>/vet')
class VetAnimal(Resource):
    def post(self, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')
        targeted_animal.vet()
        return jsonify(targeted_animal)


@api.route('/animal/<animal_id>/home')
class SetHomeAnimal(Resource):
    def post(self, animal_id):
        args = set_home_parser.parse_args()
        enclosure_id = args['enclosure_id']
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} has not been found')
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')
        targeted_animal.set_home(enclosure_id)
        return jsonify(targeted_animal)


if __name__ == '__main__':
    app.run(debug=False, port=7890)
