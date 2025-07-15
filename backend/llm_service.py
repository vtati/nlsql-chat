import openai

class LLMService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_sql(self, question: str, schema: str) -> str:
        """Generate SQL query from natural language question"""
        
        system_prompt = f"""You are an expert SQL developer. Convert natural language questions to SQLite queries using ONLY the provided database schema.

IMPORTANT DATABASE SCHEMA:
{schema}

CRITICAL RULES:
1. ONLY use table and column names that exist in the schema above
2. Only generate SELECT queries
3. Use proper SQLite syntax
4. Return ONLY the SQL query, no explanations or markdown
5. Use INNER JOIN or LEFT JOIN when combining tables
6. Use LIKE for text searches (SQLite doesn't have ILIKE)
7. Use LIMIT for queries that might return many results
8. If a question asks for data that doesn't exist in the schema, return a simple query on available data

EXAMPLE QUERIES FOR THIS DATABASE:
Question: "Show me all customers"
SQL: SELECT * FROM customers LIMIT 50

Question: "What are the most expensive products?"
SQL: SELECT product_name, unit_price FROM products ORDER BY unit_price DESC LIMIT 10

Question: "Show customers from Germany"
SQL: SELECT company_name, contact_name, city FROM customers WHERE country = 'Germany'

Question: "List products by category"
SQL: SELECT p.product_name, c.category_name, p.unit_price FROM products p JOIN categories c ON p.category_id = c.category_id ORDER BY c.category_name

Question: "How many customers are there?"
SQL: SELECT COUNT(*) as customer_count FROM customers

Question: "Show orders with customer information"
SQL: SELECT o.order_id, c.company_name, o.order_date FROM orders o JOIN customers c ON o.customer_id = c.customer_id LIMIT 20

REMEMBER: Only use columns and tables that exist in the schema provided above!
"""

        user_prompt = f"Question: {question}\nSQL:"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-4",  # Upgraded to GPT-4 for better accuracy
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=300,
                temperature=0.0  # Lower temperature for more consistent results
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response - remove any markdown formatting
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.startswith('```'):
                sql_query = sql_query[3:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            # Remove any extra whitespace or newlines
            sql_query = sql_query.strip()
            
            return sql_query
            
        except Exception as e:
            # Fallback to GPT-3.5-turbo if GPT-4 fails
            try:
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=300,
                    temperature=0.0
                )
                
                sql_query = response.choices[0].message.content.strip()
                
                # Clean up the response
                if sql_query.startswith('```sql'):
                    sql_query = sql_query[6:]
                if sql_query.startswith('```'):
                    sql_query = sql_query[3:]
                if sql_query.endswith('```'):
                    sql_query = sql_query[:-3]
                
                return sql_query.strip()
                
            except Exception as fallback_error:
                raise Exception(f"LLM service error: {str(fallback_error)}")