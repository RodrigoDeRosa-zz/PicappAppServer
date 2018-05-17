from src.model.connectors.shared_server_connector import SharedServerConnector
from src.model.exceptions.response_exceptions import *
from src.model.exceptions.request_exceptions import *
from src.utils.logger_config import Logger
from requests.exceptions import ConnectionError


class SharedServerService(object):

    def __init__(self):
        self.connector = SharedServerConnector()
        self.logger = Logger(__name__)

    def create_user(self, user_info):
        """Receives an UserInfo dict, posts it to sharedserverURL/user and returns the new user's information"""
        try:
            new_user = self.connector.create_user(user_info)
            self.logger.info('User successfully retrieved from connector.')
        except BadRequestException as bre:
            # Bad parameters
            self.logger.error(str(bre))
            raise InvalidDataException(bre.message)
        except UnauthorizedException as ue:
            # Incorrect server token
            self.logger.error(str(ue))
            raise InvalidDataException(ue.message)
        except InternalServerErrorException as isee:
            # External error
            self.logger.error(str(isee))
            raise UnexpectedErrorException(isee.message)
        except ConnectionError as ce:
            self.logger.error(str(ce))
            raise ConnectionFailException()
        # Return new user
        return new_user

    def get_new_token(self, user_info):
        """ Processes the request to the shared server to get a new token for a given user."""
        try:
            token = self.connector.get_new_token(user_info)
            self.logger.info('Token successfully retrieved from connector.')
        except (BadRequestException, NotFoundException) as e:
            # Request fail
            self.logger.error(str(e))
            raise InvalidDataException(e.message)
        except InternalServerErrorException as isee:
            # External error
            self.logger.error(str(isee))
            raise UnexpectedErrorException(isee.message)
        except ConnectionError as ce:
            self.logger.error(str(ce))
            raise ConnectionFailException()
        # Return new token
        return token

    def delete_user(self, username):
        """Asks the shared server for deletion of a user related to user_info."""
        try:
            result = self.connector.delete_user(username)
            self.logger.info('User {} successfully deleted from Shared Server'.format(result))
            return result
        except (BadRequestException, NotFoundException) as e:
            # Request fail
            self.logger.error(str(e))
            raise InvalidDataException(e.message)
        except InternalServerErrorException as isee:
            # External error
            self.logger.error(str(isee))
            raise UnexpectedErrorException(isee.message)
        except ConnectionError as ce:
            self.logger.error(str(ce))
            raise ConnectionFailException()
