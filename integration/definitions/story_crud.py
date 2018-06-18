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

post_private_story_body_ok = {
  "media": "some_magic_image_uri",
  "timestamp": 1524157743,
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": True
}

expected_private_post_story_ok_body = {
  "story_id": NotNonePlaceholder(),
  "media": "some_magic_image_uri",
  "timestamp": 1524157743,
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": True,
  "username": test_user1["username"]
}

expected_private_post_story_ok = expected_response(expected_private_post_story_ok_body, 200)


expected_get_story_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": 1524157743,
    "location": "some_magic_maps_location",
    "description": "No caption needed",
    "title": "RIP Pacha",
    "is_private": "true",
    "username": test_user1["username"],
    'comments': [],
    'reactions': {},
    'story_id': NotNonePlaceholder()
}

expected_get_story_ok = expected_response(expected_get_story_ok_body, 200)

expected_get_story_not_friends = expected_error_response(403)

expected_delete_story_not_own = expected_error_response(403)

expected_get_story_not_found = expected_error_response(404)

expected_delete_story_ok = expected_response({"target_story_id": NotNonePlaceholder()}, 200)


post_public_story_body_ok = {
  "media": "some_magic_image_uri",
  "timestamp": "1524157743",
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": "false"
}

expected_public_post_story_ok_body = {
  "story_id": NotNonePlaceholder(),
  "media": "some_magic_image_uri",
  "timestamp": 1524157743,
  "location": "some_magic_maps_location",
  "description": "No caption needed",
  "title": "RIP Pacha",
  "is_private": False,
  "username": test_user1["username"]
}

expected_public_post_story_ok = expected_response(expected_public_post_story_ok_body, 200)

reaction_body_missing_reaction = {}

expected_reaction_missing_reaction = expected_error_response(400)

reaction_body_funny = {"reaction": "funny"}

expected_reaction_ok_user_2_funny = expected_response({
                "reacting_user_id": test_user2["username"],
                "reaction": "funny"
}, 200)

reaction_body_like = {"reaction": "like"}

expected_reaction_ok_user_1_like = expected_response({
                "reacting_user_id": test_user1["username"],
                "reaction": "like"
}, 200)

comment_body_missing_field ={
    "timestamp": "1524157743"
}

expected_comment_missing_field = expected_error_response(400)

comment_body_ok_1 = {
  "timestamp": 2222222222,
  "comment": "first comment"
}
expected_comment_ok_1_body = {"timestamp": 2222222222, "comment": "first comment",
                              "commenting_user_id": test_user1["username"]}

expected_comment_ok_1 = expected_response(expected_comment_ok_1_body, 200)

comment_body_ok_2 = {
  "timestamp": 3333333333,
  "comment": "got lag"
}

expected_comment_ok_2_body = {"timestamp": 3333333333, "comment": "got lag",
                              "commenting_user_id": test_user1["username"]}

expected_comment_ok_2 = expected_response(expected_comment_ok_2_body, 200)

comment_body_ok_3 = {
  "timestamp": 1111111111,
  "comment": "no i'm first"
}
expected_comment_ok_3_body = {"timestamp": 1111111111, "comment": "no i'm first",
                              "commenting_user_id": test_user2["username"]}

expected_comment_ok_3 = expected_response(expected_comment_ok_3_body, 200)

expected_get_public_story_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": 1524157743,
    "location": "some_magic_maps_location",
    "description": "No caption needed",
    "title": "RIP Pacha",
    "is_private": "false",
    "username": test_user1["username"],
    'comments': [expected_comment_ok_3_body, expected_comment_ok_1_body, expected_comment_ok_2_body],
    'reactions': {
        test_user1["username"]: "like",
        test_user2["username"]: "funny"
    },
    'story_id': NotNonePlaceholder()
}

expected_get_public_story_public_ok = expected_response(expected_get_public_story_ok_body, 200)

reaction_body_dislike = {"reaction": "dislike"}

expected_reaction_ok_user_1_dislike = expected_response({
                "reacting_user_id": test_user1["username"],
                "reaction": "dislike"
}, 200)

reaction_body_boring = {"reaction": "boring"}

expected_reaction_ok_user_2_boring = expected_response({
                "reacting_user_id": test_user2["username"],
                "reaction": "boring"
}, 200)

expected_get_public_story_ok_changed_body = {
    "media": "some_magic_image_uri",
    "timestamp": 1524157743,
    "location": "some_magic_maps_location",
    "description": "No caption needed",
    "title": "RIP Pacha",
    "is_private": "false",
    "username": test_user1["username"],
    'comments': [expected_comment_ok_3_body, expected_comment_ok_1_body, expected_comment_ok_2_body],
    'reactions': {
        test_user1["username"]: "dislike",
        test_user2["username"]: "boring"
    },
    'story_id': NotNonePlaceholder()
}

expected_get_public_story_public_ok_changed = expected_response(expected_get_public_story_ok_changed_body, 200)