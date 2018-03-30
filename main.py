from flask import Flask
from flask import json

app = Flask(__name__)


@app.route('/')
def get_id_by_name():
    data = {'id': 'someOtherId', 'name': 'rodrigo.de.rosa'}
    response = app.response_class(
        status=200,
        mimetype='application/json',
        response=json.dumps(data)
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)