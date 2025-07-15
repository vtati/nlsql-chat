from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any
import os
from dotenv import load_dotenv

from database import DatabaseManager
from llm_service import LLMService

load_dotenv()

app = FastAPI(title="Natural Language to SQL API", version="1.0.0")

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

# Initialize services
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
        
        # Generate SQL using LLM
        sql_query = await llm_service.generate_sql(request.question, schema)
        
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
        await db_manager.test_connection()
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}