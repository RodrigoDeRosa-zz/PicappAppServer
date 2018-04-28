import unittest
import unittest.mock as mock
from src.resources.login import LoginResource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import MissingFieldException
from src.model.services.shared_server_service import SharedServerService,InvalidDataException,UnexpectedErrorException,NoServerException
from tests.mocks.responses.token_response_mock import token_object_mock
from tests.mocks.object_id_mock import object_id_mock
from src.security.token import Token


class LoginResourceTestCase(unittest.TestCase):

    def test_login_successful(self):
        user_mock = "user"
        pw_mock = "pw"
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value=user_mock)
        service._get_password_from_request = mock.MagicMock(return_value=pw_mock)
        SharedServerService.get_new_token = mock.MagicMock(return_value=token_object_mock)
        Token.save_new = mock.MagicMock(return_value=object_id_mock)
        Token.identify = mock.MagicMock(return_value=user_mock)
        ResponseBuilder.build_response = lambda response, status_code = 200: response
        self.assertEqual(service.post()['token'], token_object_mock)

    def test_login_missing_field(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(side_effect=MissingFieldException("password"))
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 400)

    def test_login_invalid_data(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value="pw")
        SharedServerService.get_new_token = mock.MagicMock(side_effect=InvalidDataException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 400)

    def test_login_unexpected(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value="pw")
        SharedServerService.get_new_token = mock.MagicMock(side_effect=UnexpectedErrorException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 500)

    def test_login_noserver(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value="pw")
        SharedServerService.get_new_token = mock.MagicMock(side_effect=NoServerException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(), 500)
