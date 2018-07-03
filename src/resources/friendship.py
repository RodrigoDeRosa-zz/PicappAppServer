from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.utils.logger_config import Logger
from src.utils.stats import StatCollector
from src.security.token import Token, ExpiredTokenException, InvalidTokenException
from src.model.friendship import Friendship, AlreadyFriendsException, UserNotFoundException, \
    NotFriendsException


class FriendshipResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def post(self, username):
        """Send a friendship request to username or accept his/her previously sent request."""
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_username = Token.identify(token)

            # save intent to be friends from (user) to username
            action_performed = Friendship.wants_to_be_friends_with(caller_username, username)

            # tell username about request/confirmation
            # if action_performed == FriendshipState.friends: ... elif .request_sent ...
            # => done at Firebase

            # generate response
            output = {"target_user_id": username}

            # save stat
            StatCollector.save_event_friendship_request_sent()

            # return response
            return ResponseBuilder.build_response(output)

        except (MissingFieldException, ExpiredTokenException, InvalidTokenException,
                AlreadyFriendsException, UserNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def delete(self, username):
        """Delete an existing friendship with or reject a request for one from username."""
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_username = Token.identify(token)

            # save intent to be friends from (user) to username
            action_performed = Friendship.wants_to_not_be_friends_with(caller_username, username)

            # generate response
            output = {"target_user_id": username}

            # return response
            return ResponseBuilder.build_response(output)

        except (MissingFieldException, ExpiredTokenException, InvalidTokenException,
                UserNotFoundException, NotFriendsException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def get(self, username):
        """Get the friendship state between username and caller"""
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            caller_username = Token.identify(token)

            # save intent to be friends from (user) to username
            friendship_state = Friendship.get_friendship_state_from_to(caller_username, username)

            # generate response
            output = {"friendship_state": friendship_state}

            # return response
            return ResponseBuilder.build_response(output)

        except (MissingFieldException, ExpiredTokenException, InvalidTokenException,
                UserNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)