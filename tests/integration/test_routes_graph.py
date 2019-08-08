import unittest
from routes_graph import RoutesGraph


class RoutesGraphTestCase(unittest.TestCase):

    def test_load_data_with_test_data_fills_airlines(self):
        import os

        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        self.assertIn('AC', routes_graph.airlines)

    def test_load_data_with_full_data_loads_six_airlines(self):
        import os

        os.environ['DATADIR'] = 'full'
        routes_graph = RoutesGraph()
        self.assertEqual(len(routes_graph.airlines), 6)

    def test_load_data_with_full_data_loads_turkish_airlines(self):
        import os

        os.environ['DATADIR'] = 'full'
        routes_graph = RoutesGraph()
        self.assertIn('TK', routes_graph.airlines)

    def test_load_data_with_test_data_creates_adjacency_dict_of_lists_size_four(self):
        import os

        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        self.assertEqual(len(routes_graph.airports), 5)

    def test_load_data_with_full_data_creates_adjacency_dict_of_lists_size_5652(self):
        import os

        os.environ['DATADIR'] = 'full'
        routes_graph = RoutesGraph()
        self.assertEqual(len(routes_graph.airports), 5653)

    def test_get_airport_connections_with_test_data_returns_yyz(self):
        import os

        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('YYZ'), list)

    def test_get_airport_connections_with_full_data_returns_ykh(self):
        import os

        os.environ['DATADIR'] = 'full'
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('YKH'), list)

    def test_get_airport_connections_with_test_data_raises_exception_when_unknown_airport(self):
        import os
        from exceptions import AirportNotFound

        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('YKH')

    def test_get_airport_connections_with_test_data_raises_exception_when_airport_in_lowercase(self):
        import os
        from exceptions import AirportNotFound

        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('yyz')
