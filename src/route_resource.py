from flask_restful import Resource

class RouteResource(Resource):

    def __init__(self, routes_graph):
        self._routes_graph = routes_graph

    def get(self):
        from exceptions import InvalidInput, OriginEqualsDestination

        try:
            origin, destination = self._get_and_validate_input()
            route_data = self._routes_graph.get_route(origin, destination)
            return self._build_response(route_data, destination)
        except InvalidInput as exception:
            return exception.as_flask_restful_response()
        except OriginEqualsDestination:
            return {'message': 'Take the bus, please'}, 400

    def _get_and_validate_input(self):
        from flask import request

        origin = request.args.get('origin')
        destination = request.args.get('destination')
        origin = self._validate_origin(origin)
        destination = self._validate_destination(destination)
        return origin, destination

    def _validate_origin(self, origin):
        return self._validate_airport_code(origin, 'origin')

    def _validate_destination(self, destination):
        return self._validate_airport_code(destination, 'destination')

    def _validate_airport_code(self, airport_code, endpoint_type):
        from exceptions import InvalidInput

        if not airport_code:
            raise InvalidInput(400, 'Missing {} airport'.format(endpoint_type))
        airport_code = airport_code.upper()
        if not self._routes_graph.is_valid_airport(airport_code):
            raise InvalidInput(404, 'Invalid {}'.format(endpoint_type.title()))
        return airport_code

    def _build_response(self, route_data, destination_airport_code):
        if route_data and route_data[-1][0] == destination_airport_code:
            return {'route': self._build_route_from_data(route_data)}
        else:
            return {'message': 'No Route'}, 404

    def _build_route_from_data(self, route_data):
        route = []
        next_airport = route_data.pop(0)
        while len(route_data) > 0:
            next_airport = self._add_connection_to_route(next_airport, route, route_data)
        return route

    def _add_connection_to_route(self, origin_airport, route, route_data):
        destination = route_data.pop(0)
        flight = {
            'airline': destination[1],
            'from': origin_airport[0],
            'to': destination[0]
        }
        route.append(flight)
        return destination
