from flask import request


class MissingFieldException(Exception):
    pass


class RequestBuilder(object):

    @staticmethod
    def get_field_from_request(key):
        try:
            return request.json[key]
        except Exception:
            raise MissingFieldException("Missing field "+key)
