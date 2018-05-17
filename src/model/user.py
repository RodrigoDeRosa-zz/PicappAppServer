from src.model.database import mongo
from src.utils.logger_config import Logger
from pymongo.collection import ReturnDocument


class UserAlreadyExistsException(Exception):
    def __init__(self):
        self.message = "Username already exists"
        self.error_code = 400

    def __str__(self):
        return self.message


class UserNotFoundException(Exception):
    def __init__(self):
        self.message = "Username was not found"
        self.error_code = 404

    def __str__(self):
        return self.message


def _user(username):
    """Silently returns the current user referencing the username, used to prevent using old versions of
    documents. Should only be used internally when editing documents."""
    return User._get_users_db().find_one({'username': username})


class User(object):

    @staticmethod
    def _get_users_db():
        return mongo.db.users

    @staticmethod
    def _get_all():
        Logger(__name__).info('Retrieving all users.')
        return User._get_users_db().find()

    @staticmethod
    def _get_one(query):
        Logger(__name__).info('Retrieving user with query {}.'.format(query))
        return User._get_users_db().find_one(query)

    @staticmethod
    def _insert_one(new_user):
        Logger(__name__).info('Inserting user with query {}.'.format(new_user))
        return User._get_users_db().insert(new_user)

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all users.')
        return User._get_users_db().delete_many({})

    @staticmethod
    def _update_user_by_username(username, updated_param_dict):
        Logger(__name__).info('Updating user {} with value {}'.format(username, updated_param_dict))
        return mongo.db.users.find_one_and_update(filter={'username': username},
                                                  update={"$set": updated_param_dict},
                                                  return_document=ReturnDocument.AFTER)

    @staticmethod
    def _push_to_user_by_username(username, pushed_param_dict):
        Logger(__name__).info('Pushing to user {} with value {}'.format(username, pushed_param_dict))
        return mongo.db.users.find_one_and_update(filter={'username': username},
                                                  update={"$push": pushed_param_dict},
                                                  return_document=ReturnDocument.AFTER)

    @staticmethod
    def _delete_field_by_username(username, deleted_param_dict):
        Logger(__name__).info('Deleting fields of user {} with value {}'.format(username, deleted_param_dict))
        return mongo.db.users.find_one_and_update(filter={'username': username},
                                                  update={"$unset": deleted_param_dict},
                                                  return_document=ReturnDocument.AFTER)

    @staticmethod
    def _delete_one(username):
        Logger(__name__).info('Deleting user {}.'.format(username))
        return User._get_users_db().find_one_and_delete({'username': username})

    @staticmethod
    def _make_new_user(new_user_data):
        new_user = {}
        # define the required fields
        required_fields = ['username']
        for field in required_fields:
            assert(field in new_user_data)
            new_user[field] = new_user_data[field]

        # init the blank/default ones
        new_user['profile_pic'] = None
        new_user['friends'] = {}
        new_user['stories'] = []
        new_user['name'] = new_user['username']

        # return the new profile
        return new_user

    @staticmethod
    def _build_profile_from_user(user_data):
        profile = {}
        # retrieve all info fields (the ones that are just plain info)
        retrieved_info_fields = ['username', 'profile_pic', 'name']
        for field in retrieved_info_fields:
            profile[field] = user_data[field]
        profile['number of friends'] = len(user_data['friends'])
        profile['number of stories'] = len(user_data['stories'])
        """
#ACTIVATE ON STORIES RELEASE
        # retrieve a preview for every story
        profile['stories'] = []
        for story_id in user_data['stories']:
            profile['stories'].append(Stories.make_preview(story_id))
        """
        # return the profile
        return profile

    @staticmethod
    def _make_account_info_from_user(user):
        account_info = {}

        # retrieve relevant fields
        retrieved_info_fields = ['username', 'profile_pic', 'name']
        for field in retrieved_info_fields:
            account_info[field] = user[field]
        # TODO: anything else?

        # return the info
        return account_info

    @staticmethod
    def save_new(user_data):
        """Saves a new user from user_data containing [username] and returns its _id identifier"""
        # check for already-existent user with that username
        if User._get_one({'username': user_data['username']}):
            raise UserAlreadyExistsException

        # create new user
        new_profile = User._make_new_user(user_data)

        # save into DB
        new_user_id = User._insert_one(new_profile)
        Logger(__name__).info('New user {} was saved.'.format(user_data['username']))

        # return the id (what for? we may never know)
        return new_user_id

    @staticmethod
    def get_profile(username):
        """Returns username's profile or raises a UserNotFoundException"""
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        profile = User._build_profile_from_user(user)
        Logger(__name__).info("Profile for user {} was retrieved".format(username))
        return profile

    @staticmethod
    def get_account_info(username):
        """Gets account information related to username"""
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        account_info = User._make_account_info_from_user(user)
        Logger(__name__).info("Account info for user {} was retrieved".format(username))
        return account_info

    @staticmethod
    def delete_user(username):
        """Deletes user from the Application Server or raises a UserNotFoundException"""
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        deleted_name = User._safe_delete_user(user)
        Logger(__name__).info("Account for user {} was deleted at User".format(deleted_name))
        return deleted_name

    @staticmethod
    def _safe_delete_user(user):
        # delete from every friend
        username = user['username']
        for friend_name in user['friends']:
            friend_user = User._get_one({'username': friend_name})
            # if for any reason user didn't exist anymore, continue silently
            if friend_user is None:
                continue
            # friend_user['friends'].pop(username)
            entry = 'friends.'+username
            User._delete_field_by_username(friend_user['username'], {entry: ""})
        # delete every owned Story and related Reactions and Comments
        # TODO: ADD WHEN STORIES ARE SUPPORTED

        # now that the user is isolated, delete it
        User._delete_one(username)
        return username

    @staticmethod
    def change_account_info(username, new_data):
        User._update_user_by_username(username, new_data)
        new_user_data = {}
        updated_user = _user(username)
        for field in new_data.keys():
            new_user_data[field] = updated_user[field]
        return new_user_data
