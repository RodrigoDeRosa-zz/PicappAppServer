from flask_restful import Resource

from src.utils.logger_config import Logger
from src.utils.stats import StatCollector
from src.utils.response_builder import ResponseBuilder


class StatsResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self):
        output = {}

        # get number of stories posted
        output["stories posted"] = StatCollector.get_number_of_stories_posted()

        # get number of friendship requests sent
        output["friendship requests sent"] = StatCollector.get_number_of_friendship_requests_sent()

        # get number of flashes posted
        output["flashes posted"] = StatCollector.get_number_of_flashes_posted()

        # get number of errors responded
        output["error responses sent"] = StatCollector.get_number_of_error_responses()

        # return response
        return ResponseBuilder.build_response(output)
