import unittest
from unittest.mock import MagicMock, patch

from src.model.flash import FlashNotFoundException, Flash
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.flash_data_mocks import flash_data_mock_with_title_and_description


class FlashTestCase(unittest.TestCase):

    def mocked_user_get_one(self, query):
        return user_mock_without_stories_or_friends

    def mocked_flash_insert_one(self, query):
        return object_id_mock

    def test_save_new_flash_successful(self):
        with patch.object(Flash, "_insert_one") as mocked_insert:
            mocked_insert.side_effect = self.mocked_flash_insert_one

            flash_data_mock = flash_data_mock_with_title_and_description
            flash_data_mock['username'] = 'pepito'
            expected_output = object_id_mock

            self.assertEqual(Flash.save_new(flash_data_mock), expected_output)
