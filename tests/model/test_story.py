import unittest
from unittest.mock import MagicMock, patch

from src.model.story import Story, User

from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description


class StoryTestCase(unittest.TestCase):

    def mocked_user_get_one(self, query):
        return user_mock_without_stories_or_friends

    def mocked_story_insert_one(self, query):
        return object_id_mock
'''
    def test_successful_save_new(self):
        with patch.object(User, "_get_one") as mocked_user_get_one, \
            patch.object(Story, "_insert_one") as mocked_story_get_one:
'''