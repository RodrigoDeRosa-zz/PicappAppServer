import pprint

from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument
from src.model.user import User, UserNotFoundException, _user
from bson.objectid import ObjectId

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
    def _make_new_story(new_story_data):
        new_story = {}
        # define the required fields
        required_fields = ['username', 'timestamp', 'is_private', 'location']
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
