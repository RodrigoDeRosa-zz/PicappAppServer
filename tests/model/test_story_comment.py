import unittest
from unittest.mock import MagicMock, patch

from src.model.story_comment import StoryCommentNotFoundException, StoryComment
from tests.mocks.story_comment_mock import story_comment_mock, internal_story_comment_mock


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
            mocked_delete_one.side_effect = MagicMock(side_effect=StoryCommentNotFoundException)

            StoryComment.delete_comment(aux_id)
        exc = context.exception
        self.assertEqual(exc.error_code, 404)
        self.assertEqual(exc.message, "Story comment was not found")
