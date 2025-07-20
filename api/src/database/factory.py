"""
Database factory for creating appropriate database adapters.
"""
from urllib.parse import urlparse
from .adapters import DatabaseAdapter, SQLiteAdapter, PostgreSQLAdapter, MySQLAdapter


class DatabaseFactory:
    """Factory class to create appropriate database adapter."""
    
    @staticmethod
    def create_adapter(connection_string: str) -> DatabaseAdapter:
        """Create database adapter based on connection string."""
        parsed = urlparse(connection_string)
        scheme = parsed.scheme.lower()
        
        if scheme.startswith('sqlite'):
            return SQLiteAdapter(connection_string)
        elif scheme.startswith('postgresql') or scheme.startswith('postgres'):
            return PostgreSQLAdapter(connection_string)
        elif scheme.startswith('mysql'):
            return MySQLAdapter(connection_string)
        elif scheme.startswith('mssql') or scheme.startswith('sqlserver'):
            # TODO: Implement SQL Server adapter
            raise NotImplementedError("SQL Server support coming soon")
        elif scheme.startswith('oracle'):
            # TODO: Implement Oracle adapter
            raise NotImplementedError("Oracle support coming soon")
        else:
            raise ValueError(f"Unsupported database type: {scheme}")
    
    @staticmethod
    def get_supported_databases():
        """Get information about supported database types."""
        return {
            "SQLite": {
                "driver": "aiosqlite",
                "features": {
                    "case_insensitive_search": False,
                    "limit_syntax": "LIMIT",
                    "supports_schemas": False,
                    "file_based": True
                },
                "example_url": "sqlite:///database.db"
            },
            "PostgreSQL": {
                "driver": "asyncpg",
                "features": {
                    "case_insensitive_search": True,  # ILIKE support
                    "limit_syntax": "LIMIT",
                    "supports_schemas": True,
                    "file_based": False
                },
                "example_url": "postgresql://user:password@host:port/database"
            },
            "MySQL": {
                "driver": "aiomysql",
                "features": {
                    "case_insensitive_search": False,  # Use LOWER() function
                    "limit_syntax": "LIMIT",
                    "supports_schemas": True,
                    "file_based": False
                },
                "example_url": "mysql://user:password@host:port/database"
            },
            "SQL Server": {
                "driver": "pyodbc",
                "features": {
                    "case_insensitive_search": False,  # Use LOWER() function
                    "limit_syntax": "TOP",
                    "supports_schemas": True,
                    "file_based": False
                },
                "example_url": "mssql://user:password@host:port/database"
            },
            "Oracle": {
                "driver": "cx_Oracle",
                "features": {
                    "case_insensitive_search": False,  # Use UPPER()/LOWER() functions
                    "limit_syntax": "ROWNUM",
                    "supports_schemas": True,
                    "file_based": False
                },
                "example_url": "oracle://user:password@host:port/service"
            }
        }