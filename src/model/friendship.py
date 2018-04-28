from src.model.database import mongo
from src.utils.logger_config import Logger
from src.model.user import User, UserNotFoundException

from enum import Enum


class AlreadyFriendsException(Exception):
    def __init__(self):
        self.message = "Users are already friends"
        self.error_code = 400

    def __str__(self):
        return self.message


class FriendshipState(Enum):
    # if they are not friends there should be no relation at all, hence no "not_friends = 0"
    request_sent = 1
    request_received = 2
    friends = 3


class Friendship(object):

    @staticmethod
    def _send_request_from_to(origin_user, destiny_user):
        destiny_user['friends'][origin_user['username']] = FriendshipState.request_received
        origin_user['friends'][destiny_user['username']] = FriendshipState.request_sent
        return FriendshipState.request_sent

    @staticmethod
    def _are_friends(user1, user2):
        if user1['friends'][user2['username']] == FriendshipState.friends:
            assert user2['friends'][user1['username']] == FriendshipState.friends
            return True
        return False

    @staticmethod
    def _confirm_friends(user1, user2):
        assert user2['username'] in user1['friends']
        assert user1['username'] in user2['friends']

        user1['friends'][user2['username']] = FriendshipState.friends
        user2['friends'][user1['username']] = FriendshipState.friends

        return FriendshipState.friends

    @staticmethod
    def wants_to_be_friends_with(origin_username, destiny_username):
        """Declares an intention from origin to be friends with destiny, sending a request to
        destiny or confirming the relation if the inverse had been previously stated.
        Returns a FriendshipState which can be request_sent or friends depending on the previous."""
        # retrieve the DB user representations
        origin_user = User._get_one({'username': origin_username})
        destiny_user = User._get_one({'username': destiny_username})

        # if one of them was not found raise exception
        if origin_user is None or destiny_user is None:
            raise UserNotFoundException

        # if destiny had NOT already wanted to be friends with origin
        if origin_username not in destiny_user['friends']:
            return Friendship._send_request_from_to(origin_user, destiny_user)

        # if destiny is already friends with origin
        if Friendship._are_friends(origin_user, destiny_user):
            raise AlreadyFriendsException

        # only other cases are: invitation already sent or needed confirmation
        # and this first case should not be possible
        assert destiny_user['friends'][origin_user['username']] == FriendshipState.request_sent
        assert origin_user['friends'][destiny_user['username']] == FriendshipState.request_received

        # so now it should be confirmed
        return Friendship._confirm_friends(origin_user, destiny_user)
