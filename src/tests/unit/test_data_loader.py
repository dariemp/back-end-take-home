import unittest
from unittest.mock import patch
from data_loader import DataLoader


@patch('csv.reader')
@patch('builtins.open')
class DataLoaderTestCase(unittest.TestCase):

    class MockFileObject(object):
        def __init__(self, file_path):
            self._file_path = file_path

        def __enter__(self):
            return self._file_path.rsplit('/', 1)[-1]

        def __exit__(self, *args, **kwargs):
            pass

    def test_load_airlines_loads_airlines(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        data_loader = DataLoader()
        self.assertEqual(data_loader.load_airlines(), {'AC', 'UA', 'WS'})

    def test_load_airports_and_routes_loads_airports(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        self.assertEqual(set(data_loader.load_airports_and_routes(valid_airlines).keys()), {'YYZ', 'LAX', 'BOG', 'JFK', 'YVR'})

    def test_load_airports_and_routes_returns_yyz(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        self.assertIsInstance(data_loader.load_airports_and_routes(valid_airlines)['YYZ'], dict)

    def test_load_airports_and_routes_returns_bog(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        self.assertIsInstance(data_loader.load_airports_and_routes(valid_airlines)['BOG'], dict)

    def test_load_airports_and_routes_raises_exception_when_unknown_airport(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        with self.assertRaises(KeyError):
            data_loader.load_airports_and_routes(valid_airlines)['YKH']

    def test_load_airports_and_routes_raises_exception_when_airport_in_lowercase(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        with self.assertRaises(KeyError):
            data_loader.load_airports_and_routes(valid_airlines)['yyz']

    def test_load_airports_and_routes_loads_route_yyz_to_jfk(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        airports_connections = data_loader.load_airports_and_routes(valid_airlines)
        self.assertIn('JFK', airports_connections['YYZ'])

    def test_load_airports_and_routes_loads_route_yyz_to_bog(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        airports_connections = data_loader.load_airports_and_routes(valid_airlines)
        self.assertIn('BOG', airports_connections['YYZ'])

    def test_load_airports_and_routes_loads_route_lax_to_yvr(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        airports_connections = data_loader.load_airports_and_routes(valid_airlines)
        self.assertIn('YVR', airports_connections['LAX'])

    def test_load_airports_and_routes_loads_route_does_not_load_route_bog_yyz(self, mock_open, mock_csv_reader):
        self._prepare_mocks(mock_open, mock_csv_reader)
        valid_airlines = self._get_valid_airlines_set()
        data_loader = DataLoader()
        airports_connections = data_loader.load_airports_and_routes(valid_airlines)
        self.assertNotIn('YYZ', airports_connections['BOG'])

    def _prepare_mocks(self, mock_open, mock_csv_reader):
        self._set_mock_open_return_values(mock_open)
        self._set_csv_reader_return_values(mock_csv_reader)

    def _set_mock_open_return_values(self, mock_open):
        mock_open.side_effect = self._get_mock_file

    def _get_mock_file(self, file_path, mode, **kwargs):
        return self.MockFileObject(file_path)

    def _set_csv_reader_return_values(self, mock_csv_reader):
        mock_csv_reader.side_effect = lambda file_spec: \
            {
                'airlines.csv': self._get_test_airlines,
                'airports.csv': self._get_test_airports,
                'routes.csv': self._get_test_routes
            }[file_spec]()

    def _get_test_airlines(self):
        return iter(
            [['Name','2 Digit Code','3 Digit Code','Country'],
             ['Air Canada', 'AC', 'ACA', 'Canada'],
             ['WestJet', 'WS', 'WJA','Canada'],
             ['United Airlines', 'UA', 'UAL', 'United States']])

    def _get_valid_airlines_set(self):
        return set(['AC', 'UA', 'WS'])

    def _get_test_airports(self):
        return iter(
            [['Name', 'City', 'Country', 'IATA 3', 'Latitute', 'Longitude'],
             ['Lester B. Pearson International Airport', 'Toronto', 'Canada', 'YYZ', 43.67720032, -79.63059998],
             ['El Dorado International Airport', 'Bogota', 'Colombia', 'BOG', 4.70159, -74.1469],
             ['Los Angeles International Airport', 'Los Angeles', 'United States', 'LAX', 33.94250107, -118.4079971],
             ['Vancouver International Airport', 'Vancouver', 'Canada', 'YVR', 49.19390106, -123.1839981],
             ['John F Kennedy International Airport', 'New York', 'United States', 'JFK', 40.63980103, -73.77890015]])

    def _get_test_routes(self):
        return iter(
            [['Airline Id', 'Origin', 'Destination'],
             ['AC', 'YYZ', 'JFK'],
             ['AC', 'YYZ', 'BOG'],
             ['UA', 'LAX', 'YVR'],
             ['XX', 'BOG', 'YYZ']])
