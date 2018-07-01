from integration.definitions.general_definitions import test_user1, test_user2, bad_request_response_body, \
    NotNonePlaceholder, expected_response, expected_error_response, unauthorized_response_body

import time
now_timestamp = int(time.time()) * 1000
str_timestamp = str(now_timestamp)

post_flash_body_ok = {
      "media": "some_magic_image_uri",
      "timestamp": str_timestamp,
      "location": "some_magic_maps_location",
      "description": "no caption needed",
      "title": "rip pacha"
}

post_flash_body_missing_location = {
    "media": "some_magic_image_uri",
    "timestamp": str_timestamp,
    "description": "no caption needed",
    "title": "rip pacha"
}

post_flash_body_timestamp_not_integer = {
    "media": "some_magic_image_uri",
    "timestamp": "15asd24157743",
    "location": "some_magic_maps_location",
    "description": "no caption needed",
    "title": "rip pacha"
}


expected_post_flash_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": now_timestamp,
    "location": "some_magic_maps_location",
    "description": "no caption needed",
    "title": "rip pacha",
    "flash_id": NotNonePlaceholder(),
    "username":  test_user1["username"]
}
expected_post_flash_ok = expected_response(expected_post_flash_ok_body, 200)

expected_get_flash_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": now_timestamp,
    "location": "some_magic_maps_location",
    "description": "no caption needed",
    "title": "rip pacha",
    "username":  test_user1["username"],
    "flash_id": NotNonePlaceholder()
}
expected_get_flash_ok = expected_response(expected_get_flash_ok_body, 200)

expected_delete_flash_ok_body = {
    "target_flash_id": NotNonePlaceholder()
}
expected_delete_flash_ok = expected_response(expected_delete_flash_ok_body, 200)

expected_post_flash_missing_location = expected_error_response(400)

expected_post_flash_timestamp_not_integer = expected_error_response(400)

expected_get_flash_not_friends =  expected_error_response(403)

expected_delete_flash_not_own =  expected_error_response(403)

expected_get_flash_not_found =  expected_error_response(404)


post_flash2_body_ok = {
      "media": "some_magic_image_uri",
      "timestamp": str_timestamp,
      "location": "some_magic_maps_location",
}

expected_post_flash2_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": now_timestamp,
    "location": "some_magic_maps_location",
    "description": "",
    "title": "",
    "flash_id": NotNonePlaceholder(),
    "username": test_user1["username"]
}
expected_post_flash2_ok = expected_response(expected_post_flash2_ok_body, 200)

expected_get_flash2_ok_body = {
    "media": "some_magic_image_uri",
    "timestamp": now_timestamp,
    "location": "some_magic_maps_location",
    "description": "",
    "title": "",
    "flash_id": NotNonePlaceholder(),
    "username": test_user1["username"]
}
expected_get_flash2_ok = expected_response(expected_get_flash2_ok_body, 200)