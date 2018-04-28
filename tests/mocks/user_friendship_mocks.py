# each of these variables is a dict of "source" and "target" users, with properties
# as specified in user_mock.py
from src.model.friendship import FriendshipState

users_mock_not_friends = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source",
                                     'stories': [], 'friends': {}, 'profile_pic': None},
                          'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target",
                                     'stories': [], 'friends': {}, 'profile_pic': None}}

users_mock_sent = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                              'friends': {"target": FriendshipState.request_sent},
                              'profile_pic': None},
                   'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                              'friends': {"source": FriendshipState.request_received},
                              'profile_pic': None}}

users_mock_received = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                                  'friends': {"target": FriendshipState.request_received},
                                  'profile_pic': None},
                       'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                                  'friends': {"source": FriendshipState.request_sent},
                                  'profile_pic': None}}

users_mock_friends = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                                 'friends': {"target": FriendshipState.friends},
                                 'profile_pic': None},
                      'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                                 'friends': {"source": FriendshipState.friends},
                                 'profile_pic': None}}