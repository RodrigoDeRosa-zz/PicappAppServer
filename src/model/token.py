from src.model.database import mongo


class InvalidTokenException(Exception):
    pass


class ExpiredTokenException(Exception):
    pass


class Token(object):

    @staticmethod
    def _get_tokens_db():
        return mongo.db.tokens

    @staticmethod
    def validate(token):
        """Receives a token and uses to identify a User, or raises an exception"""
        # with mongo.db.tokens as Tokens, tk = Tokens.find_one({'token': token}
        # if tk is None:
        #   raise InvalidToken
        # if somehow.get_epochs > tk['expiresAt']:
        #   raise ExpiredTokenException
        # return tk['username']
        raise NotImplementedError()

    @staticmethod
    def create(token,expiration_epochs,username):
        """Saves to DB a newly created Token with expiration date (in epochs) associated
        with a user"""
        # with mongo.db.tokens as Tokens,
        # tk = Tokens.find_one({'username':username})
        # Tokens.insert({'token': token, 'expiresAt': expiration_epochs, 'username': username}

        # if i wanted to force only one active session
        # if tk is not None:
        #   tk.find_and_delete({'_id':tk['_id']}
