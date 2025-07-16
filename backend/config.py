"""
Configuration management for multi-database support
"""
import os
from typing import Dict, Any
from dotenv import load_dotenv

load_dotenv()


class DatabaseConfig:
    """Database configuration management"""
    
    # Predefined database configurations for easy switching
    SAMPLE_DATABASES = {
        "sqlite_local": {
            "url": "sqlite:///northwind.db",
            "description": "Local SQLite database with sample data",
            "requires_setup": True
        },
        "postgresql_demo": {
            "url": "postgresql://readonly:readonly@postgres.demo.com:5432/northwind",
            "description": "Demo PostgreSQL database (read-only)",
            "requires_setup": False
        },
        "mysql_demo": {
            "url": "mysql://demo:demo@mysql.demo.com:3306/northwind",
            "description": "Demo MySQL database (read-only)",
            "requires_setup": False
        }
    }
    
    @staticmethod
    def get_database_url() -> str:
        """Get database URL from environment or use default"""
        return os.getenv("DATABASE_URL", DatabaseConfig.SAMPLE_DATABASES["sqlite_local"]["url"])
    
    @staticmethod
    def get_openai_api_key() -> str:
        """Get OpenAI API key from environment"""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        return api_key
    
    @staticmethod
    def get_supported_databases() -> Dict[str, Any]:
        """Get list of supported database types and their features"""
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


class AppConfig:
    """Application configuration"""
    
    # API Configuration
    API_TITLE = "Natural Language to SQL API"
    API_VERSION = "2.0.0"
    API_DESCRIPTION = """
    Enhanced Natural Language to SQL API with multi-database support.
    
    Supported databases:
    - SQLite (development)
    - PostgreSQL (production)
    - MySQL/MariaDB (production)
    - SQL Server (enterprise)
    - Oracle (enterprise)
    """
    
    # CORS Configuration
    CORS_ORIGINS = [
        "http://localhost:3000",  # React dev server
        "https://*.vercel.app",   # Vercel deployments
        "*"  # Allow all origins for development
    ]
    
    # Query Configuration
    MAX_QUERY_RESULTS = 1000
    QUERY_TIMEOUT_SECONDS = 30
    
    # LLM Configuration
    DEFAULT_LLM_MODEL = "gpt-4"
    FALLBACK_LLM_MODEL = "gpt-3.5-turbo"
    LLM_TEMPERATURE = 0.0
    LLM_MAX_TOKENS = 300
    
    @staticmethod
    def get_cors_origins():
        """Get CORS origins from environment or use defaults"""
        env_origins = os.getenv("CORS_ORIGINS")
        if env_origins:
            return env_origins.split(",")
        return AppConfig.CORS_ORIGINS
    
    @staticmethod
    def is_development() -> bool:
        """Check if running in development mode"""
        return os.getenv("ENVIRONMENT", "development").lower() == "development"
    
    @staticmethod
    def is_production() -> bool:
        """Check if running in production mode"""
        return os.getenv("ENVIRONMENT", "development").lower() == "production"


# Environment-specific configurations
ENVIRONMENT_CONFIGS = {
    "development": {
        "database_url": "sqlite:///northwind.db",
        "debug": True,
        "log_level": "DEBUG"
    },
    "staging": {
        "database_url": os.getenv("STAGING_DATABASE_URL", "postgresql://user:pass@staging-db:5432/nlsql"),
        "debug": False,
        "log_level": "INFO"
    },
    "production": {
        "database_url": os.getenv("PRODUCTION_DATABASE_URL"),
        "debug": False,
        "log_level": "WARNING"
    }
}


def get_config() -> Dict[str, Any]:
    """Get configuration based on current environment"""
    env = os.getenv("ENVIRONMENT", "development").lower()
    config = ENVIRONMENT_CONFIGS.get(env, ENVIRONMENT_CONFIGS["development"])
    
    # Override with environment variables if present
    if os.getenv("DATABASE_URL"):
        config["database_url"] = os.getenv("DATABASE_URL")
    
    return config