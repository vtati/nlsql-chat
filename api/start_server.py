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
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )