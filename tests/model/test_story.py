import unittest
from unittest.mock import MagicMock, patch

from src.model.story import Story, User, UserNotFoundException

from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description


class StoryTestCase(unittest.TestCase):

    def mocked_user_get_one(self, query):
        return user_mock_without_stories_or_friends

    def mocked_story_insert_one(self, query):
        return object_id_mock

    def mocked_add_story_to_user(self, username, story_id):
        pass

    def test_successful_save_new(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             patch.object(Story, "_insert_one") as mocked_story_insert, \
             patch.object(Story, "_add_story_id_to_user") as mocked_story_add_to_user:
            mocked_story_insert.side_effect = self.mocked_story_insert_one
            mocked_user_get.side_effect = self.mocked_user_get_one
            mocked_story_add_to_user.side_effect = self.mocked_add_story_to_user

            story_data = dict(story_data_mock_with_title_and_description)
            story_data['username'] = "pedro"

            self.assertEqual(Story.save_new(story_data), object_id_mock)

    def test_save_new_user_not_found(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             patch.object(Story, "_insert_one") as mocked_story_insert, \
             self.assertRaises(UserNotFoundException):
            mocked_story_insert.side_effect = self.mocked_story_insert_one
            mocked_user_get.side_effect = MagicMock(return_value=None)

            story_data = dict(story_data_mock_with_title_and_description)
            story_data['username'] = "pedro"

            Story.save_new(story_data)
