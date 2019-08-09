import unittest
from unittest.mock import patch, Mock
from flask_restful import request
from routes_graph import RoutesGraph
from route_resource import RouteResource
from server import create_app


class RouteResourceTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()

    def test_get_returns_route_yyz_jfk(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'JFK'}
        graph_get_route_response = [('YYZ', None), ('JFK', 'AC')]
        response = self._mock_get_request(get_request_args, graph_get_route_response)
        expected_response = {
            'route': [{'airline': 'AC', 'from': 'YYZ', 'to': 'JFK'}]
        }
        self.assertEqual(expected_response, response)

    def test_get_returns_route_yyz_yvr(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'YVR'}
        graph_get_route_response = [('YYZ', None), ('JFK', 'AC'), ('LAX', 'UA'), ('YVR', 'AC')]
        response = self._mock_get_request(get_request_args, graph_get_route_response)
        expected_response = {
            'route': [{'airline': 'AC', 'from': 'YYZ', 'to': 'JFK'},
                      {'airline': 'UA', 'from': 'JFK', 'to': 'LAX'},
                      {'airline': 'AC', 'from': 'LAX', 'to': 'YVR'}]
        }
        self.assertEqual(expected_response, response)

    def test_get_returns_404_when_route_does_not_exis(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'EOH'}
        graph_get_route_response = None
        response = self._mock_get_request(get_request_args, graph_get_route_response)
        self.assertEqual(response[1], 404)

    def test_get_returns_error_message_when_route_does_not_exist(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'EOH'}
        graph_get_route_response = None
        response = self._mock_get_request(get_request_args, graph_get_route_response)
        self.assertEqual(response[0], {'message': 'No Route'})

    def _mock_get_request(self, get_request_args, graph_get_route_response):
        mock_graph = Mock()
        mock_graph.get_route.return_value = graph_get_route_response
        with self.app.test_request_context():
            with patch('flask_restful.request.args.get') as mock_request_args_get:
                mock_request_args_get.side_effect = lambda x: get_request_args.get(x)
                route_resource = RouteResource(mock_graph)
                response = route_resource.get()
        return response
