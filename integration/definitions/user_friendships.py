from integration.definitions.general_definitions import test_user1, test_user2, bad_request_response_body, \
    NotNonePlaceholder, expected_response, unauthorized_response_body, expected_error_response

# These are so that minimum amount of things from user_crud is used
friendship_signup_body_1 = dict(test_user1)
friendship_login_body_1 = dict(test_user1)
friendship_expected_signup_response_ok_1 = expected_response(dict(friendship_signup_body_1), 200)
friendship_expected_login_response_ok_1 = expected_response(
    {"token": {"expiresAt": NotNonePlaceholder(), "token": NotNonePlaceholder()},
     "username": test_user1['username']}, 200)
friendship_delete_myaccount_body_ok_1 = dict(test_user1)
friendship_expected_delete_account_response_ok_1 = expected_response({
    "username": test_user1['username']
}, 200)

friendship_signup_body_2 = dict(test_user2)
friendship_login_body_2 = dict(test_user2)
friendship_expected_signup_response_ok_2 = expected_response(dict(friendship_signup_body_2), 200)
friendship_expected_login_response_ok_2 = expected_response(
    {"token": {"expiresAt": NotNonePlaceholder(), "token": NotNonePlaceholder()},
     "username": test_user2['username']}, 200)
friendship_delete_myaccount_body_ok_2 = dict(test_user2)
friendship_expected_delete_account_response_ok_2 = expected_response({
    "username": test_user2['username']
}, 200)

# Real friendship ones

expected_send_friend_request_failed_wrong_token = expected_response(bad_request_response_body, 400)

expected_send_friend_request_failed_not_found = expected_error_response(404)

expected_send_friend_request_ok_1_to_2 = expected_response({
    "target_user_id": test_user2["username"]
}, 200)

expected_reject_friend_request_ok_2_to_1 = expected_response({
    "target_user_id": test_user1["username"]
}, 200)

expected_send_friend_request_ok_2_to_1 = dict(expected_reject_friend_request_ok_2_to_1)

expected_accept_friend_request_ok_1_to_2 = dict(expected_send_friend_request_ok_1_to_2)

expected_accept_friend_request_failed = expected_error_response(400)

expected_dissolve_friend_request_ok_1_to_2 = dict(expected_send_friend_request_ok_1_to_2)

expected_send_friend_request_failed_not_friends = expected_error_response(400)
