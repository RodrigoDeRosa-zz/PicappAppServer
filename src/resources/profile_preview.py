from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.user import User, UserNotFoundException
from src.utils.logger_config import Logger
from src.security.token import ExpiredTokenException, Token, InvalidTokenException


class ProfilePreviewResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            callee_user = Token.identify(token)

            # get profile info from user username
            profile_preview = User.get_profile_preview(username)

            # generate response
            self.logger.info('User profile preview found for: {}'.format(username))
            output = profile_preview

            # return response
            return ResponseBuilder.build_response(output)

        except (UserNotFoundException, ExpiredTokenException, MissingFieldException,
                InvalidTokenException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')