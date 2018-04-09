from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder


class PingResource(Resource):
    def get(self):
        return ResponseBuilder.build_response({}, status_code=200)
