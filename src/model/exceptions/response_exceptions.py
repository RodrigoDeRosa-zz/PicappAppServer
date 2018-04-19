class ResponseException(Exception):
    """Generic exception, receives a JSON including code and error message"""
    def __init__(self, data):
        self.message = data['message']
        self.error_code = data['code']

    def __str__(self):
        return self.message


class BadRequestException(ResponseException):
    """Exception for code 400"""
    pass


class UnauthorizedException(ResponseException):
    """Exception for code 401"""
    pass


class NotFoundException(ResponseException):
    """Exception for code 404"""
    pass


class ConflictException(ResponseException):
    """Exception for code 409"""
    pass


class InternalServerErrorException(ResponseException):
    """Exception for code 500"""
    pass


class ConnectionFailException(ResponseException):
    """To be thrown on connection to external server failure"""
    def __init__(self):
        super(ConnectionFailException, self).__init__({
            'message': "Failed to connect to external server.",
            'code': 500
        })


class InvalidResponseException(Exception):
    """To be thrown when the data inside the response is not correct."""
    pass
