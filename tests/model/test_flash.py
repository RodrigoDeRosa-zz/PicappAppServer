import unittest
from unittest.mock import MagicMock, patch

from src.model.flash import FlashNotFoundException, Flash, time
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.flash_data_mocks import flash_data_mock_with_title_and_description
from tests.mocks.flash_mock import flash_mock
from bson.objectid import ObjectId


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

    def test_get_flash_not_found(self):
        with patch.object(Flash, "_get_one_by_id") as mocked_flash_get, \
             self.assertRaises(FlashNotFoundException) as context:
            mocked_flash_get.side_effect = MagicMock(return_value=None)
            mocked_flash_id = object_id_mock

            Flash.get_flash(mocked_flash_id)

        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_get_flash_successful(self):
        with patch.object(Flash, "_get_one_by_id") as mocked_flash_get:

            internal_flash_mock = dict(flash_mock)
            internal_flash_mock['_id'] = ObjectId(internal_flash_mock.pop('flash_id'))
            expected_flash = flash_mock

            mocked_flash_get.side_effect = MagicMock(return_value=internal_flash_mock)

            self.assertEqual(Flash.get_flash('asd'), expected_flash)

    def test_successful_delete_flash(self):
        with patch.object(Flash, "_delete_one") as mocked_delete_one:

            mocked_internal_flash = dict(flash_mock)
            mocked_internal_flash["_id"] = ObjectId(mocked_internal_flash.pop('flash_id'))

            mocked_delete_one.side_effect = MagicMock(return_value=mocked_internal_flash)

            self.assertEqual(Flash.delete_flash(object_id_mock), object_id_mock)

    def test_delete_flash_not_found(self):
        with patch.object(Flash, "_delete_one") as mocked_delete_one,\
             self.assertRaises(FlashNotFoundException) as context:

            mocked_delete_one.side_effect = MagicMock(return_value=None)

            Flash.delete_flash(object_id_mock)
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Flash was not found")

    def test_get_deprecated_flash_raises_exception(self):
        with patch.object(Flash, "_get_one") as mocked_get_one, \
             patch.object(time, "time") as mocked_get_time, \
             self.assertRaises(FlashNotFoundException) as context:

            deprecating_timestamp = flash_mock['timestamp'] + 20000  # surely exceeds threshold
            mocked_get_time.side_effect = MagicMock(return_value=deprecating_timestamp)
            mocked_get_one.side_effect = MagicMock(return_value=flash_mock)

            Flash.get_flash(object_id_mock)

        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Flash was not found")

    def test_get_many_flashes_does_not_return_deprecated_ones(self):
        with patch.object(Flash, "_unsafe_get_many") as mocked_unsafe_get_many, \
             patch.object(time, "time") as mocked_get_time:

            not_deprecated_flash1 = dict(flash_mock)
            deprecated_flash1 = dict(flash_mock)
            deprecated_flash2 = dict(flash_mock)

            fake_now = not_deprecated_flash1['timestamp'] + 100  # just so that it is not timestamp

            deprecated_flash1['timestamp'] = fake_now - 30000000  # surely below threshold
            deprecated_flash2['timestamp'] = fake_now - 25000000  # surely below threshold

            all_flashes_from_username = [not_deprecated_flash1, deprecated_flash1, deprecated_flash2]

            mocked_get_time.side_effect = MagicMock(return_value=fake_now / 1000)  # fake seconds instead of milli
            mocked_unsafe_get_many.side_effect = MagicMock(return_value=all_flashes_from_username)

            self.assertEqual(Flash._get_many({"some": "query"}), [not_deprecated_flash1])
