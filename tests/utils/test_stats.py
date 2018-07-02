import unittest
from unittest.mock import patch, MagicMock

from src.utils.stats import StatCollector
from tests.mocks.object_id_mock import object_id_mock


class StatCollectorTestCase(unittest.TestCase):

    def setUp(self):
        self.fake_db = []

    def mock_insert(self, dicc):
        self.fake_db.append(dicc)
        return object_id_mock

    def mock_get_many(self, query):
        event_type = query["event"]
        return [dicc for dicc in self.fake_db if dicc["event"] == event_type]

    def test_save_story_post_returns_id(self):
        with patch.object(StatCollector, "_insert_into_db") as mocked_insert:

            mocked_insert.side_effect = self.mock_insert

            aux_timestamp = 192193239

            self.assertEqual(StatCollector.save_event_story_post(aux_timestamp), object_id_mock)

    def test_get_story_post_returns_1_elem(self):
        with patch.object(StatCollector, "_insert_into_db") as mocked_insert, \
             patch.object(StatCollector, "_get_many") as mocked_get_many:

            mocked_insert.side_effect = self.mock_insert
            mocked_get_many.side_effect = self.mock_get_many

            aux_timestamp = 192193239

            StatCollector.save_event_story_post(aux_timestamp)

            self.assertEqual(StatCollector.get_number_of_stories_posted(), [aux_timestamp])

    def test_get_flash_post_after_story_returns_empty(self):
        with patch.object(StatCollector, "_insert_into_db") as mocked_insert, \
             patch.object(StatCollector, "_get_many") as mocked_get_many:

            mocked_insert.side_effect = self.mock_insert
            mocked_get_many.side_effect = self.mock_get_many

            aux_timestamp = 192193239

            StatCollector.save_event_story_post(aux_timestamp)

            self.assertEqual(StatCollector.get_number_of_flashes_posted(), [])

    def test_get_friendship_post_after_2_posts_returns_2(self):
        with patch.object(StatCollector, "_insert_into_db") as mocked_insert, \
             patch.object(StatCollector, "_get_many") as mocked_get_many:

            mocked_insert.side_effect = self.mock_insert
            mocked_get_many.side_effect = self.mock_get_many

            aux_timestamp1 = 192193239
            aux_timestamp2 = 651453131

            StatCollector.save_event_friendship_request_sent(aux_timestamp1)
            StatCollector.save_event_friendship_request_sent(aux_timestamp2)

            self.assertEqual(StatCollector.get_number_of_friendship_requests_sent(),
                             [aux_timestamp1, aux_timestamp2])

    def test_get_flash_post_after_1_ok_2_other_returns_1(self):
        with patch.object(StatCollector, "_insert_into_db") as mocked_insert, \
             patch.object(StatCollector, "_get_many") as mocked_get_many:

            mocked_insert.side_effect = self.mock_insert
            mocked_get_many.side_effect = self.mock_get_many

            aux_timestamp_wrong1 = 192193239
            aux_timestamp_wrong2 = 651453131
            aux_timestamp_ok = 135431581

            StatCollector.save_event_friendship_request_sent(aux_timestamp_wrong1)
            StatCollector.save_event_flash_post(aux_timestamp_ok)
            StatCollector.save_event_story_post(aux_timestamp_wrong2)

            self.assertEqual(StatCollector.get_number_of_flashes_posted(), [aux_timestamp_ok])
