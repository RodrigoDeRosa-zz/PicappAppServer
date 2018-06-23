from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.flash import Flash, FlashNotFoundException
from src.model.friendship import Friendship
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException


class FlashResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')

    def get(self, flash_id):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get story by story_id
            flash = Flash.get_flash(flash_id)

            # if <username is not the uploader> and <uploader and username are not friends> return 403
            uploader = flash["username"]
            if username != uploader and not Friendship.are_friends(username, uploader):
                return ResponseBuilder.build_error_response("Flash is not from a friend", 403)

            # return response
            return ResponseBuilder.build_response(flash)

        except (InvalidTokenException, MissingFieldException, ExpiredTokenException,
                FlashNotFoundException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)
