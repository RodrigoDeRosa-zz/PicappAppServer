from src.persistance.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument
from src.model.story_comment import StoryComment
from bson.objectid import ObjectId
from src.model.story_reaction_types import *


class StoryNotFoundException(Exception):
    def __init__(self):
        self.message = "Story was not found"
        self.error_code = 404


class StoryReactionNotFoundException(Exception):
    def __init__(self):
        self.message = "Story reaction was not found"
        self.error_code = 404


class Story(object):

    @staticmethod
    def _get_stories_db():
        return mongo.db.stories

    @staticmethod
    def _get_all():
        Logger(__name__).info('Retrieving all stories.')
        return Story._get_stories_db().find()

    @staticmethod
    def _get_one(query):
        Logger(__name__).info('Retrieving story with query {}.'.format(query))
        return Story._get_stories_db().find_one(query)

    @staticmethod
    def _get_one_by_id(story_id):
        return Story._get_one({'_id': ObjectId(story_id)})

    @staticmethod
    def _get_many(query):
        Logger(__name__).info('Retrieving all stories matching query {}.'.format(query))
        return Story._get_stories_db().find(query)

    @staticmethod
    def _insert_one(new_story):
        Logger(__name__).info('Inserting story with query {}.'.format(new_story))
        return Story._get_stories_db().insert(new_story)

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all stories.')
        return Story._get_stories_db().delete_many({})

    @staticmethod
    def _update_story(story_id, updated_param_dict):
        Logger(__name__).info('Updating story {} with value {}'.format(story_id, updated_param_dict))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"$set": updated_param_dict},
                                                    return_document=ReturnDocument.AFTER)

    @staticmethod
    def _add_item_to_story(story_id, pushed_param_dict):
        Logger(__name__).info('Pushing to story {} with value {}'.format(story_id, pushed_param_dict))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"$push": pushed_param_dict},
                                                    return_document=ReturnDocument.AFTER)

    @staticmethod
    def _delete_one(story_id):
        Logger(__name__).info('Deleting story {}.'.format(story_id))
        return Story._get_stories_db().find_one_and_delete({'_id': ObjectId(story_id)})

    @staticmethod
    def _delete_field_on_story(story_id, deleted_field_dict):
        Logger(__name__).info('Deleting field {} on story {}'.format(deleted_field_dict, story_id))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"$unset": deleted_field_dict})

    @staticmethod
    def _pull_array_item_from_story(story_id, pulled_field_dict):
        Logger(__name__).info('Pulling array item {} from story {}'.format(pulled_field_dict, story_id))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"$pull": pulled_field_dict},
                                                    return_document=ReturnDocument.AFTER)

    @staticmethod
    def _make_new_story(new_story_data):
        new_story = {}
        # define the required fields
        required_fields = ['username', 'timestamp', 'is_private', 'location', 'media']
        optional_fields = ['title', 'description']
        default_optional_values = {'title': "", 'description': ""}

        # ASSERTION
        for field in optional_fields:
            assert field in default_optional_values
        # end ASSERTION

        for field in required_fields:
            assert(field in new_story_data)
            new_story[field] = new_story_data[field]

        for field in optional_fields:
            field_value = default_optional_values[field]
            if field in new_story_data:
                field_value = new_story_data[field]
            new_story[field] = field_value

        # init the blank ones
        new_story['reactions'] = {}
        new_story['comments'] = []

        # return the new profile
        return new_story

    @staticmethod
    def save_new(story_data):
        """Saves a new story from story_data containing [username,] and returns its _id identifier"""
        # aux username reference
        username = story_data['username']

        # create new story
        new_story = Story._make_new_story(story_data)

        # save into DB
        new_story_id_obj = Story._insert_one(new_story)
        new_story_id = str(new_story_id_obj)

        Logger(__name__).info('New story {} by user {} was saved.'.format(new_story_id,
                                                                          username))

        # return the id
        return new_story_id

    @staticmethod
    def get_story(story_id):
        """Get story represented by story_id formatted to be JSON serializable, or raise
         StoryNotFound exception if no story was found"""
        Logger(__name__).info('Looking for story {}.'.format(story_id))
        story = Story._get_one_by_id(story_id)
        if story is None:
            raise StoryNotFoundException
        return Story._serialize_story(story)

    @staticmethod
    def _serialize_story(story_obj):
        # _make_new_story can be abused to make a new dict from an obj rather than data
        serialized = Story._make_new_story(story_obj)

        # patch booleans
        for k, v in serialized.items():
            if k in ['is_private']:
                serialized[k] = "true" if v else "false"

        # story_id
        story_id = str(story_obj['_id'])
        serialized["story_id"] = story_id

        # reactions
        serialized["reactions"] = story_obj["reactions"]

        # comments
        serialized["comments"] = StoryComment.get_comments_on_story(story_id)

        Logger(__name__).debug("Serialized story retrieved is {}".format(serialized))
        return serialized

    @staticmethod
    def react_to_story(story_id, username, sanitized_reaction):
        """React to story represented by story_id as username, with reaction 'reaction'"""
        if Story._get_one_by_id(story_id) is None:
            raise StoryNotFoundException
        updated_story = Story._update_story(story_id, {"reactions."+username: sanitized_reaction})
        Logger(__name__).info("User {} has reacted {} to Story_id {}.".format(username, sanitized_reaction, story_id))
        return updated_story["reactions"][username]

    @staticmethod
    def delete_reaction(story_id, username):
        """Delete username's reaction on the story represented by story_id."""
        Logger(__name__).info('Deleting reaction from user {} on story {}.'.format(username, story_id))
        updated_story = Story._delete_field_on_story(story_id, {"reactions."+username: ""})
        if updated_story is None:
            raise StoryReactionNotFoundException
        return updated_story["reactions"][username]

    @staticmethod
    def comment_on_story(story_id, username, comment_text, timestamp):
        """Comment on a story represented by story_id as username, with comment_text and at timestamp."""
        Logger(__name__).info('Trying to set comment from user {} on story {} at timestamp {}.'.format(
            username, story_id, timestamp))
        if Story._get_one_by_id(story_id) is None:
            raise StoryNotFoundException
        new_comment_id = StoryComment.make_new_comment(comment_text, username, timestamp, story_id)
        return StoryComment.get_comment(new_comment_id)

    @staticmethod
    def delete_story(story_id):
        """Delete a story and its reactions and comments."""
        Logger(__name__).info("Deleting story_id {}.".format(story_id))
        deleted_story_id = Story._safe_delete_story(story_id)
        return deleted_story_id

    @staticmethod
    def _safe_delete_story(story_id):
        # delete reactions and comments, and possible links to them
        StoryComment.delete_comments_on_story(story_id)

        # delete the story itself
        deleted_story = Story._delete_one(story_id)
        if deleted_story is None:
            raise StoryNotFoundException

        return deleted_story['_id']

    @staticmethod
    def delete_stories_from_user(username):
        """Safely delete all stories uploaded by username and return a list of their ids"""
        Logger(__name__).info("Deleting all stories from user {}.".format(username))
        story_ids = [str(story_obj['_id']) for story_obj in Story._get_many({'username': username})]

        deleted_ids = []
        for story_id in story_ids:
            deleted_ids.append(Story._safe_delete_story(story_id))

        return deleted_ids

    @staticmethod
    def get_stories_by_username(username, include_privates=True):
        """Get all stories uploaded by username, sorted by timestamp in descending order"""
        Logger(__name__).info('Getting all stories from user {}.'.format(username))
        # get all stories matching username
        serialized_stories = [Story._serialize_story(story_obj) for
                              story_obj in Story._get_many({'username': username})]

        # if not include_privates, take them out
        if not include_privates:
            serialized_stories = [story for story in serialized_stories if story["is_private"] == "false"]

        # sort inplace in descending order by timestamp
        serialized_stories.sort(key=lambda srz_story: srz_story["timestamp"], reverse=True)

        # return sorted list
        return serialized_stories

    @staticmethod
    def get_stories_feed_data_by_username(username, include_privates=True):
        """Get all stories uploaded by username, formatted for easier use of Feed Builder"""
        # get all stories matching username
        Logger(__name__).info('Getting feed data from stories for user {}.'.format(username))
        story_feed_blocks = [Story._get_feed_story_data(story_obj) for
                             story_obj in Story._get_many({'username': username})]

        # if not include_privates, take them out
        if not include_privates:
            story_feed_blocks = [block for block in story_feed_blocks if not block["is_private"]]

        return story_feed_blocks

    @staticmethod
    def _get_feed_story_data(story_obj):
        reactions = [reaction for reaction in story_obj["reactions"].values()]
        comments = StoryComment.get_comments_on_story(str(story_obj['_id']))
        return {
            "story_id": str(story_obj['_id']),
            "title": story_obj['title'],
            "description": story_obj['description'],
            "likes": reactions.count(STORY_REACTION_LIKE),
            "dislikes": reactions.count(STORY_REACTION_DISLIKE),
            "funnies": reactions.count(STORY_REACTION_FUNNY),
            "borings": reactions.count(STORY_REACTION_BORING),
            "number of comments": len(comments),
            "location": story_obj['location'],
            "timestamp": story_obj['timestamp'],
            "is_private": story_obj['is_private'],
            "uploader": story_obj["username"]
        }
