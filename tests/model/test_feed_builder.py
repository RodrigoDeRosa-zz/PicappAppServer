import unittest
from unittest.mock import MagicMock, patch

from src.model.feed_builder import FeedBuilder, User, Story

from tests.mocks.story_mock import story_mock_public_without_comments_or_reactions
from tests.mocks.story_feed_data_mocks import *


class FeedBuilderTestCase(unittest.TestCase):

    def get_feed_data_mocks(self, username):
        return [bad_story_feed_data_mock, good_story_feed_data_mock, hot_story_feed_data_mock]

    def mocked_get_epochs(self):
        return current_epochs_mock

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

    def test_get_feed_contains_all_stories(self):
        with patch.object(User, "get_feed_data") as mocked_get_feed_data,\
             patch.object(FeedBuilder, "_format_feed_story") as mocked_format_story,\
             patch('src.model.feed_builder.get_current_epochs') as mocked_get_current_epochs:

            mocked_format_story.side_effect = lambda x: x  # return only the story_id
            mocked_get_feed_data.side_effect = self.get_feed_data_mocks
            mocked_get_current_epochs.side_effect = self.mocked_get_epochs

            expected_set = set([feed_data["story_id"] for feed_data in self.get_feed_data_mocks('pepe')])

            self.assertEqual(set(FeedBuilder.get_feed_for_username("pepe")), expected_set)

    def test_get_feed_prioritizes_hot_over_good_over_old_over_bad(self):
        with patch.object(User, "get_feed_data") as mocked_get_feed_data, \
                patch.object(FeedBuilder, "_format_feed_story") as mocked_format_story, \
                patch('src.model.feed_builder.get_current_epochs') as mocked_get_current_epochs:
            mocked_format_story.side_effect = lambda x: x  # return only the story_id
            mocked_get_feed_data.side_effect = self.get_feed_data_mocks
            mocked_get_current_epochs.side_effect = self.mocked_get_epochs

            expected_ordered_list = [hot_story_feed_data_mock, good_story_feed_data_mock, bad_story_feed_data_mock]
            expected_ids = [feed_data["story_id"] for feed_data in expected_ordered_list]

            self.assertEqual(FeedBuilder.get_feed_for_username("pepe"), expected_ids)
