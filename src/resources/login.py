from flask_restful import Resource

from src.model.services.shared_server_service import SharedServerService
from src.utils.response_builder import ResponseBuilder
from src.model.exceptions.response_exceptions import *
from src.model.exceptions.request_exceptions import *
from src.utils.request_builder import MissingFieldException, RequestBuilder
from src.utils.logger_config import Logger


class LoginResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)
        self.shared_server_service = SharedServerService()

    def post(self):
        try:
            user_data = {}
            user_data['username'] = self._get_username_from_request()
            user_data['password'] = self._get_password_from_request()
            self.logger.info('User data generated. ({})'.format(user_data))
            output_dict = self.shared_server_service.get_new_token(user_data)
            # do something about Token expiration date
            response = {'username':user_data['username'],'token': output_dict}
            self.logger.info('Token received from service. ({})'.format(response))
            return ResponseBuilder.build_response(response)
        except MissingFieldException as mfe:
            return ResponseBuilder.build_error_response(str(mfe), 400)  # check status_code
        except InvalidDataException as ide:
            return ResponseBuilder.build_error_response(str(ide), 400)  # check status_code
        except NoServerException as nse:
            return ResponseBuilder.build_error_response(str(nse), 500)  # check status_code
        except UnexpectedErrorException as uee:
            return ResponseBuilder.build_error_response(str(uee), 500)  # check status_code
        except ConnectionFailException as cfe:
            return ResponseBuilder.build_error_response(str(cfe), 500)  # check status_code

    def _get_username_from_request(self):
        return RequestBuilder.get_field_from_request('username')

    def _get_password_from_request(self):
        return RequestBuilder.get_field_from_request('password')
