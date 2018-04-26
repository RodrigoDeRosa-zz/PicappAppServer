from flask_restful import Resource

from src.security.token import Token, ExpiredTokenException, InvalidTokenException
from src.model.user import User
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.utils.response_builder import ResponseBuilder
from src.utils.logger_config import Logger


class MyAccountResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            callee_user = Token.identify(token)

            if callee_user != username:
                return ResponseBuilder.build_error_response("Username is not own", 403)

            # get user data
            user = User.get_one({'username': username})

            # generate response
            output = {'username': user['username']}  # fetch data
            self.logger.info('User account retrieved. ({})'.format(output))

            # return response
            return ResponseBuilder.build_response(output)

        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)  # check status code
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)  # check status code

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')
