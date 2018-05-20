#!/usr/bin/env python3

# usage: pytest integration/integration_tests.py
# TODO: add environments other than heroku

import requests
import unittest
import json
from pprint import pprint

from integration.definitions.user_crud import *

HOST = "heroku"
DEBUG_MODE = True
STANDARD_TIMEOUT = 999  # seconds


def get_uri_from_host():
    target_roots = {"heroku": 'https://picapp-app-server.herokuapp.com',
                    "docker": 'localhost:5000',
                    "local": 'localhost:8000'}

    # TODO:for now only heroku is supported
    assert HOST == "heroku"

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

    def test_user_CD(self):
        """STEP 1: signup OK
        STEP 2: signup FAILED(user taken)
        STEP 3: login FAILED(user not found)
        STEP 4: login OK
        STEP 5: delete account FAILED (wrong token)
        STEP 6: delete account FAILED (wrong user)
        STEP 7: delete account OK"""

        # STEP 1: sign up with new valid user (signup OK)
        uri = self.root_uri + "/users/signup"
        b = json.dumps(signup_body)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)

        expected = expected_signup_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 2: sign up with taken user (signup FAILED(taken))
        uri = self.root_uri + "/users/signup"
        r = requests.post(uri,
                          data=json.dumps(signup_body),
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)

        expected = expected_signup_response_already_taken
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 3: login with non existant user (login FAILED(not found))
        uri = self.root_uri + "/users/login"
        b = json.dumps(login_body_not_found)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)

        expected = expected_login_response_not_found
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 4: login with valid user (login OK)
        uri = self.root_uri + "/users/login"
        b = json.dumps(login_body_ok)
        r = requests.post(uri,
                          data=b,
                          headers={'Content-Type': 'Application/json'},
                          timeout=STANDARD_TIMEOUT)

        expected = expected_login_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # IMPORTANT: KEEP THE TOKEN
        token = str(r.json()['token']['token'])

        # STEP 5: try to delete account but wrong token (delete account FAILED(wrong token))
        uri = self.root_uri + "/users/{}/myaccount".format(login_body_ok['username'])
        print("uri is "+uri+"\n")
        b = json.dumps(delete_myaccount_body_ok)
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': str(int(token)+1)},
                            timeout=STANDARD_TIMEOUT)

        expected = expected_delete_account_response_wrong_token
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 6: delete account FAILED (wrong user)
        uri = self.root_uri + "/users/{}/myaccount".format(login_body_ok['username']+"asd")
        b = json.dumps(delete_myaccount_body_ok)
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': token},
                            timeout=STANDARD_TIMEOUT)

        expected = expected_delete_account_response_wrong_user
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))

        # STEP 7: successfully delete account (delete account OK)
        uri = self.root_uri + "/users/{}/myaccount".format(login_body_ok['username'])
        b = json.dumps(delete_myaccount_body_ok)
        r = requests.delete(uri,
                            data=b,
                            headers={'Content-Type': 'Application/json',
                                     'token': token},
                            timeout=STANDARD_TIMEOUT)

        expected = expected_delete_account_response_ok
        self.assertEqual(r.status_code, expected['status_code'], get_msg(b, r))
        self.assertEqual(r.json(), expected['body'], get_msg(b, r))
