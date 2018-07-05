from src.model.user import User
from src.utils.logger_config import Logger

FEED_FLASHES_PER_USER = 10


class FlashFeedBuilder(object):

    @staticmethod
    def get_flash_feed_for_username(username):
        Logger(__name__).info('Getting flash-feed for user {}.'.format(username))

        # retrieve up to 10 flashes per friend
        feed_flashes = User.get_feed_flashes(username, FEED_FLASHES_PER_USER)

        Logger(__name__).info('Serving {} flashes for user {}\'s flash-feed.'.format(
            len(feed_flashes), username))

        # sort by timestamp in descending order and format (add name and profile_pic)
        prioritized_flashes = [FlashFeedBuilder._format_feed_flash(srz_flash) for srz_flash in
                               sorted(feed_flashes, key=lambda ffd: ffd['timestamp'], reverse=True)]

        Logger(__name__).info('Serving flash-feed for user {}.'.format(username))

        return prioritized_flashes

    @staticmethod
    def _format_feed_flash(srz_flash):
        uploader = srz_flash['username']
        profile_preview = User.get_profile_preview(uploader)

        srz_flash['name'] = profile_preview['name']
        srz_flash['profile_pic'] = profile_preview['profile_pic']
        return srz_flash
