# Natural Language to SQL Chat Interface

A chat-based application that converts natural language queries into SQL statements and executes them against a relational database.

## 📋 Documentation

- **[Requirements Document](docs/requirements.md)** - Detailed functional and non-functional requirements
- **[Design Document](docs/design-document.md)** - System architecture and technical design
- **[API Documentation](docs/api-documentation.md)** - Complete API reference and examples

## 🏗️ Project Structure

```
├── backend/                 # Python FastAPI backend
│   ├── main.py             # FastAPI application
│   ├── database.py         # Database management
│   ├── llm_service.py      # LLM integration
│   ├── requirements.txt    # Python dependencies
│   ├── .env               # Environment configuration
│   └── setup_sample_db.py # Sample database setup
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/    # React components
│   │   └── App.js        # Main application
│   ├── package.json      # Node.js dependencies
│   └── public/           # Static assets
├── docs/                  # Documentation
│   ├── requirements.md   # Requirements specification
│   ├── design-document.md # Technical design
│   └── api-documentation.md # API reference
├── README.md             # This file
└── start.bat            # Quick start script
```

## 🚀 MVP Features

- **Natural Language Processing**: Convert plain English questions to SQL
- **Chat Interface**: Real-time conversational UI with message history
- **SQL Generation**: Powered by OpenAI GPT-3.5-turbo
- **Query Execution**: Safe execution of SELECT queries only
- **Result Display**: Tabular format with export capabilities
- **Schema Detection**: Automatic database schema extraction
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
   cp backend/.env.example backend/.env
   
   # Edit backend/.env and add your OpenAI API key:
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Setup sample database:**
   ```bash
   cd backend
   python setup_sample_db.py
   ```

4. **Start the application:**
   ```bash
   # Option 1: Use the start script (Windows)
   start.bat
   
   # Option 2: Manual startup
   # Terminal 1 - Backend
   cd backend
   pip install -r requirements.txt
   uvicorn main:app --reload
   
   # Terminal 2 - Frontend
   cd frontend
   npm install
   npm start
   ```

5. **Access the application:**
   - **Frontend**: http://localhost:3000
   - **Backend API**: http://localhost:8000
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

## 🔧 Configuration

### Database Configuration
```bash
# SQLite (default)
DATABASE_URL=sqlite:///sample_database.db

# PostgreSQL
DATABASE_URL=postgresql://user:password@host:port/database

# MySQL
DATABASE_URL=mysql://user:password@host:port/database
```

### LLM Configuration
```bash
# OpenAI (default)
OPENAI_API_KEY=your_openai_api_key_here

# Future: Support for other LLM providers
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