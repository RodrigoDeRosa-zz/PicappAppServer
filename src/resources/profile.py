from flask import request
from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder
from src.model.user import User
from src.utils.logger_config import Logger


class UserNotFoundException(Exception):
    pass


class ProfileResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self, username):
        # search one by given username
        try:
            user = self._find_one_user({'username': username})
            output = {'username': user['username']}
            self.logger.info('User profile found: {}'.format(output))
            response = {'result': output}
            return ResponseBuilder.build_response(response)
        except UserNotFoundException:
            status_code = 404
            err_msg = "No user found with that name"
            self.logger.error(err_msg)
            return ResponseBuilder.build_error_response(err_msg, status_code)

    # deprecated until user has more info than username and password
    """
    def put(self, username):
        # get data received
        new_age = self._get_age_from_request()

        # look for user and update, returning user info after being updated
        updated_user = User.update_profile(username, {'age': new_age})
        # if match found able to update
        if updated_user:
            output = {'name': updated_user['name'], 'age': updated_user['age']}
            self.logger.info('User profile updated. ({})'.format(output))
        else:  # no matches
            output = "No user found with that name"
            self.logger.info('No user was found to update for username: {}'.format(username))
        # formatting
        response = {'result': output}
        return ResponseBuilder.build_response(response)
    """

    def delete(self, username):
        # search one by username and delete
        user = User.delete_one(username)
        if user:  # match found
            output = {'username': user['username']}
            self.logger.info('User profile deleted. ({})'.format(output))
        else:  # no matches
            output = "No user found with that name"
            self.logger.info('No user was found to delete for username: {}'.format(username))
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def _find_one_user(self, query):
        user = User.get_one(query)
        if not user:
            raise UserNotFoundException("No user found matching criteria")
        return user
    """
    def _get_age_from_request(self):
        return request.json['age']
    """