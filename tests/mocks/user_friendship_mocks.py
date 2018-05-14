# each of these variables is a dict of "source" and "target" users, with properties
# as specified in user_mock.py
from src.model.friendship import FRIENDSHIP_STATE_FRIENDS, FRIENDSHIP_STATE_RECEIVED, FRIENDSHIP_STATE_SENT

users_mock_not_friends = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source",
                                     'stories': [], 'friends': {}, 'profile_pic': None},
                          'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target",
                                     'stories': [], 'friends': {}, 'profile_pic': None}}

users_mock_sent = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                              'friends': {"target": FRIENDSHIP_STATE_SENT},
                              'profile_pic': None},
                   'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                              'friends': {"source": FRIENDSHIP_STATE_RECEIVED},
                              'profile_pic': None}}

users_mock_received = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                                  'friends': {"target": FRIENDSHIP_STATE_RECEIVED},
                                  'profile_pic': None},
                       'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                                  'friends': {"source": FRIENDSHIP_STATE_SENT},
                                  'profile_pic': None}}

users_mock_friends = {'source': {'_id': '5ad79a63a8817419a237e688', 'username': "source", 'stories': [],
                                 'friends': {"target": FRIENDSHIP_STATE_FRIENDS},
                                 'profile_pic': None},
                      'target': {'_id': '5ad79a63a8817419a237e689', 'username': "target", 'stories': [],
                                 'friends': {"source": FRIENDSHIP_STATE_FRIENDS},
                                 'profile_pic': None}}