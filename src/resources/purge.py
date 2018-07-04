from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.utils.request_builder import RequestBuilder, MissingFieldException
from src.model.flash import Flash
from src.model.internal_token import SERVER_TOKEN
from src.security.token import InvalidTokenException


class PurgeResource(Resource):

    def post(self):
        try:
            # validate against internal token
            internal_token = self._get_token_from_header()

            if internal_token != SERVER_TOKEN:
                raise InvalidTokenException

            # delete deprecated flashes
            number_of_deletions = Flash.delete_deprecated_flashes()

            # generate response
            output = {'deleted': number_of_deletions}

            # return response
            return ResponseBuilder.build_response(output)

        except (InvalidTokenException, MissingFieldException) as e:
            return ResponseBuilder.build_error_response(e.message, e.error_code)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')
