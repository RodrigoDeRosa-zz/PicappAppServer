from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.user import User
from src.utils.logger_config import Logger
from src.utils.stats import StatCollector
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.security.input_sanitizer import InvalidFormatException, InputSanitizer


class StoriesResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def post(self):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get data from request
            story_data = {}
            story_data['media'] = self._get_media_from_request()
            story_data['location'] = self._get_location_from_request()
            timestamp = self._get_timestamp_from_request()
            is_private = self._get_privateness_from_request()
            story_data['title'] = self._try_get_title_from_request()
            story_data['description'] = self._try_get_description_from_request()
            story_data['username'] = username

            # validated data
            story_data['timestamp'] = InputSanitizer.sanitize_integer(timestamp)
            story_data['is_private'] = InputSanitizer.sanitize_boolean(is_private)

            # ask SS for storage service?

            # save new Story at AS
            self.logger.debug("At POST@/stories got story_data {}".format(story_data))
            new_story_id = User.save_new_story(story_data)

            # generate response
            response = dict(story_data)
            response['story_id'] = new_story_id

            # save stat
            StatCollector.save_event_story_post(story_data["timestamp"])

            # return response
            return ResponseBuilder.build_response(response)

        except (MissingFieldException, InvalidTokenException, ExpiredTokenException,
                InvalidFormatException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_media_from_request(self):
        return RequestBuilder.get_field_from_request('media')

    def _get_timestamp_from_request(self):
        return RequestBuilder.get_field_from_request('timestamp')

    def _get_location_from_request(self):
        return RequestBuilder.get_field_from_request('location')

    def _get_privateness_from_request(self):
        return RequestBuilder.get_field_from_request('is_private')

    def _try_get_title_from_request(self):
        return RequestBuilder.get_field_from_request_or_default('title', "")

    def _try_get_description_from_request(self):
        return RequestBuilder.get_field_from_request_or_default('description', "")
