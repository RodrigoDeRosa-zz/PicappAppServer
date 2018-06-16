from flask_restful import Resource

from src.model.feed_builder import FeedBuilder
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException


class FeedResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def get(self):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get feed
            feed_stories = FeedBuilder.get_feed_for_username(username)

            # generate response
            output = {"stories": feed_stories}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, MissingFieldException, ExpiredTokenException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
