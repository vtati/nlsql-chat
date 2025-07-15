# Natural Language to SQL Chat Interface - Design Document

## 1. System Architecture

### 1.1 High-Level Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │    Backend      │    │   External      │
│   (React)       │    │   (FastAPI)     │    │   Services      │
├─────────────────┤    ├─────────────────┤    ├─────────────────┤
│ • Chat UI       │◄──►│ • REST API      │◄──►│ • OpenAI API    │
│ • Result Tables │    │ • Query Engine  │    │ • Database      │
│ • State Mgmt    │    │ • Schema Mgmt   │    │                 │
└─────────────────┘    └─────────────────┘    └─────────────────┘
```

### 1.2 Component Architecture

#### 1.2.1 Frontend Components
```
src/
├── components/
│   ├── ChatInterface.js      # Main chat component
│   ├── MessageList.js        # Message display
│   ├── QueryInput.js         # Input handling
│   ├── ResultTable.js        # Data table display
│   └── LoadingSpinner.js     # Loading states
├── services/
│   ├── apiService.js         # Backend API calls
│   └── formatService.js      # Data formatting
├── hooks/
│   ├── useChat.js           # Chat state management
│   └── useQuery.js          # Query execution
└── utils/
    ├── constants.js         # App constants
    └── helpers.js           # Utility functions
```

#### 1.2.2 Backend Components
```
backend/
├── main.py                  # FastAPI application
├── database.py              # Database management
├── llm_service.py           # LLM integration
├── models/                  # Pydantic models
│   ├── request_models.py    # API request models
│   └── response_models.py   # API response models
├── services/
│   ├── query_service.py     # Query processing
│   ├── schema_service.py    # Schema management
│   └── validation_service.py # Input validation
└── utils/
    ├── config.py            # Configuration
    ├── logger.py            # Logging setup
    └── exceptions.py        # Custom exceptions
```

## 2. Data Flow Design

### 2.1 Query Processing Flow

```
User Input → Frontend → Backend → LLM Service → SQL Generation
    ↓                                               ↓
Result Display ← Frontend ← Backend ← Database ← Query Execution
```

### 2.2 Detailed Data Flow

1. **User Input Processing**
   - User types natural language question
   - Frontend validates input and shows loading state
   - Request sent to backend API

2. **Backend Processing**
   - Receive query request
   - Load database schema
   - Send question + schema to LLM service
   - Receive generated SQL query

3. **Query Execution**
   - Validate SQL query for safety
   - Execute query against database
   - Format results for frontend

4. **Response Handling**
   - Send results back to frontend
   - Display SQL query and results
   - Update conversation history

### 2.3 Error Handling Flow

```
Error Occurs → Log Error → Generate User Message → Display in UI
     ↓
Retry Logic → Fallback Options → Graceful Degradation
```

## 3. Database Design

### 3.1 Sample Database Schema

```sql
-- Customers table
CREATE TABLE customers (
    customer_id INTEGER PRIMARY KEY,
    company_name TEXT NOT NULL,
    contact_name TEXT,
    city TEXT,
    country TEXT,
    phone TEXT
);

-- Products table
CREATE TABLE products (
    product_id INTEGER PRIMARY KEY,
    product_name TEXT NOT NULL,
    category TEXT,
    unit_price REAL,
    units_in_stock INTEGER
);

-- Orders table
CREATE TABLE orders (
    order_id INTEGER PRIMARY KEY,
    customer_id INTEGER,
    order_date TEXT,
    total_amount REAL,
    FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
);
```

### 3.2 Schema Information Storage

```python
# Schema representation for LLM context
schema_context = {
    "tables": [
        {
            "name": "customers",
            "columns": [
                {"name": "customer_id", "type": "INTEGER", "primary_key": True},
                {"name": "company_name", "type": "TEXT", "nullable": False},
                # ... more columns
            ],
            "relationships": [
                {"table": "orders", "type": "one_to_many", "key": "customer_id"}
            ]
        }
        # ... more tables
    ]
}
```

## 4. API Design

### 4.1 REST API Endpoints

#### 4.1.1 Query Execution
```http
POST /query
Content-Type: application/json

{
    "question": "Show me all customers from Germany",
    "schema": "optional_schema_override"
}

Response:
{
    "sql_query": "SELECT * FROM customers WHERE country = 'Germany'",
    "results": [
        {"customer_id": 1, "company_name": "Alfreds Futterkiste", ...},
        ...
    ],
    "columns": ["customer_id", "company_name", "contact_name", ...],
    "row_count": 2,
    "execution_time": 0.045
}
```

#### 4.1.2 Schema Retrieval
```http
GET /schema

Response:
{
    "schema": "Database Schema:\n\nTable: customers\n  - customer_id: INTEGER NOT NULL (PRIMARY KEY)\n  ...",
    "tables": ["customers", "products", "orders"],
    "last_updated": "2024-01-15T10:30:00Z"
}
```

#### 4.1.3 Health Check
```http
GET /health

Response:
{
    "status": "healthy",
    "database": "connected",
    "llm_service": "available",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

### 4.2 WebSocket API (Future Enhancement)
```javascript
// Real-time query streaming
ws://localhost:8000/ws/query
{
    "type": "query",
    "data": {
        "question": "Show me all customers",
        "session_id": "user_session_123"
    }
}
```

## 5. User Interface Design

### 5.1 Chat Interface Layout

```
┌─────────────────────────────────────────────────────────────┐
│                    Natural Language to SQL                  │
│                Ask questions about your database            │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  [User] Show me all customers from Germany                  │
│                                                             │
│  [Bot] Generated SQL:                                       │
│        SELECT * FROM customers WHERE country = 'Germany'    │
│                                                             │
│        Results (2 rows):                                    │
│        ┌─────────────┬──────────────────┬─────────────┐    │
│        │ customer_id │ company_name     │ city        │    │
│        ├─────────────┼──────────────────┼─────────────┤    │
│        │ 1           │ Alfreds Futte... │ Berlin      │    │
│        │ 6           │ Blauer See De... │ Mannheim    │    │
│        └─────────────┴──────────────────┴─────────────┘    │
│                                                             │
├─────────────────────────────────────────────────────────────┤
│ [Ask a question about your database...        ] [Send]     │
└─────────────────────────────────────────────────────────────┘
```

### 5.2 Component Hierarchy

```
App
├── Header
├── ChatInterface
│   ├── MessageList
│   │   ├── UserMessage
│   │   ├── BotMessage
│   │   │   ├── SQLDisplay
│   │   │   └── ResultTable
│   │   └── LoadingMessage
│   └── QueryInput
│       ├── TextInput
│       └── SendButton
└── Footer
```

### 5.3 State Management

```javascript
// Chat state structure
const chatState = {
    messages: [
        {
            id: "msg_1",
            type: "user",
            content: "Show me all customers",
            timestamp: "2024-01-15T10:30:00Z"
        },
        {
            id: "msg_2",
            type: "bot",
            content: {
                sql_query: "SELECT * FROM customers",
                results: [...],
                columns: [...],
                row_count: 10
            },
            timestamp: "2024-01-15T10:30:05Z"
        }
    ],
    isLoading: false,
    error: null,
    schema: "...",
    connectionStatus: "connected"
};
```

## 6. Security Design

### 6.1 Input Validation

```python
# SQL injection prevention
def validate_sql_query(query: str) -> bool:
    """Validate SQL query for safety"""
    dangerous_keywords = [
        'DROP', 'DELETE', 'UPDATE', 'INSERT', 
        'ALTER', 'CREATE', 'TRUNCATE', 'EXEC'
    ]
    
    query_upper = query.upper().strip()
    
    # Only allow SELECT queries
    if not query_upper.startswith('SELECT'):
        return False
    
    # Check for dangerous keywords
    for keyword in dangerous_keywords:
        if keyword in query_upper:
            return False
    
    return True
```

### 6.2 Authentication & Authorization (Future)

```python
# JWT token validation
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer

security = HTTPBearer()

async def verify_token(token: str = Depends(security)):
    """Verify JWT token"""
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

### 6.3 Environment Configuration

```python
# Secure configuration management
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str
    openai_api_key: str
    secret_key: str = "your-secret-key"
    debug: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## 7. Performance Optimization

### 7.1 Database Optimization

```python
# Connection pooling
from sqlalchemy.pool import QueuePool

engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True
)
```

### 7.2 Caching Strategy

```python
# Query result caching
from functools import lru_cache
import hashlib

@lru_cache(maxsize=100)
def get_cached_query_result(query_hash: str):
    """Cache query results for repeated queries"""
    pass

def generate_query_hash(question: str, schema: str) -> str:
    """Generate hash for caching key"""
    content = f"{question}:{schema}"
    return hashlib.md5(content.encode()).hexdigest()
```

### 7.3 Frontend Optimization

```javascript
// React optimization techniques
import { memo, useMemo, useCallback } from 'react';

const ResultTable = memo(({ data, columns }) => {
    const memoizedData = useMemo(() => 
        data.map(row => ({ ...row, id: generateId() })), 
        [data]
    );
    
    return <Table data={memoizedData} columns={columns} />;
});
```

## 8. Error Handling Strategy

### 8.1 Error Categories

```python
# Custom exception hierarchy
class NLSQLException(Exception):
    """Base exception for NL to SQL application"""
    pass

class DatabaseConnectionError(NLSQLException):
    """Database connection issues"""
    pass

class QueryGenerationError(NLSQLException):
    """LLM query generation issues"""
    pass

class QueryExecutionError(NLSQLException):
    """SQL query execution issues"""
    pass
```

### 8.2 Error Response Format

```json
{
    "error": {
        "code": "QUERY_EXECUTION_ERROR",
        "message": "Unable to execute query: table 'invalid_table' does not exist",
        "details": {
            "sql_query": "SELECT * FROM invalid_table",
            "suggestion": "Check table names in your database schema"
        },
        "timestamp": "2024-01-15T10:30:00Z"
    }
}
```

## 9. Testing Strategy

### 9.1 Backend Testing

```python
# Unit tests for query generation
import pytest
from llm_service import LLMService

@pytest.fixture
def llm_service():
    return LLMService(api_key="test_key")

def test_simple_query_generation(llm_service):
    schema = "Table: customers\n  - name: TEXT\n  - city: TEXT"
    question = "Show me all customers"
    
    result = llm_service.generate_sql(question, schema)
    assert "SELECT" in result.upper()
    assert "customers" in result.lower()
```

### 9.2 Frontend Testing

```javascript
// Component testing with React Testing Library
import { render, screen, fireEvent } from '@testing-library/react';
import ChatInterface from './ChatInterface';

test('sends query when user submits question', async () => {
    render(<ChatInterface />);
    
    const input = screen.getByPlaceholderText(/ask a question/i);
    const button = screen.getByRole('button', { name: /send/i });
    
    fireEvent.change(input, { target: { value: 'Show me all customers' } });
    fireEvent.click(button);
    
    expect(screen.getByText(/loading/i)).toBeInTheDocument();
});
```

### 9.3 Integration Testing

```python
# End-to-end API testing
import httpx
import pytest

@pytest.mark.asyncio
async def test_query_endpoint():
    async with httpx.AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/query", json={
            "question": "Show me all customers",
            "schema": ""
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "sql_query" in data
        assert "results" in data
```

## 10. Deployment Architecture

### 10.1 Development Environment

```yaml
# docker-compose.yml
version: '3.8'
services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///app.db
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./backend:/app
  
  frontend:
    build: ./frontend
    ports:
      - "3000:3000"
    volumes:
      - ./frontend:/app
    depends_on:
      - backend
```

### 10.2 Production Deployment

```yaml
# Production considerations
services:
  backend:
    image: nlsql-backend:latest
    replicas: 3
    environment:
      - DATABASE_URL=postgresql://user:pass@db:5432/nlsql
      - REDIS_URL=redis://redis:6379
    
  frontend:
    image: nlsql-frontend:latest
    
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
```

## 11. Monitoring and Logging

### 11.1 Application Metrics

```python
# Prometheus metrics
from prometheus_client import Counter, Histogram, generate_latest

query_counter = Counter('nlsql_queries_total', 'Total queries processed')
query_duration = Histogram('nlsql_query_duration_seconds', 'Query processing time')

@query_duration.time()
async def process_query(question: str):
    query_counter.inc()
    # Process query...
```

### 11.2 Structured Logging

```python
import structlog

logger = structlog.get_logger()

async def execute_query(sql_query: str):
    logger.info(
        "query_execution_started",
        sql_query=sql_query,
        user_id="anonymous",
        timestamp=datetime.utcnow()
    )
```

This comprehensive design document provides the technical foundation for implementing the Natural Language to SQL Chat Interface, covering all major architectural decisions, implementation details, and operational considerations.