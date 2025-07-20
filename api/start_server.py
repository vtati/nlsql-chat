"""
Simple server startup script with direct environment loading
"""
import os
import sys
import uvicorn
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables from config/.env
config_dir = Path(__file__).parent / "config"
env_file = config_dir / ".env"
load_dotenv(env_file)

# Verify environment variables are loaded
print(f"Database URL: {os.getenv('DATABASE_URL', 'Not found')}")
print(f"OpenAI API Key: {'Configured' if os.getenv('OPENAI_API_KEY') else 'Not found'}")

if __name__ == "__main__":
    print("Starting Natural Language to SQL API Server...")
    
    # Get port from environment (Render uses PORT env var)
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    host = os.getenv("API_HOST", "0.0.0.0")
    
    # Disable reload in production
    is_production = os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    print(f"Server starting on {host}:{port}")
    print(f"Environment: {os.getenv('ENVIRONMENT', 'development')}")
    print(f"Reload: {not is_production}")
    
    uvicorn.run(
        "src.main:app",
        host=host,
        port=port,
        reload=not is_production
    )