import unittest
import warnings

def warn(*args, **kwargs):
    # Disable annoying deprecation warning
    pass
warnings.warn = warn


class RouteResourceTestCase(unittest.TestCase):

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

    def test_get_returns_400_if_missing_origin(self):
        get_request_args = {'destination': 'EOH'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[1], 400)

    def test_get_returns_error_message_if_missing_origin(self):
        get_request_args = {'destination': 'EOH'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[0], {'message': 'Missing origin airport'})

    def test_get_returns_400_if_missing_destination(self):
        get_request_args = {'origin': 'YYZ'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[1], 400)

    def test_get_returns_error_message_if_missing_destination(self):
        get_request_args = {'origin': 'YYZ'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[0], {'message': 'Missing destination airport'})

    def test_get_returns_404_if_invalid_origin(self):
        get_request_args = {'origin': 'XXX', 'destination': 'EOH'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[1], 404)

    def test_get_returns_error_message_if_invalid_origin(self):
        get_request_args = {'origin': 'XXX', 'destination': 'EOH'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[0], {'message': 'Invalid Origin'})

    def test_get_returns_404_if_invalid_destination(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'XXX'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[1], 404)

    def test_get_returns_error_message_if_invalid_destination(self):
        get_request_args = {'origin': 'YYZ', 'destination': 'XXX'}
        response = self._mock_get_request(get_request_args, None)
        self.assertEqual(response[0], {'message': 'Invalid Destination'})

    def _mock_get_request(self, get_request_args, graph_get_route_response):
        from unittest.mock import patch, Mock
        from route_resource import RouteResource
        from server import create_app

        mock_graph = Mock()
        mock_graph.is_valid_airport.side_effect = lambda x: x != 'XXX'
        mock_graph.get_route.return_value = graph_get_route_response
        with patch('routes_graph.RoutesGraph'):
            app = create_app()
            with app.test_request_context():
                with patch('flask_restful.request.args.get') as mock_request_args_get:
                    mock_request_args_get.side_effect = lambda x: get_request_args.get(x)
                    route_resource = RouteResource(mock_graph)
                    response = route_resource.get()
        return response
