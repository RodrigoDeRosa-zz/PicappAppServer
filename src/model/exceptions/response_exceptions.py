class ResponseException(Exception):
    """Generic exception, receives a JSON including code and error message"""
    def __init__(self, data):
        self.message = data['message']

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


class InvalidResponseException(Exception):
    """To be thrown when the data inside the response is not correct."""
    pass