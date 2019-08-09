class AirportNotFound(Exception):
    pass

class OriginEqualsDestination(Exception):
    pass

class InvalidInput(Exception):

    def __init__(self, status_code, message):
        self._status_code = status_code
        self._message = message

    def as_flask_restful_response(self):
        return {'message': self._message}, self._status_code
