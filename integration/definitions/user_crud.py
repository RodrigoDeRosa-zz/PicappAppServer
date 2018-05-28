from integration.definitions.general_definitions import test_user1, test_user2, bad_request_response_body, \
    NotNonePlaceholder, expected_response, unauthorized_response_body

signup_body = dict(test_user1)

expected_signup_response_ok = expected_response(dict(signup_body), 200)

expected_signup_response_already_taken = expected_response(bad_request_response_body,
                                                           400)

login_body_ok = dict(test_user1)

login_body_wrong_password = {
    "username": test_user1['username'],
    "password": "asd"
}

login_body_not_found = dict(test_user2)

expected_login_response_ok = expected_response({"token": {"expiresAt": NotNonePlaceholder(),
                                                "token": NotNonePlaceholder()},
                                                "username": test_user1['username']}, 200)

expected_login_response_wrong_password = expected_response(bad_request_response_body, 400)

expected_login_response_not_found = expected_response(bad_request_response_body, 400)

delete_myaccount_body_ok = dict(test_user1)

expected_delete_account_response_wrong_token = expected_response(bad_request_response_body, 400)

expected_delete_account_response_wrong_user = expected_response(unauthorized_response_body, 403)

expected_delete_account_response_ok = expected_response({
    "username": test_user1['username']
}, 200)

expected_get_account_info_failed = expected_response(unauthorized_response_body, 403)

expected_get_account_info_ok = expected_response({
    "username": test_user1["username"],
    "name": test_user1["username"],
    "profile_pic": None
}, 200)

edit_info_body_ok = {
    "name": "new_name",
    "profile_pic": "new_profile_pic"
}

expected_edit_account_info_ok = expected_response({}, 200)
