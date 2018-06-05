from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId


class StoryCommentNotFoundException(Exception):
    def __init__(self):
        self.message = "Story comment was not found"
        self.error_code = 404


class StoryComment(object):

    @staticmethod
    def _get_comments_db():
        return mongo.db.story_comments

    @staticmethod
    def _get_all():
        Logger(__name__).info('Retrieving all story comments.')
        return StoryComment._get_comments_db().find()

    @staticmethod
    def _get_many(query):
        Logger(__name__).info('Retrieving all story comments matching query {}.'.format(query))
        return StoryComment._get_comments_db().find(query)

    @staticmethod
    def _get_one(query):
        Logger(__name__).info('Retrieving story comment with query {}.'.format(query))
        return StoryComment._get_comments_db().find_one(query)

    @staticmethod
    def _get_one_by_id(comment_id):
        return StoryComment._get_one({'_id': ObjectId(comment_id)})

    @staticmethod
    def _insert_one(new_comment):
        Logger(__name__).info('Inserting story comment with query {}.'.format(new_comment))
        return StoryComment._get_comments_db().insert(new_comment)

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all story comments.')
        return StoryComment._get_comments_db().delete_many({})

    @staticmethod
    def _delete_many(query):
        Logger(__name__).info('Deleting all story comments matching query {}.'.format(query))
        return StoryComment._get_comments_db().delete_many(query)

    @staticmethod
    def _update_story(comment_id, updated_param_dict):
        Logger(__name__).info('Updating story comment {} with value {}'.format(comment_id, updated_param_dict))
        return mongo.db.story_comments.find_one_and_update(filter={'_id': ObjectId(comment_id)},
                                                           update={"$set": updated_param_dict},
                                                           return_document=ReturnDocument.AFTER)

    @staticmethod
    def _add_item_to_story(comment_id, pushed_param_dict):
        Logger(__name__).info('Pushing to story comment {} with value {}'.format(comment_id, pushed_param_dict))
        return mongo.db.story_comments.find_one_and_update(filter={'_id': ObjectId(comment_id)},
                                                           update={"$push": pushed_param_dict},
                                                           return_document=ReturnDocument.AFTER)

    @staticmethod
    def _delete_one(comment_id):
        Logger(__name__).info('Deleting story comment {}.'.format(comment_id))
        return StoryComment._get_comments_db().find_one_and_delete({'_id': comment_id})

    @staticmethod
    def _delete_field_on_story(comment_id, deleted_field_dict):
        Logger(__name__).info('Deleting field {} on story comment {}'.format(deleted_field_dict, comment_id))
        return mongo.db.story_comments.find_one_and_update(filter={'_id': ObjectId(comment_id)},
                                                           update={"$unset": deleted_field_dict})

    @staticmethod
    def _pull_array_item_from_story(comment_id, pulled_field_dict):
        Logger(__name__).info('Pulling array item {} from story comment {}'.format(pulled_field_dict, comment_id))
        return mongo.db.story_comments.find_one_and_update(filter={'_id': ObjectId(comment_id)},
                                                           update={"$pull": pulled_field_dict},
                                                           return_document=ReturnDocument.AFTER)

    @staticmethod
    def _make_new(text, username, timestamp, story_id):
        return {
            "comment": text,
            "username": username,
            "timestamp": timestamp,
            "story_id": story_id
        }

    @staticmethod
    def make_new_comment(comment_text, username, timestamp, story_id):
        """Generate a comment from username on story_id with comment_text and timestamp."""
        # make new comment structure
        new_comment = StoryComment._make_new(comment_text, username, timestamp, story_id)

        # save it to DB
        new_comment_obj = StoryComment._insert_one(new_comment)
        new_comment_id = str(new_comment_obj)

        # log it
        Logger(__name__).info('New comment {} on story {} by user {} was saved.'.format(new_comment_id,
                                                                                        story_id,
                                                                                        username))
        # return the id
        return new_comment_id

    @staticmethod
    def delete_comment(comment_id):
        """Delete the comment identified by comment_id."""
        deleted_comment = StoryComment._delete_one(comment_id)
        if deleted_comment is None:
            raise StoryCommentNotFoundException
        return deleted_comment['_id']

    @staticmethod
    def get_comment(comment_id):
        """Get comment identified by comment_id or raise StoryCommentNotFoundException if none
        was found."""
        comment_obj = StoryComment._get_one_by_id(comment_id)
        if comment_obj is None:
            raise StoryCommentNotFoundException
        return StoryComment._serialize_comment(comment_obj)

    @staticmethod
    def _serialize_comment(comment_obj):
        return {"timestamp": comment_obj["timestamp"], "commenting_user_id": comment_obj["username"],
                "comment": comment_obj["comment"]}

    @staticmethod
    def get_comments_on_story(story_id):
        """Get all comments for story_id, sorted by timestamp in ascending order."""
        # get all comments matching story_id
        serialized_comments = [StoryComment._serialize_comment(comment_obj) for
                               comment_obj in StoryComment._get_many({'story_id': story_id})]

        # sort inplace in ascending order by timestamp
        serialized_comments.sort(key=lambda srz_comment: srz_comment["timestamp"])

        # return sorted list
        return serialized_comments

    @staticmethod
    def delete_comments_on_story(story_id):
        """Delete all comments on story_id"""
        StoryComment._delete_many({'story_id': story_id})

