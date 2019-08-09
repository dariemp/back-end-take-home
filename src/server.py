from flask import Flask
from flask_restful import Api
from route_resource import RouteResource
from routes_graph import RoutesGraph


def create_app():
    app = Flask(__name__)
    api = Api(app)
    routes_graph = RoutesGraph()
    set_api_endpoints(api, routes_graph)
    return app


def set_api_endpoints(api, routes_graph):
    api.add_resource(RouteResource, '/route', resource_class_kwargs={'routes_graph': routes_graph})
