#!/usr/bin/env python3
"""
Script to create a sample SQLite database with test data
"""
import asyncio
import aiosqlite

async def create_sample_database():
    """Create a sample database with customers, products, and orders"""
    
    # Connect to database (creates file if it doesn't exist)
    async with aiosqlite.connect('sample_database.db') as db:
        
        # Create customers table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS customers (
                customer_id INTEGER PRIMARY KEY,
                company_name TEXT NOT NULL,
                contact_name TEXT,
                city TEXT,
                country TEXT,
                phone TEXT
            )
        ''')
        
        # Create products table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS products (
                product_id INTEGER PRIMARY KEY,
                product_name TEXT NOT NULL,
                category TEXT,
                unit_price REAL,
                units_in_stock INTEGER
            )
        ''')
        
        # Create orders table
        await db.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                order_id INTEGER PRIMARY KEY,
                customer_id INTEGER,
                order_date TEXT,
                total_amount REAL,
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
        ''')
        
        # Insert sample customers
        customers_data = [
            (1, 'Alfreds Futterkiste', 'Maria Anders', 'Berlin', 'Germany', '030-0074321'),
            (2, 'Ana Trujillo Emparedados', 'Ana Trujillo', 'México D.F.', 'Mexico', '(5) 555-4729'),
            (3, 'Antonio Moreno Taquería', 'Antonio Moreno', 'México D.F.', 'Mexico', '(5) 555-3932'),
            (4, 'Around the Horn', 'Thomas Hardy', 'London', 'UK', '(171) 555-7788'),
            (5, 'Berglunds snabbköp', 'Christina Berglund', 'Luleå', 'Sweden', '0921-12 34 65'),
            (6, 'Blauer See Delikatessen', 'Hanna Moos', 'Mannheim', 'Germany', '0621-08460'),
            (7, 'Blondel père et fils', 'Frédérique Citeaux', 'Strasbourg', 'France', '88.60.15.31'),
            (8, 'Bólido Comidas preparadas', 'Martín Sommer', 'Madrid', 'Spain', '(91) 555 22 82'),
            (9, 'Bon app', 'Laurence Lebihans', 'Marseille', 'France', '91.24.45.40'),
            (10, 'Bottom-Dollar Marketse', 'Elizabeth Lincoln', 'Tsawassen', 'Canada', '(604) 555-4729')
        ]
        
        await db.executemany('''
            INSERT OR REPLACE INTO customers 
            (customer_id, company_name, contact_name, city, country, phone) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''', customers_data)
        
        # Insert sample products
        products_data = [
            (1, 'Chai', 'Beverages', 18.00, 39),
            (2, 'Chang', 'Beverages', 19.00, 17),
            (3, 'Aniseed Syrup', 'Condiments', 10.00, 13),
            (4, 'Chef Anton\'s Cajun Seasoning', 'Condiments', 22.00, 53),
            (5, 'Chef Anton\'s Gumbo Mix', 'Condiments', 21.35, 0),
            (6, 'Grandma\'s Boysenberry Spread', 'Condiments', 25.00, 120),
            (7, 'Uncle Bob\'s Organic Dried Pears', 'Produce', 30.00, 15),
            (8, 'Northwoods Cranberry Sauce', 'Condiments', 40.00, 6),
            (9, 'Mishi Kobe Niku', 'Meat/Poultry', 97.00, 29),
            (10, 'Ikura', 'Seafood', 31.00, 31),
            (11, 'Queso Cabrales', 'Dairy Products', 21.00, 22),
            (12, 'Queso Manchego La Pastora', 'Dairy Products', 38.00, 86),
            (13, 'Konbu', 'Seafood', 6.00, 24),
            (14, 'Tofu', 'Produce', 23.25, 35),
            (15, 'Genen Shouyu', 'Condiments', 15.50, 39)
        ]
        
        await db.executemany('''
            INSERT OR REPLACE INTO products 
            (product_id, product_name, category, unit_price, units_in_stock) 
            VALUES (?, ?, ?, ?, ?)
        ''', products_data)
        
        # Insert sample orders
        orders_data = [
            (1, 1, '2024-01-15', 250.50),
            (2, 2, '2024-01-16', 180.75),
            (3, 1, '2024-01-18', 95.00),
            (4, 3, '2024-01-20', 320.25),
            (5, 4, '2024-01-22', 150.00),
            (6, 5, '2024-01-25', 275.80),
            (7, 2, '2024-01-28', 420.15),
            (8, 6, '2024-02-01', 185.50),
            (9, 7, '2024-02-03', 95.75),
            (10, 8, '2024-02-05', 310.00),
            (11, 1, '2024-02-08', 125.25),
            (12, 9, '2024-02-10', 200.00),
            (13, 10, '2024-02-12', 175.50),
            (14, 3, '2024-02-15', 290.75),
            (15, 4, '2024-02-18', 155.00)
        ]
        
        await db.executemany('''
            INSERT OR REPLACE INTO orders 
            (order_id, customer_id, order_date, total_amount) 
            VALUES (?, ?, ?, ?)
        ''', orders_data)
        
        await db.commit()
        
        print("✅ Sample database created successfully!")
        print("📊 Database contains:")
        
        # Show table counts
        cursor = await db.execute("SELECT COUNT(*) FROM customers")
        customer_count = (await cursor.fetchone())[0]
        await cursor.close()
        
        cursor = await db.execute("SELECT COUNT(*) FROM products")
        product_count = (await cursor.fetchone())[0]
        await cursor.close()
        
        cursor = await db.execute("SELECT COUNT(*) FROM orders")
        order_count = (await cursor.fetchone())[0]
        await cursor.close()
        
        print(f"   - {customer_count} customers")
        print(f"   - {product_count} products")
        print(f"   - {order_count} orders")

if __name__ == "__main__":
    asyncio.run(create_sample_database())