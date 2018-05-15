import unittest
from unittest.mock import MagicMock, patch

from src.resources.stories import StoriesResource, Story
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import MissingFieldException
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description, story_data_mock_without_title_or_description
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.token_mock import token_mock
from tests.mocks.object_id_mock import object_id_mock


class StoriesResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_info_mock['username']

    def mocked_save_new(self, story_data):
        return object_id_mock

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_successful_post_with_optional_fields(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "save_new") as mocked_story,\
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder:
            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = self.mocked_save_new
            mocked_response_builder.side_effect = self.mocked_build_response

            aux = story_data_mock_with_title_and_description

            service = StoriesResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_privateness_from_request = MagicMock(return_value=aux['is_private'])
            service._get_timestamp_from_request = MagicMock(return_value=aux['timestamp'])
            service._get_location_from_request = MagicMock(return_value=aux['location'])
            service._get_media_from_request = MagicMock(return_value=aux['media'])
            service._try_get_description_from_request = MagicMock(return_value=aux['description'])
            service._try_get_title_from_request = MagicMock(return_value=aux['title'])
            self.assertEqual(service.post()['story_id'], object_id_mock)

    def test_missing_required_field(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "save_new") as mocked_story,\
                patch.object(ResponseBuilder, "build_error_response")as mocked_response_builder:
            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = self.mocked_save_new
            mocked_response_builder.side_effect = self.mocked_build_error_response

            aux = story_data_mock_with_title_and_description

            service = StoriesResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_privateness_from_request = MagicMock(return_value=aux['is_private'])
            service._get_timestamp_from_request = MagicMock(return_value=aux['timestamp'])
            service._get_location_from_request = MagicMock(side_effect=MissingFieldException("location"))
            service._get_media_from_request = MagicMock(return_value=aux['media'])
            service._try_get_description_from_request = MagicMock(return_value=aux['description'])
            service._try_get_title_from_request = MagicMock(return_value=aux['title'])

            self.assertEqual(service.post(), 400)

    def test_successful_post_without_optional_fields(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "save_new") as mocked_story,\
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder:
            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = self.mocked_save_new
            mocked_response_builder.side_effect = self.mocked_build_response

            aux = story_data_mock_without_title_or_description

            service = StoriesResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_privateness_from_request = MagicMock(return_value=aux['is_private'])
            service._get_timestamp_from_request = MagicMock(return_value=aux['timestamp'])
            service._get_location_from_request = MagicMock(return_value=aux['location'])
            service._get_media_from_request = MagicMock(return_value=aux['media'])
            service._try_get_description_from_request = MagicMock(return_value="")
            service._try_get_title_from_request = MagicMock(return_value="")
            self.assertEqual(service.post()['story_id'], object_id_mock)