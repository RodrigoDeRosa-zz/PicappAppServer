import unittest
from unittest.mock import MagicMock, patch

from src.security.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from tests.mocks.user_mock import user_mock_without_stories_or_friends, account_info_mock_without_stories_or_friends
from tests.mocks.object_id_mock import object_id_mock
from src.resources.myaccount import MyAccountResource, MissingFieldException, NoServerException, InvalidDataException, UnexpectedErrorException, ConnectionFailException
from src.utils.response_builder import ResponseBuilder
from src.model.user import User


class MyAccountTestCase(unittest.TestCase):

    def mocked_build_response(self,output,status_code=200):
        return output

    def mocked_build_error_response(self,output,status_code):
        return status_code

    def test_get_myaccount(self):
        with patch.object(Token, "identify") as mocked_token_identify,\
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_response
            mocked_token_identify.side_effect = MagicMock(return_value=user_mock_without_stories_or_friends['username'])
            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            User._get_one = MagicMock(return_value=user_mock_without_stories_or_friends)
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']),
                             account_info_mock_without_stories_or_friends)

    def test_get_myaccount_missing_field(self):
        with patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            service = MyAccountResource()
            service._get_token_from_header = MagicMock(side_effect=MissingFieldException("token"))
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 400)

    def test_get_myaccount_expired_token(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_token_identify.side_effect = ExpiredTokenException()
            mocked_builder_response.side_effect = self.mocked_build_error_response
            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 400)

    def test_get_myaccount_username_does_not_match_token(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            another_username = "asd"
            assert another_username != user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=another_username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.get(user_mock_without_stories_or_friends['username']), 403)

    def test_delete_myaccount_expired_token(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            mocked_token_identify.side_effect = ExpiredTokenException()

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            self.assertEqual(service.delete(user_mock_without_stories_or_friends['username']), 400)

    def test_delete_myaccount_invalid_data(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            username = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service.shared_server_service.delete_user = MagicMock(side_effect=InvalidDataException)
            self.assertEqual(service.delete(username), 400)

    def test_delete_myaccount_connection_fail(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            username = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service.shared_server_service.delete_user = MagicMock(side_effect=ConnectionFailException)
            self.assertEqual(service.delete(username), 500)

    def test_delete_myaccount_no_server(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            username = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service.shared_server_service.delete_user = MagicMock(side_effect=NoServerException)
            self.assertEqual(service.delete(username), 500)

    def test_delete_myaccount_unexpected_error(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response:
            mocked_builder_response.side_effect = self.mocked_build_error_response
            username = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service.shared_server_service.delete_user = MagicMock(side_effect=UnexpectedErrorException)
            self.assertEqual(service.delete(username), 500)

    def test_delete_myaccount_successful(self):
        with patch.object(Token, "identify") as mocked_token_identify, \
             patch.object(ResponseBuilder, "build_response") as mocked_builder_response,\
             patch.object(User, "delete_user") as mocked_user_delete_user,\
             patch.object(Token, "log_out") as mocked_token_log_out:
            mocked_builder_response.side_effect = self.mocked_build_response
            username = user_mock_without_stories_or_friends['username']
            mocked_token_identify.side_effect = MagicMock(return_value=username)
            mocked_token_log_out.side_effect = MagicMock(return_value=object_id_mock)
            mocked_user_delete_user.side_effect = MagicMock(return_value=username)

            service = MyAccountResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service.shared_server_service.delete_user = MagicMock(return_value=username)
            self.assertEqual(service.delete(username)['username'], username)
