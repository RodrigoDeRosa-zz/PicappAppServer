import requests
import json
from src.model.internal_token import SERVER_TOKEN


HEROKU_ROOT_URI = 'https://picapp-app-server.herokuapp.com'


PURGE_RELATIVE_PATH = "/admin/purge"


def send_purge_request(target_base_uri):
    target_uri = target_base_uri + PURGE_RELATIVE_PATH
    return requests.post(target_uri, data=json.dumps({}),
                         headers={'Content-Type': 'Application/json', 'token': SERVER_TOKEN})


if __name__ == '__main__':
    base_uri = HEROKU_ROOT_URI
    response = send_purge_request(base_uri)
    print(response.json())
