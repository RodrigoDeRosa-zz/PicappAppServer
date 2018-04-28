import unittest
import unittest.mock as mock
from src.resources.profile import ProfileResource, UserNotFoundException
from src.model.user import User
from src.utils.response_builder import ResponseBuilder
from tests.mocks.user_mock import user_mock_without_stories_or_friends, profile_mock_without_stories_or_friends
from tests.mocks.token_mock import token_mock
from src.security.token import Token


class ProfileResourceTestCase(unittest.TestCase):

    def test_get_user(self):
        mock_name = user_mock_without_stories_or_friends['username']
        Token.identify = mock.MagicMock(return_value=mock_name)
        service = ProfileResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        User._get_one = mock.MagicMock(return_value=user_mock_without_stories_or_friends)
        ResponseBuilder.build_response = lambda output, status_code=200: output
        self.assertEqual(service.get(mock_name), profile_mock_without_stories_or_friends)

    def test_get_user_not_found(self):
        mock_name = user_mock_without_stories_or_friends['username']
        service = ProfileResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(return_value=mock_name)
        User._get_one = mock.MagicMock(return_value=None)
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(mock_name), 404)
