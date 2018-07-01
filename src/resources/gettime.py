from flask_restful import Resource
from src.utils.response_builder import ResponseBuilder

import time
from _datetime import datetime


class TimeResource(Resource):

    def get(self):
        times = {}
        times["epochs"] = int(time.time())
        times["datetime"] = str(datetime.now())
        times["datetime to epochs"] = int(datetime.now().timestamp())
        times["are the same"] = times["epochs"] == times["datetime to epochs"]

        return ResponseBuilder.build_response(times)
