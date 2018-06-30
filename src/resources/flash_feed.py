from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.flash_feed_builder import FlashFeedBuilder
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException


class FlashFeedResource(Resource):

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

            # get feed of flashes
            feed_flashes = FlashFeedBuilder.get_flash_feed_for_username(username)

            # generate response
            output = {"flashes": feed_flashes}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, MissingFieldException, ExpiredTokenException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
