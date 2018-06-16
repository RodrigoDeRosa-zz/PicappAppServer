import unittest
from unittest.mock import MagicMock, patch
from src.model.user import User, UserNotFoundException, Story
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description
from tests.mocks.story_mock import *
from tests.mocks.user_mock import user_mock_without_stories_or_friends, profile_mock_without_stories_or_friends, \
    user_mock_without_stories_with_friends


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

    def test_get_profile_preview_not_found(self):
        with patch.object(User, "_get_one") as mocked_user_get, \
             self.assertRaises(UserNotFoundException) as context:
            mocked_user_get.side_effect = MagicMock(side_effect=UserNotFoundException)

            User.get_profile_preview("pepe")

        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_get_profile_preview_successful(self):
        with patch.object(User, "_get_one") as mocked_user_get:

            aux_user_obj = user_mock_without_stories_or_friends
            aux_username = aux_user_obj['username']
            expected_preview = {
                "username": aux_user_obj['username'],
                "profile_pic": aux_user_obj['profile_pic'],
                "name": aux_user_obj['name']
            }
            mocked_user_get.side_effect = MagicMock(return_value=aux_user_obj)
            self.assertEqual(User.get_profile_preview(aux_username), expected_preview)

    def test_get_user_feed_data(self):
        with patch('src.model.user._user') as mocked_user:

            internal_user_mock = dict(user_mock_without_stories_with_friends)

            expected_user_feed_data = {
                "friend_ids": {"friend_id1", "friend_id2"},  # WARNING: hardcoded from the mock above
                "number of friends": 2,
                "number of stories": 5
            }
            mocked_user.side_effect = MagicMock(return_value=internal_user_mock)
            self.assertEqual(User._get_user_feed_data("pepe", expected_user_feed_data["number of stories"]),
                             expected_user_feed_data)
