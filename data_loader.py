import os
import csv

class DataLoader(object):

    def __init__(self):
        data_sub_directory = os.environ.get('DATADIR', 'full')
        self._data_path = os.path.join(os.getcwd(), 'data', data_sub_directory)

    def load_airlines(self):
        airlines_file_path = os.path.join(self._data_path, 'airlines.csv')
        return self._load_airlines_from_csv(airlines_file_path)

    def load_airports_and_routes(self, valid_airlines_set):
        airports_file_path = os.path.join(self._data_path, 'airports.csv')
        routes_file_path = os.path.join(self._data_path, 'routes.csv')
        airports_connection = self._load_airports_from_csv(airports_file_path)
        return self._load_routes_from_csv(routes_file_path, airports_connection, valid_airlines_set)

    def _load_airlines_from_csv(self, airlines_file_path):
        airlines_set = set()
        self._load_csv(airlines_file_path, airlines_set, self._load_airline)
        return airlines_set

    def _load_airports_from_csv(self, airports_file_path):
        airports_connections = {}
        self._load_csv(airports_file_path, airports_connections, self._load_airport)
        return airports_connections

    def _load_routes_from_csv(self, routes_file_path, airports_connection, valid_airlines_set):
        self._load_csv(routes_file_path, (airports_connection, valid_airlines_set), self._load_route)
        return airports_connection

    def _load_csv(self, file_path, data_bucket, row_proccessing_function):
        with open(file_path, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            self._skip_header(csv_reader)
            for row in csv_reader:
                row_proccessing_function(data_bucket, row)

    def _skip_header(self, csv_reader):
        next(csv_reader)

    def _load_airline(self, airlines_set, row):
        airline = row[1]
        airlines_set.add(airline)

    def _load_airport(self, airports_dict, row):
        airport = row[3]
        airports_dict[airport] = {}

    def _load_route(self, airports_and_airlines, row):
        airport_connections, valid_airlines_set = airports_and_airlines
        airline, origin_airport, destination_airport = row
        if (airline in valid_airlines_set and
            origin_airport in airport_connections and
            destination_airport in airport_connections):
            connecting_airlines = airport_connections[origin_airport].setdefault(destination_airport, [])
            connecting_airlines.append(airline)
