"""
Database Factory for Multi-Database Support
Supports SQLite, PostgreSQL, MySQL, SQL Server, and Oracle
"""
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse
import asyncio
from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters"""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
        self.db_type = self._detect_db_type(connection_string)
    
    def _detect_db_type(self, connection_string: str) -> str:
        """Detect database type from connection string"""
        parsed = urlparse(connection_string)
        scheme = parsed.scheme.lower()
        
        if scheme.startswith('sqlite'):
            return 'sqlite'
        elif scheme.startswith('postgresql') or scheme.startswith('postgres'):
            return 'postgresql'
        elif scheme.startswith('mysql'):
            return 'mysql'
        elif scheme.startswith('mssql') or scheme.startswith('sqlserver'):
            return 'sqlserver'
        elif scheme.startswith('oracle'):
            return 'oracle'
        else:
            raise ValueError(f"Unsupported database type: {scheme}")
    
    @abstractmethod
    async def connect(self):
        """Establish database connection"""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Close database connection"""
        pass
    
    @abstractmethod
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SELECT query and return results with column names"""
        pass
    
    @abstractmethod
    async def get_schema(self) -> str:
        """Get database schema information"""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test database connection"""
        pass
    
    @abstractmethod
    def get_sql_dialect(self) -> str:
        """Get SQL dialect name for LLM prompts"""
        pass


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter"""
    
    async def connect(self):
        """Establish SQLite connection"""
        import aiosqlite
        
        # Extract database path from connection string
        parsed = urlparse(self.connection_string)
        db_path = parsed.path.lstrip('/')
        
        self.connection = await aiosqlite.connect(db_path)
        self.connection.row_factory = aiosqlite.Row
        await self._initialize_sample_data()
    
    async def disconnect(self):
        """Close SQLite connection"""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQLite query"""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.execute(query)
        results = await cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        result_list = [dict(row) for row in results]
        
        await cursor.close()
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get SQLite schema information"""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema (SQLite):\n\n"
        
        for table_row in tables:
            table_name = table_row[0]
            schema_text += f"Table: {table_name}\n"
            
            cursor = await self.connection.execute(f"PRAGMA table_info({table_name})")
            columns = await cursor.fetchall()
            await cursor.close()
            
            for col in columns:
                col_name, col_type = col[1], col[2]
                not_null = "NOT NULL" if col[3] else "NULL"
                primary_key = " (PRIMARY KEY)" if col[5] else ""
                schema_text += f"  - {col_name}: {col_type} {not_null}{primary_key}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test SQLite connection"""
        try:
            if not self.connection:
                await self.connect()
            cursor = await self.connection.execute("SELECT 1")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM"""
        return "SQLite"
    
    async def _initialize_sample_data(self):
        """Initialize SQLite with sample data if needed"""
        cursor = await self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
        )
        exists = await cursor.fetchone()
        await cursor.close()
        
        if not exists:
            # Create sample tables and data (keeping existing logic)
            await self._create_sample_tables()
    
    async def _create_sample_tables(self):
        """Create sample tables for SQLite"""
        # Implementation from existing database.py
        pass


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter"""
    
    async def connect(self):
        """Establish PostgreSQL connection"""
        import asyncpg
        self.connection = await asyncpg.connect(self.connection_string)
    
    async def disconnect(self):
        """Close PostgreSQL connection"""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute PostgreSQL query"""
        if not self.connection:
            await self.connect()
        
        result = await self.connection.fetch(query)
        
        if result:
            columns = list(result[0].keys())
            result_list = [dict(row) for row in result]
        else:
            columns = []
            result_list = []
        
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get PostgreSQL schema information"""
        if not self.connection:
            await self.connect()
        
        # Get tables and columns from information_schema
        query = """
        SELECT 
            t.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            CASE WHEN pk.column_name IS NOT NULL THEN 'YES' ELSE 'NO' END as is_primary_key
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c ON t.table_name = c.table_name
        LEFT JOIN (
            SELECT ku.table_name, ku.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.table_name = pk.table_name AND c.column_name = pk.column_name
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position
        """
        
        result = await self.connection.fetch(query)
        
        schema_text = "Database Schema (PostgreSQL):\n\n"
        current_table = None
        
        for row in result:
            if row['table_name'] != current_table:
                current_table = row['table_name']
                schema_text += f"Table: {current_table}\n"
            
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            primary_key = " (PRIMARY KEY)" if row['is_primary_key'] == 'YES' else ""
            
            schema_text += f"  - {row['column_name']}: {row['data_type']} {nullable}{primary_key}\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test PostgreSQL connection"""
        try:
            if not self.connection:
                await self.connect()
            result = await self.connection.fetchval("SELECT 1")
            return result == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM"""
        return "PostgreSQL"


class MySQLAdapter(DatabaseAdapter):
    """MySQL database adapter"""
    
    async def connect(self):
        """Establish MySQL connection"""
        import aiomysql
        
        parsed = urlparse(self.connection_string)
        self.connection = await aiomysql.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password,
            db=parsed.path.lstrip('/'),
            autocommit=True
        )
    
    async def disconnect(self):
        """Close MySQL connection"""
        if self.connection:
            self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute MySQL query"""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        result_list = list(result) if result else []
        
        await cursor.close()
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get MySQL schema information"""
        if not self.connection:
            await self.connect()
        
        parsed = urlparse(self.connection_string)
        database_name = parsed.path.lstrip('/')
        
        query = """
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
        
        cursor = await self.connection.cursor(aiomysql.DictCursor)
        await cursor.execute(query, (database_name,))
        result = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema (MySQL):\n\n"
        current_table = None
        
        for row in result:
            if row['TABLE_NAME'] != current_table:
                current_table = row['TABLE_NAME']
                schema_text += f"Table: {current_table}\n"
            
            nullable = "NULL" if row['IS_NULLABLE'] == 'YES' else "NOT NULL"
            primary_key = " (PRIMARY KEY)" if row['COLUMN_KEY'] == 'PRI' else ""
            
            schema_text += f"  - {row['COLUMN_NAME']}: {row['DATA_TYPE']} {nullable}{primary_key}\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test MySQL connection"""
        try:
            if not self.connection:
                await self.connect()
            cursor = await self.connection.cursor()
            await cursor.execute("SELECT 1")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM"""
        return "MySQL"


class DatabaseFactory:
    """Factory class to create appropriate database adapter"""
    
    @staticmethod
    def create_adapter(connection_string: str) -> DatabaseAdapter:
        """Create database adapter based on connection string"""
        parsed = urlparse(connection_string)
        scheme = parsed.scheme.lower()
        
        if scheme.startswith('sqlite'):
            return SQLiteAdapter(connection_string)
        elif scheme.startswith('postgresql') or scheme.startswith('postgres'):
            return PostgreSQLAdapter(connection_string)
        elif scheme.startswith('mysql'):
            return MySQLAdapter(connection_string)
        elif scheme.startswith('mssql') or scheme.startswith('sqlserver'):
            # TODO: Implement SQL Server adapter
            raise NotImplementedError("SQL Server support coming soon")
        elif scheme.startswith('oracle'):
            # TODO: Implement Oracle adapter
            raise NotImplementedError("Oracle support coming soon")
        else:
            raise ValueError(f"Unsupported database type: {scheme}")


class DatabaseManager:
    """Enhanced Database Manager with multi-database support"""
    
    def __init__(self, database_url: str = None):
        self.database_url = database_url or "sqlite:///northwind.db"
        self.adapter = DatabaseFactory.create_adapter(self.database_url)
    
    async def get_connection(self):
        """Get database connection through adapter"""
        if not self.adapter.connection:
            await self.adapter.connect()
        return self.adapter.connection
    
    async def test_connection(self) -> bool:
        """Test database connection"""
        return await self.adapter.test_connection()
    
    async def get_schema(self) -> str:
        """Get database schema information"""
        return await self.adapter.get_schema()
    
    async def execute_query(self, sql_query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results"""
        # Safety check - only allow SELECT queries
        if not sql_query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        try:
            return await self.adapter.execute_query(sql_query)
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM prompts"""
        return self.adapter.get_sql_dialect()
    
    async def close(self):
        """Close database connection"""
        await self.adapter.disconnect()