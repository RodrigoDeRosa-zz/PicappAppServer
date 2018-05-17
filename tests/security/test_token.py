import unittest
from unittest.mock import MagicMock, patch
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from tests.mocks.token_object_mock import token_object_mock


class TokenTestCase(unittest.TestCase):
    """These tests should not be ran with the others, as they use a deeper Model than the resources
    and other functionality. Run them separately to check Token works, they are left as regression
    tests."""

    def mocked_successful_find_token(self, token):
        return token_object_mock

    def mocked_failed_find_token(self, token):
        return None

    def mocked_get_current_epochs_always_ok(self):
        return -1

    def test_successful_identify(self):
        with patch.object(Token, "_find_token") as mocked_token_find_token,\
             patch.object(Token, "_get_current_epochs") as mocked_token_epochs:
            mocked_token_epochs.side_effect = self.mocked_get_current_epochs_always_ok
            mocked_token_find_token.side_effect = self.mocked_successful_find_token

            self.assertEqual(Token.identify(token_object_mock['token']), token_object_mock['username'])

    def test_invalid_identify(self):
        with patch.object(Token,"_find_token") as mocked_token_find_token,\
             patch.object(Token,"_get_current_epochs") as mocked_token_epochs, \
             self.assertRaises(InvalidTokenException) as context:
            mocked_token_epochs.side_effect = self.mocked_get_current_epochs_always_ok
            mocked_token_find_token.side_effect = self.mocked_failed_find_token
            Token.identify(token_object_mock['token'])
        exc = context.exception
        self.assertEqual(exc.error_code, 400)
        self.assertEqual(exc.message, "Received token was invalid")

    def test_expired_identify(self):
        with patch.object(Token, "_find_token") as mocked_token_find_token,\
             patch.object(Token, "_get_current_epochs") as mocked_token_epochs, \
             self.assertRaises(ExpiredTokenException) as context:
            current_time = token_object_mock['expiresAt'] + 1
            mocked_token_epochs.side_effect = MagicMock(return_value=current_time)
            mocked_token_find_token.side_effect = self.mocked_successful_find_token
            Token.identify(token_object_mock['token'])
        exc = context.exception
        self.assertEqual(exc.error_code, 400)
        self.assertEqual(exc.message, "Received token has expired")
