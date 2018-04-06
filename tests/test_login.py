import unittest
import unittest.mock as mock
from src.resources.login import LoginResource
from src.resources.response_builder import ResponseBuilder
from src.resources.request_builder import MissingFieldException
from src.model.sharedserver_proxy import SharedServerProxy,InvalidDataException,UnexpectedErrorException,NoServerException
# from tests.mocks.token_mock import token_mock
from tests.mocks.sharedserver_post_token_mock import sharedserver_post_token_mock

class LoginResourceTestCase(unittest.TestCase):

    def test_login_succesful(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value = "user")
        service._get_password_from_request = mock.MagicMock(return_value = "pw")
        SharedServerProxy.post_token = mock.MagicMock(return_value = sharedserver_post_token_mock)
        ResponseBuilder.build_response = lambda response,status_code = 200 : response
        self.assertEqual(service.post()['token'],sharedserver_post_token_mock['token'])

    def test_login_missingfield(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(side_effect = MissingFieldException())
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(),400)

    def test_login_invaliddata(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value = "pw")
        SharedServerProxy.post_token = mock.MagicMock(side_effect = InvalidDataException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(),401)

    def test_login_unexpected(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value = "pw")
        SharedServerProxy.post_token = mock.MagicMock(side_effect = UnexpectedErrorException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(),500)

    def test_login_noserver(self):
        service = LoginResource()
        service._get_username_from_request = mock.MagicMock(return_value="user")
        service._get_password_from_request = mock.MagicMock(return_value = "pw")
        SharedServerProxy.post_token = mock.MagicMock(side_effect = NoServerException)
        ResponseBuilder.build_response = lambda response, status_code: status_code
        self.assertEqual(service.post(),500)
