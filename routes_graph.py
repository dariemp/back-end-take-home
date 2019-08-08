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
        from data_loader import DataLoader

        data_loader = DataLoader()
        self._airlines = data_loader.load_airlines()
        self._airports_connections = data_loader.load_airports()

    def get_airport_connections(self, airport_code):
        try:
            return self._airports_connections[airport_code]
        except KeyError:
            from exceptions import AirportNotFound
            raise AirportNotFound()
