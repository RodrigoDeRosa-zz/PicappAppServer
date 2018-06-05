import unittest
from unittest.mock import MagicMock, patch

from src.resources.story_comment import StoryCommentResource, Story, MissingFieldException, StoryNotFoundException
from src.security.input_sanitizer import InputSanitizer, InvalidFormatException
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from src.model.story_reaction_types import *

from tests.mocks.token_mock import token_mock
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_comment_mock import story_comment_mock


class StoryCommentResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_info_mock['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_failed_post_comment_missing_field(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "comment_on_story") as mocked_comment, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            comment_mock = story_comment_mock

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_comment.side_effect = MagicMock(return_value=comment_mock)

            service = StoryCommentResource()
            service._get_token_from_header = MagicMock(side_effect=MissingFieldException("token"))
            service._get_comment_text_from_request = MagicMock(return_value=comment_mock["comment"])
            service._get_timestamp_from_request = MagicMock(return_value=comment_mock["timestamp"])

            self.assertEqual(service.post(object_id_mock), 400)

    def test_successful_post_comment(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "comment_on_story") as mocked_comment, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            comment_mock = story_comment_mock

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_comment.side_effect = MagicMock(return_value=comment_mock)

            service = StoryCommentResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service._get_comment_text_from_request = MagicMock(return_value=comment_mock["comment"])
            service._get_timestamp_from_request = MagicMock(return_value=comment_mock["timestamp"])

            self.assertEqual(service.post(object_id_mock), comment_mock)

    def test_failed_post_comment_story_not_found(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "comment_on_story") as mocked_comment, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            comment_mock = story_comment_mock

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_comment.side_effect = MagicMock(side_effect=StoryNotFoundException)

            service = StoryCommentResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)
            service._get_comment_text_from_request = MagicMock(return_value=comment_mock["comment"])
            service._get_timestamp_from_request = MagicMock(return_value=comment_mock["timestamp"])

            self.assertEqual(service.post(object_id_mock), 404)