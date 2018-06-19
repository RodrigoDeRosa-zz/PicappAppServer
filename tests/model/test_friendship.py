import unittest
from unittest.mock import patch, MagicMock

from src.security.token import Token
from tests.mocks.token_mock import token_mock
from tests.mocks.user_mock import user_mock_without_stories_with_friends
from src.utils.response_builder import ResponseBuilder
from src.model.friendship import UserNotFoundException, FRIENDSHIP_STATE_NOT_FRIENDS, \
    FRIENDSHIP_STATE_FRIENDS, Friendship, _user, User


class FriendshipTestcase(unittest.TestCase):

    def test_get_friends_user_not_found(self):
        with patch('src.model.friendship._user') as mocked_get_user,\
             self.assertRaises(UserNotFoundException) as context:
            mocked_get_user.side_effect = MagicMock(return_value=None)

            Friendship.get_friends(user_mock_without_stories_with_friends['username'])
        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_get_friends_successful(self):
        with patch('src.model.friendship._user') as mocked_get_user,\
             patch.object(User, "get_profile_preview") as mocked_get_profile_preview:

            user_mock = dict(user_mock_without_stories_with_friends)
            username = user_mock['username']

            expected_friends = ['friend_id1', 'friend_id2']  # INTENTIONALLY HARDCODED

            mocked_get_user.side_effect = MagicMock(return_value=user_mock)
            mocked_get_profile_preview.side_effect = lambda x: x

            # don't check order
            self.assertCountEqual(Friendship.get_friends(username), expected_friends)
