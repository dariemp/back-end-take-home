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
        return list(self._airports_with_routes.keys())

    def load_data(self):
        data_sub_directory = os.environ.get('DATADIR', 'full')
        data_path = os.path.join(os.getcwd(), 'data', data_sub_directory)
        self._load_airlines(data_path)
        self._load_airports(data_path)

    def get_airport_connections(self, airport_code):
        try:
            return self._airports_with_routes[airport_code]
        except KeyError:
            from exceptions import AirportNotFound
            raise AirportNotFound()

    def _load_airlines(self, data_path):
        self._airlines = []
        airlines_file_path = os.path.join(data_path, 'airlines.csv')
        self._load_airlines_from_csv(airlines_file_path)

    def _load_airlines_from_csv(self, airlines_file_path):
        with open(airlines_file_path, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                self._airlines.append(row[1])

    def _load_airports(self, data_path):
        self._airports_with_routes = {}
        airports_file_path = os.path.join(data_path, 'airports.csv')
        self._load_airports_from_csv(airports_file_path)

    def _load_airports_from_csv(self, airports_file_path):
        with open(airports_file_path, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                self._airports_with_routes[row[3]] = []
