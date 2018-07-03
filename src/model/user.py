from src.persistence.database import mongo
from src.persistence.persistence import Persistence
from src.utils.logger_config import Logger
from src.model.story import Story
from src.model.flash import Flash


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
    return Persistence.get_one(User._get_coll(), {'username': username})


class User(object):

    @staticmethod
    def _get_coll():
        return mongo.db.users

    @staticmethod
    def _get_all():
        Logger(__name__).info('Retrieving all users.')
        return Persistence.get_all(User._get_coll())

    @staticmethod
    def _get_one(query):
        Logger(__name__).info('Retrieving user with query {}.'.format(query))
        return Persistence.get_one(User._get_coll(), query)

    @staticmethod
    def _insert_one(new_user):
        Logger(__name__).info('Inserting user with query {}.'.format(new_user))
        return Persistence.insert_one(User._get_coll(), new_user)

    @staticmethod
    def _delete_all():
        Logger(__name__).info('Deleting all users.')
        return Persistence.delete_all(User._get_coll())

    @staticmethod
    def _update_user_by_username(username, updated_param_dict):
        Logger(__name__).info('Updating user {} with value {}'.format(username, updated_param_dict))
        return Persistence.update_one(User._get_coll(), {'username': username}, updated_param_dict)

    @staticmethod
    def _delete_field_by_username(username, deleted_param_dict):
        Logger(__name__).info('Deleting fields of user {} with value {}'.format(username, deleted_param_dict))
        return Persistence.unset_on_one(User._get_coll(), {'username': username}, deleted_param_dict)

    @staticmethod
    def _delete_one(username):
        Logger(__name__).info('Deleting user {}.'.format(username))
        return Persistence.delete_one(User._get_coll(), {'username': username})

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
        new_user['name'] = new_user['username']

        # return the new profile
        return new_user

    @staticmethod
    def _build_profile_from_user(user_data, caller_username):
        # retrieve all stories uploaded by username
        friend_ids = [friend_id for friend_id, friendship_state in user_data["friends"].items()
                      if friendship_state == "friends"]

        # include privates only if caller username is a friend of target user or him/herself
        target_ids = friend_ids + [user_data["username"]]
        stories = Story.get_stories_by_username(user_data["username"], caller_username in target_ids)

        # return the profile
        return {
            # general data
            'username': user_data['username'],
            'profile_pic': user_data['profile_pic'],
            'name': user_data['name'],
            # stories uploaded
            'stories': stories,
            # interesting numbers
            'number of friends': len(friend_ids),
            'number of stories': len(stories)
        }

    @staticmethod
    def _make_account_info_from_user(user):
        account_info = {}

        # retrieve relevant fields
        retrieved_info_fields = ['username', 'profile_pic', 'name']
        for field in retrieved_info_fields:
            account_info[field] = user[field]

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
    def get_profile(username, caller_username):
        """Returns username's profile or raises a UserNotFoundException"""
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        profile = User._build_profile_from_user(user, caller_username)
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
        # delete every owned Story and (related Reactions and Comments? should they be deleted?)
        Story.delete_stories_from_user(username)
        Flash.delete_flashes_from_user(username)

        # now that the user is isolated, delete it
        User._delete_one(username)
        return username

    @staticmethod
    def change_account_info(username, new_data):
        Logger(__name__).info('Changing account info for user {}.'.format(username))
        User._update_user_by_username(username, new_data)
        new_user_data = {}
        updated_user = _user(username)
        for field in new_data.keys():
            new_user_data[field] = updated_user[field]
        return new_user_data

    @staticmethod
    def save_new_story(story_data):
        """Facade for Story.save_new, also checks that user indeed exists"""
        username = story_data['username']
        Logger(__name__).info('Trying to save new story for user {}.'.format(username))
        # check user exists
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        return Story.save_new(story_data)

    @staticmethod
    def _get_stories_feed_data(username, include_privates=False):
        """Formats stories uploaded by this user for easier use of the Feed Builder."""
        # get all stories feed data from username
        story_feed_blocks = Story.get_stories_feed_data_by_username(username, include_privates)

        # get user specific feed data
        user_feed_data = User._get_user_feed_data(username, len(story_feed_blocks))

        # add them to story feed blocks
        [story_feed_block.update(user_feed_data) for story_feed_block in story_feed_blocks]
        return story_feed_blocks

    @staticmethod
    def _get_user_feed_data(username, number_of_stories):
        user_obj = _user(username)
        friend_ids = [friend_id for friend_id, friendship_state in user_obj["friends"].items()
                      if friendship_state == "friends"]  # really ugly, TODO refactor this "friends"
        return {
            "friend_ids": set(friend_ids),
            "number of friends": len(friend_ids),
            "number of stories": number_of_stories
        }

    @staticmethod
    def get_feed_data(username):
        """Gets feed data from all users and all their stories for FeedBuilder usage"""
        feed_data = []

        # get target ids
        target_ids = [friend_id for friend_id, friendship_state in _user(username)["friends"].items()
                      if friendship_state == "friends"]  # really ugly, TODO refactor this "friends"
        target_ids.append(username)

        for user_obj in User._get_all():
            uploader_username = user_obj['username']
            # TODO: if username is not in uploader's friend_ids delete private stories from the feed_data
            feed_data_stories_from_this_user = User._get_stories_feed_data(uploader_username,
                                                                           uploader_username in target_ids)
            feed_data.extend(feed_data_stories_from_this_user)
        return feed_data

    @staticmethod
    def get_profile_preview(username):
        """Get profile preview for a given username, consisting of username plus profile pic and name"""
        Logger(__name__).info('Getting profile preview of user {}.'.format(username))
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        return {
            "username": username,
            "profile_pic": user['profile_pic'],
            "name": user['name']
        }

    @staticmethod
    def save_new_flash(flash_data):
        """Facade for Flash.save_new, also checks that user indeed exists"""
        username = flash_data['username']
        Logger(__name__).info('Trying to save new flash for user {}.'.format(username))
        # check user exists
        user = User._get_one({'username': username})
        if user is None:
            raise UserNotFoundException
        return Flash.save_new(flash_data)

    @staticmethod
    def get_feed_flashes(username, flashes_per_user):
        """Gets a list with up to flashes_per_user flashes from every friend of username
        and his/her own."""
        feed_flashes = []

        # target ids are friends' and own
        user_obj = User._get_one({'username': username})
        target_ids = [friend_id for friend_id, friendship_state in user_obj["friends"].items()
                      if friendship_state == "friends"]  # really ugly, TODO refactor this "friends"
        target_ids.append(username)

        for target_id in target_ids:
            # get flashes from username and take at most flashes_per_user
            target_flashes = Flash.get_flashes_from_username(target_id)[:flashes_per_user]
            feed_flashes.extend(target_flashes)
        return feed_flashes
