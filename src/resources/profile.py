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
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            callee_user = Token.identify(token)

            # get profile info from user username
            profile = User.get_profile(username, callee_user)

            # generate response
            self.logger.info('User profile found for: {}'.format(username))
            output = profile

            # return response
            return ResponseBuilder.build_response(output)

        except UserNotFoundException as e:
            err_msg = "No user found with that name"
            self.logger.info(err_msg)
            return ResponseBuilder.build_error_response(err_msg, e.error_code)
        except (ExpiredTokenException, MissingFieldException, InvalidTokenException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        
    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')
