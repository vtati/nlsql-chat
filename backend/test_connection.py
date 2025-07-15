#!/usr/bin/env python3
"""
Test script to verify database connection and basic functionality
"""
import asyncio
import os
from dotenv import load_dotenv
from database import DatabaseManager

load_dotenv()

async def test_database():
    """Test database connection and schema retrieval"""
    print("Testing database connection...")
    
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        print("❌ DATABASE_URL not found in environment variables")
        return False
    
    print(f"Database URL: {db_url}")
    
    try:
        db_manager = DatabaseManager(db_url)
        
        # Test connection
        print("Testing connection...")
        result = await db_manager.test_connection()
        print("✅ Database connection successful")
        
        # Test schema retrieval
        print("Retrieving schema...")
        schema = await db_manager.get_schema()
        print("✅ Schema retrieved successfully")
        print(f"Schema preview (first 500 chars):\n{schema[:500]}...")
        
        # Test a simple query
        print("Testing simple query...")
        results, columns = await db_manager.execute_query("SELECT 1 as test_column")
        print(f"✅ Query executed successfully. Results: {results}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {str(e)}")
        return False

def test_openai_key():
    """Test OpenAI API key presence"""
    print("Testing OpenAI API key...")
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured. Please update .env file")
        return False
    
    print("✅ OpenAI API key found")
    return True

async def main():
    print("=== Natural Language to SQL - Setup Test ===\n")
    
    # Test OpenAI key
    openai_ok = test_openai_key()
    print()
    
    # Test database
    db_ok = await test_database()
    print()
    
    if db_ok and openai_ok:
        print("🎉 All tests passed! Your setup is ready.")
    elif db_ok:
        print("⚠️  Database is working, but you need to configure OpenAI API key")
    else:
        print("❌ Setup incomplete. Please check the errors above.")

if __name__ == "__main__":
    asyncio.run(main())