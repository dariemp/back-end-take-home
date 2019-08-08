import unittest
from unittest.mock import patch
from data_loader import DataLoader
from routes_graph import RoutesGraph


@patch.object(DataLoader, 'load_airports_and_routes')
@patch.object(DataLoader, 'load_airlines')
class RoutesGraphTestCase(unittest.TestCase):

    def test_load_data_loads_airlines(self, mock_load_airlines, mock_load_airports_and_routes):
        mock_load_airlines.return_value = {'AC', 'WS'}
        routes_graph = RoutesGraph()
        self.assertEqual(routes_graph.airlines, {'AC', 'WS'})

    def test_load_data_loads_airports(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertEqual(routes_graph.airports, {'YYZ', 'BOG', 'LAX', 'JFK'})

    def test_get_airport_connections_returns_yyz(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('YYZ'), dict)

    def test_get_airport_connections_returns_bog(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('BOG'), dict)

    def test_get_airport_connections_raises_exception_when_unknown_airport(self, mock_load_airlines, mock_load_airports_and_routes):
        from exceptions import AirportNotFound

        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('YKH')

    def test_get_airport_connections_raises_exception_when_airport_in_lowercase(self, mock_load_airlines, mock_load_airports_and_routes):
        import os
        from exceptions import AirportNotFound

        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('yyz')

    def test_get_route_returns_route_yyz_jfk(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        route = routes_graph.get_route('YYZ', 'JFK')
        expected_route = [{'airline': 'AC', 'from': 'YYZ', 'to': 'JFK'}]
        self.assertEqual(expected_route, route)

    def test_get_route_returns_route_yyz_yvr(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        route = routes_graph.get_route('YYZ', 'YVR')
        expected_route = [{'airline': 'AC', 'from': 'YYZ', 'to': 'JFK'},
                          {'airline': 'UA', 'from': 'JFK', 'to': 'LAX'},
                          {'airline': 'AC', 'from': 'LAX', 'to': 'YVR'}]
        self.assertEqual(expected_route, route)

    def _set_test_airports_connections(self, mock_load_airports_and_routes):
        mock_load_airports_and_routes.return_value = {
            'YYZ': {'JFK': ['AC']},
            'JFK': {'LAX': ['UA']},
            'LAX': {'YVR': ['AC']},
            'BOG': {'YYZ': ['AC']}
        }
