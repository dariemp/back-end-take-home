import os
import csv

class RoutesGraph(object):

    def __init__(self):
        self.load_data()

    @property
    def airlines(self):
        return self._airlines

    def load_data(self):
        data_sub_directory = os.environ.get('DATADIR', 'full')
        data_path = os.path.join(os.getcwd(), 'data', data_sub_directory)
        self._load_airlines(data_path)

    def _load_airlines(self, data_path):
        self._airlines = []
        airlines_file_path = os.path.join(data_path, 'airlines.csv')
        self._load_airlines_csv(airlines_file_path)

    def _load_airlines_csv(self, airlines_file_path):
        with open(airlines_file_path, 'r', newline='') as f: 
            csv_reader = csv.reader(f)
            next(csv_reader)
            for row in csv_reader:
                self._airlines.append(row[1])