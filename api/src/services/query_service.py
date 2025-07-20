"""
Query processing service.
"""
import time
from typing import Tuple, List, Dict, Any
from ..database.manager import DatabaseManager
from .llm_service import LLMService
from ..models.query_models import QueryRequest, QueryResponse


class QueryService:
    """Service for processing natural language queries."""
    
    def __init__(self, db_manager: DatabaseManager, llm_service: LLMService):
        self.db_manager = db_manager
        self.llm_service = llm_service
    
    async def process_query(self, request: QueryRequest) -> QueryResponse:
        """Process a natural language query and return results."""
        start_time = time.time()
        
        try:
            # Get database schema if not provided
            schema = request.schema
            if not schema:
                schema = await self.db_manager.get_schema()
            
            # Generate SQL using LLM with database-specific dialect
            sql_dialect = self.db_manager.get_sql_dialect()
            sql_query = await self.llm_service.generate_sql(
                request.question, 
                schema, 
                sql_dialect
            )
            
            # Execute query
            results, columns = await self.db_manager.execute_query(sql_query)
            
            # Calculate execution time
            execution_time_ms = (time.time() - start_time) * 1000
            
            return QueryResponse(
                sql_query=sql_query,
                results=results,
                columns=columns,
                row_count=len(results),
                execution_time_ms=round(execution_time_ms, 2)
            )
            
        except Exception as e:
            raise Exception(f"Query processing error: {str(e)}")
    
    async def get_database_schema(self) -> str:
        """Get the current database schema."""
        return await self.db_manager.get_schema()
    
    async def test_database_connection(self) -> bool:
        """Test the database connection."""
        return await self.db_manager.test_connection()
    
    def get_database_info(self) -> Dict[str, Any]:
        """Get database information."""
        return self.db_manager.get_database_info()