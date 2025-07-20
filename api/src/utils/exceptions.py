"""
Custom exceptions for the application.
"""


class NLSQLException(Exception):
    """Base exception for Natural Language to SQL application."""
    pass


class DatabaseConnectionError(NLSQLException):
    """Raised when database connection fails."""
    pass


class QueryGenerationError(NLSQLException):
    """Raised when LLM query generation fails."""
    pass


class QueryExecutionError(NLSQLException):
    """Raised when SQL query execution fails."""
    pass


class UnsupportedDatabaseError(NLSQLException):
    """Raised when database type is not supported."""
    pass


class InvalidQueryError(NLSQLException):
    """Raised when query is invalid or unsafe."""
    pass


class ConfigurationError(NLSQLException):
    """Raised when application configuration is invalid."""
    pass