from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.utils.logger_config import Logger
from src.security.token import Token, ExpiredTokenException, InvalidTokenException
from src.model.friendship import Friendship, FriendshipState, AlreadyFriendsException, UserNotFoundException, \
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
            # TODO if action_performed == FriendshipState.friends: ... elif .request_sent ...

            # generate response
            output = {"target_user_id": username}

            # return response
            return ResponseBuilder.build_response(output)

        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except AlreadyFriendsException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except UserNotFoundException as e:
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

        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except ExpiredTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except InvalidTokenException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except UserNotFoundException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
        except NotFriendsException as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)