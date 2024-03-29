from src.model.story_reaction_types import *

story_mock_public_without_comments_or_reactions = {'media': "some_uri",
                                                   'location': "some_magic_maps_location",
                                                   'timestamp': 1615456,
                                                   'title': "some title",
                                                   'is_private': "false",
                                                   'description': "some description",
                                                   'comments': [],
                                                   'username': "martin.errazquin",
                                                   'reactions': {},
                                                   'story_id': '537eed02ed345b2e039652d2'}

story_mock_private_without_comments_or_reactions = {'media': "some_uri",
                                                    'location': "some_magic_maps_location",
                                                    'timestamp': 1615456,
                                                    'title': "some title",
                                                    'is_private': "true",
                                                    'description': "some description",
                                                    'username': "martin.errazquin",
                                                    'comments': [],
                                                    'reactions': {},
                                                    'story_id': '537eed02ed345b2e039652d2'}

story_mock_private_with_reaction = {'media': "some_uri",
                                    'location': "some_magic_maps_location",
                                    'timestamp': 1615456,
                                    'title': "some title",
                                    'is_private': "true",
                                    'description': "some description",
                                    'username': "martin.errazquin",
                                    'comments': [],
                                    'reactions': {
                                        "fercho.steel": STORY_REACTION_BORING
                                    },
                                    'story_id': '537eed02ed345b2e039652d2'}
