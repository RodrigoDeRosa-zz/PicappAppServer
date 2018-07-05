from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument


class Persistence(object):

    @staticmethod
    def get_all(target_collection):
        Logger(__name__).debug('Retrieving all elements from collection {}.'.format(
            target_collection.name))

        return target_collection.find()

    @staticmethod
    def get_one(target_collection, query):
        Logger(__name__).debug('Retrieving one element from collection {} matching query {}.'.format(
            target_collection.name, query))

        return target_collection.find_one(query)

    @staticmethod
    def get_many(target_collection, query):
        Logger(__name__).debug('Retrieving all elements from collection {} matching query {}.'.format(
            target_collection.name, query))

        return target_collection.find(query)

    @staticmethod
    def insert_one(target_collection, new_element):
        Logger(__name__).debug('Inserting new element {} in collection {}.'.format(
            new_element, target_collection.name))

        return target_collection.insert(new_element)

    @staticmethod
    def delete_one(target_collection, query):
        Logger(__name__).debug('Deleting one element matching query {} in collection {}.'.format(
            query, target_collection.name))

        return target_collection.find_one_and_delete(query)

    @staticmethod
    def delete_all(target_collection):
        Logger(__name__).debug('Deleting all elements in collection {}.'.format(
            target_collection.name))

        return target_collection.delete_many({})

    @staticmethod
    def update_one(target_collection, query, updated_param_dict):
        Logger(__name__).debug('Updating one element in collection {} matching query {} with value {}'.format(
            target_collection.name, query, updated_param_dict))

        return target_collection.find_one_and_update(filter=query,
                                                     update={"$set": updated_param_dict},
                                                     return_document=ReturnDocument.AFTER)

    @staticmethod
    def add_item_to_one(target_collection, query, pushed_param_dict):
        Logger(__name__).debug('Pushing to one element of collection {} matching query {} with value {}'.format(
            target_collection.name, query, pushed_param_dict))

        return target_collection.find_one_and_update(filter=query,
                                                     update={"$push": pushed_param_dict},
                                                     return_document=ReturnDocument.AFTER)

    @staticmethod
    def unset_on_one(target_collection, query, deleted_field_dict):
        Logger(__name__).debug('Deleting field {} on element {} of collection {}'.format(
            deleted_field_dict, query, target_collection.name))

        return target_collection.find_one_and_update(filter=query,
                                                     update={"$unset": deleted_field_dict})

    @staticmethod
    def delete_many(target_collection, query):
        Logger(__name__).debug('Deleting all elements from collection {} matching query {}.'.format(
            target_collection, query))

        return target_collection.delete_many(query)