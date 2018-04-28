import unittest
import unittest.mock as mock

from src.security.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from tests.mocks.user_mock import user_mock_without_stories_or_friends, account_info_mock_without_stories_or_friends
from src.resources.myaccount import MyAccountResource, MissingFieldException
from src.utils.response_builder import ResponseBuilder
from src.model.user import User


class MyAccountTestCase(unittest.TestCase):

    def test_get_myaccount(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        User._get_one = mock.MagicMock(return_value=user_mock_without_stories_or_friends)
        Token.identify = mock.MagicMock(return_value=user_mock_without_stories_or_friends['username'])
        ResponseBuilder.build_response = lambda output, status_code=200: output
        self.assertEqual(service.get(user_mock_without_stories_or_friends['username']),
                         account_info_mock_without_stories_or_friends)

    def test_get_myaccount_missing_field(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(side_effect=MissingFieldException("token"))
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 400)

    def test_get_myaccount_expired_token(self):
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(side_effect=ExpiredTokenException)
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 400)

    def test_get_myaccount_username_does_not_match_token(self):
        another_username = "asd"
        assert another_username != user_mock_without_stories_or_friends['username']
        service = MyAccountResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(return_value=another_username)
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 403)
