from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument
from bson.objectid import ObjectId


class FlashNotFoundException(Exception):
    def __init__(self):
        self.message = "Flash was not found"
        self.error_code = 404


class Flash(object):

    @staticmethod
    def _get_flashes_db():
        return mongo.db.flashes

    @staticmethod
    def _get_all():
        Logger(__name__).info('Retrieving all flashes.')
        return Flash._get_flashes_db().find()

    @staticmethod
    def _get_one(query):
        Logger(__name__).info('Retrieving flash with query {}.'.format(query))
        return Flash._get_flashes_db().find_one(query)

    @staticmethod
    def _get_one_by_id(flash_id):
        return Flash._get_one({'_id': ObjectId(flash_id)})

    @staticmethod
    def _get_many(query):
        Logger(__name__).info('Retrieving all flashes matching query {}.'.format(query))
        return Flash._get_flashes_db().find(query)

    @staticmethod
    def _insert_one(new_flash):
        Logger(__name__).info('Inserting flash with query {}.'.format(new_flash))
        return Flash._get_flashes_db().insert(new_flash)

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all flashes.')
        return Flash._get_flashes_db().delete_many({})

    @staticmethod
    def _update_flash(flash_id, updated_param_dict):
        Logger(__name__).info('Updating flash {} with value {}'.format(flash_id, updated_param_dict))
        return Flash._get_flashes_db().find_one_and_update(filter={'_id': ObjectId(flash_id)},
                                                           update={"$set": updated_param_dict},
                                                           return_document=ReturnDocument.AFTER)

    @staticmethod
    def _add_item_to_flash(flash_id, pushed_param_dict):
        Logger(__name__).info('Pushing to flash {} with value {}'.format(flash_id, pushed_param_dict))
        return Flash._get_flashes_db().find_one_and_update(filter={'_id': ObjectId(flash_id)},
                                                           update={"$push": pushed_param_dict},
                                                           return_document=ReturnDocument.AFTER)

    @staticmethod
    def _delete_one(flash_id):
        Logger(__name__).info('Deleting flash {}.'.format(flash_id))
        return Flash._get_flashes_db().find_one_and_delete({'_id': ObjectId(flash_id)})

    @staticmethod
    def save_new(flash_data):
        """Saves a new flash from flash_data and returns its _id identifier"""
        # aux username reference
        username = flash_data['username']

        # create new flash
        new_flash = Flash._make_new_flash(flash_data)

        # save into DB
        new_flash_id_obj = Flash._insert_one(new_flash)
        new_flash_id = str(new_flash_id_obj)

        Logger(__name__).info("Flash_id {} was added by user {}.".format(new_flash_id, username))

        # return the id
        return new_flash_id

    @staticmethod
    def _make_new_flash(flash_data):
        required_fields = ['username', 'media', 'location', 'title', 'description', 'timestamp']

        # retrieve required fields from flash_data
        return {k: flash_data[k] for k in required_fields}
