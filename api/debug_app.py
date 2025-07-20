"""
Debug script to test FastAPI app creation
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
config_dir = Path(__file__).parent / "config"
env_file = config_dir / ".env"
load_dotenv(env_file)

print(f"Database URL: {os.getenv('DATABASE_URL')}")
print(f"OpenAI API Key: {'Configured' if os.getenv('OPENAI_API_KEY') else 'Not found'}")

try:
    print("Testing FastAPI app creation...")
    from src.main import app
    print("✅ FastAPI app created successfully")
    
    print("Testing health endpoint...")
    from src.api.routes import health_check
    print("✅ Health endpoint imported successfully")
    
except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()