class ExpectedResponse(object):

    def __init__(self, expected_body, expected_status_code, expected_headers=None):
        """Expected body/headers must be dictionaries which to comply as response body/headers.
        Expected status code must be a number of HTTP code expected."""
        self.body = expected_body
        self.code = expected_status_code
        self.headers = expected_headers

    def matches(self, body, code, headers=None):
        body_ok = self.body == body if self.body else True
        code_ok = self.code == code if self.code else True
        headers_ok = self.headers == headers if self.headers else True
        return body_ok and code_ok and headers_ok


class NotNonePlaceholder(object):
    """only check that object is not None"""
    def __eq__(self, other):
        return other is not None


def expected_response(body, status_code, headers=None):
    return {'body': body, 'status_code': status_code, 'headers': headers}


def expected_error_response(status_code):
    return expected_response({
        "status_code": status_code,
        "message": NotNonePlaceholder()
    }, status_code)


test_user1 = {
    "username": "integration_user14",
    "password": "password1"
}

test_user2 = {
    "username": "integration_test_usr2_4",
    "password": "password2"
}

bad_request_response_body = {
    "status_code": 400,
    "message": NotNonePlaceholder()
}

unauthorized_response_body = {
    "status_code": 403,
    "message": NotNonePlaceholder()
}


