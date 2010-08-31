class OpenInviterException(Exception):
    pass

class InvalidService(OpenInviterException):
    pass

class LoginFailed(OpenInviterException):
    pass