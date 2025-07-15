# Natural Language to SQL Chat Interface - API Documentation

## Overview

The Natural Language to SQL API provides endpoints for converting natural language questions into SQL queries and executing them against a database. The API is built using FastAPI and provides both REST endpoints and comprehensive error handling.

**Base URL**: `http://localhost:8000`  
**API Version**: 1.0.0  
**Content-Type**: `application/json`

## Authentication

Currently, the API does not require authentication for the MVP version. Future versions will implement JWT-based authentication.

## Endpoints

### 1. Health Check

Check the health status of the API and its dependencies.

**Endpoint**: `GET /health`

**Response**:
```json
{
    "status": "healthy",
    "database": "connected",
    "timestamp": "2024-01-15T10:30:00Z"
}
```

**Status Codes**:
- `200 OK`: Service is healthy
- `503 Service Unavailable`: Service or dependencies are unhealthy

**Example**:
```bash
curl -X GET "http://localhost:8000/health"
```

### 2. Execute Natural Language Query

Convert a natural language question to SQL and execute it against the database.

**Endpoint**: `POST /query`

**Request Body**:
```json
{
    "question": "string",
    "schema": "string (optional)"
}
```

**Parameters**:
- `question` (required): Natural language question about the database
- `schema` (optional): Database schema override. If not provided, the system will auto-detect the schema

**Response**:
```json
{
    "sql_query": "SELECT * FROM customers WHERE country = 'Germany'",
    "results": [
        {
            "customer_id": 1,
            "company_name": "Alfreds Futterkiste",
            "contact_name": "Maria Anders",
            "city": "Berlin",
            "country": "Germany",
            "phone": "030-0074321"
        }
    ],
    "columns": ["customer_id", "company_name", "contact_name", "city", "country", "phone"],
    "row_count": 1
}
```

**Status Codes**:
- `200 OK`: Query executed successfully
- `400 Bad Request`: Invalid request format
- `500 Internal Server Error`: Query execution failed

**Example**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Show me all customers from Germany"
     }'
```

### 3. Get Database Schema

Retrieve the current database schema information.

**Endpoint**: `GET /schema`

**Response**:
```json
{
    "schema": "Database Schema:\n\nTable: customers\n  - customer_id: INTEGER NOT NULL (PRIMARY KEY)\n  - company_name: TEXT NOT NULL\n  - contact_name: TEXT NULL\n  - city: TEXT NULL\n  - country: TEXT NULL\n  - phone: TEXT NULL\n\nTable: products\n  - product_id: INTEGER NOT NULL (PRIMARY KEY)\n  - product_name: TEXT NOT NULL\n  - category: TEXT NULL\n  - unit_price: REAL NULL\n  - units_in_stock: INTEGER NULL\n\nTable: orders\n  - order_id: INTEGER NOT NULL (PRIMARY KEY)\n  - customer_id: INTEGER NULL\n  - order_date: TEXT NULL\n  - total_amount: REAL NULL"
}
```

**Status Codes**:
- `200 OK`: Schema retrieved successfully
- `500 Internal Server Error`: Failed to retrieve schema

**Example**:
```bash
curl -X GET "http://localhost:8000/schema"
```

### 4. Root Endpoint

Basic API information endpoint.

**Endpoint**: `GET /`

**Response**:
```json
{
    "message": "Natural Language to SQL API"
}
```

## Error Handling

### Error Response Format

All error responses follow a consistent format:

```json
{
    "detail": "Error message describing what went wrong"
}
```

### Common Error Scenarios

#### 1. Invalid SQL Query Generation
**Status**: `500 Internal Server Error`
```json
{
    "detail": "LLM service error: Unable to generate valid SQL query"
}
```

#### 2. Database Connection Error
**Status**: `500 Internal Server Error`
```json
{
    "detail": "Query execution error: database connection failed"
}
```

#### 3. Unsafe Query Attempt
**Status**: `500 Internal Server Error`
```json
{
    "detail": "Only SELECT queries are allowed"
}
```

#### 4. Invalid Request Format
**Status**: `422 Unprocessable Entity`
```json
{
    "detail": [
        {
            "loc": ["body", "question"],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

## Request/Response Examples

### Example 1: Simple Data Retrieval

**Request**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Show me all customers"
     }'
```

**Response**:
```json
{
    "sql_query": "SELECT * FROM customers",
    "results": [
        {
            "customer_id": 1,
            "company_name": "Alfreds Futterkiste",
            "contact_name": "Maria Anders",
            "city": "Berlin",
            "country": "Germany",
            "phone": "030-0074321"
        },
        {
            "customer_id": 2,
            "company_name": "Ana Trujillo Emparedados",
            "contact_name": "Ana Trujillo",
            "city": "México D.F.",
            "country": "Mexico",
            "phone": "(5) 555-4729"
        }
    ],
    "columns": ["customer_id", "company_name", "contact_name", "city", "country", "phone"],
    "row_count": 10
}
```

### Example 2: Filtered Query

**Request**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "What are the top 5 most expensive products?"
     }'
```

**Response**:
```json
{
    "sql_query": "SELECT * FROM products ORDER BY unit_price DESC LIMIT 5",
    "results": [
        {
            "product_id": 9,
            "product_name": "Mishi Kobe Niku",
            "category": "Meat/Poultry",
            "unit_price": 97.0,
            "units_in_stock": 29
        },
        {
            "product_id": 8,
            "product_name": "Northwoods Cranberry Sauce",
            "category": "Condiments",
            "unit_price": 40.0,
            "units_in_stock": 6
        }
    ],
    "columns": ["product_id", "product_name", "category", "unit_price", "units_in_stock"],
    "row_count": 5
}
```

### Example 3: Aggregation Query

**Request**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "How many customers are from each country?"
     }'
```

**Response**:
```json
{
    "sql_query": "SELECT country, COUNT(*) as customer_count FROM customers GROUP BY country ORDER BY customer_count DESC",
    "results": [
        {
            "country": "Germany",
            "customer_count": 2
        },
        {
            "country": "Mexico",
            "customer_count": 2
        },
        {
            "country": "UK",
            "customer_count": 1
        }
    ],
    "columns": ["country", "customer_count"],
    "row_count": 6
}
```

### Example 4: Join Query

**Request**:
```bash
curl -X POST "http://localhost:8000/query" \
     -H "Content-Type: application/json" \
     -d '{
       "question": "Show me customers with their total order amounts"
     }'
```

**Response**:
```json
{
    "sql_query": "SELECT c.company_name, c.contact_name, SUM(o.total_amount) as total_orders FROM customers c LEFT JOIN orders o ON c.customer_id = o.customer_id GROUP BY c.customer_id, c.company_name, c.contact_name ORDER BY total_orders DESC",
    "results": [
        {
            "company_name": "Ana Trujillo Emparedados",
            "contact_name": "Ana Trujillo",
            "total_orders": 600.9
        },
        {
            "company_name": "Alfreds Futterkiste",
            "contact_name": "Maria Anders",
            "total_orders": 470.75
        }
    ],
    "columns": ["company_name", "contact_name", "total_orders"],
    "row_count": 10
}
```

## Rate Limiting

Currently, no rate limiting is implemented in the MVP version. Future versions will include:
- Rate limiting per IP address
- API key-based quotas
- Usage analytics

## CORS Configuration

The API is configured to accept requests from:
- `http://localhost:3000` (React development server)
- Additional origins can be configured in production

## Interactive API Documentation

FastAPI automatically generates interactive API documentation:

- **Swagger UI**: `http://localhost:8000/docs`
- **ReDoc**: `http://localhost:8000/redoc`

These interfaces allow you to:
- Explore all available endpoints
- Test API calls directly from the browser
- View detailed request/response schemas
- Download OpenAPI specification

## SDK and Client Libraries

### JavaScript/TypeScript Client

```javascript
class NLSQLClient {
    constructor(baseURL = 'http://localhost:8000') {
        this.baseURL = baseURL;
    }
    
    async query(question, schema = '') {
        const response = await fetch(`${this.baseURL}/query`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ question, schema })
        });
        
        if (!response.ok) {
            throw new Error(`Query failed: ${response.statusText}`);
        }
        
        return await response.json();
    }
    
    async getSchema() {
        const response = await fetch(`${this.baseURL}/schema`);
        return await response.json();
    }
    
    async healthCheck() {
        const response = await fetch(`${this.baseURL}/health`);
        return await response.json();
    }
}

// Usage
const client = new NLSQLClient();
const result = await client.query('Show me all customers');
```

### Python Client

```python
import requests
from typing import Dict, Any, Optional

class NLSQLClient:
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
    
    def query(self, question: str, schema: Optional[str] = None) -> Dict[str, Any]:
        """Execute a natural language query"""
        payload = {"question": question}
        if schema:
            payload["schema"] = schema
            
        response = requests.post(f"{self.base_url}/query", json=payload)
        response.raise_for_status()
        return response.json()
    
    def get_schema(self) -> Dict[str, Any]:
        """Get database schema"""
        response = requests.get(f"{self.base_url}/schema")
        response.raise_for_status()
        return response.json()
    
    def health_check(self) -> Dict[str, Any]:
        """Check API health"""
        response = requests.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()

# Usage
client = NLSQLClient()
result = client.query("Show me all customers")
print(result["sql_query"])
```

## Troubleshooting

### Common Issues

1. **Connection Refused**
   - Ensure the backend server is running on port 8000
   - Check if the port is blocked by firewall

2. **OpenAI API Errors**
   - Verify your OpenAI API key is correctly set in `.env`
   - Check your OpenAI account has sufficient credits

3. **Database Connection Issues**
   - Ensure the SQLite database file exists
   - Run `python setup_sample_db.py` to create sample data

4. **CORS Errors**
   - Verify the frontend is running on `http://localhost:3000`
   - Check CORS configuration in `main.py`

### Debug Mode

To enable debug mode, set the environment variable:
```bash
export DEBUG=true
```

This will provide more detailed error messages and stack traces.

## Changelog

### Version 1.0.0 (Current)
- Initial API implementation
- Basic query execution
- Schema retrieval
- Health check endpoint
- SQLite database support

### Planned Features
- Authentication and authorization
- Rate limiting
- Query caching
- WebSocket support for real-time queries
- Multiple database support
- Query history and favorites