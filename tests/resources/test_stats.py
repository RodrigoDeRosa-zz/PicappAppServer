import unittest
from unittest.mock import MagicMock, patch

from src.resources.stats import *


class StatsResourceTestCase(unittest.TestCase):

    def mocked_build_response(self, output, status_code=200):
        return output

    def test_get_stats_formatted_ok(self):
        with patch.object(StatCollector, "get_number_of_stories_posted") as mocked_get_stories_posted, \
             patch.object(StatCollector, "get_number_of_flashes_posted") as mocked_get_flashes_posted, \
             patch.object(StatCollector, "get_number_of_friendship_requests_sent") as \
                     mocked_get_friend_requests_posted, \
             patch.object(ResponseBuilder, "build_response") as mocked_respond,\
             patch.object(StatCollector, "get_number_of_error_responses") as mocked_get_error_responses:

            # not checking format of elements
            mock_number_of_stories = [1835135]
            mock_number_of_flashes = []
            mock_number_of_friend_requests = [132132, 132153, 12315351, 12312312]
            mock_number_of_error_responses = [1321536851, 455456455256]

            mocked_get_flashes_posted.side_effect = MagicMock(return_value=mock_number_of_flashes)
            mocked_get_stories_posted.side_effect = MagicMock(return_value=mock_number_of_stories)
            mocked_get_friend_requests_posted.side_effect = MagicMock(return_value=mock_number_of_friend_requests)
            mocked_get_error_responses.side_effect = MagicMock(return_value=mock_number_of_error_responses)
            mocked_respond.side_effect = self.mocked_build_response

            expected_output = {
                STORIES_POSTED_TAG: mock_number_of_stories,
                FLASHES_POSTED_TAG: mock_number_of_flashes,
                FRIENDSHIP_REQUESTS_SENT_TAG: mock_number_of_friend_requests,
                ERROR_RESPONSES_TAG: mock_number_of_error_responses
            }

            service = StatsResource()

            self.assertEqual(service.get(), expected_output)
