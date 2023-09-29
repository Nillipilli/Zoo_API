import json
from datetime import date
from json import JSONEncoder
from flask.json.provider import JSONProvider


# had to add this class using this post: https://shorturl.at/qEJZ6
class CustomJSONProvider(JSONProvider):

    def dumps(self, obj, **kwargs):
        return json.dumps(obj, **kwargs, cls=ZooJsonEncoder)

    def loads(self, s: str | bytes, **kwargs):
        return json.loads(s, **kwargs)


class ZooJsonEncoder(JSONEncoder):
    def default(self, obj):
        try:
            # handle date separately
            if isinstance(obj, date):
                return obj.isoformat()

            # check if object is iterable
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            # when object is not iterable
            return list(iterable)

        return obj.__dict__
