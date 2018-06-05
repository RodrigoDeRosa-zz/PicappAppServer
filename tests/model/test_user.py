import unittest
from unittest.mock import MagicMock, patch
from src.model.user import User, UserNotFoundException, Story
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description


class UserTestCase(unittest.TestCase):

    def mocked_story_insert_one(self, query):
        return object_id_mock

    def test_save_new_user_not_found(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             patch.object(Story, "save_new") as mocked_story_save, \
             self.assertRaises(UserNotFoundException):
            mocked_story_save.side_effect = self.mocked_story_insert_one
            mocked_user_get.side_effect = MagicMock(return_value=None)

            story_data = dict(story_data_mock_with_title_and_description)
            story_data['username'] = "pedro"

            User.save_new_story(story_data)

