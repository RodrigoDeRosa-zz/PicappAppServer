from flask import Flask
from flask_restful import Api
from configparser import ConfigParser
from src.utils.logger_config import Logger
from src.model.database import mongo
from src.model.index_creation import create_indexes
from src.resources.user import UserResource
from src.resources.profile import ProfileResource
from src.resources.ping import PingResource
from src.resources.login import LoginResource
from src.resources.myaccount import MyAccountResource
from src.resources.signup import SignUpResource
from src.resources.cleaner import CleanerResource
from src.resources.friendship import FriendshipResource
from src.resources.stories import StoriesResource
from src.resources.story import StoryResource
from src.resources.story_reaction import StoryReactionResource
from src.resources.story_comment import StoryCommentResource
from src.resources.feed import FeedResource
from src.resources.profile_preview import ProfilePreviewResource
from src.resources.friendlist import FriendListResource
from src.resources.flashes import FlashesResource
from src.resources.flash import FlashResource
from src.resources.flash_feed import FlashFeedResource


LOCAL_MONGO = 'mongodb://localhost:27017/restdb'
CLOUD_MONGO = 'mongodb://heroku_lw3s78tf:dhk2glio3fs16ket6aapjc2867@ds229549.mlab.com:29549/heroku_lw3s78tf'
app = Flask(__name__)
api = Api(app)
logger = Logger(__name__)

app.config['MONGO_DBNAME'] = 'restdb'


api.add_resource(UserResource, "/users")
api.add_resource(ProfileResource, "/users/<username>")
api.add_resource(PingResource, "/ping")
api.add_resource(LoginResource, "/users/login")
api.add_resource(MyAccountResource, "/users/<username>/myaccount")
api.add_resource(SignUpResource, "/users/signup")
api.add_resource(CleanerResource, "/admin/clean")
api.add_resource(FriendshipResource, "/users/<username>/friendship")
api.add_resource(StoriesResource, "/stories")
api.add_resource(StoryResource, "/stories/<story_id>")
api.add_resource(StoryReactionResource, "/stories/<story_id>/reactions")
api.add_resource(StoryCommentResource, "/stories/<story_id>/comments")
api.add_resource(FeedResource, "/feed")
api.add_resource(ProfilePreviewResource, "/users/<username>/preview")
api.add_resource(FriendListResource, "/users/<username>/friends")
api.add_resource(FlashesResource, "/flashes")
api.add_resource(FlashResource, "/flashes/<flash_id>")
api.add_resource(FlashFeedResource, "/flashfeed")


def run_app(local=True, external_server=False):
    parser = ConfigParser()
    parser.add_section('shared_server')

    if local:
        app.config['MONGO_URI'] = LOCAL_MONGO
        if external_server:
            logger.info('Setting Heroku as Shared Server host.')
            parser.set('shared_server', 'host', 'https://picappss.herokuapp.com')
        else:
            logger.info('Setting localhost as Shared Server host.')
            parser.set('shared_server', 'host', 'http://localhost:3000')
        logger.info('Starting app with local database.')
    else:
        app.config['MONGO_URI'] = CLOUD_MONGO
        logger.info('Setting Heroku as Shared Server host.')
        parser.set('shared_server', 'host', 'https://picappss.herokuapp.com')
        logger.info('Starting app with remote database')
    with open('config.cfg', 'w') as file:
        parser.write(file)
        file.close()
    mongo.init_app(app)
    # creation of indexes
    with app.app_context():
        create_indexes()
    logger.info('Database initialized.')
    return app


if __name__ == '__main__':
    app.config['MONGO_URI'] = LOCAL_MONGO
    app.run(host='0.0.0.0', port=8080, threaded=True)
