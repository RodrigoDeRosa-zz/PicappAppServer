from flask import request
from flask_restful import Resource

from src.utils.response_builder import ResponseBuilder
from src.model.user import User
from src.utils.logger_config import Logger


class UserResource(Resource):

    def __init__(self):
        self.logger = Logger(__name__)

    def get(self):
        output = []
        # for each user in DB
        for user in User.get_all():
            output.append({'username': user['username']})
        # formatting
        self.logger.info('User list fetched. ({})'.format(output))
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def post(self):
        # get data
        new_name = self._get_user_name_from_request()
        new_age = self._get_user_age_from_request()

        # TO DO validate username-already-taken

        # insert into DB
        user = {'name': new_name, 'age': new_age}
        new_user_id = User.insert_one(user)
        self.logger.info('User ({}) added to DB with id {}'.format(user, new_user_id))

        # return fresh data from DB
        new_user = User.get_one({'_id': new_user_id})

        # formatting
        output = {'name': new_user['name'], 'age': new_user['age']}
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def delete(self):
        # delete all
        delete_result = User.delete_all()
        self.logger.info('All users were deleted from DB.')
        # return amount of users deleted
        output = str(delete_result.deleted_count) + " users were deleted"
        response = {'result': output}
        return ResponseBuilder.build_response(response)

    def _get_user_name_from_request(self):
        return request.json['name']

    def _get_user_age_from_request(self):
        return request.json['age']
