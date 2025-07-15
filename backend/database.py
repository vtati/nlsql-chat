import aiosqlite
import asyncio
import os
from typing import List, Dict, Any, Tuple

class DatabaseManager:
    def __init__(self, database_url: str = None):
        # Use SQLite for simplicity - extract path from URL or use default
        if database_url and database_url.startswith('sqlite:///'):
            self.db_path = database_url.replace('sqlite:///', '')
        else:
            self.db_path = 'sample_database.db'
        self.connection = None
    
    async def get_connection(self):
        """Get database connection"""
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
            self.connection.row_factory = aiosqlite.Row
        return self.connection
    
    async def test_connection(self):
        """Test database connection"""
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT 1")
        result = await cursor.fetchone()
        await cursor.close()
        return result[0] if result else None
    
    async def get_schema(self) -> str:
        """Get database schema information"""
        conn = await self.get_connection()
        
        # Get all tables
        cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema:\n\n"
        
        for table_row in tables:
            table_name = table_row[0]
            schema_text += f"Table: {table_name}\n"
            
            # Get column information for each table
            cursor = await conn.execute(f"PRAGMA table_info({table_name})")
            columns = await cursor.fetchall()
            await cursor.close()
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else "NULL"
                default_val = f" DEFAULT {col[4]}" if col[4] else ""
                primary_key = " (PRIMARY KEY)" if col[5] else ""
                
                schema_text += f"  - {col_name}: {col_type} {not_null}{default_val}{primary_key}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    async def execute_query(self, sql_query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results"""
        # Safety check - only allow SELECT queries for MVP
        if not sql_query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        conn = await self.get_connection()
        
        try:
            cursor = await conn.execute(sql_query)
            results = await cursor.fetchall()
            await cursor.close()
            
            # Get column names from cursor description
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert to list of dictionaries
            result_list = [dict(row) for row in results]
            
            return result_list, columns
            
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
    
    def __del__(self):
        # SQLite connections should be closed explicitly with await
        pass