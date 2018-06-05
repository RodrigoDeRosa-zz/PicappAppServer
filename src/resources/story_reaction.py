from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.story import Story, StoryNotFoundException
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.security.input_sanitizer import InputSanitizer, InvalidFormatException


class StoryReactionResource(Resource):

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

            # get the reaction type
            reaction = self._get_reaction_from_request()
            reaction = InputSanitizer.sanitize_story_reaction(reaction)

            # post reaction to story by story_id
            saved_reaction = Story.react_to_story(story_id, username, reaction)

            # generate response
            output = {
                "reacting_user_id": username,
                "reaction": saved_reaction
            }

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, ExpiredTokenException, InvalidFormatException,
                MissingFieldException, StoryNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_reaction_from_request(self):
        return RequestBuilder.get_field_from_request('reaction')

