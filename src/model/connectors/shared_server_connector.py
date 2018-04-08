import requests
import time
from src.model.exceptions.response_exceptions import *

SHARED_SERVER_HOST = 'https://picappss.herokuapp.com'
NEW_TOKEN_PATH = '/token'


class SharedServerConnector(object):

    def __init__(self):
        self.success_codes = [200, 201, 204]

    def get_new_token(self, user_info):
        """Gets a token for a given user"""
        response = requests.post(SHARED_SERVER_HOST + NEW_TOKEN_PATH,
                                 data=user_info,
                                 headers={'content-type': 'application/json'})
        # Handle error codes
        if response.status_code not in self.success_codes:
            handle_error(response)
        # Get data
        token = response.json()['token']
        # Check data
        if token['expiresAt'] < time.time():
            raise InvalidResponseException('Expiration time is previous to current time!')
        # Return object
        return token


def handle_error(response):
    """Handles request error and raises necessary exception."""
    if response.status_code == 400:
        raise BadRequestException(response.json())
    elif response.status_code == 401:
        raise UnauthorizedException(response.json())
    elif response.status_code == 404:
        raise NotFoundException(response.json())
    elif response.status_code == 409:
        raise ConflictException(response.json())
    elif response.status_code == 500:
        raise InternalServerErrorException(response.json())
