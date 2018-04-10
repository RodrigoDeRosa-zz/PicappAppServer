import unittest
import unittest.mock as mock
from src.resources.profile import ProfileResource,UserNotFoundException
from src.utils.response_builder import ResponseBuilder
from tests.mocks.user_mock import user_mock


class ProfileResourceTestCase(unittest.TestCase):

    def test_get_user(self):
        mock_name = user_mock['name']

        service = ProfileResource()
        service._find_one_user = mock.MagicMock(return_value=user_mock)
        ResponseBuilder.build_response = mock.MagicMock(return_value=user_mock)
        self.assertEqual(service.get(mock_name),user_mock)

    def test_get_user_not_found(self):
        service = ProfileResource()
        service._find_one_user = mock.Mock(side_effect=UserNotFoundException())
        ResponseBuilder.build_response = lambda response, status_code: status_code  # Solo devuelve el status_code
        response = service.get("asd")
        self.assertEqual(response,404)
