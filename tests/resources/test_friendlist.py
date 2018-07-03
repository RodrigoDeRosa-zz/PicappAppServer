import unittest
from unittest.mock import patch, MagicMock

from src.security.token import Token
from tests.mocks.token_mock import token_mock
from tests.mocks.user_mock import user_mock_without_stories_with_friends
from src.utils.response_builder import ResponseBuilder
from src.resources.friendlist import Friendship, FriendListResource, MissingFieldException


class FriendListResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_mock_without_stories_with_friends["username"]

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_get_friend_list_missing_field(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(ResponseBuilder, "build_error_response") as mocked_response_build, \
             patch.object(Friendship, "get_friends") as mocked_get_friends:
            mocked_response_build.side_effect = self.mocked_build_error_response
            mocked_token.side_effect = self.mocked_identify
            mocked_get_friends.side_effect = MagicMock(return_value=[])

            service = FriendListResource()
            service._get_token_from_header = MagicMock(side_effect=MissingFieldException("token"))

            self.assertEqual(service.get(user_mock_without_stories_with_friends["username"]), 400)

    def test_get_friend_list_successful(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(ResponseBuilder, "build_response") as mocked_response_build, \
             patch.object(Friendship, "get_friends") as mocked_get_friends:

            expected_list = []
            mocked_response_build.side_effect = self.mocked_build_response
            mocked_token.side_effect = self.mocked_identify
            mocked_get_friends.side_effect = MagicMock(return_value=expected_list)

            service = FriendListResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(user_mock_without_stories_with_friends["username"])["friends"],
                             expected_list)
