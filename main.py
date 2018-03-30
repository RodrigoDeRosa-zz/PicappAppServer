from flask import Flask
from flask import json

app = Flask(__name__)


@app.route('/')
def get_id_by_name():
    data = {'id': 'someOtherId', 'name': 'rodrigo.de-rosa'}
    response = app.response_class(
        status=200,
        mimetype='application/json',
        response=json.dumps(data)
    )
    return response


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, threaded=True)

"""
- stage: build docker image
    script:
    - docker login -u="$DOCKER_USERNAME" -p="$DOCKER_PASSWORD"
    - docker build -t picapp-app-server .
    - docker images
    - docker tag picapp-app-server $DOCKER_USERNAME/picapp-app-server
    - docker push $DOCKER_USERNAME/picapp-app-server
"""