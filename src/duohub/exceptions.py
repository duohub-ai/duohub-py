class DuohubError(Exception):
    """Base exception for Duohub errors"""
    pass

class APIError(DuohubError):
    """Raised when the API returns an error"""
    pass

class AuthenticationError(DuohubError):
    """Raised when there's an authentication problem"""
    pass