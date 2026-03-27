class BookAppError(Exception):
    """Base exception for book app domain and application errors."""


class ValidationError(BookAppError, ValueError):
    """Raised when user input or data fails validation."""


class NotFoundError(BookAppError):
    """Raised when a requested book or resource does not exist."""


class StorageError(BookAppError):
    """Raised when loading or saving persistent data fails."""
