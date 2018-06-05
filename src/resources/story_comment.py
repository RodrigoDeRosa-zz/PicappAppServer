from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.story import Story, StoryNotFoundException
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.security.input_sanitizer import InputSanitizer, InvalidFormatException


class StoryCommentResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def post(self, story_id):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get data from request
            comment_text = self._get_comment_text_from_request()
            timestamp = self._get_timestamp_from_request()

            # sanitize data
            timestamp = InputSanitizer.sanitize_positive_integer(timestamp)

            # post reaction to story by story_id
            saved_comment = Story.comment_on_story(story_id, username, comment_text, timestamp)

            # generate response
            output = saved_comment

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, ExpiredTokenException, InvalidFormatException,
                MissingFieldException, StoryNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_comment_text_from_request(self):
        return RequestBuilder.get_field_from_request("comment")

    def _get_timestamp_from_request(self):
        return RequestBuilder.get_field_from_request("timestamp")
