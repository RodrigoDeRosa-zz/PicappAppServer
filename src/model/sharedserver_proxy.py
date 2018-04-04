
MOCK_TOKEN = "asd"  # delete as soon as post_token is implemented
MOCK_EXPIRATION_DATE = 1514764800  # delete as soon as post_token is implemented, corresponds to 1/1/2019


class InvalidDataException(Exception):
    pass


class NoServerException(Exception):
    pass


class UnexpectedErrorException(Exception):
    pass


class SharedServerProxy(object):

    @staticmethod
    def post_user(data_dict):
        """Receives an UserInfo dict, posts it to sharedserverURL/user and returns response's
        status code if successful, or raises exception"""
        # data formatting
        # To be implemented
        data_dict['placeholder'] = "something"  # just to shut up linter
        # send petition to Shared Server with AppToken
        # To be implemented
        response_status_code = 200  # MOCK

        # return status code, possibly raise exception
        return response_status_code

    @staticmethod
    def post_token(data_dict):
        """Receives a dict with username and password, posts it to sharedserverURL/token and
        returns token and expiration date as dict, or raises exception"""
        # data formatting
        # To be implemented
        data_dict['placeholder'] = "something"  # just to shut up linter
        # send petition to Shared Server
        # To be implemented
        response = {'token': MOCK_TOKEN, 'expiresAt': MOCK_EXPIRATION_DATE}  # MOCK

        # return status code, possibly raise exception
        return response
