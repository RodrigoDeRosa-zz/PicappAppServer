import unittest
import unittest.mock as mock

from src.security.token import Token, ExpiredTokenException
from tests.mocks.token_mock import token_mock
from tests.mocks.user_friendship_mocks import users_mock_not_friends, users_mock_received, users_mock_friends
from src.resources.friendship import FriendshipResource
from src.utils.response_builder import ResponseBuilder
from src.model.user import User
from src.model.friendship import Friendship, UserNotFoundException, AlreadyFriendsException, FriendshipState


class FriendshipResourceTestCase(unittest.TestCase):

    def test_send_friendship_request(self):
        src_usr = dict(users_mock_not_friends['source'])
        tgt_usr = dict(users_mock_not_friends['target'])
        service = FriendshipResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(return_value=src_usr['username'])
        User._get_one = lambda query: users_mock_not_friends[query['username']]
        ResponseBuilder.build_response = lambda output, status_code=200: output
        self.assertEqual(service.post(tgt_usr['username'])['target_user_id'], tgt_usr['username'])
        self.assertEqual(src_usr['friends']['target'], FriendshipState.request_sent)
        self.assertEqual(tgt_usr['friends']['source'], FriendshipState.request_received)

    def test_confirm_friendship_request(self):
        src_usr = dict(users_mock_received['source'])
        tgt_usr = dict(users_mock_received['target'])
        service = FriendshipResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(return_value=src_usr['username'])
        User._get_one = lambda query: users_mock_received[query['username']]
        ResponseBuilder.build_response = lambda output, status_code=200: output
        self.assertEqual(service.post(tgt_usr['username'])['target_user_id'], tgt_usr['username'])
        self.assertEqual(src_usr['friends']['target'], FriendshipState.friends)
        self.assertEqual(tgt_usr['friends']['source'], FriendshipState.friends)

    def test_already_friends(self):
        src_usr = dict(users_mock_friends['source'])
        tgt_usr = dict(users_mock_friends['target'])
        service = FriendshipResource()
        service._get_token_from_header = mock.MagicMock(return_value=token_mock)
        Token.identify = mock.MagicMock(return_value=src_usr['username'])
        User._get_one = lambda query: users_mock_friends[query['username']]
        ResponseBuilder.build_response = lambda output, status_code: status_code
        self.assertEqual(service.post(tgt_usr['username']), 400)
        self.assertEqual(src_usr['friends']['target'], FriendshipState.friends)
        self.assertEqual(tgt_usr['friends']['source'], FriendshipState.friends)
