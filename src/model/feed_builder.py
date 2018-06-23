import time

from business_rules import run_all
from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import (BaseVariables,
                                      numeric_rule_variable)
from src.model.user import User
from src.model.story import Story
from src.utils.logger_config import Logger

INITIAL_SCORE = 10
BONUS_SCALING = 0.3
PENALTY_SCALING = 0.1

NICE_STORY_BONUS = 5
HOT_BONUS = 10
UNINTERESTING_STORY_PENALTY = 3


class FeedBuilder(object):

    @staticmethod
    def get_feed_for_username(username):
        Logger(__name__).info('Getting feed for user {}.'.format(username))

        # get all stories by iterating over usernames, use username to filter private, non-friend ones
        stories_feed_data = User.get_feed_data(username)

        Logger(__name__).info('Prioritizing {} stories for user {}\'s feed.'.format(
            len(stories_feed_data), username))

        # calculate priorities
        for story_feed_data in stories_feed_data:
            set_score(story_feed_data, INITIAL_SCORE)

            run_all(rule_list=rules,
                    stop_on_first_trigger=False,
                    defined_actions=StoryActions(story_feed_data),
                    defined_variables=StoryVariables(story_feed_data))

        prioritized_stories = [story_feed_data['story_id'] for story_feed_data
                               in sorted(stories_feed_data,
                                         key=lambda sfd: get_score(sfd),
                                         reverse=True)]

        Logger(__name__).info('Serving feed for user {}.'.format(username))
        # get stories in according order, add feed-specific fields of user's name and profile pic
        return [FeedBuilder._format_feed_story(story_id) for story_id in prioritized_stories]

    @staticmethod
    def _format_feed_story(story_id):
        serialized_story = Story.get_story(story_id)
        uploader = serialized_story['username']
        profile_preview = User.get_profile_preview(uploader)

        serialized_story['name'] = profile_preview['name']
        serialized_story['profile_pic'] = profile_preview['profile_pic']
        return serialized_story


def epochs_as_days(epochs):
    """Returns rounded number of days elapsed in number of epochs given"""
    return round(epochs/86400)  # number of epochs in 1 day


def get_current_epochs():
    return int(time.time())


def set_score(story_feed_data, new_score):
    story_feed_data["score"] = new_score


def get_score(story_feed_data):
    return story_feed_data["score"]


class StoryVariables(BaseVariables):

    def __init__(self, story_feed_data):
        self.story = story_feed_data

    @numeric_rule_variable()
    def likes(self):
        return self.story["likes"]

    @numeric_rule_variable
    def dislikes(self):
        return self.story["dislikes"]

    @numeric_rule_variable
    def number_of_friends(self):
        return self.story["number of friends"]

    @numeric_rule_variable
    def days_since_post(self):
        return epochs_as_days(get_current_epochs() - self.story["timestamp"])

    @numeric_rule_variable
    def number_of_comments(self):
        return self.story["number of comments"]

    @numeric_rule_variable
    def like_dislike_rate(self):
        likes = self.story["likes"]
        dislikes = self.story["dislikes"]
        return float(likes) / (likes+dislikes)


class StoryActions(BaseActions):

    def __init__(self, story_feed_data):
        self.story = story_feed_data

    @rule_action(params={"bonus": FIELD_NUMERIC})
    def apply_bonus(self, bonus):
        new_score = get_score(self.story) + BONUS_SCALING * bonus
        set_score(self.story, new_score)

    @rule_action(params={"penalty": FIELD_NUMERIC})
    def apply_penalty(self, penalty):
        new_score = get_score(self.story) + PENALTY_SCALING * penalty
        set_score(self.story, new_score)


rules = [
    # likes > 3 AND comments > 2    -> NICE STORY
    {
        "conditions": {"all": [
            {
                "name": "likes",
                "operator": "greater_than",
                "value": 3
            },
            {
                "name": "number_of_comments",
                "operator": "greater_than",
                "value": 2
            }
        ]},
        "actions": [
            {
                "name": "apply_bonus",
                "params": {"bonus": NICE_STORY_BONUS}
            }
        ]
    },
    # likes > 2 AND days_since_post <= 2  -> HOT
    {
        "conditions": {"all": [
            {
                "name": "likes",
                "operator": "greater_than",
                "value": 2
            },
            {
                "name": "days_since_post",
                "operator": "less_than_or_equal_to",
                "value": 2
            }
        ]},
        "actions": [
            {
                "name": "apply_bonus",
                "params": {"bonus": HOT_BONUS}
            }
        ]
    },
    # days_since_post >= 5 or like_dislike_rate < 0.3
    {
        "conditions": {"any": [
            {
                "name": "days_since_post",
                "operator": "greater_than_or_equal_to",
                "value": 5

            },
            {
                "name": "like_dislike_rate",
                "operator": "less_than",
                "value": 0.3
            }
        ]},
        "actions": [
            {
                "name": "apply_penalty",
                "params": {"penalty": UNINTERESTING_STORY_PENALTY}
            }
        ]
    }
]

