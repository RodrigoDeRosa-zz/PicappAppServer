# complies with Users stored in AppServer DB
# Has:
# _id
# username
# friends
# profile_pic
# name
from src.model.friendship import FRIENDSHIP_STATE_FRIENDS, FRIENDSHIP_STATE_RECEIVED, FRIENDSHIP_STATE_SENT

user_mock_without_stories_or_friends = {'_id': '5ad79a63a8817419a237e671', 'username': "Maxi",
                                        'friends': {}, 'profile_pic': None, 'name': "Maxi"}

account_info_mock_without_stories_or_friends = {'username': "Maxi", 'profile_pic': None, 'name': "Maxi"}

profile_mock_without_stories_or_friends = {'username': "Maxi", 'number of stories': 0,
                                           'number of friends': 0, 'profile_pic': None, 'name': "Maxi",
                                           'stories': []}

user_mock_without_stories_with_friends = {'_id': '5ad79a63a8817419a237e671', 'username': "Maxi",
                                          'friends': {
                                            'friend_id1': FRIENDSHIP_STATE_FRIENDS,
                                            'friend_id2': FRIENDSHIP_STATE_FRIENDS,
                                            'not_friend_id1': FRIENDSHIP_STATE_RECEIVED,
                                            'not_friend_id2': FRIENDSHIP_STATE_SENT},
                                          'profile_pic': None, 'name': "Maxi"}