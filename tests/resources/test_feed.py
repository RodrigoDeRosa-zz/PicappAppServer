import unittest
from unittest.mock import patch, MagicMock

from src.security.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from src.resources.feed import FeedResource, FeedBuilder
from src.utils.response_builder import ResponseBuilder
from src.model.friendship import Friendship, UserNotFoundException, AlreadyFriendsException, FRIENDSHIP_STATE_SENT, FRIENDSHIP_STATE_RECEIVED, FRIENDSHIP_STATE_FRIENDS, NotFriendsException
from src.utils.request_builder import RequestBuilder, MissingFieldException


class FeedResourceTestCase(unittest.TestCase):

    def mocked_identify(self, token):
        return

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_feed_missing_field(self):
        with patch.object(FeedBuilder, "get_feed_for_username") as mocked_get_feed, \
             patch.object(ResponseBuilder, "build_response") as mocked_response_build:
            mocked_response_build.side_effect = self.mocked_build_error_response

            mocked_get_feed.side_effect = MagicMock(return_value=[])

            service = FeedResource()
            service._get_token_from_header = MagicMock(side_effect=MissingFieldException("token"))

            self.assertEqual(service.get(), 400)

    def test_feed_get_not_empty(self):
        with patch.object(FeedBuilder, "get_feed_for_username") as mocked_get_feed, \
             patch.object(ResponseBuilder, "build_response") as mocked_response_build,\
             patch.object(Token, "identify") as mocked_token_identify:
            mocked_response_build.side_effect = self.mocked_build_response
            mocked_token_identify.side_effect = self.mocked_identify

            aux = ["story1", "story2", "story3"]  # just testing the list is returned, not the format
            mocked_get_feed.side_effect = MagicMock(return_value=aux)

            service = FeedResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get()["stories"], aux)
