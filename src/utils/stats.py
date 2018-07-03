from src.model.database import mongo
from src.utils.logger_config import Logger
import time

# types of events
STORY_POST = "story_post"
FRIENDSHIP_REQUEST_SENT = "friendship_post"
FLASH_POST = "flash_post"
ERROR_RESPONSE = "error_response"


def objects_to_timestamps(objs_iterable):
    """Receives an iterable of objects containing field 'timestamp' and returns a list of those
    timestamps"""
    return [obj["timestamp"] for obj in objs_iterable]


def get_time_in_millisec():
    """Get actual time in milliseconds"""
    return int(time.time() * 1000)


class StatCollector(object):

    @staticmethod
    def _get_stats_db():
        return mongo.db.statistics

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all stats saved.')
        return StatCollector._get_stats_db().delete_many({})

    @staticmethod
    def _get_many(query):
        return StatCollector._get_stats_db().find(query)

    @staticmethod
    def _insert_into_db(element):
        return StatCollector._get_stats_db().insert(element)

    @staticmethod
    def _save_new_event(event_type, timestamp):
        Logger(__name__).info('Saving event of type {} with timestamp {}.'.format(event_type,
                                                                                  str(timestamp)))
        new_event = {"event": event_type, "timestamp": timestamp}
        return StatCollector._insert_into_db(new_event)

    @staticmethod
    def _get_timestamps_of_event(event_type):
        Logger(__name__).info('Retrieving all events of type {}.'.format(event_type))
        event_objs_iterable = StatCollector._get_many({"event": event_type})
        return objects_to_timestamps(event_objs_iterable)

    # STORIES POSTED
    @staticmethod
    def save_event_story_post(timestamp):
        return StatCollector._save_new_event(STORY_POST, timestamp)

    @staticmethod
    def get_number_of_stories_posted():
        return StatCollector._get_timestamps_of_event(STORY_POST)

    # FRIENDSHIP INTENTS SENT
    @staticmethod
    def save_event_friendship_request_sent():
        return StatCollector._save_new_event(FRIENDSHIP_REQUEST_SENT, get_time_in_millisec())

    @staticmethod
    def get_number_of_friendship_requests_sent():
        return StatCollector._get_timestamps_of_event(FRIENDSHIP_REQUEST_SENT)

    # FLASHES POSTED
    @staticmethod
    def save_event_flash_post(timestamp):
        return StatCollector._save_new_event(FLASH_POST, timestamp)

    @staticmethod
    def get_number_of_flashes_posted():
        return StatCollector._get_timestamps_of_event(FLASH_POST)

    # ERROR RESPONSES SENT
    @staticmethod
    def save_event_error_response():
        return StatCollector._save_new_event(ERROR_RESPONSE, get_time_in_millisec())

    @staticmethod
    def get_number_of_error_responses():
        return StatCollector._get_timestamps_of_event(ERROR_RESPONSE)