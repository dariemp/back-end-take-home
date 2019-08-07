import unittest
from routes_graph import RoutesGraph

class RoutesGraphTestCase(unittest.TestCase):

    def test_load_data_with_test_data_fills_airlines(self):
        import os
        
        os.environ['DATADIR'] = 'test'
        routes_graph = RoutesGraph()
        self.assertTrue(routes_graph.airlines[0] == 'AC')
