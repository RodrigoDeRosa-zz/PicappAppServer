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

            # get flash by flash_id
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

    def delete(self, flash_id):
        try:
            # get token from header
            token = self._get_token_from_header()

            # identify with token
            username = Token.identify(token)

            # get flash by flash_id
            flash = Flash.get_flash(flash_id)

            # if username is not the uploader return 403
            flash_uploader = flash["username"]
            if username != flash_uploader:
                return ResponseBuilder.build_error_response("Flash is not own", 403)

            # delete flash
            deleted_flash_id = Flash.delete_flash(flash_id)

            # generate response
            output = {"target_flash_id": deleted_flash_id}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, ExpiredTokenException,
                FlashNotFoundException, MissingFieldException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)