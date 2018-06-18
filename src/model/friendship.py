from src.utils.logger_config import Logger
from src.model.user import User, UserNotFoundException, _user


class AlreadyFriendsException(Exception):
    def __init__(self):
        self.message = "Users are already friends"
        self.error_code = 400

    def __str__(self):
        return self.message


class NotFriendsException(Exception):
    def __init__(self):
        self.message = "Users are not friends nor is there a request to reject."
        self.error_code = 400

    def __str__(self):
        return self.message


FRIENDSHIP_STATE_SENT = "sent"
FRIENDSHIP_STATE_RECEIVED = "received"
FRIENDSHIP_STATE_FRIENDS = "friends"
FRIENDSHIP_STATE_NOT_FRIENDS = "not_friends"


class Friendship(object):

    @staticmethod
    def _change_friendship_in_to(origin_username, destiny_username, new_friendship_state):
        Logger(__name__).info('Changing Friendship state in {}: {} to state {}.'.
                              format(origin_username, destiny_username,
                                     str(new_friendship_state)))

        entry = "friends."+destiny_username
        new_origin = User._update_user_by_username(origin_username, {entry: new_friendship_state})

        Logger(__name__).info('Friendship state in {}: {} is now at state {}.'.
                              format(origin_username, destiny_username,
                                     str(new_friendship_state)))
        return new_origin

    @staticmethod
    def _delete_friendship_in(origin_username, destiny_username):
        Logger(__name__).info('Deleting Friendship state in {}: {}.'.
                              format(origin_username, destiny_username))

        entry = "friends." + destiny_username
        new_origin = User._delete_field_by_username(origin_username, {entry: ""})

        Logger(__name__).info('Friendship state in {}: {} is now deleted.'.
                              format(origin_username, destiny_username))
        return new_origin

    @staticmethod
    def _send_request_from_to(origin_username, destiny_username):
        Logger(__name__).info('Sending friend request from user {} to {}.'.format(origin_username,
                                                                                  destiny_username))

        # destiny_user['friends'][origin_user['username']] = FRIENDSHIP_STATE_RECEIVED
        Friendship._change_friendship_in_to(destiny_username, origin_username, FRIENDSHIP_STATE_RECEIVED)

        # origin_user['friends'][destiny_user['username']] = FRIENDSHIP_STATE_SENT
        Friendship._change_friendship_in_to(origin_username, destiny_username, FRIENDSHIP_STATE_SENT)

        return FRIENDSHIP_STATE_SENT

    @staticmethod
    def _are_friends(username1, username2):
        Logger(__name__).info('Evaluating whether users {} and {} are friends.'.format(username1,
                                                                                       username2))
        if username2 in _user(username1)['friends'] and \
                _user(username1)['friends'][username2] == FRIENDSHIP_STATE_FRIENDS:
            return True
        return False

    @staticmethod
    def _had_sent_request(origin_username, destiny_username):
        Logger(__name__).info('Evaluating whether user {} wanted to be friends with {} '
                              'beforehand.'.format(origin_username, destiny_username))
        if _user(destiny_username)['friends'][origin_username] == FRIENDSHIP_STATE_RECEIVED:
            return True
        return False

    @staticmethod
    def _confirm_friends(username1, username2):
        Logger(__name__).info('Confirming friendship between users {} and {}.'.format(username1,
                                                                                      username2))
        assert username2 in _user(username1)['friends']
        assert username1 in _user(username2)['friends']

        # user1['friends'][user2['username']] = FRIENDSHIP_STATE_FRIENDS
        Friendship._change_friendship_in_to(username1, username2, FRIENDSHIP_STATE_FRIENDS)

        # user2['friends'][user1['username']] = FRIENDSHIP_STATE_FRIENDS
        Friendship._change_friendship_in_to(username2, username1, FRIENDSHIP_STATE_FRIENDS)

        return FRIENDSHIP_STATE_FRIENDS

    @staticmethod
    def _reject_friendship(username1, username2):
        Logger(__name__).info('Rejecting friendship between users {} and {}.'.format(username1,
                                                                                     username2))

        # previous_state = user1['friends'].pop(user2["username"])
        previous_state = _user(username1)['friends'][username2]
        Friendship._delete_friendship_in(username1, username2)

        # user2['friends'].pop(user1["username"])
        Friendship._delete_friendship_in(username2, username1)

        return previous_state

    @staticmethod
    def wants_to_be_friends_with(origin_username, destiny_username):
        """Declares an intention from origin to be friends with destiny, sending a request to
        destiny or confirming the relation if the inverse had been previously stated.
        Returns a FriendshipState which can be request_sent or friends depending on the previous."""
        Logger(__name__).info('Username {} wants to be friends with {}.'.format(origin_username, destiny_username))
        # retrieve the DB user representations
        origin_user = User._get_one({'username': origin_username})
        destiny_user = User._get_one({'username': destiny_username})

        # if one of them was not found raise exception
        if origin_user is None or destiny_user is None:
            raise UserNotFoundException

        # if destiny had NOT already wanted to be friends with origin
        if origin_username not in destiny_user['friends']:
            return Friendship._send_request_from_to(origin_username, destiny_username)

        # if destiny is already friends with origin
        if Friendship._are_friends(origin_username, destiny_username):
            raise AlreadyFriendsException

        # only other cases are: invitation already sent or needed confirmation
        # and this first case should not be possible
        assert _user(destiny_username)['friends'][origin_username] == FRIENDSHIP_STATE_SENT
        assert _user(origin_username)['friends'][destiny_username] == FRIENDSHIP_STATE_RECEIVED

        # so now it should be confirmed
        return Friendship._confirm_friends(origin_username, destiny_username)

    @staticmethod
    def wants_to_not_be_friends_with(origin_username, destiny_username):
        """Declares an intention from origin to not be friends with destiny, being that a rejection
        of a previously received friendship request or the deletion of an existing friendship.
        Returns a FriendshipState which can be request_received or friends depending on the previous
        state."""
        Logger(__name__).info('Username {} wants to NOT be friends with {}.'.format(origin_username,
                                                                                    destiny_username))
        # retrieve the DB user representations
        origin_user = User._get_one({'username': origin_username})
        destiny_user = User._get_one({'username': destiny_username})

        # if one of them was not found raise exception
        if origin_user is None or destiny_user is None:
            raise UserNotFoundException

        # if origin doesnt know destiny or origin was the one requesting raise exception
        if destiny_username not in origin_user['friends'] or \
                origin_user['friends'][destiny_username] == FRIENDSHIP_STATE_SENT:
            raise NotFriendsException

        # if here they were already friends or destiny had sent request to origin, so delete
        assert Friendship._are_friends(origin_username, destiny_username) or \
            Friendship._had_sent_request(destiny_username, origin_username)

        return Friendship._reject_friendship(origin_username, destiny_username)

    @staticmethod
    def are_friends(username1, username2):
        return Friendship._are_friends(username1, username2)

    @staticmethod
    def get_friendship_state_from_to(origin_username, destiny_username):
        """Returns one of the friendship states according to how origin sees the relationship."""
        origin_user_obj = _user(origin_username)
        if _user(destiny_username) is None:
            raise UserNotFoundException
        if destiny_username not in origin_user_obj['friends']:
            return FRIENDSHIP_STATE_NOT_FRIENDS
        return origin_user_obj['friends'][destiny_username]