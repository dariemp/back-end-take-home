import unittest
from unittest.mock import patch
from data_loader import DataLoader


@patch('csv.reader')
@patch('%s.open' % __name__)
class DataLoaderTestCase(unittest.TestCase):

    def test_load_data_loads_airlines(self, mock_open, mock_csv_reader):
        mock_csv_reader.side_effect = lambda x: iter([['Name','2 Digit Code','3 Digit Code','Country'],
                                                      ['Air Canada', 'AC', 'ACA', 'Canada'],
                                                      ['WestJet', 'WS', 'WJA','Canada']])
        data_loader = DataLoader()
        self.assertEqual(data_loader.load_airlines(), {'AC', 'WS'})

    def test_load_data_loads_airports(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        data_loader = DataLoader()
        self.assertEqual(data_loader.load_airports(), {'YYZ':[], 'BOG':[]})

    def test_get_airport_connections_returns_yyz(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        data_loader = DataLoader()
        self.assertIsInstance(data_loader.load_airports()['YYZ'], list)

    def test_get_airport_connections_returns_bog(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        data_loader = DataLoader()
        self.assertIsInstance(data_loader.load_airports()['BOG'], list)

    def test_get_airport_connections_raises_exception_when_unknown_airport(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        data_loader = DataLoader()
        with self.assertRaises(KeyError):
            data_loader.load_airports()['YKH']

    def test_get_airport_connections_raises_exception_when_airport_in_lowercase(self, mock_open, mock_csv_reader):
        self._set_test_airports(mock_csv_reader)
        data_loader = DataLoader()
        with self.assertRaises(KeyError):
            data_loader.load_airports()['yyz']

    def _set_test_airports(self, mock_csv_reader):
        mock_csv_reader.side_effect = lambda x: iter([['Name', 'City', 'Country', 'IATA 3', 'Latitute', 'Longitude'],
                                                      ['Lester B. Pearson International Airport', 'Toronto', 'Canada', 'YYZ', 43.67720032, -79.63059998],
                                                      ['El Dorado International Airport', 'Bogota', 'Colombia', 'BOG', 4.70159, -74.1469]])
