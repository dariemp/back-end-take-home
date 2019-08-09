from flask_restful import Resource

class RouteResource(Resource):

    def __init__(self, routes_graph):
        self._routes_graph = routes_graph

    def get(self):
        from flask import request
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        route_data = self._routes_graph.get_route(origin, destination)
        return self._build_response(route_data, destination)

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
