import unittest
import unittest.mock as mock

from src.model.connectors.shared_server_connector import SharedServerConnector
from src.model.services.shared_server_service import SharedServerService
from tests.mocks.responses.token_response_mock import token_object_mock, user_object_mock


class SharedServerServiceTestCase(unittest.TestCase):

    def setUp(self):
        self.service = SharedServerService()

    def test_get_new_token_success(self):
        user_info = {'username': 'nainggolan', 'password': '30'}
        SharedServerConnector.get_new_token = mock.MagicMock(return_value=token_object_mock)
        self.assertEqual(self.service.get_new_token(user_info), token_object_mock)

    def test_create_user_success(self):
        user_info = {'username': 'salah', 'password': '21'}
        SharedServerConnector.create_user = mock.MagicMock(return_value=user_object_mock)
        self.assertEqual(self.service.create_user(user_info), user_object_mock)


if __name__ == '__main__':
    unittest.main()
