from flask_restful import Resource
from src.security.token import Token
from src.model.user import User
from src.utils.response_builder import ResponseBuilder

class CleanerResource(Resource):
    def post(self):
        """HAZARDOUS: Cleans all collections in the database. BEWARE OF DESYNC WITH SHARED SERVER."""
        user_result = User._delete_all()
        token_result = Token._delete_all()
        user_count = user_result.deleted_count
        token_count = token_result.deleted_count
        output = str(user_count) + " users and "+str(token_count)+" tokens were deleted."
        response = {'result': output}
        return ResponseBuilder.build_response(response)
