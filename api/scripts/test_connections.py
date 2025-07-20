"""
Database connection testing utility.
"""
import asyncio
import sys
from pathlib import Path

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.database.manager import DatabaseManager
from src.database.factory import DatabaseFactory
from src.core.settings import settings
from src.utils.logging import get_logger

logger = get_logger(__name__)


async def test_database_connection(db_url: str, db_name: str) -> bool:
    """Test a specific database connection."""
    print(f"\n{'='*50}")
    print(f"Testing {db_name}")
    print(f"URL: {db_url}")
    print(f"{'='*50}")
    
    try:
        # Create database manager
        db_manager = DatabaseManager(db_url)
        
        # Test connection
        print("1. Testing connection...")
        connection_ok = await db_manager.test_connection()
        if connection_ok:
            print("   ✅ Connection successful")
        else:
            print("   ❌ Connection failed")
            return False
        
        # Test schema detection
        print("2. Testing schema detection...")
        schema = await db_manager.get_schema()
        if schema and len(schema) > 50:
            print("   ✅ Schema detection successful")
            print(f"   📋 Schema preview (first 200 chars):")
            print(f"   {schema[:200]}...")
        else:
            print("   ❌ Schema detection failed or empty")
            return False
        
        # Test SQL dialect detection
        print("3. Testing SQL dialect detection...")
        dialect = db_manager.get_sql_dialect()
        print(f"   ✅ Detected dialect: {dialect}")
        
        # Test simple query execution
        print("4. Testing query execution...")
        try:
            results, columns = await db_manager.execute_query("SELECT 1 as test_column")
            if results and len(results) > 0:
                print("   ✅ Query execution successful")
                print(f"   📊 Result: {results[0]}")
            else:
                print("   ❌ Query execution returned no results")
                return False
        except Exception as e:
            print(f"   ❌ Query execution failed: {str(e)}")
            return False
        
        # Close connection
        await db_manager.close()
        print("5. Connection closed successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing {db_name}: {str(e)}")
        return False


async def test_current_database():
    """Test the currently configured database."""
    print("🔍 Testing Current Database Configuration")
    print("=" * 60)
    
    db_url = settings.database.url
    return await test_database_connection(db_url, "Current Configuration")


def print_supported_databases():
    """Print information about supported databases."""
    print("\n📚 Supported Database Types")
    print("=" * 60)
    
    supported = DatabaseFactory.get_supported_databases()
    
    for db_type, info in supported.items():
        print(f"\n{db_type}:")
        print(f"  Driver: {info['driver']}")
        print(f"  Example URL: {info['example_url']}")
        print("  Features:")
        for feature, supported_flag in info['features'].items():
            status = "✅" if supported_flag else "❌"
            print(f"    {status} {feature.replace('_', ' ').title()}")


async def main():
    """Main testing function."""
    print("🚀 Database Connection Tester")
    print("=" * 60)
    
    # Print supported databases
    print_supported_databases()
    
    # Test current database
    current_success = await test_current_database()
    
    # Print summary
    print("\n📊 Test Summary")
    print("=" * 60)
    print(f"Current Database: {'✅ PASS' if current_success else '❌ FAIL'}")
    
    if current_success:
        print("🎉 Database connection test passed!")
    else:
        print("⚠️  Database connection test failed. Check your configuration.")


if __name__ == "__main__":
    asyncio.run(main())