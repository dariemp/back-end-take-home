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
        self.assertEqual(routes_graph.airports, {'YYZ', 'BOG', 'LAX', 'JFK', 'YVR'})

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
        expected_route = [('YYZ', None), ('JFK', 'AC')]
        self.assertEqual(expected_route, route)

    def test_get_route_returns_route_yyz_yvr(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        route = routes_graph.get_route('YYZ', 'YVR')
        expected_route = [('YYZ', None), ('JFK', 'AC'), ('LAX', 'UA'), ('YVR', 'AC')]
        self.assertEqual(expected_route, route)

    def test_get_route_raises_exception_if_origin_equals_destination(self, mock_load_airlines, mock_load_airports_and_routes):
        from exceptions import OriginEqualsDestination

        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        with self.assertRaises(OriginEqualsDestination):
            routes_graph.get_route('YYZ', 'YYZ')

    def test_get_route_returns_none_if_route_not_found(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertIsNone(routes_graph.get_route('YYZ', 'ORD'))

    def test_is_valid_airport_returns_true_if_airports_exists(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertTrue(routes_graph.is_valid_airport('YYZ'))

    def test_is_valid_airport_returns_false_if_airports_does_not_exists(self, mock_load_airlines, mock_load_airports_and_routes):
        self._set_test_airports_connections(mock_load_airports_and_routes)
        routes_graph = RoutesGraph()
        self.assertFalse(routes_graph.is_valid_airport('XXX'))

    def _set_test_airports_connections(self, mock_load_airports_and_routes):
        mock_load_airports_and_routes.return_value = {
            'YYZ': {'JFK': ['AC'],
                    'BOG': ['AC']},
            'JFK': {'YYZ': ['AC'],
                    'LAX': ['UA']},
            'LAX': {'JFK': ['UA'],
                    'YVR': ['AC']},
            'YVR': {'LAX': ['AC']},
            'BOG': {'YYZ': ['AC']}
        }
