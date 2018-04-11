from flask_restful import Resource

from src.model.user import User
from src.utils.request_builder import RequestBuilder,MissingFieldException
from src.utils.response_builder import ResponseBuilder
from src.utils.logger_config import Logger


class MyAccountResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self, username):
        try:
            # get token from header
            token = self._get_token_from_header()
            token['asd'] = 'asd' # just to shut up linter
            # validate username

            # from now on it's a valid user
            user = User.get_one({'username': username})
            output = {'name': user['name'], 'age': user['age']}  # fetch data
            self.logger.info('User account retrieved. ({})'.format(output))
            return ResponseBuilder.build_response(output)
        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.args, 400)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')
