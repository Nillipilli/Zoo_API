from flask import Flask, jsonify
from flask_restx import Api, reqparse, Resource

from zoo import Zoo
from api_json_utils import CustomJSONProvider
from zoo_objects import Animal, Caretaker, Enclosure

my_zoo = Zoo()

# had to change how json gets handled using this post: https://shorturl.at/qEJZ6
app = Flask(__name__)
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

create_enclosure_parser = reqparse.RequestParser()
create_enclosure_parser.add_argument('name', type=str, required=True,
                                     help='The name of the enclosure. For example \'cave1\'')
create_enclosure_parser.add_argument('area', type=float, required=True,
                                     help='The total area of the enclosure in square meters. For example \'25.5\'')

create_caretaker_parser = reqparse.RequestParser()
create_caretaker_parser.add_argument('name', type=str, required=True,
                                     help='The name of the caretaker. For example \'Laetitia\'')
create_caretaker_parser.add_argument('address', type=str, required=True,
                                     help='The address of the caretaker. For example \'Blond-Street 19\'')

set_home_parser = reqparse.RequestParser()
set_home_parser.add_argument('enclosure_id', type=str, required=True,
                             help='The ID of the enclosure where the animal will live. For example \'en889d3a-f378-416c-9c88-2dae19fc0f3c\'')

give_birth_parser = reqparse.RequestParser()
give_birth_parser.add_argument('animal_id', type=str, required=True,
                               help='The ID of the mother animal. For example \'an889d3a-f378-416c-9c88-2dae19fc0f3c\'')

animal_death_parser = reqparse.RequestParser()
animal_death_parser.add_argument('animal_id', type=str, required=True,
                                 help='The ID of the animal that died. For example \'an889d3a-f378-416c-9c88-2dae19fc0f3c\'')


# ---- Animal API calls ----


@api.route('/animal')
class CreateAnimal(Resource):
    @api.doc(parser=create_animal_parser)
    def post(self):
        # get the parameters
        args = create_animal_parser.parse_args()
        species_name = args['species_name']
        common_name = args['common_name']
        age = args['age']

        if age < 0:
            return jsonify(f'An age of {age} is not possible')

        # create a new animal object
        new_animal = Animal(species_name, common_name, age)

        # add the animal to the zoo
        my_zoo.add_animal(new_animal)
        return jsonify(new_animal)


@api.route('/animal/<animal_id>')
class AnimalID(Resource):
    def get(self, animal_id):
        # returns None when no animal with the given ID exists
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
    @api.doc(parser=set_home_parser)
    def post(self, animal_id):
        args = set_home_parser.parse_args()
        enclosure_id = args['enclosure_id']

        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')

        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} has not been found')

        targeted_animal.set_home(targeted_enclosure)
        return jsonify(targeted_animal)


@api.route('/animal/birth')
class GiveBirthAnimal(Resource):
    @api.doc(parser=give_birth_parser)
    def post(self):
        args = give_birth_parser.parse_args()
        animal_id = args['animal_id']

        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')

        child = targeted_animal.birth()
        my_zoo.add_animal(child)
        return jsonify(child)


@api.route('/animal/death')
class DeathAnimal(Resource):
    @api.doc(parser=animal_death_parser)
    def post(self):
        args = animal_death_parser.parse_args()
        animal_id = args['animal_id']

        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')

        my_zoo.remove_animal(targeted_animal)
        return jsonify(f'Animal with ID {animal_id} has died')


# ---- Enclosure API calls ----


@api.route('/enclosure')
class CreateEnclosure(Resource):
    @api.doc(parser=create_enclosure_parser)
    def post(self):
        args = create_enclosure_parser.parse_args()
        name = args['name']
        area = args['area']

        if area <= 0:
            return jsonify(f'An area of {area} is not possible')

        new_enclosure = Enclosure(name, area)
        my_zoo.add_enclosure(new_enclosure)
        return jsonify(new_enclosure)


@api.route('/enclosure/<enclosure_id>')
class EnclosureID(Resource):
    def get(self, enclosure_id):
        # returns None when no enclosure with the given ID exists
        search_result = my_zoo.get_enclosure(enclosure_id)
        return jsonify(search_result)

    def delete(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} has not been found')
        if not my_zoo.remove_enclosure(targeted_enclosure):
            return jsonify((f'Enclosure with ID {enclosure_id} has not been '
                            'removed because the animals cannot be '
                            'transferred to another enclosure'))
        return jsonify(f'Enclosure with ID {enclosure_id} has been removed')


@api.route('/enclosures')
class AllEnclosures(Resource):
    def get(self):
        return jsonify(my_zoo.get_all_enclosures())


@api.route('/enclosure/<enclosure_id>/clean')
class CleanEnclosure(Resource):
    def post(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} has not been found')
        targeted_enclosure.clean()
        return jsonify(targeted_enclosure)


@api.route('/enclosure/<enclosure_id>/animals')
class AllAnimalsInEnclosure(Resource):
    def get(self, enclosure_id):
        targeted_enclosure = my_zoo.get_enclosure(enclosure_id)
        if not targeted_enclosure:
            return jsonify(f'Enclosure with ID {enclosure_id} has not been found')
        animals = targeted_enclosure.get_animals()
        return jsonify(animals)


# ---- Caretaker API calls ----


@api.route('/caretaker')
class CreateCaretaker(Resource):
    @api.doc(parser=create_caretaker_parser)
    def post(self):
        args = create_caretaker_parser.parse_args()
        name = args['name']
        address = args['address']

        new_caretaker = Caretaker(name, address)
        my_zoo.add_caretaker(new_caretaker)
        return jsonify(new_caretaker)


@api.route('/caretaker/<caretaker_id>')
class CaretakerID(Resource):
    def get(self, caretaker_id):
        # returns None when no caretaker with the given ID exists
        search_result = my_zoo.get_caretaker(caretaker_id)
        return jsonify(search_result)

    def delete(self, caretaker_id):
        targeted_caretaker = my_zoo.get_caretaker(caretaker_id)
        if not targeted_caretaker:
            return jsonify(f'Caretaker with ID {caretaker_id} has not been found')

        if not my_zoo.remove_caretaker(targeted_caretaker):
            return jsonify((f'Caretaker with ID {caretaker_id} has not been '
                            'removed because the animals cannot be '
                            'transferred to another caretaker'))

        return jsonify(f'Caretaker with ID {caretaker_id} has been removed')


@api.route('/caretakers')
class AllCaretakers(Resource):
    def get(self):
        return jsonify(my_zoo.get_all_caretakers())


@api.route('/caretaker/<caretaker_id>/care/<animal_id>/')
class AssignCaretaker(Resource):
    def post(self, caretaker_id, animal_id):
        targeted_animal = my_zoo.get_animal(animal_id)
        if not targeted_animal:
            return jsonify(f'Animal with ID {animal_id} has not been found')

        targeted_caretaker = my_zoo.get_caretaker(caretaker_id)
        if not targeted_caretaker:
            return jsonify(f'Caretaker with ID {caretaker_id} has not been found')

        targeted_animal.set_caretaker(targeted_caretaker)
        return jsonify(targeted_caretaker)


if __name__ == '__main__':
    app.run(debug=False, port=7890)
