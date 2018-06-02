from integration.definitions.general_definitions import test_user1, test_user2, bad_request_response_body, \
    NotNonePlaceholder, expected_response, expected_error_response, unauthorized_response_body

post_story_login_body_missing_media = {
  "timestamp": "1524157743",
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": "true"
}

expected_post_story_missing_media = expected_error_response(400)

post_story_login_body_privacy_not_boolean = {
  "timestamp": "1524157743",
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": "not_a_boolean"
}

post_story_login_body_timestamp_not_integer = {
  "timestamp": "1524157743a",
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": "true"
}

expected_post_story_invalid_format = expected_error_response(400)

post_story_body_ok = {
  "media": "some_magic_image_uri",
  "timestamp": 1524157743,
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": True
}

expected_post_story_ok_body = {
  "story_id": NotNonePlaceholder(),
  "media": "some_magic_image_uri",
  "timestamp": 1524157743,
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": True,
  "username": test_user1["username"]
}

expected_post_story_ok = expected_response(expected_post_story_ok_body, 200)


expected_get_story_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": 1524157743,
    "location": "some_magic_maps_location",
    "description": "No caption needed",
    "title": "RIP Pacha",
    "is_private": "true",
    "username": test_user1["username"],
    'comments': [],
    'reactions': {}
}

expected_get_story_ok = expected_response(expected_get_story_ok_body, 200)

expected_get_story_not_friends = expected_error_response(403)

expected_delete_story_not_own = expected_error_response(403)

expected_get_story_not_found = expected_error_response(404)















expected_delete_story_ok = expected_response({"target_story_id": NotNonePlaceholder()}, 200)