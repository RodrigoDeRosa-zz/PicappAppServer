from flask import request
from flask_restful import Resource

from src.resources.response_builder import ResponseBuilder
from src.model.database import mongo
from src.model.user import User


class UserResource(Resource):
    def get(self):
        output = []
        #for each user in DB
        for user in User.get_all():
            output.append( {'name':user['name'], 'age':user['age']} )
        #formatting
        response = {'result' : output}
        return ResponseBuilder.build_response(response)

    def post(self):
        #get data
        new_name = self._get_user_name_from_request()
        new_age = self._get_user_age_from_request()

        #TODO: validate username-already-taken

        #insert into DB
        new_user_id = User.insert_one( {'name':new_name, 'age':new_age} )

        #return fresh data from DB
        new_user = User.get_one( {'_id':new_user_id} )

        #formatting
        output = {'name':new_user['name'], 'age':new_user['age']}
        response = {'result' : output}
        return ResponseBuilder.build_response(response)

    def delete(self):
        #delete all
        delete_result = User.delete_all()
        #return amount of users deleted
        output = str(delete_result.deleted_count) + " users were deleted"
        response = {'result' : output}
        return ResponseBuilder.build_response(response)

    def _get_user_name_from_request(self):
        return request.json['name']

    def _get_user_age_from_request(self):
        return request.json['age']
