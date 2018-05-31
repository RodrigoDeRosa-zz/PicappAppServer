import unittest
from unittest.mock import MagicMock, patch

from src.model.story import Story, User, UserNotFoundException, StoryNotFoundException

from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description
from tests.mocks.story_mock import *


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

    def test_get_story_not_found(self):
        with patch.object(Story,"_get_one_by_id") as mocked_story_get, \
             self.assertRaises(StoryNotFoundException) as context:

            mocked_story_get.side_effect = MagicMock(return_value=None)

            mocked_story_id = object_id_mock

            Story.get_story(mocked_story_id)

        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_successful_get_story_public(self):
        with patch.object(Story, "_get_one_by_id") as mocked_story_get:
            # prepare special mock
            aux = story_mock_public_without_comments_or_reactions
            internal_story_mock = dict(aux)
            internal_story_mock["is_private"] = False
            internal_story_mock["timestamp"] = 1615456

            mocked_story_get.side_effect = MagicMock(return_value=internal_story_mock)
            mocked_story_id = object_id_mock

            self.assertEqual(Story.get_story(mocked_story_id), aux)

    def test_successful_get_story_private(self):
        with patch.object(Story, "_get_one_by_id") as mocked_story_get:
            # prepare special mock
            aux = story_mock_private_without_comments_or_reactions
            internal_story_mock = dict(aux)
            internal_story_mock["is_private"] = True
            internal_story_mock["timestamp"] = 1615456

            mocked_story_get.side_effect = MagicMock(return_value=internal_story_mock)
            mocked_story_id = object_id_mock

            self.assertEqual(Story.get_story(mocked_story_id), aux)

    def test_successful_post_reaction(self):
        with patch.object(Story, "_update_story") as mocked_story_update:
            aux = story_mock_private_with_reaction.copy()
            mocked_story_update.side_effect = MagicMock(return_value=story_mock_private_with_reaction)

            mocked_story_id = object_id_mock
            mocked_username, mocked_reaction = [(k,v) for k,v in aux["reactions"].items()][0]

            self.assertEqual(Story.react_to_story(mocked_story_id, mocked_username, mocked_reaction),
                             mocked_reaction)