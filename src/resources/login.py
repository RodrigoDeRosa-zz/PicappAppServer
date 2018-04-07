# from flask import request
from flask_restful import Resource

from src.resources.response_builder import ResponseBuilder
from src.model.shared_server_service import SharedServerService, InvalidDataException, NoServerException, UnexpectedErrorException
from src.resources.request_builder import MissingFieldException,RequestBuilder

class LoginResource(Resource):
    def post(self):
        try:
            user_data = {}
            user_data['username'] = self._get_username_from_request()
            user_data['password'] = self._get_password_from_request()
            output_dict = SharedServerService.post_token(user_data)
            #do something about Token expiration date
            response = {'token': output_dict['token']}
            return ResponseBuilder.build_response(response)
        except MissingFieldException as e:
            return ResponseBuilder.build_error_response(e.args,400) #check status_code
        except InvalidDataException as e:
            return ResponseBuilder.build_error_response(e.args, 401) #check status_code
        except NoServerException as e:
            return ResponseBuilder.build_error_response(e.args, 500) #check status_code
        except UnexpectedErrorException as e:
            return ResponseBuilder.build_error_response(e.args, 500) #check status_code

    def _get_username_from_request(self):
        return RequestBuilder.get_field_from_request('username')

    def _get_password_from_request(self):
        return RequestBuilder.get_field_from_request('password')
