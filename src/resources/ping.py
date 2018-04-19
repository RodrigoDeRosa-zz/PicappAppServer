from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.logger_config import Logger


class PingResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self):
        self.logger.debug('Pinged.')
        return ResponseBuilder.build_response({}, status_code=200)
