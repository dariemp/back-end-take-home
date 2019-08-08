import unittest
from unittest.mock import patch
from routes_graph import RoutesGraph


@patch('csv.reader')
@patch('%s.open' % __name__)
class RoutesGraphTestCase(unittest.TestCase):

    def test_load_data_loads_airlines(self, mock_open, mock_csv_reader):
        mock_csv_reader.side_effect = lambda x: iter([['Name','2 Digit Code','3 Digit Code','Country'],
                                                      ['Air Canada', 'AC', 'ACA', 'Canada'],
                                                      ['WestJet', 'WS', 'WJA','Canada']])
        routes_graph = RoutesGraph()
        self.assertEqual(routes_graph.airlines, {'AC', 'WS'})

    def test_load_data_loads_airports(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        routes_graph = RoutesGraph()
        self.assertEqual(routes_graph.airports, {'YYZ', 'BOG'})

    def test_get_airport_connections_returns_yyz(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('YYZ'), list)

    def test_get_airport_connections_returns_bog(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        routes_graph = RoutesGraph()
        self.assertIsInstance(routes_graph.get_airport_connections('BOG'), list)

    def test_get_airport_connections_raises_exception_when_unknown_airport(self, mock_open, mock_csv_reader):
        from exceptions import AirportNotFound

        self._set_test_airports(mock_csv_reader)
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('YKH')

    def test_get_airport_connections_raises_exception_when_airport_in_lowercase(self, mock_open, mock_csv_reader):
        import os
        from exceptions import AirportNotFound

        self._set_test_airports(mock_csv_reader)
        routes_graph = RoutesGraph()
        with self.assertRaises(AirportNotFound):
            routes_graph.get_airport_connections('yyz')

    def _set_test_airports(self, mock_csv_reader):
        mock_csv_reader.side_effect = lambda x: iter([['Name', 'City', 'Country', 'IATA 3', 'Latitute', 'Longitude'],
                                                      ['Lester B. Pearson International Airport', 'Toronto', 'Canada', 'YYZ', 43.67720032, -79.63059998],
                                                      ['El Dorado International Airport', 'Bogota', 'Colombia', 'BOG', 4.70159, -74.1469]])
