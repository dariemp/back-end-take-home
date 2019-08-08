import os
import csv

class RoutesGraph(object):

    def __init__(self):
        self.load_data()

    @property
    def airlines(self):
        return self._airlines

    @property
    def airports(self):
        return set(self._airports_connections.keys())

    def load_data(self):
        from data_loader import DataLoader

        data_loader = DataLoader()
        self._airlines = data_loader.load_airlines()
        self._airports_connections = data_loader.load_airports_and_routes(self._airlines)

    def get_route(self, origin_airport_code, destination_airport_code):
        if origin_airport_code == destination_airport_code:
            raise Exception()
        return self._get_route(origin_airport_code, destination_airport_code)

    def get_airport_connections(self, airport_code):
        try:
            return self._airports_connections[airport_code]
        except KeyError:
            from exceptions import AirportNotFound
            raise AirportNotFound()

    def _get_route(self, origin_airport_code, destination_airport_code):
        visited_airports_set = set()
        queue = []
        airport_code = origin_airport_code
        route_data = [(airport_code, None)]
        queue.append(route_data)
        while airport_code != destination_airport_code and len(queue) > 0:
            route_data = self._explore_connections(route_data, visited_airports_set, queue)
            airport_code = route_data[-1][0]
            visited_airports_set.add(airport_code)
        return self._build_route(airport_code, destination_airport_code, route_data)

    def _explore_connections(self, route_data, visited_airports_set, queue):
        airport_code = route_data[-1][0]
        airport_connections = self.get_airport_connections(airport_code)
        connections_not_visited = self._get_connections_not_visited(airport_connections, visited_airports_set)
        for connection_airport_code in connections_not_visited:
            connection_airline = airport_connections[connection_airport_code][0]
            self._add_connection_to_queue(connection_airport_code, connection_airline, route_data, queue)
        route_data = queue.pop(0)
        return route_data

    def _get_connections_not_visited(self, airport_connections, visited_airports_set):
        return set(airport_connections.keys()) - visited_airports_set

    def _add_connection_to_queue(self, airport_code, airline, route_data, queue):
        route_entry = (airport_code, airline)
        connection_route_data = route_data + [route_entry]
        queue.append(connection_route_data)

    def _build_route(self, last_airport_code, destination_airport_code, route_data):
        if last_airport_code == destination_airport_code:
            return self._build_route_from_data(route_data)
        return None

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
