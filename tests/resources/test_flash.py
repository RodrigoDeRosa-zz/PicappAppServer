import unittest
from unittest.mock import MagicMock, patch

from src.resources.flash import FlashResource, FlashNotFoundException, Friendship, Flash
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from tests.mocks.flash_mock import flash_mock
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.token_mock import token_mock
from tests.mocks.object_id_mock import object_id_mock


class FlashResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_info_mock['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_get_flash_not_found(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Flash, "get_flash") as mocked_flash, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
             patch.object(Friendship, "are_friends") as mocked_are_friends:

            mocked_token.side_effect = self.mocked_identify
            mocked_flash.side_effect = MagicMock(side_effect=FlashNotFoundException)
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_are_friends.side_effect = MagicMock(return_value=True)

            service = FlashResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(object_id_mock), 404)

    def test_get_flash_not_friends(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Flash, "get_flash") as mocked_flash, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
             patch.object(Friendship, "are_friends") as mocked_are_friends:

            mocked_token.side_effect = self.mocked_identify
            mocked_flash.side_effect = MagicMock(return_value=flash_mock)
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_are_friends.side_effect = MagicMock(return_value=False)

            service = FlashResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(object_id_mock), 403)

    def test_get_flash_successful(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Flash, "get_flash") as mocked_flash, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
             patch.object(Friendship, "are_friends") as mocked_are_friends:

            mocked_token.side_effect = self.mocked_identify
            mocked_flash.side_effect = MagicMock(return_value=flash_mock)
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_are_friends.side_effect = MagicMock(return_value=True)

            service = FlashResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(object_id_mock), flash_mock)
