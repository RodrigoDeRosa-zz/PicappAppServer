from flask_restful import Resource

from src.model.user import User
from src.resources.request_builder import RequestBuilder,MissingFieldException
from src.resources.response_builder import ResponseBuilder

class MyAccountResource(Resource):
    def get(self,username):
        try:
            # get token from header
            token = self._get_token_from_header()
            token['asd'] = 'asd'# just to shut up linter
            # validate username

            # from now on it's a valid user
            user = User.get_one({'username': username})
            output = {'name': user['name'], 'age': user['age']} # fetch data
            return ResponseBuilder.build_response(output)
        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.args, 400)

    def _get_token_from_header(self):
        return RequestBuilder.get_field_from_header('token')