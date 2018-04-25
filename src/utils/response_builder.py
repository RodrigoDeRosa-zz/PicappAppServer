from flask import jsonify
from flask import make_response
from src.utils.logger_config import Logger


class ResponseBuilder(object):

    @staticmethod
    def build_response(response, status_code=200):
        return make_response(jsonify(response), status_code)

    @staticmethod
    def build_error_response(error_message, status_code):
        response = {'message': error_message, 'status_code': status_code}
        Logger(__name__).info('Response created: {}'.format(response))
        return ResponseBuilder.build_response(response, status_code)
