"""
API routes for the Natural Language to SQL application.
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from ..models.query_models import (
    QueryRequest, 
    QueryResponse, 
    DatabaseInfo, 
    SchemaResponse, 
    HealthResponse
)
from ..services.query_service import QueryService
from ..database.manager import DatabaseManager
from ..services.llm_service import LLMService
from ..core.settings import settings

# Create router
router = APIRouter()

# Dependency injection
def get_database_manager() -> DatabaseManager:
    """Get database manager instance."""
    return DatabaseManager(settings.database.url)

def get_llm_service() -> LLMService:
    """Get LLM service instance."""
    return LLMService()

def get_query_service(
    db_manager: DatabaseManager = Depends(get_database_manager),
    llm_service: LLMService = Depends(get_llm_service)
) -> QueryService:
    """Get query service instance."""
    return QueryService(db_manager, llm_service)


@router.get("/", summary="Root endpoint")
async def root():
    """Root endpoint returning API information."""
    return {
        "message": "Natural Language to SQL API",
        "version": settings.api.version,
        "description": "Convert natural language questions to SQL queries",
        "status": "running",
        "environment": settings.environment,
        "endpoints": {
            "health": "/health",
            "query": "/query", 
            "schema": "/schema",
            "database_info": "/database-info",
            "docs": "/docs"
        }
    }


@router.post("/query", response_model=QueryResponse, summary="Execute natural language query")
async def execute_query(
    request: QueryRequest,
    query_service: QueryService = Depends(get_query_service)
):
    """
    Execute a natural language query against the database.
    
    - **question**: Natural language question to convert to SQL
    - **schema**: Optional database schema override
    """
    try:
        return await query_service.process_query(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/schema", response_model=SchemaResponse, summary="Get database schema")
async def get_schema(query_service: QueryService = Depends(get_query_service)):
    """
    Get the current database schema information.
    """
    try:
        schema = await query_service.get_database_schema()
        
        # Extract table names from schema
        tables = []
        for line in schema.split('\n'):
            if line.startswith('Table: '):
                table_name = line.replace('Table: ', '').strip()
                tables.append(table_name)
        
        return SchemaResponse(
            schema=schema,
            tables=tables,
            last_updated=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/database-info", response_model=DatabaseInfo, summary="Get database information")
async def get_database_info(query_service: QueryService = Depends(get_query_service)):
    """
    Get information about the connected database including type and supported features.
    """
    try:
        info = query_service.get_database_info()
        return DatabaseInfo(**info)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/health", response_model=HealthResponse, summary="Health check")
async def health_check(query_service: QueryService = Depends(get_query_service)):
    """
    Check the health status of the API and database connection.
    """
    try:
        connection_status = await query_service.test_database_connection()
        db_info = query_service.get_database_info()
        
        return HealthResponse(
            status="healthy" if connection_status else "unhealthy",
            database="connected" if connection_status else "disconnected",
            database_type=db_info["database_type"],
            version=settings.api.version,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )
    except Exception as e:
        return HealthResponse(
            status="unhealthy",
            database="error",
            database_type="unknown",
            version=settings.api.version,
            timestamp=datetime.utcnow().isoformat() + "Z"
        )