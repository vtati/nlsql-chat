# Project Structure

## Root Directory Layout
```
├── backend/                 # Python FastAPI backend
├── frontend/               # React frontend application
├── docs/                   # Project documentation
├── .kiro/                  # Kiro IDE configuration
├── README.md              # Main project documentation
├── start.bat              # Windows development startup script
└── deployment configs     # Various deployment configurations
```

## Backend Structure (`backend/`)
```
backend/
├── main.py                # FastAPI application entry point
├── database.py            # Database connection and query management
├── llm_service.py         # OpenAI LLM integration service
├── setup_sample_db.py     # Sample database initialization
├── test_connection.py     # Connection testing utility
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (not in git)
├── .env.example          # Environment template
├── sample_database.db    # SQLite sample database
├── northwind.db          # Additional sample database
└── deployment files      # Procfile, railway.json, etc.
```

## Frontend Structure (`frontend/`)
```
frontend/
├── src/
│   ├── components/       # React components
│   │   ├── ChatInterface.js    # Main chat component
│   │   └── ChatInterface.css   # Component styles
│   ├── App.js           # Main React application
│   └── index.js         # React entry point
├── public/              # Static assets
├── build/               # Production build output
├── package.json         # Node.js dependencies and scripts
├── package-lock.json    # Dependency lock file
└── deployment files     # vercel.json, etc.
```

## Documentation Structure (`docs/`)
```
docs/
├── requirements.md       # Functional and non-functional requirements
├── design-document.md    # Technical architecture and design
└── api-documentation.md  # API endpoints and usage examples
```

## Key File Purposes

### Backend Core Files
- `main.py` - FastAPI app with CORS, routes, and request/response models
- `database.py` - DatabaseManager class for schema extraction and query execution
- `llm_service.py` - LLMService class for OpenAI integration and SQL generation

### Frontend Core Files
- `ChatInterface.js` - Main chat UI component handling user input and message display
- `App.js` - Root React component with routing and global state

### Configuration Files
- `.env` files - Environment-specific configuration (API keys, database URLs)
- `requirements.txt` - Python package dependencies
- `package.json` - Node.js dependencies and build scripts

## Naming Conventions
- **Python files**: snake_case (e.g., `llm_service.py`, `setup_sample_db.py`)
- **JavaScript files**: PascalCase for components (e.g., `ChatInterface.js`)
- **Database files**: lowercase with underscores (e.g., `sample_database.db`)
- **Documentation**: kebab-case (e.g., `design-document.md`)

## Import Patterns
- **Backend**: Relative imports within modules, absolute for external packages
- **Frontend**: ES6 imports, React components imported by name

## Database Files
- `sample_database.db` - Main SQLite database with customers, products, orders
- `northwind.db` - Additional sample database
- Schema includes proper foreign key relationships between tables

## Development Workflow
1. Backend runs on `localhost:8000` with auto-reload
2. Frontend runs on `localhost:3000` with hot reload
3. CORS configured to allow frontend-backend communication
4. Use `start.bat` for quick Windows development setup