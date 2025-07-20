# Technology Stack

## Backend
- **Framework**: FastAPI (Python)
- **Server**: Uvicorn ASGI server
- **Database**: SQLite (development), PostgreSQL/MySQL (production)
- **LLM Integration**: OpenAI API (GPT-3.5-turbo/GPT-4)
- **Environment**: Python 3.8+

### Key Dependencies
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `aiosqlite` - Async SQLite driver
- `openai` - OpenAI API client
- `python-dotenv` - Environment variable management
- `pydantic` - Data validation

## Frontend
- **Framework**: React 18+
- **Build Tool**: Create React App
- **HTTP Client**: Axios
- **Testing**: React Testing Library, Jest

### Key Dependencies
- `react` & `react-dom` - Core React
- `axios` - HTTP requests
- `react-scripts` - Build tooling

## Development Environment
- **OS**: Windows (cmd shell)
- **Package Managers**: pip (Python), npm (Node.js)

## Common Commands

### Development Setup
```bash
# API setup
cd api
pip install -r config/requirements.txt
python -m src.main

# Web setup  
cd web
npm install
npm start
```

### Quick Start
```bash
# Windows batch script
scripts/start.bat
```

### Testing
```bash
# Database connection testing
cd api
python scripts/test_connections.py

# Database setup
python scripts/setup_database.py

# Web testing
cd web
npm test
```

### Health Checks
```bash
# API health check
curl http://localhost:8000/health

# Database info
curl http://localhost:8000/database-info

# Sample query test
curl -X POST http://localhost:8000/query -H "Content-Type: application/json" -d '{"question": "Show me all customers"}'
```

## Deployment Platforms
- **Backend**: Railway, Heroku (Procfile included)
- **Frontend**: Vercel (vercel.json configured)
- **Alternative**: Nixpacks support (nixpacks.toml)

## Environment Configuration
- Backend uses `.env` file for secrets (OpenAI API key, database URL)
- Frontend uses environment variables for API endpoints
- Example files provided: `.env.example`