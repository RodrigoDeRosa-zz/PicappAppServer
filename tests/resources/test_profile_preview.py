import unittest
from unittest.mock import patch, MagicMock

from src.model.user import User
from src.resources.profile_preview import ProfilePreviewResource, UserNotFoundException, MissingFieldException
from tests.mocks.token_mock import token_mock
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from tests.mocks.user_mock import user_mock_without_stories_or_friends


class ProfilePreviewResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_mock_without_stories_or_friends['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_get_profile_preview_not_found(self):
        with patch.object(User, "get_profile_preview") as mocked_get_preview,\
             patch.object(Token, "identify") as mocked_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_build_response:

            mocked_build_response.side_effect = self.mocked_build_error_response
            mocked_identify.side_effect = self.mocked_identify
            mocked_get_preview.side_effect = MagicMock(side_effect=UserNotFoundException())

            service = ProfilePreviewResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 404)

    def test_get_profile_preview_successful(self):
        with patch.object(User, "get_profile_preview") as mocked_get_preview,\
             patch.object(Token, "identify") as mocked_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_build_response:

            expected_response = {k: user_mock_without_stories_or_friends[k] for k in
                                 ["name", "username", "profile_pic"]}

            mocked_build_response.side_effect = self.mocked_build_response
            mocked_identify.side_effect = self.mocked_identify
            mocked_get_preview.side_effect = MagicMock(return_value=expected_response)

            service = ProfilePreviewResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']),
                             expected_response)
