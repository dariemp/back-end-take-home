import unittest
from server import create_app


class TestServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.app = create_app()
        cls.client = cls.app.test_client()

    def test_yyz_to_yyz_with_test_data_returns_400(self):
        resp = self._send_request('YYZ', 'YYZ')
        self.assertEqual(resp.status_code, 400)

    def test_yyz_to_yyz_with_test_data_returns_correct_error_message(self):
        resp = self._send_request('YYZ', 'YYZ')
        expected_data = {'message': 'Take the bus, please'}
        self.assertEqual(resp.json, expected_data)

    def test_yyz_to_jfk_with_test_data_returns_200(self):
        resp = self._send_request('YYZ', 'JFK')
        self.assertEqual(resp.status_code, 200)

    def test_yyz_to_jfk_with_test_data_returns_correct_route(self):
        resp = self._send_request('YYZ', 'JFK')
        expected_data = {'route': [{'airline':'AC', 'from':'YYZ', 'to':'JFK'}]}
        self.assertEqual(resp.json, expected_data)

    def test_yyz_to_yvr_with_test_data_returns_200(self):
        resp = self._send_request('YYZ', 'YVR')
        self.assertEqual(resp.status_code, 200)

    def test_yyz_to_yvr_with_test_data_returns_correct_route(self):
        resp = self._send_request('YYZ', 'YVR')
        expected_data = {'route': [{'airline':'AC', 'from':'YYZ', 'to':'YVR'}]}
        self.assertEqual(resp.json, expected_data)

    def test_yyz_to_ord_with_test_data_returns_404(self):
        resp = self._send_request('YYZ', 'EOH')
        self.assertEqual(resp.status_code, 404)

    def test_yyz_to_ord_with_test_data_returns_correct_error_message(self):
        resp = self._send_request('YYZ', 'EOH')
        expected_data = {'message': 'No Route'}
        self.assertEqual(resp.json, expected_data)

    def test_xxx_to_ord_with_test_data_returns_404(self):
        resp = self._send_request('XXX', 'ORD')
        self.assertEqual(resp.status_code, 404)

    def test_xxx_to_ord_with_test_data_returns_correct_error_message(self):
        resp = self._send_request('XXX', 'ORD')
        expected_data = {'message': 'Invalid Origin'}
        self.assertEqual(resp.json, expected_data)

    def test_ord_to_xxx_with_test_data_returns_404(self):
        resp = self._send_request('ORD', 'XXX')
        self.assertEqual(resp.status_code, 404)

    def test_ord_to_xxx_with_test_data_returns_correct_error_message(self):
        resp = self._send_request('ORD', 'XXX')
        expected_data = {'message': 'Invalid Destination'}
        self.assertEqual(resp.json, expected_data)

    def _send_request(self, origin, destination):
        return self.client.get('/route?origin={}&destination={}'.format(origin, destination))
