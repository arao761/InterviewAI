"""
Custom exceptions for PrepWise application.
"""

class PrepWiseException(Exception):
    """Base exception for PrepWise application."""
    def __init__(self, message: str = "An error occurred in PrepWise", status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)