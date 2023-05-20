from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_404_NOT_FOUND, HTTP_500_INTERNAL_SERVER_ERROR

class InvalidInputException(HTTPException):
    def __init__(self, detail: str):
        super().__init__(status_code=HTTP_400_BAD_REQUEST, detail=detail)

class UserNotFoundException(HTTPException):
    def __init__(self, username: str):
        detail = f"User with username '{username}' not found"
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=detail)

class DatabaseException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=HTTP_500_INTERNAL_SERVER_ERROR, detail=message)

class AutoCompleteException(HTTPException):
    def __init__(slef, message:str):
        super().__init__(status_code=HTTP_404_NOT_FOUND, detail=message)


def handle_exception(request: Request, exception: Exception) -> JSONResponse:
    status_code = 500
    error = "Internal Server Error"
    message = str(exception)

    if hasattr(exception, "status_code"):
        status_code = exception.status_code
        if hasattr(exception, "detail"):
            message = exception.detail
    elif hasattr(exception, "status"):
        status_code = exception.status
        if hasattr(exception, "message"):
            message = exception.message

    error_response = ErrorResponseModel(error=error, code=status_code, message=message)
    return JSONResponse(status_code=status_code, content=error_response.dict())