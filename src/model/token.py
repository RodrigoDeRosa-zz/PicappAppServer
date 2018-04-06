from src.model.database import mongo
import time


class ExpiredTokenException(Exception):
    pass


class Token(object):

    @staticmethod
    def _get_tokens_db():
        return mongo.db.tokens

    @staticmethod
    def _get_current_epochs():
        return int(time.time())

    @staticmethod
    def validate(token):
        """Receives a token and looks for it in the database, returning True or False whether it is found
        or not, or raising an exception if it expired"""
        tk = Token._get_tokens_db().find_one({'token': token})
        if tk is None:
            return False
        if Token._get_current_epochs() > tk['expiresAt']:
            raise ExpiredTokenException
        return True

    @staticmethod
    def create(token, expiration_epochs, username):
        """Saves to DB a newly created Token with expiration date (in epochs) associated
        with a user"""
        tk = Token._get_tokens_db().find_one({'username': username})
        new_token_id = Token._get_tokens_db().insert({'token': token, 'expiresAt': expiration_epochs, 'username': username})
        # enforce only one active session
        if tk is not None:
            tk.find_and_delete({'_id': tk['_id']})
        return new_token_id
