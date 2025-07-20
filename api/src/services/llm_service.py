"""
Large Language Model service for SQL generation.
"""
import openai
from typing import Dict, Any
from ..core.simple_settings import settings


class LLMService:
    """LLM Service for generating SQL queries with multi-database support."""
    
    def __init__(self, api_key: str = None):
        self.client = openai.OpenAI(api_key=api_key or settings.openai_api_key)
    
    async def generate_sql(self, question: str, schema: str, sql_dialect: str = "SQLite") -> str:
        """Generate SQL query from natural language question with dialect support."""
        
        # Get dialect-specific instructions
        dialect_instructions = self._get_dialect_instructions(sql_dialect)
        
        system_prompt = f"""You are an expert SQL developer. Convert natural language questions to {sql_dialect} queries using ONLY the provided database schema.

IMPORTANT DATABASE SCHEMA:
{schema}

CRITICAL RULES:
1. ONLY use table and column names that exist in the schema above
2. Only generate SELECT queries
3. Use proper {sql_dialect} syntax
4. Return ONLY the SQL query, no explanations or markdown
5. Use INNER JOIN or LEFT JOIN when combining tables
6. {dialect_instructions['text_search']}
7. Use {dialect_instructions['limit_syntax']} for queries that might return many results
8. If a question asks for data that doesn't exist in the schema, return a simple query on available data

{dialect_instructions['examples']}

REMEMBER: Only use columns and tables that exist in the schema provided above!
"""

        user_prompt = f"Question: {question}\nSQL:"
        
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_primary_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.llm_max_tokens,
                temperature=settings.llm_temperature
            )
            
            sql_query = response.choices[0].message.content.strip()
            return self._clean_sql_response(sql_query)
            
        except Exception:
            # Fallback to secondary model
            try:
                response = self.client.chat.completions.create(
                    model=settings.llm_fallback_model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=settings.llm_max_tokens,
                    temperature=settings.llm_temperature
                )
                
                sql_query = response.choices[0].message.content.strip()
                return self._clean_sql_response(sql_query)
                
            except Exception as fallback_error:
                raise Exception(f"LLM service error: {str(fallback_error)}")
    
    def _clean_sql_response(self, sql_query: str) -> str:
        """Clean up the SQL response from LLM."""
        # Remove any markdown formatting
        if sql_query.startswith('```sql'):
            sql_query = sql_query[6:]
        if sql_query.startswith('```'):
            sql_query = sql_query[3:]
        if sql_query.endswith('```'):
            sql_query = sql_query[:-3]
        
        # Remove any extra whitespace or newlines
        return sql_query.strip()
    
    def _get_dialect_instructions(self, sql_dialect: str) -> Dict[str, str]:
        """Get database-specific SQL instructions for LLM prompts."""
        
        dialect_configs = {
            "SQLite": {
                "text_search": "Use LIKE for text searches (SQLite doesn't have ILIKE)",
                "limit_syntax": "LIMIT",
                "examples": """EXAMPLE QUERIES FOR SQLite:
Question: "Show me all customers"
SQL: SELECT * FROM customers LIMIT 50

Question: "What are the most expensive products?"
SQL: SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 10

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers"""
            },
            
            "PostgreSQL": {
                "text_search": "Use ILIKE for case-insensitive text searches, LIKE for case-sensitive",
                "limit_syntax": "LIMIT",
                "examples": """EXAMPLE QUERIES FOR PostgreSQL:
Question: "Show me all customers"
SQL: SELECT * FROM customers LIMIT 50

Question: "What are the most expensive products?"
SQL: SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 10

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "Find customers with 'market' in company name"
SQL: SELECT company_name, contact_name FROM customers WHERE company_name ILIKE '%market%'

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers"""
            },
            
            "MySQL": {
                "text_search": "Use LIKE for text searches, use LOWER() for case-insensitive searches",
                "limit_syntax": "LIMIT",
                "examples": """EXAMPLE QUERIES FOR MySQL:
Question: "Show me all customers"
SQL: SELECT * FROM customers LIMIT 50

Question: "What are the most expensive products?"
SQL: SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 10

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "Find customers with 'market' in company name (case-insensitive)"
SQL: SELECT company_name, contact_name FROM customers WHERE LOWER(company_name) LIKE LOWER('%market%')

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers"""
            },
            
            "SQL Server": {
                "text_search": "Use LIKE for text searches, use LOWER() for case-insensitive searches",
                "limit_syntax": "TOP",
                "examples": """EXAMPLE QUERIES FOR SQL Server:
Question: "Show me all customers"
SQL: SELECT TOP 50 * FROM customers

Question: "What are the most expensive products?"
SQL: SELECT TOP 10 product_name, unit_price FROM products ORDER BY unit_price DESC

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "Find customers with 'market' in company name (case-insensitive)"
SQL: SELECT company_name, contact_name FROM customers WHERE LOWER(company_name) LIKE LOWER('%market%')

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers"""
            },
            
            "Oracle": {
                "text_search": "Use LIKE for text searches, use UPPER() or LOWER() for case-insensitive searches",
                "limit_syntax": "ROWNUM",
                "examples": """EXAMPLE QUERIES FOR Oracle:
Question: "Show me all customers"
SQL: SELECT * FROM customers WHERE ROWNUM <= 50

Question: "What are the most expensive products?"
SQL: SELECT * FROM (SELECT product_name, unit_price FROM products ORDER BY unit_price DESC) WHERE ROWNUM <= 10

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "Find customers with 'market' in company name (case-insensitive)"
SQL: SELECT company_name, contact_name FROM customers WHERE UPPER(company_name) LIKE UPPER('%market%')

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers"""
            }
        }
        
        return dialect_configs.get(sql_dialect, dialect_configs["SQLite"])