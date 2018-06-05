import unittest
from unittest.mock import MagicMock, patch
from src.model.user import User, UserNotFoundException, Story
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description
from tests.mocks.story_mock import *
from tests.mocks.user_mock import user_mock_without_stories_or_friends, profile_mock_without_stories_or_friends


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

    def test_get_profile_not_found(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             self.assertRaises(UserNotFoundException) as context:
            mocked_user_get.side_effect = MagicMock(return_value=None)

            User.get_profile("pedro")

        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_get_profile_successful(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             patch.object(Story, "get_stories_by_username") as mocked_story_get_stories:
            aux_timestamp = 123123
            aux_story1 = dict(story_mock_private_with_reaction)
            aux_story1["timestamp"] = aux_timestamp

            aux_story2 = dict(story_mock_private_with_reaction)
            aux_story2["timestamp"] = aux_timestamp+1

            aux_story3 = dict(story_mock_private_with_reaction)
            aux_story3["timestamp"] = aux_timestamp+2

            expected_profile = profile_mock_without_stories_or_friends
            expected_profile["stories"] = [aux_story3, aux_story2, aux_story1]
            expected_profile["number of stories"] = 3

            mocked_user_get.side_effect = MagicMock(return_value=user_mock_without_stories_or_friends)
            mocked_story_get_stories.side_effect = MagicMock(return_value=expected_profile["stories"])

            self.assertEqual(User.get_profile("asd"), expected_profile)

