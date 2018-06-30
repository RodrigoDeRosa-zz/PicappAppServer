from integration.definitions.general_definitions import test_user1, test_user2, bad_request_response_body, \
    NotNonePlaceholder, expected_response, expected_error_response, unauthorized_response_body

import time

expected_get_flashfeed_empty_body = {"flashes": []}

expected_get_flashfeed_empty = expected_response(expected_get_flashfeed_empty_body, 200)


def make_expected_body_from_post(post_body, uploader_username):
    aux = dict(post_body)
    aux["username"] = uploader_username
    aux["flash_id"] = NotNonePlaceholder()
    return aux


def make_feed_flash_from_expected(expected_body):
    aux = dict(expected_body)
    aux["name"] = aux["username"]
    aux["profile_pic"] = None
    return aux


# timestamps are not "now" and have differences just to make sure they do not evaluate to same number
# not making better design because making this smooth is not the point
now_timestamp = int(time.time())

flashfeed_post_flash_body_2_1 = {
      "media": "some_magic_image_uri",
      "timestamp": now_timestamp-20,
      "location": "some_magic_maps_location",
      "description": "no caption needed",
      "title": "2-1"
}

flashfeed_post_flash_body_1_1 = {
      "media": "some_magic_image_uri",
      "timestamp": now_timestamp-10,
      "location": "some_magic_maps_location",
      "description": "no caption needed",
      "title": "1-1"
}

flashfeed_post_flash_body_2_2 = {
      "media": "some_magic_image_uri",
      "timestamp": now_timestamp,
      "location": "some_magic_maps_location",
      "description": "no caption needed",
      "title": "2-2"
}

flashfeed_post_flash_body_expired = {
      "media": "some_magic_image_uri",
      "timestamp": now_timestamp - 80000,
      "location": "some_magic_maps_location",
      "description": "no caption needed",
      "title": "expired"
}

usrnm1 = test_user1["username"]
usrnm2 = test_user2["username"]

expected_flashfeed_post_flash_2_1_body = make_expected_body_from_post(flashfeed_post_flash_body_2_1, usrnm2)
expected_flashfeed_post_flash_1_1_body = make_expected_body_from_post(flashfeed_post_flash_body_1_1, usrnm1)
expected_flashfeed_post_flash_2_2_body = make_expected_body_from_post(flashfeed_post_flash_body_2_2, usrnm2)
expected_flashfeed_post_flash_expired_body = make_expected_body_from_post(flashfeed_post_flash_body_expired, usrnm2)

expected_flashfeed_post_flash_2_1 = expected_response(expected_flashfeed_post_flash_2_1_body, 200)
expected_flashfeed_post_flash_1_1 = expected_response(expected_flashfeed_post_flash_1_1_body, 200)
expected_flashfeed_post_flash_2_2 = expected_response(expected_flashfeed_post_flash_2_2_body, 200)
expected_flashfeed_post_flash_expired = expected_response(expected_flashfeed_post_flash_expired_body, 200)

expected_2_1_feed = make_feed_flash_from_expected(expected_flashfeed_post_flash_2_1_body)
expected_1_1_feed = make_feed_flash_from_expected(expected_flashfeed_post_flash_1_1_body)
expected_2_2_feed = make_feed_flash_from_expected(expected_flashfeed_post_flash_2_2_body)

expected_get_flashfeed_11_body = {
    'flashes': [expected_1_1_feed]
}

expected_get_flashfeed_11 = expected_response(expected_get_flashfeed_11_body, 200)

expected_get_flashfeed_22_21_body = {
    'flashes': [expected_2_2_feed, expected_2_1_feed]
}

expected_get_flashfeed_22_21 = expected_response(expected_get_flashfeed_22_21_body, 200)

expected_get_flashfeed_22_11_21_body = {
    'flashes': [expected_2_2_feed, expected_1_1_feed, expected_2_1_feed]
}

expected_get_flashfeed_22_11_21 = expected_response(expected_get_flashfeed_22_11_21_body, 200)