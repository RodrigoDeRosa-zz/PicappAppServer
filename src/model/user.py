from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument


class User(object):

    @staticmethod
    def _get_users_db():
        return mongo.db.users

    @staticmethod
    def get_all():
        Logger(__name__).info('Retrieving all users.')
        return User._get_users_db().find()

    @staticmethod
    def get_one(query):
        Logger(__name__).info('Retrieving user with query {}.'.format(query))
        return User._get_users_db().find_one(query)

    @staticmethod
    def insert_one(new_user):
        Logger(__name__).info('Inserting user with query {}.'.format(new_user))
        return User._get_users_db().insert(new_user)

    @staticmethod
    def delete_all():
        Logger(__name__).info('Deleting all users.')
        return User._get_users_db().delete_many({})

    @staticmethod
    def update_profile(username, updated_param_dict):
        Logger(__name__).info('Updating user {} with value {}'.format(username, updated_param_dict))
        return mongo.db.users.find_one_and_update(filter={'name': username},
                                                  update={"$set": updated_param_dict},
                                                  return_document=ReturnDocument.AFTER)

    @staticmethod
    def delete_one(username):
        Logger(__name__).info('Deleting user {}.'.format(username))
        return User._get_users_db().find_one_and_delete({'name': username})
