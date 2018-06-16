import unittest
from unittest.mock import MagicMock, patch

from src.model.feed_builder import FeedBuilder, User, Story

from tests.mocks.story_mock import story_mock_public_without_comments_or_reactions


class FeedBuilderTestCase(unittest.TestCase):

    def test_format_story(self):
        with patch.object(Story, "get_story") as mocked_get_story,\
             patch.object(User, "get_profile_preview") as mocked_get_profile_preview:
            aux_story = dict(story_mock_public_without_comments_or_reactions)
            profile_preview_mock = {
                "name": "pepe",
                "profile_pic": "some_link",
                "username": aux_story['username']
            }
            expected_formatted_story = dict(aux_story)
            expected_formatted_story['name'] = profile_preview_mock['name']
            expected_formatted_story['profile_pic'] = profile_preview_mock['profile_pic']

            mocked_get_story.side_effect = MagicMock(return_value=aux_story)
            mocked_get_profile_preview.side_effect = MagicMock(return_value=profile_preview_mock)

            self.assertEqual(FeedBuilder._format_feed_story("some_id"), expected_formatted_story)
