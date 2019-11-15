# pylint: disable=C0114

from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    """
    Error raised when a user is not permitted to take an action
    """
    code = 403
    message = "Access Forbidden"


class Value_Error(HTTPException):
    # pylint: disable=C0103
    """
    Error raised when a value is missing or incorrect in some way.
    Renamed to Value_Error to avoid clashing with python's builtin
    ValueError.
    """
    code = 400
    message = "Incorrect value"
