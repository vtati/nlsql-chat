"""
Multi-Database Setup Utility
Initialize sample data for different database types
"""
import asyncio
import os
from dotenv import load_dotenv
from database_factory import DatabaseManager
from config import DatabaseConfig

load_dotenv()


class DatabaseSetup:
    """Database setup utility for different database types"""
    
    def __init__(self, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.db_type = db_manager.get_sql_dialect()
    
    async def create_sample_tables(self):
        """Create sample tables with appropriate syntax for each database type"""
        
        if self.db_type == "SQLite":
            await self._create_sqlite_tables()
        elif self.db_type == "PostgreSQL":
            await self._create_postgresql_tables()
        elif self.db_type == "MySQL":
            await self._create_mysql_tables()
        else:
            raise NotImplementedError(f"Sample data creation not implemented for {self.db_type}")
    
    async def _create_sqlite_tables(self):
        """Create SQLite tables"""
        print("Creating SQLite tables...")
        
        # This will use the existing logic from the SQLiteAdapter
        # The adapter handles table creation automatically
        await self.db_manager.get_connection()
        print("✅ SQLite tables created successfully")
    
    async def _create_postgresql_tables(self):
        """Create PostgreSQL tables"""
        print("Creating PostgreSQL tables...")
        
        # Check if tables already exist
        try:
            result, _ = await self.db_manager.execute_query(
                "SELECT COUNT(*) FROM customers LIMIT 1"
            )
            if result:
                print("✅ Tables already exist with data")
                return
        except:
            pass  # Tables don't exist, create them
        
        # Create tables with PostgreSQL-specific syntax
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id VARCHAR(5) PRIMARY KEY,
                company_name VARCHAR(40) NOT NULL,
                contact_name VARCHAR(30),
                contact_title VARCHAR(30),
                address VARCHAR(60),
                city VARCHAR(15),
                region VARCHAR(15),
                postal_code VARCHAR(10),
                country VARCHAR(15),
                phone VARCHAR(24),
                fax VARCHAR(24)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id SERIAL PRIMARY KEY,
                category_name VARCHAR(15) NOT NULL,
                description TEXT
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                product_name VARCHAR(40) NOT NULL,
                supplier_id INTEGER,
                category_id INTEGER,
                quantity_per_unit VARCHAR(20),
                unit_price DECIMAL(10,2),
                units_in_stock INTEGER,
                units_on_order INTEGER,
                reorder_level INTEGER,
                discontinued INTEGER DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id SERIAL PRIMARY KEY,
                customer_id VARCHAR(5),
                employee_id INTEGER,
                order_date DATE,
                required_date DATE,
                shipped_date DATE,
                ship_via INTEGER,
                freight DECIMAL(10,2),
                ship_name VARCHAR(40),
                ship_address VARCHAR(60),
                ship_city VARCHAR(15),
                ship_region VARCHAR(15),
                ship_postal_code VARCHAR(10),
                ship_country VARCHAR(15),
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            )
            """
        ]
        
        # Execute table creation
        for sql in tables_sql:
            try:
                await self.db_manager.adapter.connection.execute(sql)
                print(f"✅ Created table")
            except Exception as e:
                print(f"❌ Error creating table: {e}")
        
        print("✅ PostgreSQL tables created successfully")
    
    async def _create_mysql_tables(self):
        """Create MySQL tables"""
        print("Creating MySQL tables...")
        
        # Similar to PostgreSQL but with MySQL-specific syntax
        tables_sql = [
            """
            CREATE TABLE IF NOT EXISTS customers (
                customer_id VARCHAR(5) PRIMARY KEY,
                company_name VARCHAR(40) NOT NULL,
                contact_name VARCHAR(30),
                contact_title VARCHAR(30),
                address VARCHAR(60),
                city VARCHAR(15),
                region VARCHAR(15),
                postal_code VARCHAR(10),
                country VARCHAR(15),
                phone VARCHAR(24),
                fax VARCHAR(24)
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS categories (
                category_id INT AUTO_INCREMENT PRIMARY KEY,
                category_name VARCHAR(15) NOT NULL,
                description TEXT
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS products (
                product_id INT AUTO_INCREMENT PRIMARY KEY,
                product_name VARCHAR(40) NOT NULL,
                supplier_id INT,
                category_id INT,
                quantity_per_unit VARCHAR(20),
                unit_price DECIMAL(10,2),
                units_in_stock INT,
                units_on_order INT,
                reorder_level INT,
                discontinued INT DEFAULT 0,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            ) ENGINE=InnoDB
            """,
            """
            CREATE TABLE IF NOT EXISTS orders (
                order_id INT AUTO_INCREMENT PRIMARY KEY,
                customer_id VARCHAR(5),
                employee_id INT,
                order_date DATE,
                required_date DATE,
                shipped_date DATE,
                ship_via INT,
                freight DECIMAL(10,2),
                ship_name VARCHAR(40),
                ship_address VARCHAR(60),
                ship_city VARCHAR(15),
                ship_region VARCHAR(15),
                ship_postal_code VARCHAR(10),
                ship_country VARCHAR(15),
                FOREIGN KEY (customer_id) REFERENCES customers (customer_id)
            ) ENGINE=InnoDB
            """
        ]
        
        # Execute table creation
        for sql in tables_sql:
            try:
                cursor = await self.db_manager.adapter.connection.cursor()
                await cursor.execute(sql)
                await cursor.close()
                print(f"✅ Created table")
            except Exception as e:
                print(f"❌ Error creating table: {e}")
        
        print("✅ MySQL tables created successfully")
    
    async def insert_sample_data(self):
        """Insert sample data appropriate for the database type"""
        print(f"Inserting sample data for {self.db_type}...")
        
        # Sample data that works across all database types
        sample_data = {
            "customers": [
                ('ALFKI', 'Alfreds Futterkiste', 'Maria Anders', 'Sales Representative', 'Obere Str. 57', 'Berlin', None, '12209', 'Germany', '030-0074321', '030-0076545'),
                ('ANATR', 'Ana Trujillo Emparedados y helados', 'Ana Trujillo', 'Owner', 'Avda. de la Constitución 2222', 'México D.F.', None, '05021', 'Mexico', '(5) 555-4729', '(5) 555-3745'),
                ('ANTON', 'Antonio Moreno Taquería', 'Antonio Moreno', 'Owner', 'Mataderos 2312', 'México D.F.', None, '05023', 'Mexico', '(5) 555-3932', None),
                ('AROUT', 'Around the Horn', 'Thomas Hardy', 'Sales Representative', '120 Hanover Sq.', 'London', None, 'WA1 1DP', 'UK', '(171) 555-7788', '(171) 555-6750'),
                ('BERGS', 'Berglunds snabbköp', 'Christina Berglund', 'Order Administrator', 'Berguvsvägen 8', 'Luleå', None, 'S-958 22', 'Sweden', '0921-12 34 65', '0921-12 34 67')
            ],
            "categories": [
                ('Beverages', 'Soft drinks, coffees, teas, beers, and ales'),
                ('Condiments', 'Sweet and savory sauces, relishes, spreads, and seasonings'),
                ('Dairy Products', 'Cheeses'),
                ('Grains/Cereals', 'Breads, crackers, pasta, and cereal'),
                ('Meat/Poultry', 'Prepared meats')
            ]
        }
        
        try:
            # Insert customers
            if self.db_type == "SQLite":
                await self._insert_sqlite_data(sample_data)
            elif self.db_type in ["PostgreSQL", "MySQL"]:
                await self._insert_sql_data(sample_data)
            
            print("✅ Sample data inserted successfully")
            
        except Exception as e:
            print(f"❌ Error inserting sample data: {e}")
    
    async def _insert_sqlite_data(self, sample_data):
        """Insert data for SQLite"""
        # SQLite adapter handles this automatically
        pass
    
    async def _insert_sql_data(self, sample_data):
        """Insert data for PostgreSQL/MySQL"""
        # Check if data already exists
        try:
            result, _ = await self.db_manager.execute_query("SELECT COUNT(*) FROM customers")
            if result and result[0]['count'] > 0:
                print("✅ Sample data already exists")
                return
        except:
            pass
        
        # Insert customers
        customer_sql = """
        INSERT INTO customers 
        (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
        VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)
        """ if self.db_type == "PostgreSQL" else """
        INSERT INTO customers 
        (customer_id, company_name, contact_name, contact_title, address, city, region, postal_code, country, phone, fax) 
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        
        for customer in sample_data["customers"]:
            try:
                if self.db_type == "PostgreSQL":
                    await self.db_manager.adapter.connection.execute(customer_sql, *customer)
                else:  # MySQL
                    cursor = await self.db_manager.adapter.connection.cursor()
                    await cursor.execute(customer_sql, customer)
                    await cursor.close()
            except Exception as e:
                print(f"Warning: Could not insert customer {customer[0]}: {e}")


async def setup_database(db_url: str = None):
    """Setup database with sample data"""
    if not db_url:
        db_url = DatabaseConfig.get_database_url()
    
    print(f"🚀 Setting up database: {db_url}")
    
    try:
        # Create database manager
        db_manager = DatabaseManager(db_url)
        
        # Test connection first
        print("1. Testing connection...")
        if not await db_manager.test_connection():
            print("❌ Cannot connect to database")
            return False
        print("✅ Connection successful")
        
        # Create setup instance
        setup = DatabaseSetup(db_manager)
        
        # Create tables
        print("2. Creating tables...")
        await setup.create_sample_tables()
        
        # Insert sample data
        print("3. Inserting sample data...")
        await setup.insert_sample_data()
        
        # Verify setup
        print("4. Verifying setup...")
        schema = await db_manager.get_schema()
        if schema and len(schema) > 100:
            print("✅ Database setup completed successfully")
            print(f"📋 Schema preview:\n{schema[:300]}...")
            return True
        else:
            print("❌ Database setup verification failed")
            return False
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        return False
    finally:
        if 'db_manager' in locals():
            await db_manager.close()


async def main():
    """Main setup function"""
    print("🔧 Multi-Database Setup Utility")
    print("=" * 50)
    
    # Setup current database
    success = await setup_database()
    
    if success:
        print("\n🎉 Database setup completed successfully!")
        print("You can now run the application with this database.")
    else:
        print("\n❌ Database setup failed!")
        print("Please check your database configuration and try again.")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        custom_url = sys.argv[1]
        print(f"Setting up custom database: {custom_url}")
        asyncio.run(setup_database(custom_url))
    else:
        asyncio.run(main())