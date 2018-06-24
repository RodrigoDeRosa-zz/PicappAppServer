from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.user import User
from src.utils.logger_config import Logger
from src.security.token import Token, InvalidTokenException, ExpiredTokenException
from src.security.input_sanitizer import InvalidFormatException, InputSanitizer


class FlashesResource(Resource):

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
            flash_data = {}
            flash_data['media'] = self._get_media_from_request()
            flash_data['location'] = self._get_location_from_request()
            timestamp = self._get_timestamp_from_request()
            flash_data['title'] = self._try_get_title_from_request()
            flash_data['description'] = self._try_get_description_from_request()
            flash_data['username'] = username

            # validated data
            flash_data['timestamp'] = InputSanitizer.sanitize_integer(timestamp)

            # save new flash at AS
            new_flash_id = User.save_new_flash(flash_data)

            # generate response
            response = dict(flash_data)
            response['flash_id'] = new_flash_id

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

    def _try_get_title_from_request(self):
        return RequestBuilder.get_field_from_request_or_default('title', "")

    def _try_get_description_from_request(self):
        return RequestBuilder.get_field_from_request_or_default('description', "")
