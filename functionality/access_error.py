from werkzeug.exceptions import HTTPException


class AccessError(HTTPException):
    code = 403
    message = "Access Forbidden"


class ValueError(HTTPException):
    code = 400
    message = "Incorrect value"
