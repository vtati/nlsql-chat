"""
Database setup utility for initializing sample data.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.manager import DatabaseManager
from src.core.settings import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


async def setup_database(db_url: str = None) -> bool:
    """Setup database with sample data."""
    if not db_url:
        db_url = settings.database.url
    
    print(f"🚀 Setting up database: {db_url}")
    
    try:
        # Create database manager
        db_manager = DatabaseManager(db_url)
        
        # Test connection first
        print("1. Testing connection...")
        if not await db_manager.test_connection():
            print("❌ Cannot connect to database")
            return False
        print("✅ Connection successful")
        
        # Get schema to verify setup
        print("2. Checking existing schema...")
        schema = await db_manager.get_schema()
        if schema and "customers" in schema.lower():
            print("✅ Database already contains sample data")
            print(f"📋 Schema preview:\n{schema[:300]}...")
            return True
        
        # For SQLite, the adapter will automatically create sample data
        if db_manager.get_sql_dialect() == "SQLite":
            print("3. SQLite detected - sample data will be created automatically")
            # Trigger connection to initialize data
            await db_manager.get_connection()
            
            # Verify setup
            schema = await db_manager.get_schema()
            if schema and len(schema) > 100:
                print("✅ Database setup completed successfully")
                print(f"📋 Schema preview:\n{schema[:300]}...")
                return True
            else:
                print("❌ Database setup verification failed")
                return False
        else:
            print("3. Non-SQLite database detected")
            print("⚠️  Manual setup required for production databases")
            print("   Please create tables and insert sample data manually")
            return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    finally:
        if 'db_manager' in locals():
            await db_manager.close()


async def main():
    """Main setup function."""
    print("🔧 Database Setup Utility")
    print("=" * 50)
    
    # Setup current database
    success = await setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the application with this database.")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your database configuration and try again.")


if __name__ == "__main__":
    asyncio.run(main())