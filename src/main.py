"""Main module"""
from flask import Flask
from flask import json


APP = Flask(__name__)


@APP.route('/')
def get_id_by_name():
    """Testing method"""
    data = {'id': 'someOtherId', 'name': 'rodrigo.de.rosa'}
    response = APP.response_class(
        status=200,
        mimetype='application/json',
        response=json.dumps(data)
    )
    return response


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, threaded=True)
