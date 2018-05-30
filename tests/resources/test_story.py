import unittest
from unittest.mock import MagicMock, patch

from src.resources.story import StoryResource, Story, Friendship, StoryNotFoundException
from src.security.token import Token
from src.utils.response_builder import ResponseBuilder
from tests.mocks.story_mock import story_mock_public_without_comments_or_reactions, story_mock_private_without_comments_or_reactions
from tests.mocks.user_info_mock import user_info_mock
from tests.mocks.token_mock import token_mock
from tests.mocks.object_id_mock import object_id_mock


class StoryResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return user_info_mock['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def mocked_are_friends_true(self, username1, username2):
        return True

    def mocked_are_friends_false(self, username1, username2):
        return False

    def test_successful_get_story_public(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "get_story") as mocked_story, \
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
                patch.object(Friendship, "are_friends") as mocked_are_friends:
            aux = story_mock_public_without_comments_or_reactions

            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = MagicMock(return_value=aux)
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_are_friends.side_effect = self.mocked_are_friends_true

            service = StoryResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.get(object_id_mock), aux)

    def test_successful_get_own_story_private(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "get_story") as mocked_story, \
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
                patch.object(Friendship, "are_friends") as mocked_are_friends:

            aux = dict(story_mock_private_without_comments_or_reactions)
            aux['username'] = self.mocked_identify("")  # make it so that uploader is the one requesting

            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = MagicMock(return_value=aux)
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_are_friends.side_effect = self.mocked_are_friends_false

            service = StoryResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.get(object_id_mock), aux)

    def test_failed_get_story_not_found(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "get_story") as mocked_story, \
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
                patch.object(Friendship, "are_friends") as mocked_are_friends:

            aux = story_mock_public_without_comments_or_reactions

            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = MagicMock(side_effect=StoryNotFoundException())
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_are_friends.side_effect = self.mocked_are_friends_false

            service = StoryResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.get(object_id_mock), 404)

    def test_successful_get_friend_story_private(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "get_story") as mocked_story, \
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
                patch.object(Friendship, "are_friends") as mocked_are_friends:

            aux = dict(story_mock_private_without_comments_or_reactions)
            aux['username'] = self.mocked_identify("")+"asd"  # make it so that uploader is NOT the one requesting

            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = MagicMock(return_value=aux)
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_are_friends.side_effect = self.mocked_are_friends_true

            service = StoryResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.get(object_id_mock), aux)

    def test_failed_get_not_friend_story_private(self):
        with patch.object(Token, "identify") as mocked_token, \
                patch.object(Story, "get_story") as mocked_story, \
                patch.object(ResponseBuilder, "build_response")as mocked_response_builder,\
                patch.object(Friendship, "are_friends") as mocked_are_friends:

            aux = dict(story_mock_private_without_comments_or_reactions)
            aux['username'] = self.mocked_identify("")+"asd"  # make it so that uploader is NOT the one requesting

            mocked_token.side_effect = self.mocked_identify
            mocked_story.side_effect = MagicMock(return_value=aux)
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_are_friends.side_effect = self.mocked_are_friends_false

            service = StoryResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.get(object_id_mock), 403)