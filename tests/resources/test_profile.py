import unittest
from unittest.mock import patch, MagicMock
from src.resources.profile import ProfileResource, UserNotFoundException
from src.model.user import User
from src.utils.response_builder import ResponseBuilder
from tests.mocks.user_mock import user_mock_without_stories_or_friends, profile_mock_without_stories_or_friends
from tests.mocks.token_mock import token_mock
from src.security.token import Token


class ProfileResourceTestCase(unittest.TestCase):

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_get_user_profile(self):
        with patch.object(Token, "identify") as mocked_token_identify,\
             patch.object(User, "get_profile") as mocked_get_profile, \
             patch.object(ResponseBuilder, "build_response") as mocked_build_response:
            mock_name = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=mock_name)
            mocked_get_profile.side_effect = MagicMock(return_value=profile_mock_without_stories_or_friends)
            mocked_build_response.side_effect = self.mocked_build_response

            service = ProfileResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(mock_name), profile_mock_without_stories_or_friends)

    def test_get_user_not_found(self):
        with patch.object(Token, "identify") as mocked_token_identify,\
             patch.object(User, "get_profile") as mocked_get_profile, \
             patch.object(ResponseBuilder, "build_error_response") as mocked_build_response:
            mock_name = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=mock_name)
            mocked_get_profile.side_effect = MagicMock(side_effect=UserNotFoundException())
            mocked_build_response.side_effect = self.mocked_build_error_response

            service = ProfileResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(mock_name), 404)
