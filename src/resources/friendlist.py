from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.utils.logger_config import Logger
from src.security.token import Token, ExpiredTokenException, InvalidTokenException
from src.model.friendship import UserNotFoundException, Friendship


class FriendListResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def get(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_username = Token.identify(token)

            # get a list of friends as profile previews
            friend_list = Friendship.get_friends(username)

            # generate response
            output = {"friends": friend_list}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, MissingFieldException, ExpiredTokenException,
                UserNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
