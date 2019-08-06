from flask import Flask
from flask_restful import Api
from route_resource import RouteResource


def create_app():
    app = Flask(__name__)
    api = Api(app)
    set_api_endpoints(api)
    return app


def set_api_endpoints(api):
    api.add_resource(RouteResource, '/route')


if __name__ == "__main__":
    app = create_app()
    app.run()
