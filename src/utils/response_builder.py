from flask import jsonify
from flask import make_response
from src.utils.logger_config import Logger
from src.utils.stats import StatCollector


class ResponseBuilder(object):

    @staticmethod
    def build_response(response, status_code=200):
        Logger(__name__).info('Response created: {}'.format(response))
        return make_response(jsonify(response), status_code)

    @staticmethod
    def build_error_response(error_message, status_code):
        response = {'message': error_message, 'status_code': status_code}
        StatCollector.save_event_error_response()
        return ResponseBuilder.build_response(response, status_code)
