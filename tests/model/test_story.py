import unittest
from unittest.mock import MagicMock, patch

from src.model.story import Story, StoryNotFoundException, StoryReactionNotFoundException, StoryComment, Persistence

from tests.mocks.user_mock import user_mock_without_stories_or_friends
from tests.mocks.object_id_mock import object_id_mock
from tests.mocks.story_data_mock import story_data_mock_with_title_and_description
from tests.mocks.story_mock import *


def first_item_of_dict(dicc):
    return [(k, v) for k, v in dicc.items()][0]


class StoryTestCase(unittest.TestCase):

    def setUp(self):
        self.original_get_coll = Story._get_coll
        Story._get_coll = MagicMock(return_value="asd")

    def tearDown(self):
        Story._get_coll = self.original_get_coll

    def mocked_user_get_one(self, coll, query):
        return user_mock_without_stories_or_friends

    def mocked_story_insert_one(self, coll, query):
        return object_id_mock

    def test_successful_save_new(self):
        with patch.object(Persistence, "insert_one") as mocked_story_insert:
            mocked_story_insert.side_effect = self.mocked_story_insert_one

            story_data = dict(story_data_mock_with_title_and_description)
            story_data['username'] = "pedro"

            self.assertEqual(Story.save_new(story_data), object_id_mock)

    def test_get_story_not_found(self):
        with patch.object(Persistence, "get_one") as mocked_story_get, \
             self.assertRaises(StoryNotFoundException) as context:

            mocked_story_get.side_effect = MagicMock(return_value=None)

            mocked_story_id = object_id_mock

            Story.get_story(mocked_story_id)

        exc = context.exception
        self.assertEqual(exc.error_code, 404)

    def test_successful_get_story_public(self):
        with patch.object(Persistence, "get_one") as mocked_story_get,\
             patch.object(StoryComment, "get_comments_on_story") as mocked_get_comments:
            # prepare special mock
            aux = story_mock_public_without_comments_or_reactions
            internal_story_mock = dict(aux)
            internal_story_mock["is_private"] = False
            internal_story_mock["timestamp"] = 1615456
            internal_story_mock["_id"] = aux['story_id']

            mocked_story_get.side_effect = MagicMock(return_value=internal_story_mock)
            mocked_story_id = aux['story_id']
            mocked_get_comments.side_effect = MagicMock(return_value=[])

            self.assertEqual(Story.get_story(mocked_story_id), aux)

    def test_successful_get_story_private(self):
        with patch.object(Persistence, "get_one") as mocked_story_get,\
             patch.object(StoryComment, "get_comments_on_story") as mocked_get_comments:
            # prepare special mock
            aux = story_mock_private_without_comments_or_reactions
            internal_story_mock = dict(aux)
            internal_story_mock["is_private"] = True
            internal_story_mock["timestamp"] = 1615456
            internal_story_mock["_id"] = aux['story_id']

            mocked_story_get.side_effect = MagicMock(return_value=internal_story_mock)
            mocked_story_id = aux['story_id']
            mocked_get_comments.side_effect = MagicMock(return_value=[])

            self.assertEqual(Story.get_story(mocked_story_id), aux)

    def test_successful_post_reaction(self):
        with patch.object(Persistence, "update_one") as mocked_story_update,\
             patch.object(Persistence, "get_one") as mocked_get_one:
            aux = story_mock_private_with_reaction.copy()
            mocked_story_update.side_effect = MagicMock(return_value=story_mock_private_with_reaction)
            mocked_get_one.side_effect = MagicMock(
                return_value=object_id_mock)  # just a placeholder, not what it's actually expected

            mocked_story_id = object_id_mock
            mocked_username, mocked_reaction = first_item_of_dict(aux["reactions"])

            self.assertEqual(Story.react_to_story(mocked_story_id, mocked_username, mocked_reaction),
                             mocked_reaction)

    def test_successful_delete_reaction(self):
        with patch.object(Persistence, "unset_on_one") as mocked_delete_reaction:
            mocked_delete_reaction.side_effect = MagicMock(return_value=story_mock_private_with_reaction)

            mocked_username, mocked_reaction = first_item_of_dict(story_mock_private_with_reaction["reactions"])

            self.assertEqual(Story.delete_reaction(object_id_mock, mocked_username), mocked_reaction)

    def test_delete_reaction_not_found(self):
        with patch.object(Persistence, "unset_on_one") as mocked_delete_reaction,\
             self.assertRaises(StoryReactionNotFoundException) as context:
            mocked_delete_reaction.side_effect = MagicMock(return_value=None)

            Story.delete_reaction(object_id_mock, "pedro")
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Story reaction was not found")

    def test_successful_delete_story(self):
        with patch.object(Persistence, "delete_one") as mocked_delete_one,\
             patch.object(StoryComment, "delete_comments_on_story") as mocked_delete_comments:

            mocked_internal_story = dict(story_mock_private_with_reaction)
            mocked_internal_story["_id"] = object_id_mock

            mocked_delete_one.side_effect = MagicMock(return_value=mocked_internal_story)
            mocked_delete_comments.side_effect = MagicMock()  # do nothing

            self.assertEqual(Story.delete_story(object_id_mock), object_id_mock)

    def test_delete_story_not_found(self):
        with patch.object(Persistence, "delete_one") as mocked_delete_one,\
             self.assertRaises(StoryNotFoundException) as context,\
             patch.object(StoryComment, "delete_comments_on_story") as mocked_delete_comments:

            mocked_internal_story = dict(story_mock_private_with_reaction)
            mocked_internal_story["_id"] = object_id_mock

            mocked_delete_one.side_effect = MagicMock(return_value=None)
            mocked_delete_comments.side_effect = MagicMock()  # do nothing

            Story.delete_story(object_id_mock)
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Story was not found")

    def test_get_stories_by_username_empty(self):
        with patch.object(Persistence, "get_many") as mocked_get_many:
            mocked_get_many.side_effect = MagicMock(return_value=[])

            self.assertEqual(Story.get_stories_by_username("pepe"), [])

    def test_get_stories_by_username_not_empty(self):
        with patch.object(Persistence, "get_many") as mocked_get_many,\
             patch.object(StoryComment, "get_comments_on_story") as mocked_get_comments,\
             patch.object(Story, "_serialize_story") as mocked_serialize:

            aux_timestamp = 123123
            aux_story1 = dict(story_mock_private_with_reaction)
            aux_story1["timestamp"] = aux_timestamp
            aux_story1["_id"] = object_id_mock

            aux_story2 = dict(aux_story1)
            aux_story2["timestamp"] = aux_timestamp + 1

            aux_story3 = dict(aux_story1)
            aux_story3["timestamp"] = aux_timestamp + 2

            unsorted_stories = [aux_story1, aux_story3, aux_story2]
            sorted_stories = [aux_story3, aux_story2, aux_story1]

            mocked_get_many.side_effect = MagicMock(return_value=unsorted_stories)
            mocked_get_comments.side_effect = MagicMock(return_value=[])
            mocked_serialize.side_effect = lambda x: x

            self.assertEqual(Story.get_stories_by_username("pepe"), sorted_stories)

    def test_get_feed_data_from_one_story_object(self):
        with patch.object(StoryComment, "get_comments_on_story") as mocked_get_comments:
            mocked_get_comments.side_effect = MagicMock(return_value=[])

            aux_story = dict(story_mock_private_with_reaction)
            aux_story["_id"] = object_id_mock

            reactions = [x for x in aux_story["reactions"].values()]

            expected_feed_data = {
                "story_id": object_id_mock,
                "title": aux_story['title'],
                "description": aux_story['description'],
                "likes": reactions.count(STORY_REACTION_LIKE),
                "dislikes": reactions.count(STORY_REACTION_DISLIKE),
                "funnies": reactions.count(STORY_REACTION_FUNNY),
                "borings": reactions.count(STORY_REACTION_BORING),
                "number of comments": len(aux_story['comments']),
                "location": aux_story['location'],
                "timestamp": aux_story['timestamp'],
                "is_private": aux_story['is_private'],
                "uploader": aux_story["username"]
            }

            self.assertEqual(Story._get_feed_story_data(aux_story), expected_feed_data)
