from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument
from src.model.user import User, UserNotFoundException, _user
from bson.objectid import ObjectId


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
        return Story._get_stories_db().find_one_and_delete({'username': story_id})

    @staticmethod
    def _delete_field_on_story(story_id, deleted_field_dict):
        Logger(__name__).info('Deleting field {} on story {}'.format(deleted_field_dict, story_id))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"unset": deleted_field_dict})

    @staticmethod
    def _pull_array_item_from_story(story_id, pulled_field_dict):
        Logger(__name__).info('Pulling array item {} from story {}'.format(pulled_field_dict, story_id))
        return mongo.db.stories.find_one_and_update(filter={'_id': ObjectId(story_id)},
                                                    update={"pull": pulled_field_dict},
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
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException

        # create new story
        new_story = Story._make_new_story(story_data)

        # save into DB
        new_story_id_obj = Story._insert_one(new_story)
        new_story_id = str(new_story_id_obj)

        Logger(__name__).info('New story {} by user {} was saved.'.format(new_story_id,
                                                                          username))

        Story._add_story_id_to_user(username, new_story_id)

        Logger(__name__).info("Story_id {} was added to user {}.".format(new_story_id, username))

        # return the id
        return new_story_id

    @staticmethod
    def _add_story_id_to_user(username, story_id):
        # add it to the array
        # user['stories'].append(story_id)
        User._push_to_user_by_username(username, {'stories': story_id})

    @staticmethod
    def get_story(story_id):
        """Get story represented by story_id formatted to be JSON serializable, or raise
         StoryNotFound exception if no story was found"""
        story = Story._get_one_by_id(story_id)
        if story is None:
            raise StoryNotFoundException
        return Story._serialize_to_dict(story)

    @staticmethod
    def _serialize_to_dict(story_obj):
        # _make_new_story can be abused to make a new dict from an obj rather than data
        serialized = Story._make_new_story(story_obj)

        # patch booleans
        for k, v in serialized.items():
            if k in ['is_private']:
                serialized[k] = "true" if v else "false"

        # TODO: convert reactions and comments to something "understandable"

        return serialized

    @staticmethod
    def react_to_story(story_id, username, sanitized_reaction):
        """React to story represented by story_id as username, with reaction 'reaction'"""
        updated_story = Story._update_story(story_id, {"reactions."+username: sanitized_reaction})
        Logger(__name__).info("User {} has reacted {} to Story_id {}.".format(username, sanitized_reaction, story_id))
        return updated_story["reactions"][username]

    @staticmethod
    def delete_reaction(story_id, username):
        """Delete username's reaction on the story represented by story_id."""
        updated_story = Story._delete_field_on_story(story_id, {"reactions."+username: ""})
        if updated_story is None:
            raise StoryReactionNotFoundException
        return updated_story["reactions"][username]
