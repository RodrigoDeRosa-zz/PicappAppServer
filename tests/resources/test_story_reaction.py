import unittest
from unittest.mock import MagicMock, patch

from src.resources.story_reaction import StoryReactionResource, Story, MissingFieldException, StoryNotFoundException
from src.security.input_sanitizer import InputSanitizer, InvalidFormatException
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from src.model.story_reaction_types import *

from tests.mocks.token_mock import token_mock
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_reaction_mock import story_reaction_mock_like

class StoryReactionResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_info_mock['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_failed_post_reaction_invalid_reaction(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "react_to_story") as mocked_react, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            reaction = STORY_REACTION_LIKE
            not_reaction = reaction+"asd"

            assert not_reaction not in ALLOWED_STORY_REACTIONS
            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_react.side_effect = MagicMock(return_value=STORY_REACTION_LIKE)

            service = StoryReactionResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_reaction_from_request = MagicMock(return_value=not_reaction)

            self.assertEqual(service.post(object_id_mock), 400)

    def test_failed_post_reaction_missing_reaction_field(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "react_to_story") as mocked_react, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_react.side_effect = MagicMock(return_value=STORY_REACTION_LIKE)

            service = StoryReactionResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_reaction_from_request = MagicMock(side_effect=MissingFieldException("reaction"))

            self.assertEqual(service.post(object_id_mock), 400)

    def test_failed_post_reaction_story_not_found(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "react_to_story") as mocked_react, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            reaction = STORY_REACTION_FUNNY

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_react.side_effect = MagicMock(side_effect=StoryNotFoundException)

            service = StoryReactionResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_reaction_from_request = MagicMock(return_value=reaction)

            self.assertEqual(service.post(object_id_mock), 404)

    def test_successful_post_reaction_like(self):
        with patch.object(Token, "identify") as mocked_token, \
             patch.object(Story, "react_to_story") as mocked_react, \
             patch.object(ResponseBuilder, "build_response")as mocked_response_builder:

            reaction = STORY_REACTION_LIKE

            mocked_token.side_effect = self.mocked_identify
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_react.side_effect = MagicMock(return_value=reaction)

            service = StoryReactionResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            service._get_reaction_from_request = MagicMock(return_value=reaction)

            self.assertEqual(service.post(object_id_mock), story_reaction_mock_like)
