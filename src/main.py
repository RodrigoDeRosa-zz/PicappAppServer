from flask import Flask
# from flask import request
# from flask_restful import Resource, Api
from flask_restful import Api

from src.model.database import mongo
from src.resources.user import UserResource
from src.resources.profile import ProfileResource

LOCAL_MONGO = 'mongodb://localhost:27017/restdb'
CLOUD_MONGO = 'mongodb://heroku_lw3s78tf:dhk2glio3fs16ket6aapjc2867@ds229549.mlab.com:29549/heroku_lw3s78tf'
app = Flask(__name__)
api = Api(app)

app.config['MONGO_DBNAME'] = 'restdb'


api.add_resource(UserResource, "/users")
api.add_resource(ProfileResource, "/users/<username>")


def run_app(local=True):
    if local:
        app.config['MONGO_URI'] = LOCAL_MONGO
    else:
        app.config['MONGO_URI'] = CLOUD_MONGO
    mongo.init_app(app)
    return app


if __name__ == '__main__':
    app.config['MONGO_URI'] = LOCAL_MONGO
    app.run(host='0.0.0.0', port=8080, threaded=True)


# TESTED ENDPOINTS:
# GET /users: lista todos los usuarios
# POST /users: agrega un nuevo usuario
# DELETE /users: elimina todos los usuarios
# GET /users/<username>: profile del user <username>
# PUT /users/<username>: edit del user <username>
# DELETE /users/<username>: eliminar el user <username>
