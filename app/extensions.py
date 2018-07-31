from flask.json import JSONEncoder
from datetime import datetime
from utils import DATE_FORMAT


# Overrides flask JSONEncoder.
class AppJSONEncoder(JSONEncoder):

    def default(self, obj):
        """
        If obj is a datetime object convert it to the app format.
        :param obj:
        """
        try:
            if isinstance(obj, datetime):
                return obj.strftime(DATE_FORMAT)
            iterable = iter(obj)
        except TypeError:
            pass
        else:
            return list(iterable)
        return JSONEncoder.default(self, obj)
