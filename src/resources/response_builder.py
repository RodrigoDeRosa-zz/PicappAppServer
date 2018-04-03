from flask import jsonify
from flask import make_response

class ResponseBuilder:
	@staticmethod
	def build_response(response,status_code = 200):
		return make_response(jsonify(response),status_code)


	@staticmethod
	def build_error_response(error_message,status_code):
		response = {'message':error_message, 'status_code':status_code}
		return ResponseBuilder.build_response(response,status_code)
