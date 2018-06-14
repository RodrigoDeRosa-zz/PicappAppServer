import time

from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import (BaseVariables,
                                      numeric_rule_variable,
                                      string_rule_variable)
from src.model.user import User

# TODO: take out this import when User-level feed data use is implemented
from src.model.story import Story


INITIAL_SCORE = 10
MANY_LIKES_BONUS = 2
MANY_DISLIKES_PENALTY = 2
TOO_OLD_PENALTY = 1
MANY_COMMENTS_BONUS = 3


class FeedBuilder(object):

    @staticmethod
    def get_feed_for_username(username):
        """
        USE SOMETHING LIKE THIS WHEN USERNAMES ARE BEING ITERATED ACCORDINGLY

        # get all stories by iterating over usernames, use username to filter private, non-friend ones

        stories_feed_data = User.get_stories_feed_data(username)
        """

        # <ugly> feed, not using User-level data for rules
        stories_feed_data = Story.get_all_stories_as_feed_data()
        # </ugly>

        # calculate priorities
        prioritized_stories = stories_feed_data  # FIXME: add priorities

        # return stories in according order
        return [Story.get_story(story_id) for story_id in prioritized_stories]


def epochs_as_days(epochs):
    """Returns rounded number of days elapsed in number of epochs given"""
    return round(epochs/86400)  # number of epochs in 1 day


