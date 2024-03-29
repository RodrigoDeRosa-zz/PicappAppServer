from src.persistence.database import mongo
from src.persistence.persistence import Persistence
from src.utils.logger_config import Logger
from bson.objectid import ObjectId
import time

FLASH_LIFETIME_HOURS = 4


class FlashNotFoundException(Exception):
    def __init__(self):
        self.message = "Flash was not found"
        self.error_code = 404


class Flash(object):

    @staticmethod
    def _get_coll():
        return mongo.db.flashes

    @staticmethod
    def _get_all():
        # warning, does not filter out deprecated flashes, for internal use only
        Logger(__name__).info('Retrieving all flashes.')
        return Persistence.get_all(Flash._get_coll())

    @staticmethod
    def _get_one(query):
        # warning, does not filter out deprecated flashes, for internal use only
        Logger(__name__).info('Retrieving flash with query {}.'.format(query))
        return Persistence.get_one(Flash._get_coll(), query)

    @staticmethod
    def _unsafe_get_many(query):
        # warning, does not filter out deprecated flashes, for internal use only
        Logger(__name__).info('Retrieving all flashes matching query {}.'.format(query))
        return Persistence.get_many(Flash._get_coll(), query)

    @staticmethod
    def _get_one_by_id(flash_id):
        flash_obj = Flash._get_one({'_id': ObjectId(flash_id)})
        return None if Flash._flash_is_deprecated(flash_obj) else flash_obj

    @staticmethod
    def _get_many(query):
        return Flash._filter_out_deprecated_flashes(Flash._unsafe_get_many(query))

    @staticmethod
    def _insert_one(new_flash):
        Logger(__name__).info('Inserting flash with query {}.'.format(new_flash))
        return Persistence.insert_one(Flash._get_coll(), new_flash)

    @staticmethod
    def _delete_one(flash_id):
        Logger(__name__).info('Deleting flash {}.'.format(flash_id))
        return Persistence.delete_one(Flash._get_coll(), {'_id': ObjectId(flash_id)})

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

    @staticmethod
    def get_flash(flash_id):
        """Get flash represented by flash_id formatted to be JSON serializable, or raise
         FlashNotFoundException exception if no flash was found"""
        Logger(__name__).info('Looking for flash {}.'.format(flash_id))
        flash = Flash._get_one_by_id(flash_id)
        if flash is None:
            raise FlashNotFoundException
        return Flash._serialize_flash(flash)

    @staticmethod
    def _serialize_flash(flash_obj):
        srz_flash = Flash._make_new_flash(flash_obj)

        # _id is an ObjectId so it has to be converted to string
        srz_flash['flash_id'] = str(flash_obj['_id'])
        return srz_flash

    @staticmethod
    def delete_flash(flash_id):
        """Safely delete flash"""
        Logger(__name__).info("Deleting flash_id {}.".format(flash_id))
        # try to delete it
        deleted_flash = Flash._delete_one(flash_id)
        if deleted_flash is None:
            raise FlashNotFoundException

        return str(deleted_flash['_id'])

    @staticmethod
    def delete_flashes_from_user(username):
        """Delete all flashes uploaded by user username"""
        Logger(__name__).info("Deleting all flashes from user {}.".format(username))
        flash_ids = [str(flash_obj['_id']) for flash_obj in Flash._get_many({'username': username})]

        deleted_ids = []
        for flash_id in flash_ids:
            deleted_ids.append(Flash.delete_flash(flash_id))

        return deleted_ids

    @staticmethod
    def get_flashes_from_username(username):
        """Get all flashes uploaded by username, sorted by timestamp in descending order"""
        Logger(__name__).info('Getting all flashes from user {}.'.format(username))
        # get all flashes matching username
        serialized_flashes = [Flash._serialize_flash(flash_obj) for
                              flash_obj in Flash._get_many({'username': username})]

        # sort inplace in descending order by timestamp
        serialized_flashes.sort(key=lambda srz_flash: srz_flash["timestamp"], reverse=True)

        # return sorted list
        return serialized_flashes

    @staticmethod
    def _filter_out_deprecated_flashes(flash_objs):
        return [flash_obj for flash_obj in flash_objs if not Flash._flash_is_deprecated(flash_obj)]

    @staticmethod
    def _flash_is_deprecated(flash_obj):
        # right now - number of epochs in 1 hour * number of hours allowed is the minimum epochs allowed
        if flash_obj is None:
            return True
        min_timestamp_allowed = time.time() - 3600 * FLASH_LIFETIME_HOURS  # in seconds
        min_millisecs_allowed = min_timestamp_allowed * 1000  # in milliseconds
        return flash_obj['timestamp'] <= min_millisecs_allowed

    @staticmethod
    def delete_deprecated_flashes():
        # get all and keep deprecated ones
        Logger(__name__).info('Deleting deprecated flashes')
        target_ids = [str(flash_obj['_id']) for flash_obj in Flash._get_all()
                      if Flash._flash_is_deprecated(flash_obj)]
        # delete one by one
        for target_id in target_ids:
            Flash._delete_one(target_id)

        return len(target_ids)
