import unittest
import unittest.mock as mock
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from tests.mocks.token_object_mock import token_object_mock


class TokenTestCase(unittest.TestCase):
    """These tests should not be ran with the others, as they use a deeper Model than the resources
    and other functionality. Run them separately to check Token works, they are left as regression
    tests."""

    def _test_successful_identify(self):
        Token._find_token = mock.MagicMock(return_value=token_object_mock)
        Token._get_current_epochs = mock.MagicMock(return_value=-1)
        self.assertEqual(Token.identify(token_object_mock['token']), token_object_mock['username'])

    def _test_invalid_identify(self):
        Token._find_token = mock.MagicMock(return_value=None)
        Token._get_current_epochs = mock.MagicMock(return_value=-1)
        with self.assertRaises(InvalidTokenException):
            Token.identify(token_object_mock['token'])

    def _test_expired_identify(self):
        current_time = token_object_mock['expiresAt'] + 1
        Token._find_token = mock.MagicMock(return_value=token_object_mock)
        Token._get_current_epochs = mock.MagicMock(return_value=current_time)
        with self.assertRaises(ExpiredTokenException):
            Token.identify(token_object_mock['token'])
