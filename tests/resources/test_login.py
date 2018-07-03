import unittest
from unittest.mock import MagicMock, patch
from src.resources.login import LoginResource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import MissingFieldException
from src.model.services.shared_server_service import SharedServerService,InvalidDataException,UnexpectedErrorException,NoServerException
from tests.mocks.responses.token_response_mock import token_object_mock
from tests.mocks.object_id_mock import object_id_mock
from src.security.token import Token

USER_FIELD_MOCK = "user"
PW_FIELD_MOCK = "pw"


class LoginResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return USER_FIELD_MOCK

    def mocked_save_new(self,token, expiration_epochs, username):
        return object_id_mock

    def mocked_get_new_token(self,user_info):
        return token_object_mock

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_login_successful(self):
        with patch.object(Token, "save_new") as mocked_token_save_new,\
             patch.object(Token, "identify") as mocked_token_identify,\
             patch.object(SharedServerService, "get_new_token") as mocked_SSS_get_new_token, \
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder:

            mocked_token_save_new.side_effect = self.mocked_save_new
            mocked_token_identify.side_effect = self.mocked_identify
            mocked_SSS_get_new_token.side_effect = self.mocked_get_new_token
            mocked_response_builder.side_effect = self.mocked_build_response

            service = LoginResource()
            service._get_username_from_request = MagicMock(return_value=USER_FIELD_MOCK)
            service._get_password_from_request = MagicMock(return_value=PW_FIELD_MOCK)

            self.assertEqual(service.post()['token'], token_object_mock)

    def test_login_missing_field(self):
        with patch.object(ResponseBuilder, 'build_error_response') as mocked_response_builder:
            mocked_response_builder.side_effect = self.mocked_build_error_response

            service = LoginResource()
            service._get_username_from_request = MagicMock(return_value=USER_FIELD_MOCK)
            service._get_password_from_request = MagicMock(side_effect=MissingFieldException("password"))

            self.assertEqual(service.post(), 400)

    def test_login_invalid_data(self):
        with patch.object(SharedServerService, "get_new_token") as mocked_SSS_get_new_token, \
             patch.object(ResponseBuilder, 'build_error_response') as mocked_response_builder:
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_SSS_get_new_token.side_effect = InvalidDataException()

            service = LoginResource()
            service._get_username_from_request = MagicMock(return_value=USER_FIELD_MOCK)
            service._get_password_from_request = MagicMock(return_value=PW_FIELD_MOCK)
            self.assertEqual(service.post(), 400)

    def test_login_unexpected(self):
        with patch.object(SharedServerService, "get_new_token") as mocked_SSS_get_new_token, \
             patch.object(ResponseBuilder, 'build_error_response') as mocked_response_builder:
            mocked_SSS_get_new_token.side_effect = UnexpectedErrorException()
            mocked_response_builder.side_effect = self.mocked_build_error_response

            service = LoginResource()
            service._get_username_from_request = MagicMock(return_value=USER_FIELD_MOCK)
            service._get_password_from_request = MagicMock(return_value=PW_FIELD_MOCK)
            self.assertEqual(service.post(), 500)

    def test_login_noserver(self):
        with patch.object(SharedServerService, "get_new_token") as mocked_SSS_get_new_token, \
             patch.object(ResponseBuilder, 'build_error_response') as mocked_response_builder:
            mocked_SSS_get_new_token.side_effect = NoServerException()
            mocked_response_builder.side_effect = self.mocked_build_error_response

            service = LoginResource()
            service._get_username_from_request = MagicMock(return_value=USER_FIELD_MOCK)
            service._get_password_from_request = MagicMock(return_value=PW_FIELD_MOCK)
            self.assertEqual(service.post(), 500)
