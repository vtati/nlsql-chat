"""
Test health endpoint directly
"""
import os
import sys
import asyncio
from pathlib import Path
from dotenv import load_dotenv

# Add current directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Load environment variables
config_dir = Path(__file__).parent / "config"
env_file = config_dir / ".env"
load_dotenv(env_file)

async def test_health():
    try:
        print("Testing database manager...")
        from src.database.manager import DatabaseManager
        db_manager = DatabaseManager(os.getenv('DATABASE_URL'))
        
        print("Testing database connection...")
        connection_status = await db_manager.test_connection()
        print(f"Connection status: {connection_status}")
        
        print("Testing LLM service...")
        from src.services.llm_service import LLMService
        llm_service = LLMService()
        print("LLM service created successfully")
        
        print("Testing query service...")
        from src.services.query_service import QueryService
        query_service = QueryService(db_manager, llm_service)
        
        print("Testing health check logic...")
        db_info = query_service.get_database_info()
        print(f"Database info: {db_info}")
        
        print("✅ All components work individually")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_health())