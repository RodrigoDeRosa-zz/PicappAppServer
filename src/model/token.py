from src.model.database import mongo


class ExpiredTokenException(Exception):
    pass


class Token(object):

    @staticmethod
    def _get_tokens_db():
        return mongo.db.tokens

    @staticmethod
    def validate(token):
        """Receives a token and looks for it in the database, returning True or False whether it is found
        or not, or raising an exception if it expired"""
        # with mongo.db.tokens as Tokens, tk = Tokens.find_one({'token': token}
        tk = Token._get_tokens_db().find_one({'token': token})
        if tk is None:
            return False
        # if somehow.get_present_epochs() > tk['expiresAt']
        #   raise ExpiredTokenException
        return True

    @staticmethod
    def create(token, expiration_epochs, username):
        """Saves to DB a newly created Token with expiration date (in epochs) associated
        with a user"""
        # with mongo.db.tokens as Tokens,
        # tk = Tokens.find_one({'username':username})
        # Tokens.insert({'token': token, 'expiresAt': expiration_epochs, 'username': username}

        # if i wanted to force only one active session
        # if tk is not None:
        #   tk.find_and_delete({'_id':tk['_id']}
