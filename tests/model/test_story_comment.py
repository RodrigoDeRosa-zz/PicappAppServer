import unittest
from unittest.mock import MagicMock, patch

from src.model.story_comment import StoryCommentNotFoundException, StoryComment
from tests.mocks.story_comment_mock import story_comment_mock, internal_story_comment_mock, \
    internal_story_comment_mock_post, internal_story_comment_mock_pre


class StoryCommentTestCase(unittest.TestCase):

    def test_successful_make_new_comment(self):
        with patch.object(StoryComment, "_insert_one") as mocked_insert_one:

            aux = dict(internal_story_comment_mock)
            aux_id = aux.pop("_id")
            mocked_insert_one.side_effect = MagicMock(return_value=aux_id)

            self.assertEqual(StoryComment.make_new_comment(aux["comment"], aux["username"], aux["timestamp"],
                                                           aux["story_id"]), aux_id)

    def test_successful_delete_comment(self):
        with patch.object(StoryComment, "_delete_one") as mocked_delete_one:

            aux = dict(internal_story_comment_mock)
            aux_id = aux["_id"]
            mocked_delete_one.side_effect = MagicMock(return_value=aux)

            self.assertEqual(StoryComment.delete_comment(aux_id), aux_id)

    def test_delete_comment_not_found(self):
        with patch.object(StoryComment, "_delete_one") as mocked_delete_one,\
             self.assertRaises(StoryCommentNotFoundException) as context:

            aux = dict(internal_story_comment_mock)
            aux_id = aux["_id"]
            mocked_delete_one.side_effect = MagicMock(return_value=None)

            StoryComment.delete_comment(aux_id)
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Story comment was not found")

    def test_successful_get_comment(self):
        with patch.object(StoryComment, "_get_one_by_id") as mocked_get_one:

            aux = dict(internal_story_comment_mock)
            aux_id = aux["_id"]
            mocked_get_one.side_effect = MagicMock(return_value=aux)

            self.assertEqual(StoryComment.get_comment(aux_id), story_comment_mock)

    def test_get_comment_not_found(self):
        with patch.object(StoryComment, "_get_one_by_id") as mocked_get_one,\
             self.assertRaises(StoryCommentNotFoundException) as context:

            aux = dict(internal_story_comment_mock)
            aux_id = aux["_id"]
            mocked_get_one.side_effect = MagicMock(return_value=None)

            StoryComment.get_comment(aux_id)
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Story comment was not found")

    def test_get_comments_on_story_in_correct_order(self):
        with patch.object(StoryComment, "_get_many") as mocked_get_many:
            aux = [internal_story_comment_mock, internal_story_comment_mock_post, internal_story_comment_mock_pre]
            mocked_get_many.side_effect = MagicMock(return_value=aux)

            expected_order = [internal_story_comment_mock_pre, internal_story_comment_mock, internal_story_comment_mock_post]
            expected = [{
                "timestamp": elem["timestamp"],
                "commenting_user_id": elem["username"],
                "comment": elem["comment"]
            } for elem in expected_order]

            story_id_mock = internal_story_comment_mock["story_id"]
            self.assertEqual(StoryComment.get_comments_on_story(story_id_mock), expected)
