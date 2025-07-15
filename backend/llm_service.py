import openai

class LLMService:
    def __init__(self, api_key: str):
        self.client = openai.OpenAI(api_key=api_key)
    
    async def generate_sql(self, question: str, schema: str) -> str:
        """Generate SQL query from natural language question"""
        
        system_prompt = f"""You are a SQL expert. Convert natural language questions to SQLite queries.

Database Schema:
{schema}

Rules:
1. Only generate SELECT queries
2. Use proper SQLite syntax
3. Return only the SQL query, no explanations
4. Use appropriate JOINs when needed
5. Handle case-insensitive searches with LIKE (SQLite doesn't have ILIKE)
6. Use proper table and column names from the schema
7. If the question is ambiguous, make reasonable assumptions
8. Use LIMIT for queries that might return many results

Example:
Question: "Show me all customers"
SQL: SELECT * FROM customers;
"""

        user_prompt = f"Question: {question}\nSQL:"
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=500,
                temperature=0.1
            )
            
            sql_query = response.choices[0].message.content.strip()
            
            # Clean up the response - remove any markdown formatting
            if sql_query.startswith('```sql'):
                sql_query = sql_query[6:]
            if sql_query.endswith('```'):
                sql_query = sql_query[:-3]
            
            return sql_query.strip()
            
        except Exception as e:
            raise Exception(f"LLM service error: {str(e)}")