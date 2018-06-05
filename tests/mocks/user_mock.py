# complies with Users stored in AppServer DB
# Has:
# _id
# username
# friends
# profile_pic
# name

user_mock_without_stories_or_friends = {'_id': '5ad79a63a8817419a237e671', 'username': "Maxi",
                                        'friends': [], 'profile_pic': None, 'name': "Maxi"}

account_info_mock_without_stories_or_friends = {'username': "Maxi", 'profile_pic': None, 'name': "Maxi"}

profile_mock_without_stories_or_friends = {'username': "Maxi", 'number of stories': 0,
                                           'number of friends': 0, 'profile_pic': None, 'name': "Maxi",
                                           'stories': []}