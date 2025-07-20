"""
Core application settings and configuration management.
"""
import os
from typing import Dict, Any, List
from pydantic import Field
from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from pathlib import Path

# Load .env file from config directory
config_dir = Path(__file__).parent.parent.parent / "config"
env_file = config_dir / ".env"
load_dotenv(env_file)


class DatabaseSettings(BaseSettings):
    """Database configuration settings."""
    
    url: str = Field(default="sqlite:///northwind.db", env="DATABASE_URL")
    max_connections: int = Field(default=10, env="DB_MAX_CONNECTIONS")
    connection_timeout: int = Field(default=30, env="DB_CONNECTION_TIMEOUT")
    query_timeout: int = Field(default=30, env="DB_QUERY_TIMEOUT")
    
    class Config:
        env_prefix = "DATABASE_"


class LLMSettings(BaseSettings):
    """Large Language Model configuration settings."""
    
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    primary_model: str = Field(default="gpt-4", env="LLM_PRIMARY_MODEL")
    fallback_model: str = Field(default="gpt-3.5-turbo", env="LLM_FALLBACK_MODEL")
    temperature: float = Field(default=0.0, env="LLM_TEMPERATURE")
    max_tokens: int = Field(default=300, env="LLM_MAX_TOKENS")
    
    class Config:
        env_prefix = "LLM_"


class APISettings(BaseSettings):
    """API server configuration settings."""
    
    title: str = "Natural Language to SQL API"
    version: str = "2.0.0"
    description: str = """
    Enhanced Natural Language to SQL API with multi-database support.
    
    Supported databases:
    - SQLite (development)
    - PostgreSQL (production)
    - MySQL/MariaDB (production)
    - SQL Server (enterprise)
    - Oracle (enterprise)
    """
    
    host: str = Field(default="0.0.0.0", env="API_HOST")
    port: int = Field(default=8000, env="API_PORT")
    debug: bool = Field(default=False, env="API_DEBUG")
    
    # CORS settings - Updated for production
    cors_origins: List[str] = Field(
        default=[
            "http://localhost:3000",
            "https://nlsql-chat.vercel.app",
            "https://*.vercel.app",
            "https://*.render.com",
            "https://*.onrender.com",
            "*"  # Remove this in production for security
        ],
        env="CORS_ORIGINS"
    )
    
    # Query settings
    max_query_results: int = Field(default=1000, env="MAX_QUERY_RESULTS")
    
    class Config:
        env_prefix = "API_"


class AppSettings(BaseSettings):
    """Main application settings."""
    
    environment: str = Field(default="development", env="ENVIRONMENT")
    log_level: str = Field(default="INFO", env="LOG_LEVEL")
    
    # Component settings - initialized lazily
    _database: DatabaseSettings = None
    _llm: LLMSettings = None
    _api: APISettings = None
    
    @property
    def database(self) -> DatabaseSettings:
        if self._database is None:
            self._database = DatabaseSettings()
        return self._database
    
    @property
    def llm(self) -> LLMSettings:
        if self._llm is None:
            self._llm = LLMSettings()
        return self._llm
    
    @property
    def api(self) -> APISettings:
        if self._api is None:
            self._api = APISettings()
        return self._api
    
    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.environment.lower() == "development"
    
    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.environment.lower() == "production"
    
    class Config:
        case_sensitive = False


# Global settings instance
settings = AppSettings()