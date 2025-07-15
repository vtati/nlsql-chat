import aiosqlite
import asyncio
import os
from typing import List, Dict, Any, Tuple

class DatabaseManager:
    def __init__(self, database_url: str = None):
        # Use SQLite for reliable deployment
        self.db_path = "northwind.db"
        self.connection = None
    
    async def get_connection(self):
        """Get database connection"""
        if not self.connection:
            self.connection = await aiosqlite.connect(self.db_path)
            self.connection.row_factory = aiosqlite.Row
            # Initialize database with sample data if it doesn't exist
            await self.initialize_database()
        return self.connection
    
    async def initialize_database(self):
        """Initialize database with Northwind sample data"""
        conn = self.connection
        
        # Check if tables already exist
        cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='customers'")
        exists = await cursor.fetchone()
        await cursor.close()
        
        if exists:
            return  # Database already initialized
        
        # Create customers table
        await conn.execute('''
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
        await conn.execute('''
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
        await conn.execute('''
            CREATE TABLE categories (
                category_id INTEGER PRIMARY KEY,
                category_name TEXT NOT NULL,
                description TEXT
            )
        ''')
        
        # Create orders table
        await conn.execute('''
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
        
        # Insert sample customers
        customers_data = [
            ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', None, '12209', 'Germany', '030-0074321', '030-0076545'),
            ('ANATR', 'Ana Trujillo Emparedados y helados', 'Ana Trujillo', 'Owner', 'Avda. de la Constitución 2222', 'México D.F.', None, '05021', 'Mexico', '(5) 555-4729', '(5) 555-3745'),
            ('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Owner', 'Mataderos 2312', 'México D.F.', None, '05023', 'Mexico', '(5) 555-3932', None),
            ('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', None, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750'),
            ('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Berguvsvägen 8', 'Luleå', None, 'S-958 22', 'Sweden', '0921-12 34 65', '0921-12 34 67'),
            ('BLAUS', 'Blauer See Delikatessen', 'Hanna Moos', 'Sales Representative', 'Forsterstr. 57', 'Mannheim', None, '68306', 'Germany', '0621-08460', '0621-08924'),
            ('BLONP', 'Blondesddsl père et fils', 'Frédérique Citeaux', 'Marketing Manager', '24, place Kléber', 'Strasbourg', None, '67000', 'France', '88.60.15.31', '88.60.15.32'),
            ('BOLID', 'Bólido Comidas preparadas', 'Martín Sommer', 'Owner', 'C/ Araquil, 67', 'Madrid', None, '28023', 'Spain', '(91) 555 22 82', '(91) 555 91 99'),
            ('BONAP', 'Bon app', 'Laurence Lebihan', 'Owner', '12, rue des Bouchers', 'Marseille', None, '13008', 'France', '91.24.45.40', '91.24.45.41'),
            ('BOTTM', 'Bottom-Dollar Markets', 'Elizabeth Lincoln', 'Accounting Manager', '23 Tsawassen Blvd.', 'Tsawassen', 'BC', 'T2F 8M4', 'Canada', '(604) 555-4729', '(604) 555-3745')
        ]
        
        await conn.executemany('''
            INSERT INTO customers 
            (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', customers_data)
        
        # Insert sample categories
        categories_data = [
            (1, 'Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
            (2, 'Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
            (3, 'Dairy Products', 'Cheeses'),
            (4, 'Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
            (5, 'Meat/Poultry', 'Prepared meats'),
            (6, 'Produce', 'Dried fruit and bean curd'),
            (7, 'Seafood', 'Seaweed and fish'),
            (8, 'Confections', 'Desserts, candies, and sweet breads')
        ]
        
        await conn.executemany('''
            INSERT INTO categories (category_id, category_name, description) 
            VALUES (?, ?, ?)
        ''', categories_data)
        
        # Insert sample products
        products_data = [
            (1, 'Chai', 1, 1, '10 boxes x 20 bags', 18.00, 39, 0, 10, 0),
            (2, 'Chang', 1, 1, '24 - 12 oz bottles', 19.00, 17, 40, 25, 0),
            (3, 'Aniseed Syrup', 1, 2, '12 - 550 ml bottles', 10.00, 13, 70, 25, 0),
            (4, 'Chef Antons Cajun Seasoning', 2, 2, '48 - 6 oz jars', 22.00, 53, 0, 0, 0),
            (5, 'Chef Antons Gumbo Mix', 2, 2, '36 boxes', 21.35, 0, 0, 0, 1),
            (6, 'Grandmas Boysenberry Spread', 3, 2, '12 - 8 oz jars', 25.00, 120, 0, 25, 0),
            (7, 'Uncle Bobs Organic Dried Pears', 3, 7, '12 - 1 lb pkgs.', 30.00, 15, 0, 10, 0),
            (8, 'Northwoods Cranberry Sauce', 3, 2, '12 - 12 oz jars', 40.00, 6, 0, 0, 0),
            (9, 'Mishi Kobe Niku', 4, 6, '18 - 500 g pkgs.', 97.00, 29, 0, 0, 1),
            (10, 'Ikura', 4, 8, '12 - 200 ml jars', 31.00, 31, 0, 0, 0),
            (11, 'Queso Cabrales', 5, 4, '1 kg pkg.', 21.00, 22, 30, 30, 0),
            (12, 'Queso Manchego La Pastora', 5, 4, '10 - 500 g pkgs.', 38.00, 86, 0, 0, 0),
            (13, 'Konbu', 6, 8, '2 kg box', 6.00, 24, 0, 5, 0),
            (14, 'Tofu', 6, 7, '40 - 100 g pkgs.', 23.25, 35, 0, 0, 0),
            (15, 'Genen Shouyu', 6, 2, '24 - 250 ml bottles', 15.50, 39, 0, 5, 0)
        ]
        
        await conn.executemany('''
            INSERT INTO products 
            (product_id, product_name, supplier_id, category_id, quantity_per_unit, unit_price, units_in_stock, units_on_order, reorder_level, discontinued) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', products_data)
        
        # Insert sample orders
        orders_data = [
            (10248, 'VINET', 5, '1996-07-04', '1996-08-01', '1996-07-16', 3, 32.38, 'Vins et alcools Chevalier', '59 rue de lAbbaye', 'Reims', None, '51100', 'France'),
            (10249, 'TOMSP', 6, '1996-07-05', '1996-08-16', '1996-07-10', 1, 11.61, 'Toms Spezialitäten', 'Luisenstr. 48', 'Münster', None, '44087', 'Germany'),
            (10250, 'HANAR', 4, '1996-07-08', '1996-08-05', '1996-07-12', 2, 65.83, 'Hanari Carnes', 'Rua do Paço, 67', 'Rio de Janeiro', 'RJ', '05454-876', 'Brazil'),
            (10251, 'VICTE', 3, '1996-07-08', '1996-08-05', '1996-07-15', 1, 41.34, 'Victuailles en stock', '2, rue du Commerce', 'Lyon', None, '69004', 'France'),
            (10252, 'SUPRD', 4, '1996-07-09', '1996-08-06', '1996-07-11', 2, 51.30, 'Suprêmes délices', 'Boulevard Tirou, 255', 'Charleroi', None, 'B-6000', 'Belgium')
        ]
        
        await conn.executemany('''
            INSERT INTO orders 
            (order_id, customer_id, employee_id, order_date, required_date, shipped_date, ship_via, freight, ship_name, ship_address, ship_city, ship_region, ship_postal_code, ship_country) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', orders_data)
        
        await conn.commit()
    
    async def test_connection(self):
        """Test database connection"""
        conn = await self.get_connection()
        cursor = await conn.execute("SELECT 1")
        result = await cursor.fetchone()
        await cursor.close()
        return result[0] if result else None
    
    async def get_schema(self) -> str:
        """Get database schema information for SQLite"""
        conn = await self.get_connection()
        
        # Get all tables
        cursor = await conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
        tables = await cursor.fetchall()
        await cursor.close()
        
        schema_text = "Database Schema:\n\n"
        
        for table_row in tables:
            table_name = table_row[0]
            schema_text += f"Table: {table_name}\n"
            
            # Get column information for each table
            cursor = await conn.execute(f"PRAGMA table_info({table_name})")
            columns = await cursor.fetchall()
            await cursor.close()
            
            for col in columns:
                col_name = col[1]
                col_type = col[2]
                not_null = "NOT NULL" if col[3] else "NULL"
                default_val = f" DEFAULT {col[4]}" if col[4] else ""
                primary_key = " (PRIMARY KEY)" if col[5] else ""
                
                schema_text += f"  - {col_name}: {col_type} {not_null}{default_val}{primary_key}\n"
            
            schema_text += "\n"
        
        return schema_text
    
    async def execute_query(self, sql_query: str) -> Tuple[List[Dict[str, Any]], List[str]]:
        """Execute SQL query and return results"""
        # Safety check - only allow SELECT queries for MVP
        if not sql_query.strip().upper().startswith('SELECT'):
            raise ValueError("Only SELECT queries are allowed")
        
        conn = await self.get_connection()
        
        try:
            cursor = await conn.execute(sql_query)
            results = await cursor.fetchall()
            await cursor.close()
            
            # Get column names from cursor description
            columns = [description[0] for description in cursor.description] if cursor.description else []
            
            # Convert to list of dictionaries
            result_list = [dict(row) for row in results]
            
            return result_list, columns
            
        except Exception as e:
            raise Exception(f"Query execution error: {str(e)}")
    
    async def close(self):
        """Close database connection"""
        if self.connection:
            await self.connection.close()
    
    def __del__(self):
        # SQLite connections should be closed explicitly with await
        pass