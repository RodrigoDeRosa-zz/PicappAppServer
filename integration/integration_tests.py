#!/usr/bin/env python3

# usage: pytest integration/integration_tests.py

import requests
import unittest
import json

from integration.definitions.user_crud import *
from integration.definitions.user_friendships import *
from integration.definitions.story_crud import *

HOST = "local"
DEBUG_MODE = True
STANDARD_TIMEOUT = 999  # seconds


def get_uri_from_host():
    target_roots = {"heroku": 'https://picapp-app-server.herokuapp.com',
                    "docker": 'localhost:5000',
                    "local": 'http://localhost:8000'}

    # TODO:for now only heroku and local are supported
    assert HOST in ["heroku", "local"]

    # get the host root
    return target_roots[HOST]


def get_msg(sent_body, response):
    if DEBUG_MODE:
        aux = "\nSent BODY:\n"+str(sent_body)
        aux += "\nReceived STATUS_CODE: "+str(response.status_code)
        aux += "\nReceived BODY: \n "+str(response.json())
        return aux
    return ""


class IntegrationTestCase(unittest.TestCase):

    def setUp(self):
        self.root_uri = get_uri_from_host()
        print("root uri is: "+self.root_uri)

    def sign_up_user(self, body):
        """util for almost all tests"""
        uri = self.root_uri + "/users/signup"
        b = json.dumps(body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def log_in_user(self, body):
        """util for almost all tests"""
        uri = self.root_uri + "/users/login"
        b = json.dumps(body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def delete_user(self, username, body, token):
        """util for almost all tests"""
        uri = self.root_uri + "/users/{}/myaccount".format(username)
        b = json.dumps(body)
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': token},
                            timeout=STANDARD_TIMEOUT)
        return b, r

    def test_user_CD(self):
        """STEP 1: signup OK
        STEP 2: signup FAILED(user taken)
        STEP 3: login FAILED(user not found)
        STEP 4: login OK
        STEP 5: delete account FAILED (wrong token)
        STEP 6: delete account FAILED (wrong user)
        STEP 7: delete account OK"""

        # STEP 1: sign up with new valid user (signup OK)

        b, r = self.sign_up_user(signup_body)

        expected = expected_signup_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: sign up with taken user (signup FAILED(taken))
        b, r = self.sign_up_user(signup_body)

        expected = expected_signup_response_already_taken
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: login with non existant user (login FAILED(not found))
        b, r = self.log_in_user(login_body_not_found)

        expected = expected_login_response_not_found
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 4: login with valid user (login OK)
        b, r = self.log_in_user(login_body_ok)

        expected = expected_login_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        token = str(r.json()['token']['token'])

        # STEP 5: try to delete account but wrong token (delete account FAILED(wrong token))
        b, r = self.delete_user(login_body_ok['username'], delete_myaccount_body_ok, token+"1")

        expected = expected_delete_account_response_wrong_token
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 6: delete account FAILED (wrong user)
        b, r = self.delete_user(login_body_ok['username'] + "asd", delete_myaccount_body_ok, token)

        expected = expected_delete_account_response_wrong_user
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 7: successfully delete account (delete account OK)
        b, r = self.delete_user(login_body_ok['username'], delete_myaccount_body_ok, token)

        expected = expected_delete_account_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

    def test_ping(self):
        """STEP 1: ping OK"""

        # STEP 1: ping the server, don't have to sign up nor login (ping OK)
        uri = self.root_uri + "/ping"
        b = json.dumps({})
        r = requests.get(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)
        self.assertEqual(r.status_code, 200, get_msg(b, r))

    def test_user_RU(self):
        """STEP 0a: signup
        STEP 0b: login
        STEP 1: get account info FAILED (username and token mismatch)
        STEP 2: get account info OK
        STEP 3: edit account info OK
        STEP Xa: delete account"""

        # STEP 0a: sign up with an account
        b, r = self.sign_up_user(signup_body)

        expected = expected_signup_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0b: login with that account
        b, r = self.log_in_user(login_body_ok)

        expected = expected_login_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        token = str(r.json()['token']['token'])

        # STEP 1: try to get account info from another user (get account info FAILED)
        username = login_body_ok['username']
        wrong_username = username + "asd"

        uri = self.root_uri + "/users/{}/myaccount".format(wrong_username)

        b = json.dumps({})
        r = requests.get(uri,
                         data=b,
                         headers={'Content-Type': 'Application/json',
                                  'token': token},
                         timeout=STANDARD_TIMEOUT)

        expected = expected_get_account_info_failed
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: successfully get account info from own user (get account info OK)
        uri = self.root_uri + "/users/{}/myaccount".format(username)


        b = json.dumps({})
        r = requests.get(uri,
                         data=b,
                         headers={'Content-Type': 'Application/json',
                                  'token': token},
                         timeout=STANDARD_TIMEOUT)

        expected = expected_get_account_info_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: successfully edit account info (edit account info OK)
        uri = self.root_uri + "/users/{}/myaccount".format(username)

        b = json.dumps(edit_info_body_ok)
        r = requests.put(uri,
                         data=b,
                         headers={'Content-Type': 'Application/json',
                                  'token': token},
                         timeout=STANDARD_TIMEOUT)

        expected = expected_edit_account_info_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xa: delete account
        b, r = self.delete_user(login_body_ok['username'], delete_myaccount_body_ok, token)

        expected = expected_delete_account_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

    def send_friend_YES(self, source_token, target_username):
        """Util for test_friendship"""
        uri = self.root_uri + "/users/{}/friendship".format(target_username)
        b = json.dumps({})
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json',
                                   'token': source_token},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def send_friend_NO(self, source_token, target_username):
        """Util for test_friendship"""
        uri = self.root_uri + "/users/{}/friendship".format(target_username)
        b = json.dumps({})
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': source_token},
                            timeout=STANDARD_TIMEOUT)
        return b, r

    def test_friendship(self):
        """STEP 0a: signup user 1
        STEP 0b: signup user 2
        STEP 0c: login user 1
        STEP 0d: login user 2
        STEP 1: send friendship YES from 1 to 2 FAILED(wrong token)
        STEP 2: send friendship YES from 1 to non-existant FAILED (not found)
        STEP 3: send friendship YES from 1 to 2 OK
        STEP 4: send friendship NO from 2 to 1 OK
        STEP 5: send friendship YES from 2 to 1 OK
        STEP 6: send friendship YES from 1 to 2 OK
        STEP 7: send friendship YES from 1 to 2 FAILED (already friends)
        STEP 8: send friendship YES from 2 to 1 FAILED (already friends)
        STEP 9: send friendship NO from 1 to 2 OK
        STEP 10: send friendship NO from 1 to 2 FAILED (wrong token)
        STEP 11: send friendship NO from 1 to 2 FAILED (not friends)
        STEP Xa: delete user 1
        STEP Xb: delete user 2"""

        # STEP 0a: signup with user 1
        b, r = self.sign_up_user(friendship_signup_body_1)

        expected = friendship_expected_signup_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0b: signup with user 2
        b, r = self.sign_up_user(friendship_signup_body_2)

        expected = friendship_expected_signup_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0c: log in with user 1
        b, r = self.log_in_user(friendship_login_body_1)

        expected = friendship_expected_login_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username1 = friendship_login_body_1["username"]
        token1 = str(r.json()['token']['token'])

        # STEP 0d: log in with user 2
        b, r = self.log_in_user(friendship_login_body_2)

        expected = friendship_expected_login_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username2 = friendship_login_body_2["username"]
        token2 = str(r.json()['token']['token'])

        # STEP 1: send friendship YES from 1 to 2 FAILED (wrong token)
        target_username = username2
        source_token = token1+"1"

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_send_friend_request_failed_wrong_token
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: try to send friendship to non-existent user (YES from 1 to non-existent FAILED)
        target_username = username2+"asdsda"
        source_token = token1

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_send_friend_request_failed_not_found
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: successfully send friendship request (YES from 1 to 2 OK)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_send_friend_request_ok_1_to_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 4: successfully reject friendship request (NO from 2 to 1 OK)
        target_username = username1
        source_token = token2

        b, r = self.send_friend_NO(source_token, target_username)

        expected = expected_reject_friend_request_ok_2_to_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 5: successfully send friendship request (YES from 2 to 1 OK)
        target_username = username1
        source_token = token2
        
        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_send_friend_request_ok_2_to_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 6: successfully accept friendship request (YES from 1 to 2 OK)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_accept_friend_request_ok_1_to_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 7: trying to become friends with a friend fails (YES from 1 to 2 FAILED)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_accept_friend_request_failed
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 8: trying to become friends with a friend fails (YES from 2 to 1 FAILED)
        target_username = username1
        source_token = token2

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_accept_friend_request_failed
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 9: successfully dissolve friendship (NO from 1 to 2 OK)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_NO(source_token, target_username)

        expected = expected_dissolve_friend_request_ok_1_to_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 10: try to dissolve friendship from 1 to 2 FAILED (wrong token)
        target_username = username2
        source_token = token1+"2"

        b, r = self.send_friend_NO(source_token, target_username)

        expected = expected_send_friend_request_failed_wrong_token
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 11: try to dissolve friendship but not friends (NO from 1 to 2 FAILED)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_NO(source_token, target_username)

        expected = expected_send_friend_request_failed_not_friends
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xa: delete user1
        b, r = self.delete_user(username1, friendship_delete_myaccount_body_ok_1, token1)

        expected = friendship_expected_delete_account_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xb: delete user2
        b, r = self.delete_user(username2, friendship_delete_myaccount_body_ok_2, token2)

        expected = friendship_expected_delete_account_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        """STEP 0a: signup user 1
        STEP 0b: signup user 2
        STEP 0c: login user 1
        STEP 0d: login user 2
        STEP Xa: delete user 1
        STEP Xb: delete user 2"""

    def post_story(self, body, token):
        """Util for tests on stories"""
        uri = self.root_uri + "/stories"
        b = json.dumps(body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json',
                                   'token': token},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def get_story(self, story_id, token):
        """Util for tests on stories"""
        uri = self.root_uri + "/stories/{}".format(story_id)
        b = json.dumps({})
        r = requests.get(uri,
                         data=b,
                         headers={'Content-Type': 'Application/json',
                                  'token': token},
                         timeout=STANDARD_TIMEOUT)
        return b, r

    def delete_story(self, story_id, token):
        """Util for tests on stories"""
        uri = self.root_uri + "/stories/{}".format(story_id)
        b = json.dumps({})
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': token},
                            timeout=STANDARD_TIMEOUT)
        return b, r

    def react_to_story(self, body, story_id, token):
        """Util for tests on stories"""
        uri = self.root_uri + "/stories/{}/reactions".format(story_id)
        b = json.dumps(body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json',
                                   'token': token},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def comment_on_story(self, body, story_id, token):
        """Util for tests on stories"""
        uri = self.root_uri + "/stories/{}/comments".format(story_id)
        b = json.dumps(body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json',
                                   'token': token},
                          timeout=STANDARD_TIMEOUT)
        return b, r

    def test_private_story_CRD(self):
        """STEP 0a: signup user 1
        STEP 0b: signup user 2
        STEP 0c: login user 1
        STEP 0d: login user 2
        STEP 1: post story as user 1 FAILED (missing a field)
        STEP 2: post story as user 1 FAILED (timestamp is not integer)
        STEP 3: post story as user 1 FAILED (is_private is not boolean)
        STEP 4: post story as user 1 OK
        STEP 5: get story as user 1 OK
        STEP 6: get story as user 2 FAILED (not friends)
        STEP Ma: send FRIENDSHIP YES from 1 to 2
        STEP Mb: send FRIENDSHIP YES from 2 to 1 (become friends)
        STEP 7: get story as user 2 OK
        STEP 8 delete story as user 2 FAILED (not own)
        STEP 9: delete story as user 1 OK
        STEP 10: get story as use 1 FAILED (not found)
        STEP Xa: delete user 1
        STEP Xb: delete user 2"""

        # STEP 0a: signup with user 1
        b, r = self.sign_up_user(friendship_signup_body_1)

        expected = friendship_expected_signup_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0b: signup with user 2
        b, r = self.sign_up_user(friendship_signup_body_2)

        expected = friendship_expected_signup_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0c: log in with user 1
        b, r = self.log_in_user(friendship_login_body_1)

        expected = friendship_expected_login_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username1 = friendship_login_body_1["username"]
        token1 = str(r.json()['token']['token'])

        # STEP 0d: log in with user 2
        b, r = self.log_in_user(friendship_login_body_2)

        expected = friendship_expected_login_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username2 = friendship_login_body_2["username"]
        token2 = str(r.json()['token']['token'])

        # STEP 1: post story as user 1 FAILED (missing a field)
        b, r = self.post_story(post_story_login_body_missing_media, token1)

        expected = expected_post_story_missing_media
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: post story as user 1 FAILED (timestamp is not integer)
        b, r = self.post_story(post_story_login_body_timestamp_not_integer, token1)

        expected = expected_post_story_invalid_format
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: post story as user 1 FAILED (is_private is not boolean)
        b, r = self.post_story(post_story_login_body_privacy_not_boolean, token1)

        expected = expected_post_story_invalid_format
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 4: post story as user 1 OK
        b, r = self.post_story(post_private_story_body_ok, token1)

        expected = expected_private_post_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: keep the story_id
        story_id1 = str(r.json()["story_id"])

        # STEP 5: get story as user 1 OK
        b, r = self.get_story(story_id1, token1)

        expected = expected_get_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 6: get story as user 2 FAILED (not friends)
        b, r = self.get_story(story_id1, token2)

        expected = expected_get_story_not_friends
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Ma: send FRIENDSHIP YES from 1 to 2 (step 5 of test_friendship)
        target_username = username1
        source_token = token2

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_send_friend_request_ok_2_to_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Mb: send FRIENDSHIP YES from 2 to 1 (become friends) (step 6 of test_friendship)
        target_username = username2
        source_token = token1

        b, r = self.send_friend_YES(source_token, target_username)

        expected = expected_accept_friend_request_ok_1_to_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 7: get story as user 2 OK
        b, r = self.get_story(story_id1, token2)

        expected = expected_get_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 8 delete story as user 2 FAILED (not own)
        b, r = self.delete_story(story_id1, token2)

        expected = expected_delete_story_not_own
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 9: delete story as user 1 OK
        b, r = self.delete_story(story_id1, token1)

        expected = expected_delete_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 10: get story as use 1 FAILED (not found)
        b, r = self.get_story(story_id1, token2)

        expected = expected_get_story_not_found
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xa: delete user1
        b, r = self.delete_user(username1, friendship_delete_myaccount_body_ok_1, token1)

        expected = friendship_expected_delete_account_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xb: delete user2
        b, r = self.delete_user(username2, friendship_delete_myaccount_body_ok_2, token2)

        expected = friendship_expected_delete_account_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

    def test_story_reactions_and_comments(self):
        """STEP 0a: signup user 1
        STEP 0b: signup user 2
        STEP 0c: login user 1
        STEP 0d: login user 2
        STEP 0e: post public story as user 1
        STEP 1: react to story as user 2 FAILED (missing reaction)
        STEP 2: react to story as user 2 OK (funny)
        STEP 3: react to story as user 1 OK (like)
        STEP 4: comment on story as user 1 FAILED (missing field)
        STEP 5: comment on story as user 1 OK (timestamp t_1)
        STEP 6: comment on story as user 1 OK (timestamp t_2 > t_1)
        STEP 7: comment on story as user 2 OK (timestamp t_3 < t_1)
        STEP 8: get story as user 1 OK (should show both reactions and correct order of comments)
        STEP 9: react to story as user 1 OK (dislike)
        STEP 10: react to story as user 2 OK (boring)
        STEP 11: get story as user 2 OK (should show change in reactions)
        STEP Xa: delete story
        STEP Xb: delete user 1
        STEP Xc: delete user 2"""

        # STEP 0a: signup with user 1
        b, r = self.sign_up_user(friendship_signup_body_1)

        expected = friendship_expected_signup_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0b: signup with user 2
        b, r = self.sign_up_user(friendship_signup_body_2)

        expected = friendship_expected_signup_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 0c: log in with user 1
        b, r = self.log_in_user(friendship_login_body_1)

        expected = friendship_expected_login_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username1 = friendship_login_body_1["username"]
        token1 = str(r.json()['token']['token'])

        # STEP 0d: log in with user 2
        b, r = self.log_in_user(friendship_login_body_2)

        expected = friendship_expected_login_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        username2 = friendship_login_body_2["username"]
        token2 = str(r.json()['token']['token'])

        # STEP 0e: post public story as user 1 OK
        b, r = self.post_story(post_public_story_body_ok, token1)

        expected = expected_public_post_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: keep the story_id
        story_id1 = str(r.json()["story_id"])

        # STEP 1: react to story as user 2 FAILED (missing reaction)
        b, r = self.react_to_story(reaction_body_missing_reaction, story_id1, token2)

        expected = expected_reaction_missing_reaction
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: react to story as user 2 OK (funny)
        b, r = self.react_to_story(reaction_body_funny, story_id1, token2)

        expected = expected_reaction_ok_user_2_funny
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: react to story as user 1 OK (like)
        b, r = self.react_to_story(reaction_body_like, story_id1, token1)

        expected = expected_reaction_ok_user_1_like
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 4: comment on story as user 1 FAILED (missing field)
        b, r = self.comment_on_story(comment_body_missing_field, story_id1, token1)

        expected = expected_comment_missing_field
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 5: comment on story as user 1 OK (timestamp t_1)
        b, r = self.comment_on_story(comment_body_ok_1, story_id1, token1)

        expected = expected_comment_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 6: comment on story as user 1 OK (timestamp t_2 > t_1)
        b, r = self.comment_on_story(comment_body_ok_2, story_id1, token1)

        expected = expected_comment_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 7: comment on story as user 2 OK (timestamp t_3 < t_1)
        b, r = self.comment_on_story(comment_body_ok_3, story_id1, token2)

        expected = expected_comment_ok_3
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 8: get story as user 1 OK (should show both reactions and correct order of comments)
        b, r = self.get_story(story_id1, token1)

        expected = expected_get_public_story_public_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 9: react to story as user 1 OK (dislike)
        b, r = self.react_to_story(reaction_body_dislike, story_id1, token1)

        expected = expected_reaction_ok_user_1_dislike
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 10: react to story as user 2 OK (boring)
        b, r = self.react_to_story(reaction_body_boring, story_id1, token2)

        expected = expected_reaction_ok_user_2_boring
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 11: get story as user 2 OK (should show change in reactions)
        b, r = self.get_story(story_id1, token2)

        expected = expected_get_public_story_public_ok_changed
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xa: delete story as user 1 OK
        b, r = self.delete_story(story_id1, token1)

        expected = expected_delete_story_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xb: delete user1
        b, r = self.delete_user(username1, friendship_delete_myaccount_body_ok_1, token1)

        expected = friendship_expected_delete_account_response_ok_1
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP Xc: delete user2
        b, r = self.delete_user(username2, friendship_delete_myaccount_body_ok_2, token2)

        expected = friendship_expected_delete_account_response_ok_2
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))