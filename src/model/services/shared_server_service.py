from src.model.connectors.shared_server_connector import SharedServerConnector
from src.model.exceptions.response_exceptions import *
from src.model.exceptions.request_exceptions import *


class SharedServerService(object):

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
    def get_new_token(user_info):
        """ Processes the request to the shared server to get a new token for a given user."""
        try:
            token = SharedServerConnector.get_new_token(user_info)
        except BadRequestException as bre:
            raise InvalidDataException(bre.message)
        except InternalServerErrorException as isee:
            raise UnexpectedErrorException(isee.message)
        # Return new token
        return token
