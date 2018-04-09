post_token_response_mock = {
    'metadata': {
        'version': 'v1.0.1'
    },
    'token': {
        'token': "asd", 'expiresAt': 1546311600
    }
}

bad_request_mock = {
    'code': 400,
    'message': 'Missing username!'
}

internal_error_mock = {
    'code': 500,
    'message': 'Failed to do some internal magic!'
}

unauthorized_mock = {
    'code': 401,
    'message': 'Invalid credentials!'
}

