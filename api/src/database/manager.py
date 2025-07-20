"""
Database manager for handling database operations.
"""
from typing import Dict, Any, List, Tuple
from .factory import DatabaseFactory
from .adapters import DatabaseAdapter


class DatabaseManager:
    """Enhanced Database Manager with multi-database support."""
    
    def __init__(self, database_url: str):
        self.database_url = database_url
        self.adapter: DatabaseAdapter = DatabaseFactory.create_adapter(database_url)
    
    async def get_connection(self):
        """Get database connection through adapter."""
        if not self.adapter.connection:
            await self.adapter.connect()
        return self.adapter.connection
    
    async def test_connection(self) -> bool:
        """Test database connection."""
        return await self.adapter.test_connection()
    
    async def get_schema(self) -> str:
        """Get database schema information."""
        return await self.adapter.get_schema()
    
    async def execute_query(self, sql_query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results."""
        # Safety check - only allow SELECT queries
        if not sql_query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        try:
            return await self.adapter.execute_query(sql_query)
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM prompts."""
        return self.adapter.get_sql_dialect()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information."""
        # Mask sensitive information in connection string
        masked_url = self.database_url
        if '@' in masked_url:
            parts = masked_url.split('@')
            if len(parts) == 2:
                protocol_and_creds = parts[0]
                host_and_db = parts[1]
                if '://' in protocol_and_creds:
                    protocol = protocol_and_creds.split('://')[0]
                    masked_url = f"{protocol}://***@{host_and_db}"
        else:
            masked_url = "***"
        
        # Get database features
        supported_dbs = DatabaseFactory.get_supported_databases()
        dialect = self.get_sql_dialect()
        features = supported_dbs.get(dialect, {}).get('features', {})
        
        return {
            "database_type": dialect,
            "connection_string_masked": masked_url,
            "supported_features": features
        }
    
    async def close(self):
        """Close database connection."""
        await self.adapter.disconnect()