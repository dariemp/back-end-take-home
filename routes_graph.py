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
        data_sub_directory = os.environ.get('DATADIR', 'full')
        data_path = os.path.join(os.getcwd(), 'data', data_sub_directory)
        self._airlines = self._load_airlines(data_path)
        self._airports_connections = self._load_airports(data_path)

    def get_airport_connections(self, airport_code):
        try:
            return self._airports_connections[airport_code]
        except KeyError:
            from exceptions import AirportNotFound
            raise AirportNotFound()

    def _load_airlines(self, data_path):
        airlines_file_path = os.path.join(data_path, 'airlines.csv')
        return self._load_airlines_from_csv(airlines_file_path)

    def _load_airports(self, data_path):
        airports_file_path = os.path.join(data_path, 'airports.csv')
        return self._load_airports_from_csv(airports_file_path)

    def _load_airlines_from_csv(self, airlines_file_path):
        airlines_set = set()
        self._load_csv(airlines_file_path, airlines_set, self._load_airline)
        return airlines_set

    def _load_airports_from_csv(self, airports_file_path):
        airports_connections = {}
        self._load_csv(airports_file_path, airports_connections, self._load_airport)
        return airports_connections

    def _load_csv(self, file_path, data_bucket, row_proccessing_function):
        with open(file_path, 'r', newline='') as f:
            csv_reader = csv.reader(f)
            self._skip_header(csv_reader)
            for row in csv_reader:
                row_proccessing_function(data_bucket, row)

    def _skip_header(self, csv_reader):
        next(csv_reader)

    def _load_airline(self, airlines_set, row):
        airlines_set.add(row[1])

    def _load_airport(self, airports_dict, row):
        airports_dict[row[3]] = []
