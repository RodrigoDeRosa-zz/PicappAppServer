from src.model.database import mongo

from pymongo.collection import ReturnDocument


class User:

    @staticmethod
    def get_users_db():
        return mongo.db.users

    @staticmethod
    def get_all():
        return User.get_users_db().find()

    @staticmethod
    def get_one(query):
        return User.get_users_db().find_one(query)

    @staticmethod
    def insert_one(new_user):
        return User.get_users_db().insert(new_user)

    @staticmethod
    def delete_all():
        return User.get_users_db().delete_many({})

    @staticmethod
    def update_profile(username,updated_param_dict):
        return mongo.db.users.find_one_and_update(filter={'name':username},
                                                  update={"$set": updated_param_dict},
                                                  return_document=ReturnDocument.AFTER)

    @staticmethod
    def delete_one(username):
        return mongo.db.users.find_one_and_delete({'name': username})
