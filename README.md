# Natural Language to SQL Chat Interface

A chat-based application that converts natural language queries into SQL statements and executes them against a relational database.

## 📋 Documentation

- **[Requirements Document](docs/requirements.md)** - Detailed functional and non-functional requirements
- **[Design Document](docs/design-document.md)** - System architecture and technical design
- **[API Documentation](docs/api-documentation.md)** - Complete API reference and examples

## 🏗️ Project Structure

```
├── api/                     # Backend API (FastAPI)
│   ├── src/                 # Source code
│   │   ├── core/            # Core business logic & settings
│   │   ├── database/        # Database layer & adapters
│   │   ├── services/        # Business services (LLM, Query)
│   │   ├── models/          # Data models & schemas
│   │   ├── api/             # API routes & endpoints
│   │   ├── utils/           # Utilities & exceptions
│   │   └── main.py          # Application entry point
│   ├── config/              # Configuration files
│   │   ├── requirements.txt # Python dependencies
│   │   └── .env.example     # Environment template
│   ├── scripts/             # Setup & utility scripts
│   │   ├── test_connections.py # Database testing
│   │   └── setup_database.py  # Database initialization
│   └── tests/               # Test files
├── web/                     # Frontend (React)
│   ├── src/                 # Source code
│   │   ├── components/      # React components
│   │   ├── services/        # API services
│   │   ├── hooks/           # Custom React hooks
│   │   ├── utils/           # Frontend utilities
│   │   └── App.js           # Main application
│   ├── public/              # Static assets
│   └── package.json         # Node.js dependencies
├── docs/                    # Documentation
│   ├── requirements.md      # Requirements specification
│   ├── design-document.md   # Technical design
│   └── api-documentation.md # API reference
├── scripts/                 # Project-level scripts
│   ├── start.bat           # Quick start script
│   └── test.bat            # Testing script
├── .kiro/                  # Kiro IDE configuration
└── README.md               # This file
```

## 🚀 Enhanced Features (v2.0)

- **Multi-Database Support**: SQLite, PostgreSQL, MySQL, SQL Server, Oracle
- **Natural Language Processing**: Convert plain English questions to SQL
- **Database-Aware SQL Generation**: Dialect-specific query generation
- **Chat Interface**: Real-time conversational UI with message history
- **Smart Query Optimization**: Database-specific syntax and features
- **Query Execution**: Safe execution of SELECT queries only
- **Result Display**: Tabular format with export capabilities
- **Schema Detection**: Automatic database schema extraction for all supported databases
- **Connection Testing**: Built-in database connection validation
- **Error Handling**: Comprehensive error messages and validation

## 🎯 Getting Started

### Prerequisites
- Python 3.8+
- Node.js 16+
- OpenAI API key

### Quick Start

1. **Clone and setup:**
   ```bash
   git clone <repository-url>
   cd natural-language-sql
   ```

2. **Configure environment:**
   ```bash
   # Copy environment template
   cp api/config/.env.example api/config/.env
   
   # Edit api/config/.env and add your OpenAI API key:
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Setup and test database:**
   ```bash
   cd api
   python scripts/test_connections.py  # Test connections
   python scripts/setup_database.py   # Initialize sample data
   ```

4. **Start the application:**
   ```bash
   # Option 1: Use the start script (Windows)
   scripts/start.bat
   
   # Option 2: Manual startup
   # Terminal 1 - API Server
   cd api
   pip install -r config/requirements.txt
   python -m src.main
   
   # Terminal 2 - Web Application
   cd web
   npm install
   npm start
   ```

5. **Access the application:**
   - **Web App**: http://localhost:3000
   - **API Server**: http://localhost:8000
   - **API Docs**: http://localhost:8000/docs

### Sample Queries to Try

Once running, try these natural language questions:

- **Basic queries:**
  - "Show me all customers"
  - "List all products"
  - "What orders were placed today?"

- **Filtered queries:**
  - "Show customers from Germany"
  - "Products with price over $20"
  - "Orders from January 2024"

- **Aggregations:**
  - "How many customers are there?"
  - "What's the average product price?"
  - "Total sales by country"

- **Complex queries:**
  - "Top 5 most expensive products"
  - "Customers with their order counts"
  - "Products that are out of stock"

## 🗃️ Sample Database

The application includes a sample SQLite database with:
- **10 customers** from various countries
- **15 products** across different categories
- **15 orders** with realistic data

### Database Schema
```sql
customers (customer_id, company_name, contact_name, city, country, phone)
products (product_id, product_name, category, unit_price, units_in_stock)
orders (order_id, customer_id, order_date, total_amount)
```

## 🗄️ Multi-Database Support

### Supported Databases

| Database | Status | Driver | Features |
|----------|--------|--------|----------|
| **SQLite** | ✅ Ready | aiosqlite | File-based, LIMIT syntax |
| **PostgreSQL** | ✅ Ready | asyncpg | ILIKE support, schemas |
| **MySQL/MariaDB** | ✅ Ready | aiomysql | LIMIT syntax, schemas |
| **SQL Server** | 🚧 Coming Soon | pyodbc | TOP syntax, schemas |
| **Oracle** | 🚧 Coming Soon | cx_Oracle | ROWNUM syntax, schemas |

### Database Configuration Examples

```bash
# SQLite (Development - Default)
DATABASE_URL=sqlite:///northwind.db

# PostgreSQL (Production Recommended)
DATABASE_URL=postgresql://username:password@host:port/database

# MySQL/MariaDB (Alternative Production)
DATABASE_URL=mysql://username:password@host:port/database

# SQL Server (Enterprise)
DATABASE_URL=mssql://username:password@host:port/database

# Oracle (Enterprise)
DATABASE_URL=oracle://username:password@host:port/service
```

### Database Testing & Setup

```bash
# Test all database connections
cd backend
python test_multi_db.py

# Test specific database
python test_multi_db.py "postgresql://user:pass@host:5432/db"

# Setup database with sample data
python setup_multi_db.py

# Setup specific database
python setup_multi_db.py "mysql://user:pass@host:3306/db"
```

### Database-Specific Features

#### SQLite
- **Best for**: Development, small applications
- **Features**: File-based, no server required
- **Limitations**: No concurrent writes, basic text search

#### PostgreSQL
- **Best for**: Production applications, complex queries
- **Features**: ILIKE for case-insensitive search, advanced SQL features
- **Advantages**: Excellent performance, ACID compliance

#### MySQL/MariaDB
- **Best for**: Web applications, high-traffic sites
- **Features**: Good performance, wide hosting support
- **Note**: Use LOWER() function for case-insensitive searches

#### SQL Server (Coming Soon)
- **Best for**: Enterprise Windows environments
- **Features**: TOP syntax instead of LIMIT
- **Integration**: Works well with Microsoft ecosystem

#### Oracle (Coming Soon)
- **Best for**: Large enterprise applications
- **Features**: ROWNUM for limiting results
- **Note**: Requires Oracle client libraries

## 🔧 Configuration

### Environment Variables
```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Database (choose one)
DATABASE_URL=sqlite:///northwind.db

# Optional
ENVIRONMENT=development
CORS_ORIGINS=http://localhost:3000,https://yourdomain.com
MAX_QUERY_RESULTS=1000
QUERY_TIMEOUT_SECONDS=30
```

### LLM Configuration
```bash
# OpenAI (default)
OPENAI_API_KEY=your_openai_api_key_here

# The system automatically uses:
# - GPT-4 (primary)
# - GPT-3.5-turbo (fallback)
```

## 🛡️ Security Features

- **Query Validation**: Only SELECT queries allowed
- **SQL Injection Prevention**: Input sanitization and validation
- **Safe Execution**: Read-only database access
- **Error Handling**: Secure error messages without sensitive data exposure

## 🧪 Testing

### Backend Testing
```bash
cd backend
python test_connection.py  # Test database and API connections
```

### API Testing
```bash
# Health check
curl http://localhost:8000/health

# Sample query
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"question": "Show me all customers"}'
```

## 📈 Performance

- **Query Response**: < 5 seconds for typical queries
- **Concurrent Users**: Supports 50+ simultaneous users
- **Result Sets**: Efficiently handles up to 10,000 rows
- **Caching**: Built-in query result caching (planned)

## 🔮 Roadmap

### Phase 2 (Planned)
- [ ] Multiple database support (PostgreSQL, MySQL)
- [ ] User authentication and authorization
- [ ] Query history and favorites
- [ ] Advanced visualizations
- [ ] ER diagram upload support

### Phase 3 (Future)
- [ ] Multi-user collaboration
- [ ] API access for integrations
- [ ] Advanced analytics and reporting
- [ ] Machine learning query optimization
- [ ] Enterprise security features

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Support

- **Documentation**: Check the [docs/](docs/) directory
- **API Reference**: http://localhost:8000/docs (when running)
- **Issues**: Create an issue on GitHub
- **Discussions**: Use GitHub Discussions for questions

## 🙏 Acknowledgments

- OpenAI for GPT-3.5-turbo API
- FastAPI for the excellent Python web framework
- React team for the frontend framework
- SQLite for the embedded database solution