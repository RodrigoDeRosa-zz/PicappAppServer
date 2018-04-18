import requests
import time
import json
from configparser import ConfigParser
from src.model.exceptions.response_exceptions import *
from src.utils.logger_config import Logger

BASE_PATH = "/api"
SERVER_TOKEN = '1713908341'
NEW_TOKEN_PATH = '/token'
NEW_USER_PATH = '/user'


class SharedServerConnector(object):

    def __init__(self):
        self.success_codes = [200, 201, 204]
        self.logger = Logger(__name__)
        parser = ConfigParser()
        parser.read_file(open('config.cfg'))
        self.host = parser.get('shared_server', 'host')

    def create_user(self, user_info):
        """Posts a user to the server"""
        # Generate uri
        uri = self.host + BASE_PATH + NEW_USER_PATH
        params = {'ApplicationToken': SERVER_TOKEN}
        self.logger.info('HTTP Post to URI {} with body {} and params {}'.format(uri, user_info, params))
        # Get response
        response = requests.post(uri,
                                 data=json.dumps(user_info),
                                 params=params,
                                 headers={'Content-Type': 'Application/json'})
        self.logger.info('Response received with code {}. ({})'.format(response.status_code, response.text))
        # Handle error codes
        if response.status_code not in self.success_codes:
            handle_error(response)
        # Get data
        user = response.json()['user']
        # Check response
        if user['username'] != user_info['username']:
            raise InvalidResponseException('Returned username value is different from the posted one.')
        # Return user object
        return user

    def get_new_token(self, user_info):
        """Gets a token for a given user"""
        # Generate uri
        uri = self.host + BASE_PATH + NEW_TOKEN_PATH
        self.logger.info('HTTP Post to URI {} with body {}'.format(uri, user_info))
        # Get response
        response = requests.post(uri,
                                 data=json.dumps(user_info),
                                 headers={'Content-Type': 'Application/json'})
        self.logger.info('Response received with code {}. ({})'.format(response.status_code, response.text))
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
