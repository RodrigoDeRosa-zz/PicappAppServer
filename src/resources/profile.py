from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.user import User, UserNotFoundException
from src.utils.logger_config import Logger
from src.security.token import ExpiredTokenException, Token, InvalidTokenException


class ProfileResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self, username):
        # search one by given username
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            callee_user = Token.identify(token)

            # get profile info from user username
            profile = User.get_profile(username)

            # generate response
            self.logger.info('User profile found for: {}'.format(username))
            output = profile

            # return response
            return ResponseBuilder.build_response(output)

        except UserNotFoundException as e:
            err_msg = "No user found with that name"
            self.logger.error(err_msg)
            return ResponseBuilder.build_error_response(err_msg, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        
    # deprecated until user has more info than username and password
    """
    def put(self, username):
        # get data received
        new_age = self._get_age_from_request()

        # look for user and update, returning user info after being updated
        updated_user = User.update_profile(username, {'age': new_age})
        # if match found able to update
        if updated_user:
            output = {'name': updated_user['name'], 'age': updated_user['age']}
            self.logger.info('User profile updated. ({})'.format(output))
        else:  # no matches
            output = "No user found with that name"
            self.logger.info('No user was found to update for username: {}'.format(username))
        # formatting
        response = {'result': output}
        return ResponseBuilder.build_response(response)
    """
    """
    def _get_age_from_request(self):
        return request.json['age']
    """

    """
    DEPRECATED
    def delete(self, username):
        # search one by username and delete
        user = User.delete_one(username)
        if user:  # match found
            output = {'username': user['username']}
            self.logger.info('User profile deleted. ({})'.format(output))
        else:  # no matches
            output = "No user found with that name"
            self.logger.info('No user was found to delete for username: {}'.format(username))
        response = {'result': output}
        return ResponseBuilder.build_response(response)
    """

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')
