# ================================
# src/utils/exceptions.py
# ================================
"""Custom exceptions for the application."""

class AppError(Exception):
    """Base application error."""
    pass

class ModelError(AppError):
    """Model-related errors."""
    pass

class APIError(AppError):
    """API-related errors."""
    pass

class ValidationError(AppError):
    """Validation errors."""
    pass

class ConfigurationError(AppError):
    """Configuration errors."""
    pass