"""
Database adapters for different database types.
"""
from typing import Dict, Any, List, Tuple, Optional
from urllib.parse import urlparse
import asyncio
from abc import ABC, abstractmethod


class DatabaseAdapter(ABC):
    """Abstract base class for database adapters."""
    
    def __init__(self, connection_string: str):
        self.connection_string = connection_string
        self.connection = None
        self.db_type = self._detect_db_type(connection_string)
    
    def _detect_db_type(self, connection_string: str) -> str:
        """Detect database type from connection string."""
        parsed = urlparse(connection_string)
        scheme = parsed.scheme.lower()
        
        if scheme.startswith('sqlite'):
            return 'sqlite'
        elif scheme.startswith('postgresql') or scheme.startswith('postgres'):
            return 'postgresql'
        elif scheme.startswith('mysql'):
            return 'mysql'
        elif scheme.startswith('mssql') or scheme.startswith('sqlserver'):
            return 'sqlserver'
        elif scheme.startswith('oracle'):
            return 'oracle'
        else:
            raise ValueError(f"Unsupported database type: {scheme}")
    
    @abstractmethod
    async def connect(self):
        """Establish database connection."""
        pass
    
    @abstractmethod
    async def disconnect(self):
        """Close database connection."""
        pass
    
    @abstractmethod
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SELECT query and return results with column names."""
        pass
    
    @abstractmethod
    async def get_schema(self) -> str:
        """Get database schema information."""
        pass
    
    @abstractmethod
    async def test_connection(self) -> bool:
        """Test database connection."""
        pass
    
    @abstractmethod
    def get_sql_dialect(self) -> str:
        """Get SQL dialect name for LLM prompts."""
        pass


class SQLiteAdapter(DatabaseAdapter):
    """SQLite database adapter."""
    
    async def connect(self):
        """Establish SQLite connection."""
        import aiosqlite
        import os
        
        # Extract database path from connection string
        parsed = urlparse(self.connection_string)
        db_path = parsed.path.lstrip('/')
        
        # For production, ensure database directory exists
        if os.getenv('ENVIRONMENT') == 'production':
            # Create data directory if it doesn't exist
            data_dir = '/opt/render/project/src/data'
            if os.path.exists(data_dir):
                db_path = os.path.join(data_dir, os.path.basename(db_path))
            else:
                # Fallback to current directory
                db_path = os.path.join(os.getcwd(), db_path)
        
        self.connection = await aiosqlite.connect(db_path)
        self.connection.row_factory = aiosqlite.Row
        await self._initialize_sample_data()
    
    async def disconnect(self):
        """Close SQLite connection."""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQLite query."""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.execute(query)
        results = await cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        result_list = [dict(row) for row in results]
        
        await cursor.close()
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get SQLite schema information."""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'"
        )
        tables = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema (SQLite):\n\n"
        
        for table_row in tables:
            table_name = table_row[0]
            schema_text += f"Table: {table_name}\n"
            
            cursor = await self.connection.execute(f"PRAGMA table_info({table_name})")
            columns = await cursor.fetchall()
            await cursor.close()
            
            for col in columns:
                col_name, col_type = col[1], col[2]
                not_null = "NOT NULL" if col[3] else "NULL"
                primary_key = " (PRIMARY KEY)" if col[5] else ""
                schema_text += f"  - {col_name}: {col_type} {not_null}{primary_key}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test SQLite connection."""
        try:
            if not self.connection:
                await self.connect()
            cursor = await self.connection.execute("SELECT 1")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM."""
        return "SQLite"
    
    async def _initialize_sample_data(self):
        """Initialize SQLite with sample data if needed."""
        cursor = await self.connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='customers'"
        )
        exists = await cursor.fetchone()
        await cursor.close()
        
        if not exists:
            await self._create_sample_tables()
    
    async def _create_sample_tables(self):
        """Create sample tables for SQLite."""
        # Create customers table
        await self.connection.execute('''
            CREATE TABLE customers (
                customer_id TEXT PRIMARY KEY,
                company_name TEXT NOT NULL,
                contact_name TEXT,
                contact_title TEXT,
                address TEXT,
                city TEXT,
                region TEXT,
                postal_code TEXT,
                country TEXT,
                phone TEXT,
                fax TEXT
            )
        ''')
        
        # Create products table
        await self.connection.execute('''
            CREATE TABLE products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                supplier_id INTEGER,
                category_id INTEGER,
                quantity_per_unit TEXT,
                unit_price REAL,
                units_in_stock INTEGER,
                units_on_order INTEGER,
                reorder_level INTEGER,
                discontinued INTEGER
            )
        ''')
        
        # Create categories table
        await self.connection.execute('''
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        # Create orders table
        await self.connection.execute('''
            CREATE TABLE orders (
                order_id INTEGER PRIMARY KEY,
                customer_id TEXT,
                employee_id INTEGER,
                order_date TEXT,
                required_date TEXT,
                shipped_date TEXT,
                ship_via INTEGER,
                freight REAL,
                ship_name TEXT,
                ship_address TEXT,
                ship_city TEXT,
                ship_region TEXT,
                ship_postal_code TEXT,
                ship_country TEXT,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Insert sample data
        await self._insert_sample_data()
        await self.connection.commit()
    
    async def _insert_sample_data(self):
        """Insert sample data into tables."""
        # Sample customers
        customers_data = [
            ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', None, '12209', 'Germany', '030-0074321', '030-0076545'),
            ('ANATR', 'Ana Trujillo Emparedados y helados', 'Ana Trujillo', 'Owner', 'Avda. de la Constitución 2222', 'México D.F.', None, '05021', 'Mexico', '(5) 555-4729', '(5) 555-3745'),
            ('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Owner', 'Mataderos 2312', 'México D.F.', None, '05023', 'Mexico', '(5) 555-3932', None),
            ('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', None, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750'),
            ('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Berguvsvägen 8', 'Luleå', None, 'S-958 22', 'Sweden', '0921-12 34 65', '0921-12 34 67'),
            ('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Sales Representative', 'Forsterstr. 57', 'Mannheim', None, '68306', 'Germany', '0621-08460', '0621-08924'),
        ]
        
        await self.connection.executemany('''
            INSERT INTO customers 
            (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', customers_data)
        
        # Sample categories
        categories_data = [
            (1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
            (2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
            (3, 'Dairy Products', 'Cheeses'),
            (4, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
            (5, 'Meat/Poultry', 'Prepared meats'),
        ]
        
        await self.connection.executemany('''
            INSERT INTO categories (category_id, category_name, description) 
            VALUES (?, ?, ?)
        ''', categories_data)
        
        # Sample products
        products_data = [
            (1, 'Chai', 1, 1, '10 boxes x 20 bags', 18.00, 39, 0, 10, 0),
            (2, 'Chang', 1, 1, '24 - 12 oz bottles', 19.00, 17, 40, 25, 0),
            (3, 'Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10.00, 13, 70, 25, 0),
            (4, 'Chef Antons Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.00, 53, 0, 0, 0),
            (5, 'Chef Antons Gumbo Mix', 2, 2, '36 boxes', 21.35, 0, 0, 0, 1),
        ]
        
        await self.connection.executemany('''
            INSERT INTO products 
            (product_id, product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products_data)
        
        # Sample orders
        orders_data = [
            (10248, 'ALFKI', 5, '1996-07-04', '1996-08-01', '1996-07-16', 3, 32.38, 'Alfreds Futterkiste', 'Obere Str. 57', 'Berlin', None, '12209', 'Germany'),
            (10249, 'ANATR', 6, '1996-07-05', '1996-08-16', '1996-07-10', 1, 11.61, 'Ana Trujillo Emparedados y helados', 'Avda. de la Constitución 2222', 'México D.F.', None, '05021', 'Mexico'),
        ]
        
        await self.connection.executemany('''
            INSERT INTO orders 
            (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders_data)


class PostgreSQLAdapter(DatabaseAdapter):
    """PostgreSQL database adapter."""
    
    async def connect(self):
        """Establish PostgreSQL connection."""
        import asyncpg
        self.connection = await asyncpg.connect(self.connection_string)
    
    async def disconnect(self):
        """Close PostgreSQL connection."""
        if self.connection:
            await self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute PostgreSQL query."""
        if not self.connection:
            await self.connect()
        
        result = await self.connection.fetch(query)
        
        if result:
            columns = list(result[0].keys())
            result_list = [dict(row) for row in result]
        else:
            columns = []
            result_list = []
        
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get PostgreSQL schema information."""
        if not self.connection:
            await self.connect()
        
        query = """
        SELECT 
            t.table_name,
            c.column_name,
            c.data_type,
            c.is_nullable,
            c.column_default,
            CASE WHEN pk.column_name IS NOT NULL THEN 'YES' ELSE 'NO' END as is_primary_key
        FROM information_schema.tables t
        LEFT JOIN information_schema.columns c ON t.table_name = c.table_name
        LEFT JOIN (
            SELECT ku.table_name, ku.column_name
            FROM information_schema.table_constraints tc
            JOIN information_schema.key_column_usage ku ON tc.constraint_name = ku.constraint_name
            WHERE tc.constraint_type = 'PRIMARY KEY'
        ) pk ON c.table_name = pk.table_name AND c.column_name = pk.column_name
        WHERE t.table_schema = 'public' AND t.table_type = 'BASE TABLE'
        ORDER BY t.table_name, c.ordinal_position
        """
        
        result = await self.connection.fetch(query)
        
        schema_text = "Database Schema (PostgreSQL):\n\n"
        current_table = None
        
        for row in result:
            if row['table_name'] != current_table:
                current_table = row['table_name']
                schema_text += f"Table: {current_table}\n"
            
            nullable = "NULL" if row['is_nullable'] == 'YES' else "NOT NULL"
            primary_key = " (PRIMARY KEY)" if row['is_primary_key'] == 'YES' else ""
            
            schema_text += f"  - {row['column_name']}: {row['data_type']} {nullable}{primary_key}\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test PostgreSQL connection."""
        try:
            if not self.connection:
                await self.connect()
            result = await self.connection.fetchval("SELECT 1")
            return result == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM."""
        return "PostgreSQL"


class MySQLAdapter(DatabaseAdapter):
    """MySQL database adapter."""
    
    async def connect(self):
        """Establish MySQL connection."""
        import aiomysql
        
        parsed = urlparse(self.connection_string)
        self.connection = await aiomysql.connect(
            host=parsed.hostname,
            port=parsed.port or 3306,
            user=parsed.username,
            password=parsed.password,
            db=parsed.path.lstrip('/'),
            autocommit=True
        )
    
    async def disconnect(self):
        """Close MySQL connection."""
        if self.connection:
            self.connection.close()
    
    async def execute_query(self, query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute MySQL query."""
        if not self.connection:
            await self.connect()
        
        cursor = await self.connection.cursor(aiomysql.DictCursor)
        await cursor.execute(query)
        result = await cursor.fetchall()
        
        columns = [desc[0] for desc in cursor.description] if cursor.description else []
        result_list = list(result) if result else []
        
        await cursor.close()
        return result_list, columns
    
    async def get_schema(self) -> str:
        """Get MySQL schema information."""
        if not self.connection:
            await self.connect()
        
        parsed = urlparse(self.connection_string)
        database_name = parsed.path.lstrip('/')
        
        query = """
        SELECT 
            TABLE_NAME,
            COLUMN_NAME,
            DATA_TYPE,
            IS_NULLABLE,
            COLUMN_DEFAULT,
            COLUMN_KEY
        FROM INFORMATION_SCHEMA.COLUMNS 
        WHERE TABLE_SCHEMA = %s
        ORDER BY TABLE_NAME, ORDINAL_POSITION
        """
        
        cursor = await self.connection.cursor(aiomysql.DictCursor)
        await cursor.execute(query, (database_name,))
        result = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema (MySQL):\n\n"
        current_table = None
        
        for row in result:
            if row['TABLE_NAME'] != current_table:
                current_table = row['TABLE_NAME']
                schema_text += f"Table: {current_table}\n"
            
            nullable = "NULL" if row['IS_NULLABLE'] == 'YES' else "NOT NULL"
            primary_key = " (PRIMARY KEY)" if row['COLUMN_KEY'] == 'PRI' else ""
            
            schema_text += f"  - {row['COLUMN_NAME']}: {row['DATA_TYPE']} {nullable}{primary_key}\n"
        
        return schema_text
    
    async def test_connection(self) -> bool:
        """Test MySQL connection."""
        try:
            if not self.connection:
                await self.connect()
            cursor = await self.connection.cursor()
            await cursor.execute("SELECT 1")
            result = await cursor.fetchone()
            await cursor.close()
            return result[0] == 1
        except Exception:
            return False
    
    def get_sql_dialect(self) -> str:
        """Get SQL dialect for LLM."""
        return "MySQL"