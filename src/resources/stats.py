from flask_restful import Resource

from src.utils.logger_config import Logger
from src.utils.stats import StatCollector
from src.utils.response_builder import ResponseBuilder

STORIES_POSTED_TAG = "stories"
FRIENDSHIP_REQUESTS_SENT_TAG = "friendships"
FLASHES_POSTED_TAG = "flashes"
ERROR_RESPONSES_TAG = "errors"


class StatsResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self):
        output = {}

        # get number of stories posted
        output[STORIES_POSTED_TAG] = StatCollector.get_number_of_stories_posted()

        # get number of friendship requests sent
        output[FRIENDSHIP_REQUESTS_SENT_TAG] = StatCollector.get_number_of_friendship_requests_sent()

        # get number of flashes posted
        output[FLASHES_POSTED_TAG] = StatCollector.get_number_of_flashes_posted()

        # get number of errors responded
        output[ERROR_RESPONSES_TAG] = StatCollector.get_number_of_error_responses()

        # return response
        return ResponseBuilder.build_response(output)
