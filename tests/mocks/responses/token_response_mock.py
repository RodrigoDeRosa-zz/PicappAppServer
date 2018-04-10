post_token_response_mock = {
    'metadata': {
        'version': 'v1.0.1'
    },
    'token': {
        'token': 'asd',
        'expiresAt': 1546311600
    }
}

token_object_mock = {
    'token': 'asd',
    'expiresAt': 1546311600
}

post_user_response_mock = {
    'metadata': {
        'version': 'v1.0.1'
    },
    'user': {
        'id': 'some-magic-id',
        '_rev': 'some-hash',
        'applicationOwner': 'some-other-id',
        'username': 'martin.errazquin'
    }
}

user_object_mock = {
    'id': 'some-magic-id',
    '_rev': 'some-hash',
    'applicationOwner': 'some-other-id',
    'username': 'salah'
}

missing_username_mock = {
    'code': 400,
    'message': 'Missing username!'
}

missing_password_mock = {
    'code': 400,
    'message': 'Missing password!'
}

internal_error_mock = {
    'code': 500,
    'message': 'Failed to do some internal magic!'
}

unauthorized_mock = {
    'code': 401,
    'message': 'Invalid credentials!'
}

