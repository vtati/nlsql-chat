"""
Multi-Database Connection Testing Utility
Test connections to different database types and verify schema detection
"""
import asyncio
import os
from dotenv import load_dotenv
from database_factory import DatabaseManager, DatabaseFactory
from config import DatabaseConfig

load_dotenv()


async def test_database_connection(db_url: str, db_name: str):
    """Test a specific database connection"""
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
        if schema and len(schema) > 50:  # Basic validation
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
            # Try a simple query that should work on most databases
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


async def test_sample_databases():
    """Test all predefined sample databases"""
    print("🔍 Testing Sample Databases")
    print("=" * 60)
    
    results = {}
    
    for db_key, db_config in DatabaseConfig.SAMPLE_DATABASES.items():
        success = await test_database_connection(
            db_config["url"], 
            f"{db_key} ({db_config['description']})"
        )
        results[db_key] = success
    
    return results


async def test_current_database():
    """Test the currently configured database"""
    print("🔍 Testing Current Database Configuration")
    print("=" * 60)
    
    db_url = DatabaseConfig.get_database_url()
    return await test_database_connection(db_url, "Current Configuration")


async def test_custom_database(db_url: str):
    """Test a custom database URL"""
    print("🔍 Testing Custom Database")
    print("=" * 60)
    
    return await test_database_connection(db_url, "Custom Database")


def print_supported_databases():
    """Print information about supported databases"""
    print("\n📚 Supported Database Types")
    print("=" * 60)
    
    supported = DatabaseConfig.get_supported_databases()
    
    for db_type, info in supported.items():
        print(f"\n{db_type}:")
        print(f"  Driver: {info['driver']}")
        print(f"  Example URL: {info['example_url']}")
        print("  Features:")
        for feature, supported in info['features'].items():
            status = "✅" if supported else "❌"
            print(f"    {status} {feature.replace('_', ' ').title()}")


async def main():
    """Main testing function"""
    print("🚀 Multi-Database Connection Tester")
    print("=" * 60)
    
    # Print supported databases
    print_supported_databases()
    
    # Test current database
    current_success = await test_current_database()
    
    # Test sample databases
    sample_results = await test_sample_databases()
    
    # Print summary
    print("\n📊 Test Summary")
    print("=" * 60)
    print(f"Current Database: {'✅ PASS' if current_success else '❌ FAIL'}")
    
    print("\nSample Databases:")
    for db_name, success in sample_results.items():
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"  {db_name}: {status}")
    
    total_tests = 1 + len(sample_results)
    passed_tests = (1 if current_success else 0) + sum(sample_results.values())
    
    print(f"\nOverall: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("🎉 All database tests passed!")
    else:
        print("⚠️  Some database tests failed. Check your configuration.")


if __name__ == "__main__":
    # Handle command line arguments for custom testing
    import sys
    
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
        print(f"Testing custom database URL: {custom_url}")
        asyncio.run(test_custom_database(custom_url))
    else:
        asyncio.run(main())