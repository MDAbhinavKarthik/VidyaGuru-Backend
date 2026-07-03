"""
Exception Handlers for FastAPI Application

Centralizes exception handling for VidyaGuru API errors.
Registers handlers to convert exceptions to proper HTTP responses.

Usage in main.py:
    from core.handlers import setup_exception_handlers
    
    app = FastAPI()
    setup_exception_handlers(app)
"""

from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
import logging

from core.exceptions import VidyaGuruException
from core.error_codes import ErrorCodeRegistry


logger = logging.getLogger(__name__)


def setup_exception_handlers(app: FastAPI) -> None:
    """
    Register all exception handlers with FastAPI app.
    
    Handles:
    - VidyaGuruException and all subclasses
    - Generic Exception (logs and returns generic error)
    """
    
    @app.exception_handler(VidyaGuruException)
    async def vidyaguru_exception_handler(
        request: Request,
        exc: VidyaGuruException
    ) -> JSONResponse:
        """
        Handle all VidyaGuru custom exceptions.
        Converts to structured JSON response with appropriate HTTP status.
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder({
                "error": exc.error_code or exc.__class__.__name__,
                "message": exc.message,
                "status_code": exc.status_code,
                "details": exc.details,
            })
        )
    
    @app.exception_handler(Exception)
    async def general_exception_handler(
        request: Request,
        exc: Exception
    ) -> JSONResponse:
        """
        Handle unexpected exceptions.
        Logs error and returns generic error response to avoid leaking details.
        """
        logger.error(
            f"Unhandled exception: {exc.__class__.__name__}",
            exc_info=True,
            extra={
                "request_url": str(request.url),
                "request_method": request.method,
            }
        )
        
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder({
                "error": "INTERNAL_SERVER_ERROR",
                "message": "An unexpected error occurred. Please try again or contact support.",
                "status_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
            })
        )


def get_error_response(error_code: str, **kwargs) -> dict:
    """
    Helper function to generate standardized error response.
    
    Usage:
        response = get_error_response(
            ErrorCode.USER_NOT_FOUND,
            details={"user_id": 123}
        )
    """
    status_code, message = ErrorCodeRegistry.get_all(error_code)
    
    return {
        "error": error_code,
        "message": message,
        "status_code": status_code,
        "details": kwargs.get("details", {}),
    }
