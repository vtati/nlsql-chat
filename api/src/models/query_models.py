"""
Data models for query operations.
"""
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class QueryRequest(BaseModel):
    """Request model for natural language queries."""
    
    question: str = Field(..., description="Natural language question")
    schema: Optional[str] = Field(None, description="Optional database schema override")
    
    class Config:
        json_schema_extra = {
            "example": {
                "question": "Show me all customers from Germany",
                "schema": None
            }
        }


class QueryResponse(BaseModel):
    """Response model for query results."""
    
    sql_query: str = Field(..., description="Generated SQL query")
    results: List[Dict[str, Any]] = Field(..., description="Query results")
    columns: List[str] = Field(..., description="Column names")
    row_count: int = Field(..., description="Number of rows returned")
    execution_time_ms: Optional[float] = Field(None, description="Query execution time in milliseconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "sql_query": "SELECT * FROM customers WHERE country = 'Germany' LIMIT 50",
                "results": [
                    {
                        "customer_id": "ALFKI",
                        "company_name": "Alfreds Futterkiste",
                        "city": "Berlin",
                        "country": "Germany"
                    }
                ],
                "columns": ["customer_id", "company_name", "city", "country"],
                "row_count": 1,
                "execution_time_ms": 45.2
            }
        }


class DatabaseInfo(BaseModel):
    """Database information model."""
    
    database_type: str = Field(..., description="Type of database (SQLite, PostgreSQL, etc.)")
    connection_string_masked: str = Field(..., description="Masked connection string")
    supported_features: Dict[str, Any] = Field(..., description="Database-specific features")
    
    class Config:
        json_schema_extra = {
            "example": {
                "database_type": "SQLite",
                "connection_string_masked": "sqlite:///***",
                "supported_features": {
                    "case_insensitive_search": False,
                    "limit_syntax": "LIMIT",
                    "supports_joins": True,
                    "supports_aggregations": True
                }
            }
        }


class SchemaResponse(BaseModel):
    """Database schema response model."""
    
    schema: str = Field(..., description="Database schema information")
    tables: List[str] = Field(..., description="List of table names")
    last_updated: Optional[str] = Field(None, description="Schema last updated timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "schema": "Database Schema (SQLite):\n\nTable: customers\n  - customer_id: TEXT NOT NULL (PRIMARY KEY)\n  - company_name: TEXT NOT NULL\n",
                "tables": ["customers", "products", "orders"],
                "last_updated": "2024-01-15T10:30:00Z"
            }
        }


class HealthResponse(BaseModel):
    """Health check response model."""
    
    status: str = Field(..., description="Health status")
    database: str = Field(..., description="Database connection status")
    database_type: str = Field(..., description="Database type")
    version: str = Field(..., description="API version")
    timestamp: Optional[str] = Field(None, description="Health check timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "database": "connected",
                "database_type": "SQLite",
                "version": "2.0.0",
                "timestamp": "2024-01-15T10:30:00Z"
            }
        }