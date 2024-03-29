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
            self.logger.debug("At GET@/stories requesting user is {}, uploader is {} and story {} private".format(
                username, story_uploader, "is" if is_private else "is not"))
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

    def delete(self, story_id):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get story by story_id
            story = Story.get_story(story_id)

            # if username is not the uploader return 403
            story_uploader = story["username"]
            self.logger.debug("At DELETE@/stories requesting user is {} and uploader is {}".format(
                username, story_uploader))
            if username != story_uploader:
                return ResponseBuilder.build_error_response("Story is not own", 403)

            # delete story
            deleted_story_obj = Story.delete_story(story_id)
            deleted_story_id = str(deleted_story_obj)

            # generate response
            output = {"target_story_id": deleted_story_id}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, ExpiredTokenException,
                StoryNotFoundException, MissingFieldException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)