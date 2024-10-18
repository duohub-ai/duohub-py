class DuohubError(Exception):
    """Base exception for Duohub errors"""
    pass

class APIError(DuohubError):
    """Raised when the API returns an error"""
    pass

class AuthenticationError(DuohubError):
    """Raised when there's an authentication problem"""
    pass

class ValidationError(DuohubError):
    """Raised when the data doesn't meet the expected format or constraints"""
    pass

class MissingFieldError(ValidationError):
    """Raised when a required field is missing from the data"""
    pass

class InvalidDataTypeError(ValidationError):
    """Raised when a field has an incorrect data type"""
    pass

class OutOfRangeError(ValidationError):
    """Raised when a numeric value is outside the acceptable range"""
    pass
