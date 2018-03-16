from flask import Flask
from flask import json

app = Flask(__name__)

@app.route('/id/<name>')
def get_id_by_name(name):
    data = {'id': 'someOtherId', 'name': name}
    response = app.response_class(
        status=200,
        mimetype='application/json',
        response=json.dumps(data)
    )
    return response

if __name__ == '__main__':
    app.run()
