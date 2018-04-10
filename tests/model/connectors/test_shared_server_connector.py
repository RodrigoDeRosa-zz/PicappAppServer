import unittest
from unittest import mock
from src.model.connectors.shared_server_connector import SharedServerConnector
from src.model.exceptions.response_exceptions import *
from tests.mocks.responses.token_response_mock import *

NEW_TOKEN_URI = 'https://picappss.herokuapp.com/api/token'
NEW_USER_URI = 'https://picappss.herokuapp.com/api/user'


class MockResponse:
    """Class to mock any response"""

    def __init__(self, json_data, status_code):
        self.text = json_data
        self.json_data = json_data
        self.status_code = status_code

    def json(self):
        return self.json_data


def mock_request_successful_post(*args, **kwargs):
    """Returns successful responses for posts"""
    if args[0] == NEW_TOKEN_URI:
        return MockResponse(post_token_response_mock, 200)
    elif args[0] == NEW_USER_URI:
        return MockResponse(post_user_response_mock, 200)


def mock_bad_request(*args, **kwargs):
    if args[0] == NEW_TOKEN_URI:
        return MockResponse(missing_username_mock, 400)
    elif args[0] == NEW_USER_URI:
        return MockResponse(missing_password_mock, 400)


def mock_internal_server_error(*args, **kwargs):
    if args[0]:  # == NEW_TOKEN_URI:
        return MockResponse(internal_error_mock, 500)


def mock_unauthorized_error(*args, **kwargs):
    if args[0]:  # == NEW_TOKEN_URI:
        return MockResponse(unauthorized_mock, 401)


class SharedServerConnectorTestCase(unittest.TestCase):

    def setUp(self):
        self.connector = SharedServerConnector()

    @mock.patch('requests.post', side_effect=mock_request_successful_post)
    def test_new_token_correct_user(self, mock_post):
        user_info = {'user': 'rodrigo.derosa', 'password': 'some-password'}
        token = self.connector.get_new_token(user_info)
        self.assertEqual(token, post_token_response_mock['token'])

    @mock.patch('requests.post', side_effect=mock_bad_request)
    def test_new_token_missing_field(self, mock_post):
        user_info = {'password': 'some-password'}
        with self.assertRaises(BadRequestException) as context:
            self.connector.get_new_token(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, missing_username_mock['code'])
        self.assertEqual(exception.message, missing_username_mock['message'])

    @mock.patch('requests.post', side_effect=mock_internal_server_error)
    def test_new_token_internal_error(self, mock_post):
        user_info = {'username': 'rodrigo.derosa', 'password': 'some-password'}
        with self.assertRaises(InternalServerErrorException) as context:
            self.connector.get_new_token(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, internal_error_mock['code'])
        self.assertEqual(exception.message, internal_error_mock['message'])

    @mock.patch('requests.post', side_effect=mock_unauthorized_error)
    def test_new_token_unauthorized(self, mock_post):
        """This should never happen because there is no kind of authentication for this request. Anyway, the API
        says this is a possible outcome so we test it :)"""
        user_info = {'username': 'rodrigo.derosa', 'password': 'some-password'}
        with self.assertRaises(UnauthorizedException) as context:
            self.connector.get_new_token(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, unauthorized_mock['code'])
        self.assertEqual(exception.message, unauthorized_mock['message'])

    @mock.patch('requests.post', side_effect=mock_request_successful_post)
    def test_create_user_successful(self, mock_post):
        user_info = {'username': 'martin.errazquin', 'password': 'some-other-password'}
        user = self.connector.create_user(user_info)
        self.assertEqual(user, post_user_response_mock['user'])

    @mock.patch('requests.post', side_effect=mock_bad_request)
    def test_create_user_missing_field(self, mock_post):
        user_info = {'username': 'martin.errazquin'}
        with self.assertRaises(BadRequestException) as context:
            self.connector.create_user(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, missing_password_mock['code'])
        self.assertEqual(exception.message, missing_password_mock['message'])

    @mock.patch('requests.post', side_effect=mock_internal_server_error)
    def test_create_user_internal_error(self, mock_post):
        user_info = {'username': 'martin.errazquin', 'password': 'some-other-password'}
        with self.assertRaises(InternalServerErrorException) as context:
            self.connector.create_user(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, internal_error_mock['code'])
        self.assertEqual(exception.message, internal_error_mock['message'])

    @mock.patch('requests.post', side_effect=mock_unauthorized_error)
    def test_create_user_unauthorized(self, mock_post):
        user_info = {'username': 'martin.errazquin', 'password': 'some-other-password'}
        with self.assertRaises(UnauthorizedException) as context:
            self.connector.create_user(user_info)
        exception = context.exception
        self.assertEqual(exception.error_code, unauthorized_mock['code'])
        self.assertEqual(exception.message, unauthorized_mock['message'])


if __name__ == '__main__':
    unittest.main()
