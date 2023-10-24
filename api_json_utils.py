import json
from datetime import date
from json import JSONEncoder
from flask.json.provider import JSONProvider

from zoo_objects import Animal, Caretaker, Enclosure


# had to add this class using this post: 
# https://stackoverflow.com/questions/44146087/pass-user-built-json-encoder-into-flasks-jsonify
class CustomJSONProvider(JSONProvider):

    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=ZooJsonEncoder)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)


class ZooJsonEncoder(JSONEncoder):
    def default(self, obj):
        try:
            # handle date separately (includes datetime)
            if isinstance(obj, date):
                return obj.isoformat()

            # handle Animal, Caretaker and Enclosure separately;
            # to handle circular references
            elif isinstance(obj, (Animal, Caretaker, Enclosure)):
                return obj.to_json()

            # check if object is iterable
            iterable = iter(obj)
        except TypeError:
            pass

        # gets executed when no exception occured
        else:
            # when object is not iterable
            return list(iterable)

        return obj.__dict__
