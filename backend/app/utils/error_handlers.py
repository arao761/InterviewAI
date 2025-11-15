"""
Error handlers for PrepWise application.
"""
from fastapi import Request
from fastapi.responses import JSONResponse
from app.utils.exceptions import PrepWiseException
from app.core.logging import logger


async def prepwise_exception_handler(request: Request, exc: PrepWiseException):
    """Handle PrepWise custom exceptions."""
    logger.error(f"PrepWise exception: {exc.message}")
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": "PrepWise Error", "message": exc.message}
    )


async def general_exception_handler(request: Request, exc: Exception):
    """Handle general exceptions."""
    logger.error(f"Unhandled exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={"error": "Internal Server Error", "message": "Something went wrong"}
    )