from flask import request
from src.utils.logger_config import Logger


class MissingFieldException(Exception):
    pass


class RequestBuilder(object):

    @staticmethod
    def get_field_from_request(key):
        try:
            return request.json[key]
        except Exception:
            Logger(__name__).error("Missing field: {}".format(key))
            raise MissingFieldException("Missing field " + key)

    @staticmethod
    def get_field_from_header(key):
        try:
            return request.headers[key]
        except Exception:
            Logger(__name__).error("Missing field: {}".format(key))
            raise MissingFieldException("Missing field " + key)