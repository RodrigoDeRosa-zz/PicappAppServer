import unittest
from unittest.mock import patch, MagicMock

from src.security.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from tests.mocks.user_friendship_mocks import users_mock_not_friends, users_mock_received, users_mock_friends, users_mock_sent
from src.resources.friendship import FriendshipResource, StatCollector
from src.utils.response_builder import ResponseBuilder
from src.model.friendship import Friendship, UserNotFoundException, AlreadyFriendsException, FRIENDSHIP_STATE_SENT, \
    FRIENDSHIP_STATE_RECEIVED, FRIENDSHIP_STATE_FRIENDS, NotFriendsException, FRIENDSHIP_STATE_NOT_FRIENDS


class FriendshipResourceTestCase(unittest.TestCase):

    def mocked_successful_wants_to_be_friends_with(self, source_username, target_username):
        return users_mock_not_friends['target']['username']

    def mocked_successful_wants_to_not_be_friends_with(self, source_username, target_username):
        return users_mock_not_friends['target']['username']

    def mocked_identify(self, token):
        return users_mock_not_friends['source']['username']

    def mocked_build_response(self, output, status_code=200):
        return output

    def mocked_build_error_response(self, output, status_code):
        return status_code

    def test_send_friendship_request_successful(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'wants_to_be_friends_with') as mocked_friendship,\
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder,\
             patch.object(StatCollector,"save_event_friendship_request_sent") as mocked_stats:

            mocked_token.side_effect = self.mocked_identify
            mocked_friendship.side_effect = self.mocked_successful_wants_to_be_friends_with
            mocked_response_builder.side_effect = self.mocked_build_response
            mocked_stats.side_effect = MagicMock(return_value="asdads")  # don't care about return value

            src_usr = dict(users_mock_not_friends['source'])
            tgt_usr = dict(users_mock_not_friends['target'])

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])

            self.assertEqual(service.post(tgt_usr['username'])['target_user_id'], tgt_usr['username'])

    def test_send_friendship_request_already_friends(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'wants_to_be_friends_with') as mocked_friendship,\
             patch.object(ResponseBuilder, 'build_error_response') as mocked_response_builder, \
             patch.object(StatCollector, "save_event_friendship_request_sent") as mocked_stats:

            mocked_token.side_effect = self.mocked_identify
            mocked_friendship.side_effect = MagicMock(side_effect=AlreadyFriendsException)
            mocked_response_builder.side_effect = self.mocked_build_error_response
            mocked_stats.side_effect = MagicMock(return_value="asdads")  # don't care about return value

            src_usr = dict(users_mock_not_friends['source'])
            tgt_usr = dict(users_mock_not_friends['target'])

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock['token'])
            self.assertEqual(service.post(tgt_usr['username']), 400)

    def test_delete_friendship_successful(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'wants_to_not_be_friends_with') as mocked_friendship,\
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder:

            mocked_token.side_effect = self.mocked_identify
            mocked_friendship.side_effect = self.mocked_successful_wants_to_not_be_friends_with
            mocked_response_builder.side_effect = self.mocked_build_response

            src_usr = dict(users_mock_friends['source'])
            tgt_usr = dict(users_mock_friends['target'])

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.delete(tgt_usr['username'])['target_user_id'], tgt_usr['username'])

    def test_delete_friendship_not_friends(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'wants_to_not_be_friends_with') as mocked_friendship,\
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder:

            mocked_token.side_effect = self.mocked_identify
            mocked_friendship.side_effect = MagicMock(side_effect=NotFriendsException)
            mocked_response_builder.side_effect = self.mocked_build_error_response

            src_usr = dict(users_mock_friends['source'])
            tgt_usr = dict(users_mock_friends['target'])

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.delete(tgt_usr['username']), 400)

    def test_get_friendship_not_found(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'get_friendship_state_from_to') as mocked_get_friendship,\
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder:
            
            mocked_token.side_effect = self.mocked_identify
            mocked_get_friendship.side_effect = MagicMock(side_effect=UserNotFoundException)
            mocked_response_builder.side_effect = self.mocked_build_error_response

            src_usr = dict(users_mock_friends['source'])
            tgt_usr = dict(users_mock_friends['target'])

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(tgt_usr['username']), 404)

    def test_get_friendship_not_friends(self):
        with patch.object(Token, 'identify') as mocked_token,\
             patch.object(Friendship, 'get_friendship_state_from_to') as mocked_get_friendship,\
             patch.object(ResponseBuilder, 'build_response') as mocked_response_builder:

            src_usr = dict(users_mock_not_friends['source'])
            tgt_usr = dict(users_mock_not_friends['target'])

            expected_state = FRIENDSHIP_STATE_NOT_FRIENDS
            mocked_token.side_effect = self.mocked_identify
            mocked_get_friendship.side_effect = MagicMock(return_value=expected_state)
            mocked_response_builder.side_effect = self.mocked_build_response

            service = FriendshipResource()
            service._get_token_from_header = MagicMock(return_value=token_mock)

            self.assertEqual(service.get(tgt_usr['username'])["friendship_state"], expected_state)