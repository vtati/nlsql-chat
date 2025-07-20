"""
Simplified settings that directly use environment variables
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from config/.env
config_dir = Path(__file__).parent.parent.parent / "config"
env_file = config_dir / ".env"
load_dotenv(env_file)

# Simple settings class
class Settings:
    def __init__(self):
        # Database settings
        self.database_url = os.getenv("DATABASE_URL", "sqlite:///northwind.db")
        
        # OpenAI settings
        self.openai_api_key = os.getenv("OPENAI_API_KEY")
        if not self.openai_api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        # API settings
        self.api_host = os.getenv("API_HOST", "0.0.0.0")
        self.api_port = int(os.getenv("API_PORT", "8000"))
        self.api_title = "Natural Language to SQL API"
        self.api_version = "2.0.0"
        self.api_description = "Enhanced Natural Language to SQL API with multi-database support"
        
        # CORS settings
        self.cors_origins = [
            "http://localhost:3000",
            "https://*.vercel.app",
            "*"
        ]
        
        # LLM settings
        self.llm_primary_model = os.getenv("LLM_PRIMARY_MODEL", "gpt-4")
        self.llm_fallback_model = os.getenv("LLM_FALLBACK_MODEL", "gpt-3.5-turbo")
        self.llm_temperature = float(os.getenv("LLM_TEMPERATURE", "0.0"))
        self.llm_max_tokens = int(os.getenv("LLM_MAX_TOKENS", "300"))

# Global settings instance
settings = Settings()