from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.story import Story, StoryNotFoundException
from src.model.friendship import Friendship
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.security.input_sanitizer import InputSanitizer


class StoryResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def get(self, story_id):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get story by story_id
            story = Story.get_story(story_id)

            # if <username is not the uploader> and <story is private> and ...
            # ... <uploader and username are not friends> return 403
            is_private = story["is_private"]
            story_uploader = story["username"]
            if username != story_uploader and \
               InputSanitizer.sanitize_boolean(is_private) and \
               not Friendship.are_friends(username, story_uploader):
                return ResponseBuilder.build_error_response("Story is private", 403)

            # generate response

            # return response
            return ResponseBuilder.build_response(story)

        except (InvalidTokenException, MissingFieldException, ExpiredTokenException,
                StoryNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
