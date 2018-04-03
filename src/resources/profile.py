from flask import request
from flask_restful import Resource

from src.resources.response_builder import ResponseBuilder
#from src.model.database import mongo
from src.model.user import User


class UserNotFoundException(Exception):
    pass


class ProfileResource(Resource):

    def get(self, username):
        # search one by given username
        try:
            user = self._find_one_user({'name': username})
            output = {'name': user['name'], 'age': user['age']}
            response = {'result': output}
            return ResponseBuilder.build_response(response)
        except UserNotFoundException:
            status_code = 404
            err_msg = "No user found with that name"
            return ResponseBuilder.build_error_response(err_msg,status_code)

    def put(self, username):
        # get data received
        new_age = request.json['age']

        # look for user and update, returning user info after being updated
        updated_user = User.update_profile(username, {'age': new_age})
        # if match found able to update
        if updated_user:
            output = {'name': updated_user['name'], 'age': updated_user['age']}
        else: # no matches
            output = "No user found with that name"
        # formatting
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def delete(self, username):
        # search one by username and delete
        user = User.delete_one(username)
        if user:  # match found
            output = {'name': user['name'], 'age': user['age']}
        else:  # no matches
            output = "No user found with that name"
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def _find_one_user(self, query):
        user = User.get_one(query)
        if not user:
            raise UserNotFoundException("No user found matching criteria")
        return user
