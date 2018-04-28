from flask import request
from src.utils.logger_config import Logger


class MissingFieldException(Exception):
    def __init__(self, key):
        self.message = "Missing field " + key
        self.error_code = 400

    def __str__(self):
        return self.message


class RequestBuilder(object):

    @staticmethod
    def get_field_from_request(key):
        try:
            return request.json[key]
        except Exception:
            Logger(__name__).error("Missing field: {}".format(key))
            raise MissingFieldException(key)

    @staticmethod
    def get_field_from_header(key):
        try:
            return request.headers[key]
        except Exception:
            Logger(__name__).error("Missing field: {}".format(key))
            raise MissingFieldException(key)
