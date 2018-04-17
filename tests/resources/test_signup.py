import unittest
import unittest.mock as mock

from src.model.user import User
from src.resources.signup import SignUpResource, MissingFieldException, UnexpectedErrorException, InvalidDataException, NoServerException
from src.utils.request_builder import RequestBuilder
from src.utils.response_builder import ResponseBuilder
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.responses.token_response_mock import post_user_response_mock


class SignUpResourceTestCase(unittest.TestCase):

    def test_signup_succesful(self):
        service = SignUpResource()
        service._get_password_from_request = mock.MagicMock(return_value=user_info_mock['password'])
        service._get_username_from_request = mock.MagicMock(return_value=user_info_mock['username'])
        service.shared_server_service.create_user = mock.MagicMock(return_value=post_user_response_mock['user'])
        User.insert_one = mock.MagicMock(return_value=3)  # TODO: is '3' a valid _id?
        ResponseBuilder.build_response = lambda response, status_code = 200: response
        self.assertEqual(service.post(), user_info_mock)

    def test_signup_missing_field(self):
        service = SignUpResource()
        service._get_password_from_request = mock.MagicMock(return_value=user_info_mock['password'])
        service._get_username_from_request = mock.MagicMock(side_effect = MissingFieldException)
        ResponseBuilder.build_error_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 400)

    def test_signup_no_server(self):
        service = SignUpResource()
        service._get_password_from_request = mock.MagicMock(return_value=user_info_mock['password'])
        service._get_username_from_request = mock.MagicMock(return_value=user_info_mock['username'])
        service.shared_server_service.create_user = mock.MagicMock(side_effect=NoServerException)
        ResponseBuilder.build_error_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 500)

    def test_signup_invalid_data(self):
        service = SignUpResource()
        service._get_password_from_request = mock.MagicMock(return_value=user_info_mock['password'])
        service._get_username_from_request = mock.MagicMock(return_value=user_info_mock['username'])
        service.shared_server_service.create_user = mock.MagicMock(side_effect=InvalidDataException)
        ResponseBuilder.build_error_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 400)

    def test_signup_unexpected_error(self):
        service = SignUpResource()
        service._get_password_from_request = mock.MagicMock(return_value=user_info_mock['password'])
        service._get_username_from_request = mock.MagicMock(return_value=user_info_mock['username'])
        service.shared_server_service.create_user = mock.MagicMock(side_effect=UnexpectedErrorException)
        ResponseBuilder.build_error_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 500)
