from src.persistence.database import mongo
from src.utils.logger_config import Logger
import time


class ExpiredTokenException(Exception):
    def __init__(self):
        self.message = "Received token has expired"
        self.error_code = 400

    def __str__(self):
        return self.message


class InvalidTokenException(Exception):
    def __init__(self):
        self.message = "Received token was invalid"
        self.error_code = 400

    def __str__(self):
        return self.message


class Token(object):

    @staticmethod
    def _get_tokens_db():
        return mongo.db.tokens

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all tokens.')
        return Token._get_tokens_db().delete_many({})

    @staticmethod
    def _get_current_epochs():
        return int(time.time())

    @staticmethod
    def _find_token(token):
        return Token._get_tokens_db().find_one({'token': token})

    @staticmethod
    def _create_token(token, expiration_epochs, username):
        return Token._get_tokens_db().insert({'token': token, 'expiresAt': expiration_epochs, 'username': username})

    @staticmethod
    def log_out(username):
        """Nullifies all tokens related to user."""
        return Token._get_tokens_db().remove({'username': username})

    @staticmethod
    def identify(token):
        """Receives a token and looks for it in the database, returning the username of the owner or
        raising an exception if it was not found or had expired"""
        Logger(__name__).info('Looking for token {}'.format(token))
        tk = Token._find_token(int(token))
        if tk is None:
            Logger(__name__).info("Token {} not found".format(token))
            raise InvalidTokenException
        if Token._get_current_epochs() > tk['expiresAt']:
            Logger(__name__).info("Token {} was found but it had expired".format(token))
            raise ExpiredTokenException
        Logger(__name__).info("Token {} found".format(token))
        return tk['username']

    @staticmethod
    def save_new(token, expiration_epochs, username):
        """Saves to DB a newly created Token with expiration date (in epochs) associated
        with a user"""
        tk = Token._get_tokens_db().find_one({'username': username})
        new_token_id = Token._create_token(token, expiration_epochs, username)
        Logger(__name__).info('Token {} stored for user {}, with id {}'.format(token, username, new_token_id))
        # enforce only one active session
        if tk is not None:
            Logger(__name__).info('Old token ({}) removed for user ({}).'.format(token, username))
            Token._get_tokens_db().remove({'_id': tk['_id']})
        return new_token_id
