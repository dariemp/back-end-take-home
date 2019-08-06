import unittest


class TestServer(unittest.TestCase):

    def test_create_app_returns_flask_app(self):
        from flask import Flask
        from server import create_app

        self.assertIsInstance(create_app(), Flask)

    def test_create_app_sets_routes_endpoint(self):
        from flask import url_for
        from server import create_app

        app = create_app()
        rule = next(app.url_map.iter_rules())
        with app.test_request_context():
            self.assertEqual(url_for(rule.endpoint), '/route')
