from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from database_factory import DatabaseManager
from llm_service import LLMService

load_dotenv()

app = FastAPI(title="Natural Language to SQL API", version="2.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # React dev server
        "https://*.vercel.app",   # All Vercel deployments
        "*",  # Allow all origins for now - restrict in production
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services with multi-database support
db_manager = DatabaseManager(os.getenv("DATABASE_URL"))
llm_service = LLMService(os.getenv("OPENAI_API_KEY"))

class QueryRequest(BaseModel):
    question: str
    schema: str = ""

class QueryResponse(BaseModel):
    sql_query: str
    results: List[Dict[str, Any]]
    columns: List[str]
    row_count: int

@app.get("/")
async def root():
    return {"message": "Natural Language to SQL API"}

@app.post("/query", response_model=QueryResponse)
async def execute_query(request: QueryRequest):
    try:
        # Get database schema if not provided
        if not request.schema:
            schema = await db_manager.get_schema()
        else:
            schema = request.schema
        
        # Generate SQL using LLM with database-specific dialect
        sql_dialect = db_manager.get_sql_dialect()
        sql_query = await llm_service.generate_sql(request.question, schema, sql_dialect)
        
        # Execute query
        results, columns = await db_manager.execute_query(sql_query)
        
        return QueryResponse(
            sql_query=sql_query,
            results=results,
            columns=columns,
            row_count=len(results)
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/schema")
async def get_schema():
    try:
        schema = await db_manager.get_schema()
        return {"schema": schema}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    try:
        connection_status = await db_manager.test_connection()
        return {
            "status": "healthy" if connection_status else "unhealthy",
            "database": "connected" if connection_status else "disconnected",
            "database_type": db_manager.get_sql_dialect(),
            "version": "2.0.0"
        }
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@app.get("/database-info")
async def get_database_info():
    """Get information about the connected database"""
    try:
        return {
            "database_type": db_manager.get_sql_dialect(),
            "connection_string": db_manager.database_url.split('@')[0] + '@***' if '@' in db_manager.database_url else "***",
            "supported_features": {
                "case_insensitive_search": db_manager.get_sql_dialect() in ["PostgreSQL"],
                "limit_syntax": "LIMIT" if db_manager.get_sql_dialect() != "SQL Server" else "TOP",
                "supports_joins": True,
                "supports_aggregations": True
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))