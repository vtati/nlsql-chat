import asyncpg
import asyncio
import os
from typing import List, Dict, Any, Tuple

class DatabaseManager:
    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv("DATABASE_URL")
        self.connection = None
    
    async def get_connection(self):
        """Get database connection"""
        if not self.connection:
            self.connection = await asyncpg.connect(self.database_url)
        return self.connection
    
    async def test_connection(self):
        """Test database connection"""
        conn = await self.get_connection()
        result = await conn.fetchval("SELECT 1")
        return result
    
    async def get_schema(self) -> str:
        """Get database schema information for PostgreSQL"""
        conn = await self.get_connection()
        
        # Get all tables and their columns from PostgreSQL information_schema
        query = """
        SELECT 
            t.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            CASE WHEN pk.column_name IS NOT NULL THEN 'PRIMARY KEY' ELSE NULL END as constraint_type
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c ON t.table_name = c.table_name
        LEFT JOIN (
            SELECT ku.table_name, ku.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.table_name = pk.table_name AND c.column_name = pk.column_name
        WHERE t.table_schema = 'public' 
            AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position;
        """
        
        results = await conn.fetch(query)
        
        # Format schema information
        schema_text = "Database Schema:\n\n"
        current_table = None
        
        for row in results:
            if row['table_name'] != current_table:
                if current_table is not None:
                    schema_text += "\n"
                current_table = row['table_name']
                schema_text += f"Table: {current_table}\n"
            
            constraint_info = f" ({row['constraint_type']})" if row['constraint_type'] else ""
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            default = f" DEFAULT {row['column_default']}" if row['column_default'] else ""
            
            schema_text += f"  - {row['column_name']}: {row['data_type']} {nullable}{default}{constraint_info}\n"
        
        return schema_text
    
    async def execute_query(self, sql_query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results"""
        # Safety check - only allow SELECT queries for MVP
        if not sql_query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        conn = await self.get_connection()
        
        try:
            results = await conn.fetch(sql_query)
            
            # Get column names
            columns = list(results[0].keys()) if results else []
            
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
        # Connections should be closed explicitly with await
        pass